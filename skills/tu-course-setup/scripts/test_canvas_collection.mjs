// Exercise the exact documented collector against invented, offline API pages.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const reference = fs.readFileSync(new URL('../references/canvas-collection.md', import.meta.url), 'utf8');
const blocks = [...reference.matchAll(/```js\n([\s\S]*?)```/g)].map(match => match[1]);

async function collect(failAssignments = false) {
  const requests = [];
  const context = {
    window: {}, location: {origin: 'https://canvas.example'}, COURSE_ID: 123,
    fetch: async input => {
      const url = new URL(input, 'https://canvas.example');
      requests.push(url.toString());
      let data = [], next = null, status = 200;
      if (url.pathname === '/api/v1/courses/123') {
        data = {id: 123, name: 'Invented Course', course_code: 'TEST100', time_zone: 'Europe/Amsterdam'};
      } else if (url.pathname.endsWith('/assignments')) {
        if (failAssignments) status = 403;
        else if (url.searchParams.get('page') === '2') data = [{id: 2, name: 'Second', rubric: []}];
        else {
          data = [{id: 1, name: 'First', due_at: '2030-01-02T16:00:00Z',
            submission: {score: null, user_id: 999, body: 'PRIVATE-ANSWER'},
            overrides: [{student_ids: [999]}], rubric: []}];
          next = 'https://canvas.example/api/v1/courses/123/assignments?page=2';
        }
      } else if (url.pathname.endsWith('/assignment_groups')) {
        data = [{id: 10, group_weight: 20, rules: {drop_lowest: 1}}];
      } else if (url.pathname.endsWith('/front_page')) {
        data = {url: 'home', title: 'Home', body: ''};
      }
      return {ok: status === 200, status, text: async () => 'while(1);' + JSON.stringify(data),
        headers: {get: () => next ? `<${next}>; rel="next"` : null}};
    },
  };
  const code = blocks[1].replace('(async (C, CODE) => {', 'window.collectionPromise = (async (C, CODE) => {');
  vm.runInNewContext(code, context);
  await context.window.collectionPromise;
  return {manifest: context.window._tue.manifest, requests};
}

const {manifest, requests} = await collect();
assert.equal(manifest.assignments_complete, true);
assert.equal(manifest.assignments.length, 2);
assert.equal(manifest.assignments[0].submission.score, null);
assert.equal(manifest.assignment_groups[0].rules.drop_lowest, 1);
assert.ok(requests.some(url => url.includes('include[]=submission')));
assert.ok(!JSON.stringify(manifest).includes('PRIVATE-ANSWER'));
assert.ok(!JSON.stringify(manifest).includes('student_ids'));
assert.ok(!JSON.stringify(manifest).includes('user_id'));
const failed = (await collect(true)).manifest;
assert.equal(failed.assignments_complete, false);
assert.equal(failed.assignments.length, 0);
assert.ok(failed.errors.some(error => error.startsWith('assignments:')));
console.log('Canvas collector mock: pagination, private-field filtering, grading rules and failed coverage passed.');
