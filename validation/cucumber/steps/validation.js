import {Given, When, Then} from '@cucumber/cucumber';
import assert from 'node:assert/strict';
import {fixture} from '../test/fixtures.js';
import {prepare} from '../src/model.js';
import {validate} from '../src/harness.js';
import {evaluateLaw} from '../src/laws.js';

Given('the finite candidate {string}', function (name) { this.input = fixture(name); });
When('law {int} evaluates the candidate', function (id) { this.evaluation = evaluateLaw(id, prepare(this.input)); });
Then('its conformance status is {string}', function (status) { assert.equal(this.evaluation.status, status); assert.ok(this.evaluation.evidence); });
When('the recursive validator evaluates the candidate', function () { this.report = validate(this.input); });
Then('the validation result is {string}', function (status) { assert.equal(this.report.status, status); });
Then('every pass retains its input, evidence and consequences', function () {
  assert.ok(this.report.trace.length);
  for (const r of this.report.trace) {
    assert.ok(r.input_state && r.derived_state && r.consequences);
    assert.equal(r.evaluations.length, 18);
    assert.ok(r.evaluations.every(e => e.evidence && e.provenance_receipt));
  }
});
