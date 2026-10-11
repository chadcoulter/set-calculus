import {readFileSync} from 'node:fs';
import {validate} from './harness.js';
try {
  const args = process.argv.slice(2);
  if (!args.length) throw new Error('Usage: node src/cli.js state.json [--json]');
  const report = validate(JSON.parse(readFileSync(args[0], 'utf8')));
  if (args.includes('--json')) console.log(JSON.stringify(report, null, 2));
  else {
    console.log(`${report.status}: ${report.reason}`);
    console.log(`Discovery route: ${report.discovery_route}; evaluation passes: ${report.trace.length}`);
    for (const receipt of report.trace) {
      console.log(`Pass ${receipt.pass}`);
      for (const e of receipt.evaluations) console.log(`  Law ${e.law_id}: ${e.status} - ${e.metaphor_name}`);
    }
  }
  process.exitCode = report.status === 'CLOSED' ? 0 : report.status === 'INVALID' ? 1 : 2;
} catch (error) {
  console.error(`Input error: ${error.message}`);
  process.exitCode = 3;
}
