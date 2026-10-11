import {currentRows, preservation, image, quotient, sufficientBoundary, sufficientPartition, refinePartition, same, subset, unique} from './model.js';

export const names = ['Resolution Relevance', 'Transformation Preservation', 'Viability Preservation', 'Provenance Persistence', 'Resolution Singularity', 'Quotient Termination', 'Relational Sufficiency', 'Coordinate Agnosticism', 'Boundary Stability', 'Frontier Navigation', 'Dangling Certification', 'Reopen Locality', 'Efficiency Invariance', 'Path-Relative Resolution', 'Transformational Resolution', 'Safe Compression', 'Consequence Persistence', 'Equivalence-Admissibility Independence'];
const result = (id, status, evidence, changes = {}, consequence = null) => ({law_id: id, metaphor_name: names[id-1], status, holds: status === 'PASS' ? true : status === 'FAIL' ? false : null, evidence, violated_constraint: status === 'FAIL' ? names[id-1] : null, consequence, derived_state_changes: changes});
const check = (id, ok, evidence, changes = {}, consequence = 'REJECT_CANDIDATE') => result(id, ok ? 'PASS' : 'FAIL', evidence, ok ? {} : changes, ok ? null : consequence);
const na = id => result(id, 'NOT_APPLICABLE', {reason: 'No corresponding operation or claim supplied'});
const unknown = (id, reason) => result(id, 'UNKNOWN', {reason});

export function evaluateLaw(id, s) {
  const rows = currentRows(s), request = s.requested_resolution;
  const outputs = image(rows, request), q = quotient(rows, request), p = preservation(s);
  const adm = Object.values(p).every(Boolean);
  switch (id) {
    case 1: return result(id, 'PASS', {relevant_classes: q, requested_image: outputs});
    case 2: return s.candidate_transform ? check(id, p.subject && p.relations, p) : na(id);
    case 3: return s.candidate_transform ? check(id, p.viability, {source_count: s.possibility_space.length, image_count: rows.length, viable: rows.map(r => r.viable)}) : na(id);
    case 4: return s.candidate_transform ? check(id, p.provenance, {source_provenance: s.possibility_space.map(r => [r.id, r.provenance]), image_provenance: rows.map(r => [r.source, r.provenance])}) : na(id);
    // Multiple outcomes mean unresolved, not a false law.
    case 5: return result(id, outputs.length === 1 ? 'PASS' : 'UNRESOLVED', {requested_image: outputs});
    case 6: return result(id, sufficientPartition(rows, request, s.partition) ? 'PASS' : 'UNRESOLVED', {partition: s.partition, quotient: q}, sufficientPartition(rows, request, s.partition) ? {} : {partition: refinePartition(s.partition, q)}, 'REFINE_CROSSING_BLOCKS');
    case 7: return result(id, outputs.length === 1 ? 'PASS' : 'UNRESOLVED', {requested_coordinate: request.coordinate, requested_image: outputs, constituent_values: rows.map(r => r.values)});
    case 8: {
      const irrelevant = unique(rows.flatMap(r => Object.keys(r.values))).filter(k => sufficientBoundary(rows, request, s.active_boundary.filter(x => x !== k)));
      return result(id, 'PASS', {coordinates_removable_from_selected_boundary: irrelevant});
    }
    case 9: {
      const sufficient = sufficientBoundary(rows, request, s.active_boundary);
      const redundant = s.active_boundary.filter(k => sufficientBoundary(rows, request, s.active_boundary.filter(x => x !== k)));
      if (!sufficient) return result(id, 'UNRESOLVED', {boundary: s.active_boundary}, {active_boundary: [request.coordinate]}, 'RESTORE_SUFFICIENT_BOUNDARY');
      // Remove one coordinate per pass; removing all individually redundant coordinates is unsound.
      return result(id, 'PASS', {sufficient, minimal: !redundant.length, redundant}, redundant.length ? {active_boundary: s.active_boundary.filter(k => k !== redundant[0])} : {}, redundant.length ? 'MINIMIZE_BOUNDARY' : null);
    }
    case 10: return result(id, sufficientPartition(rows, request, s.partition) ? 'PASS' : 'UNRESOLVED', {partition: s.partition, exact_frontier: same(s.partition, q), quotient: q});
    case 11: {
      if (!s.closure_certificate) return na(id);
      const c = s.closure_certificate;
      return check(id, same(c.request, request) && same(c.domain, rows.map(r => r.id)) && outputs.length === 1 && same(c.image, outputs), {certificate: c, actual_image: outputs});
    }
    case 12: {
      if (!s.previous_resolution) return na(id);
      const previous = s.previous_resolution;
      if (!rows.every(r => Object.hasOwn(previous.outcomes ?? {}, r.id))) return unknown(id, 'Prior outcomes do not cover the current domain');
      const oldImage = unique(rows.map(r => previous.outcomes[r.id]));
      const refined = refinePartition(s.partition, q);
      const reopened = oldImage.length === 1 && outputs.length > 1;
      return result(id, 'PASS', {prior_image: oldImage, current_image: outputs, reopened}, reopened && !same(refined, s.partition) ? {partition: refined} : {}, reopened ? 'REOPEN_REQUEST_QUOTIENT' : null);
    }
    case 13: {
      if (!s.previous_resolution) return na(id);
      const old = unique(Object.values(s.previous_resolution.outcomes ?? {}));
      return result(id, 'PASS', {previous_image: old, current_image: outputs, image_unchanged: subset(old, outputs) && subset(outputs, old), multiplicity: outputs.length});
    }
    case 14: {
      if (!s.continuations) return unknown(id, 'Declare the remaining continuation family; [] explicitly means no remaining path');
      if (!Array.isArray(s.continuations)) throw new Error('continuations must be an array');
      const images = s.continuations.map(c => {
        if (!rows.every(r => Object.hasOwn(c.outcomes ?? {}, r.id))) throw new Error('Continuation must cover every current row');
        return unique(rows.map(r => c.outcomes[r.id]));
      });
      return result(id, images.every(xs => xs.length === 1) ? 'PASS' : 'UNRESOLVED', {continuation_images: images});
    }
    case 15: {
      if (!s.candidate_transform) return na(id);
      if (!adm) return check(id, false, {preservation: p, requested_image: outputs});
      return result(id, outputs.length === 1 ? 'PASS' : 'UNRESOLVED', {before_image: image(s.possibility_space, request), after_image: outputs, preservation: p});
    }
    case 16: {
      if (!s.compression) return na(id);
      if (!s.continuations) return unknown(id, 'Compression requires its preserved continuation family');
      if (!rows.every(r => Object.hasOwn(s.compression.labels ?? {}, r.id))) throw new Error('Compression labels must cover every current row');
      const maps = [{outcomes: Object.fromEntries(rows.map(r => [r.id, r.values[request.coordinate]]))}, ...s.continuations];
      if (!maps.every(c => rows.every(r => Object.hasOwn(c.outcomes ?? {}, r.id)))) throw new Error('Compression continuations must cover every current row');
      const witnesses = [];
      for (const a of rows) for (const b of rows) if (same(s.compression.labels[a.id], s.compression.labels[b.id])) for (const c of maps) if (!same(c.outcomes[a.id], c.outcomes[b.id])) witnesses.push([a.id, b.id]);
      return check(id, !witnesses.length, {separated_merged_pairs: witnesses});
    }
    case 17: {
      if (!s.causal_record) return na(id);
      const c = s.causal_record;
      if (!Array.isArray(c.before_effects) || !Array.isArray(c.after_effects)) throw new Error('Causal record requires before_effects and after_effects');
      const removed = c.before_effects.filter(e => !c.after_effects.some(x => same(e, x)));
      return check(id, !c.cause_removed || !removed.length || !!c.restoration_evidence, {removed_effects: removed, restoration_evidence: c.restoration_evidence ?? null});
    }
    case 18: return s.candidate_transform ? check(id, adm, {requested_image: outputs, preservation: p, singularity_is_not_admissibility: true}) : na(id);
    default: throw new Error(`Unknown law ${id}`);
  }
}
export const registry = names.map((name, i) => ({id: i+1, name, evaluate: s => evaluateLaw(i+1, s)}));
