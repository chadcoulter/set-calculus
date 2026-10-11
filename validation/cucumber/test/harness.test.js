import test from 'node:test';
import assert from 'node:assert/strict';
import {validate, collate} from '../src/harness.js';
import {prepare, currentRows} from '../src/model.js';
import {registry, evaluateLaw} from '../src/laws.js';
import {fixture, base} from './fixtures.js';

test('quick candidate is closed only after all required evidence validates', () => {
  const input = base(), original = structuredClone(input), r = validate(input);
  assert.equal(r.status, 'CLOSED');
  assert.equal(r.discovery_route, 'QUICK_CANDIDATE');
  assert.equal(r.trace[0].evaluations.length, 18);
  assert.deepEqual(input, original);
  assert.equal(r.final_state.candidate_transform.images.length, 2);
  assert.deepEqual(r.trace[0].input_state.provenance, original.provenance);
});
test('discovery route does not change validity', () => {
  for (const route of ['KNOWLEDGE', 'CAUTIOUS_TRANSFORM', 'QUICK_CANDIDATE']) {
    const s = base(); s.discovery_route = route;
    assert.equal(validate(s).status, 'CLOSED');
  }
});
test('destructive candidates never close even with singular output', () => {
  for (const name of ['subject-loss', 'relation-loss', 'branch-loss', 'history-loss', 'unsafe-compression', 'false-reset', 'false-certificate']) {
    const r = validate(fixture(name));
    assert.equal(r.status, 'INVALID', name);
    assert.ok(r.trace[0].evaluations.some(e => e.status === 'FAIL'));
  }
});
test('remaining continuation and missing evidence prevent premature certification', () => {
  assert.equal(validate(fixture('path-split')).status, 'UNRESOLVED');
  assert.equal(validate(fixture('missing-path')).reason, 'MISSING_EVIDENCE');
  assert.equal(validate(fixture('multiple-results')).status, 'UNRESOLVED');
});
test('safe certificates, compression and persistent consequences pass', () => {
  for (const name of ['certificate', 'safe-compression', 'cause-removal']) assert.equal(validate(fixture(name)).status, 'CLOSED');
});
test('boundary minimization recurses with full state and preserves prior receipts', () => {
  const r = validate(fixture('boundary-refinement'));
  assert.equal(r.status, 'CLOSED');
  assert.equal(r.trace.length, 3);
  assert.deepEqual(r.final_state.active_boundary, []);
  assert.equal(r.final_state.prior_evaluations.length, 3);
  assert.equal(r.trace[1].input_state.prior_evaluations.length, 1);
  assert.equal(validate(fixture('boundary-refinement'), {maxPasses: 1}).reason, 'MAX_PASSES');
});
test('reopening refines only crossing blocks and preserves unrelated distinctions', () => {
  const s = fixture('reopen');
  s.partition = [['a'], ['b']];
  const r = validate(s);
  assert.equal(r.status, 'UNRESOLVED');
  assert.deepEqual(r.final_state.partition, s.partition);
  assert.equal(r.trace[0].evaluations[11].evidence.reopened, true);
});
test('all finite law evaluators produce evidence-bearing evaluations', () => {
  const s = prepare(base());
  for (const e of registry) {
    const r = e.evaluate(s);
    assert.equal(r.law_id, e.id);
    assert.ok(r.evidence);
    assert.ok(['PASS', 'FAIL', 'UNKNOWN', 'UNRESOLVED', 'NOT_APPLICABLE'].includes(r.status));
  }
});
test('coordinate sufficiency retains one of two redundant correlated coordinates', () => {
  const s = fixture('multiple-results');
  s.possibility_space.forEach(r => {r.values.copy = r.values.delivered;});
  s.active_boundary = ['delivered', 'copy'];
  const r = validate(s);
  assert.equal(r.final_state.active_boundary.length, 1);
  assert.equal(r.status, 'UNRESOLVED');
});
test('conflicting consequences preserve both alternatives', () => {
  const a = {law_id: 101, derived_state_changes: {context: 'north'}};
  const b = {law_id: 102, derived_state_changes: {context: 'south'}};
  assert.equal(collate([a, b]).conflicts.length, 1);
  const evaluators = [a, b].map(e => ({evaluate: () => ({...e, status: 'PASS', evidence: {}})}));
  const r = validate(base(), {evaluators});
  assert.equal(r.status, 'CONFLICTED');
  assert.deepEqual(r.trace[0].conflicts[0].alternatives, ['north', 'south']);
  assert.equal(r.final_state.context, undefined);
  assert.equal(r.final_state.conflicts.length, 1);
});
test('oscillating consequences stop at repeated-state boundary', () => {
  const extra = {evaluate: s => ({law_id: 101, status: 'PASS', evidence: {}, derived_state_changes: {context: s.context === 'north' ? 'south' : 'north'}})};
  const s = base(); s.context = 'north';
  const r = validate(s, {evaluators: [extra]});
  assert.equal(r.reason, 'REPEATED_STATE');
  assert.equal(r.trace.length, 2);
});
test('malformed or incomplete finite states cannot masquerade as closure', () => {
  const empty = base(); empty.possibility_space = [];
  assert.throws(() => validate(empty), /nonempty/);
  const unknown = base(); unknown.candidate_transform.images[0].source = 'ghost';
  assert.throws(() => validate(unknown), /known sources/);
  const missing = base(); delete missing.candidate_transform.images[0].values.delivered;
  assert.throws(() => validate(missing), /missing requested/);
  const partial = base(); partial.continuations = [{outcomes: {a: true}}];
  assert.throws(() => validate(partial), /cover every/);
  const bad = base(); bad.partition = [['a']];
  assert.throws(() => validate(bad), /cover every/);
  const nan = base(); nan.context = NaN;
  assert.throws(() => validate(nan), /finite JSON/);
  assert.throws(() => validate(base(), {maxPasses: 0}), /positive integer/);
});
test('law outcomes refer to candidate conformance, not truth of the law', () => {
  const s = prepare(fixture('multiple-results'));
  assert.equal(evaluateLaw(5, s).status, 'UNRESOLVED');
  assert.equal(evaluateLaw(5, s).holds, null);
  assert.equal(currentRows(s).length, 2);
});
