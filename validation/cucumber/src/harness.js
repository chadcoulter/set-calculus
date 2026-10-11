import {copy, prepare, key, currentRows, image, preservation, sufficientPartition, sufficientBoundary, same} from './model.js';
import {registry} from './laws.js';

export function collate(evaluations) {
  const changes = {}, conflicts = [];
  for (const e of evaluations) for (const [field, value] of Object.entries(e.derived_state_changes)) {
    if (Object.hasOwn(changes, field) && !same(changes[field], value)) conflicts.push({field, alternatives: [changes[field], value], law_id: e.law_id});
    else changes[field] = copy(value);
  }
  // A conflict is retained as evidence, never resolved by evaluator order.
  for (const conflict of conflicts) delete changes[conflict.field];
  return {changes, conflicts};
}
export function validate(input, {maxPasses = 32, evaluators = registry} = {}) {
  if (!Number.isInteger(maxPasses) || maxPasses < 1) throw new Error('maxPasses must be a positive integer');
  // Injected evaluators may extend the registry but cannot bypass canonical checks.
  const active = [...registry, ...evaluators.filter(e => !registry.includes(e))];
  let state = prepare(input);
  const trace = [], seen = new Set();
  const finish = (status, reason) => ({status, reason, discovery_route: state.discovery_route, final_state: {...copy(state), resolution_status: status}, trace});
  for (let pass = 0; pass < maxPasses; pass++) {
    const fingerprint = key({...state, provenance: [], prior_evaluations: []});
    if (seen.has(fingerprint)) return finish('BOUNDED_UNRESOLVED', 'REPEATED_STATE');
    seen.add(fingerprint);
    const before = copy(state);
    // Every law gets its own snapshot of the same state; mutation cannot contaminate peers.
    const evaluations = active.map(e => e.evaluate(copy(before)));
    evaluations.forEach((e, index) => {e.provenance_receipt = {pass, evaluation: index, source: 'FINITE_EVIDENCE_VALIDATOR_V1'};});
    const {changes, conflicts} = collate(evaluations);
    const next = {...copy(state), ...changes};
    const receipt = {pass, input_state: before, evaluations: copy(evaluations), consequences: copy(changes), conflicts, derived_state: copy(next)};
    trace.push(receipt);
    next.prior_evaluations.push({pass, law_statuses: evaluations.map(e => [e.law_id, e.status])});
    next.provenance.push({type: 'VALIDATION_PASS', pass, laws: evaluations.map(e => e.law_id)});
    state = next;
    if (conflicts.length) {
      state.conflicts = copy(conflicts);
      return finish('CONFLICTED', 'INCOMPATIBLE_CONSEQUENCES');
    }
    if (evaluations.some(e => e.status === 'FAIL')) return finish('INVALID', 'CANDIDATE_CONSTRAINT_VIOLATION');
    const rows = currentRows(state);
    const complete = evaluations.every(e => !['UNKNOWN', 'UNRESOLVED'].includes(e.status));
    const valid = Object.values(preservation(state)).every(Boolean);
    const ready = complete && valid && image(rows, state.requested_resolution).length === 1 && sufficientPartition(rows, state.requested_resolution, state.partition) && sufficientBoundary(rows, state.requested_resolution, state.active_boundary);
    // Re-evaluate any derived changes before certifying them.
    if (ready && !Object.keys(changes).length) return finish('CLOSED', 'SINGULAR_ADMISSIBLE_REQUEST');
    if (!Object.keys(changes).length) return finish('UNRESOLVED', evaluations.some(e => e.status === 'UNKNOWN') ? 'MISSING_EVIDENCE' : 'MULTIPLE_RELEVANT_OUTCOMES');
  }
  return finish('BOUNDED_UNRESOLVED', 'MAX_PASSES');
}
