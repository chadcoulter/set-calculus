export function base() {
  return {
    identity: 'package',
    discovery_route: 'QUICK_CANDIDATE',
    requested_resolution: {coordinate: 'delivered'},
    required_relations: ['recipient'],
    possibility_space: [
      {id: 'a', identity: 'package', values: {delivered: false, route: 'north'}, relations: ['recipient'], viable: true, provenance: ['origin-a']},
      {id: 'b', identity: 'package', values: {delivered: true, route: 'south'}, relations: ['recipient'], viable: true, provenance: ['origin-b']}
    ],
    candidate_transform: {images: [
      {source: 'a', id: 'a', identity: 'package', values: {delivered: true, route: 'north'}, relations: ['recipient'], viable: true, provenance: ['origin-a', 'delivered']},
      {source: 'b', id: 'b', identity: 'package', values: {delivered: true, route: 'south'}, relations: ['recipient'], viable: true, provenance: ['origin-b', 'delivered']}
    ]},
    active_boundary: [],
    continuations: [],
    provenance: ['candidate-found-before-validation']
  };
}
export function fixture(name) {
  const s = base();
  const rows = s.candidate_transform.images;
  switch (name) {
    case 'convergence': break;
    case 'subject-loss': rows[0].identity = 'different-package'; break;
    case 'relation-loss': rows[0].relations = []; break;
    case 'branch-loss': rows.pop(); break;
    case 'history-loss': rows[0].provenance = []; break;
    case 'multiple-results': delete s.candidate_transform; s.active_boundary = ['delivered']; break;
    case 'missing-path': delete s.continuations; break;
    case 'path-split': s.continuations = [{outcomes: {a: 'late', b: 'on-time'}}]; break;
    case 'certificate': s.closure_certificate = {domain: ['a', 'b'], request: s.requested_resolution, image: [true]}; break;
    case 'false-certificate': s.closure_certificate = {domain: ['a'], request: s.requested_resolution, image: [true]}; break;
    case 'safe-compression': s.compression = {labels: {a: 0, b: 0}}; break;
    case 'unsafe-compression': s.compression = {labels: {a: 0, b: 0}}; s.continuations = [{outcomes: {a: 'late', b: 'on-time'}}]; break;
    case 'reopen': delete s.candidate_transform; s.active_boundary = ['delivered']; s.previous_resolution = {outcomes: {a: true, b: true}}; break;
    case 'cause-removal': s.causal_record = {cause_removed: true, before_effects: ['damage'], after_effects: ['damage']}; break;
    case 'false-reset': s.causal_record = {cause_removed: true, before_effects: ['damage'], after_effects: []}; break;
    case 'boundary-refinement': s.active_boundary = ['route', 'delivered']; break;
    default: throw new Error(`Unknown fixture ${name}`);
  }
  return s;
}
