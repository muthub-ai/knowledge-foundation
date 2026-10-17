// Dump the content folder of the muthub.org repository to JSON for seed_from_site.py.
// Usage: node tools/librarian/dump-site-content.js <path-to-site-repo> site-content.json  (needs the typescript package)

const ts = require(process.env.TYPESCRIPT_PATH || 'typescript');
const fs = require('fs'), path = require('path'), Module = require('module');
const root = process.argv[2];
const cache = {};
function load(file) {
  if (cache[file]) return cache[file].exports;
  const src = fs.readFileSync(file, 'utf8');
  const out = ts.transpileModule(src, { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 } }).outputText;
  const m = { exports: {} }; cache[file] = m;
  const req = (p) => {
    let f = p.startsWith('@/') ? path.join(root, p.slice(2)) : path.resolve(path.dirname(file), p);
    for (const c of [f, f + '.ts', f + '.tsx', path.join(f, 'index.ts')]) if (fs.existsSync(c) && fs.statSync(c).isFile()) return load(c);
    return require(p);
  };
  new Function('exports', 'require', 'module', out)(m.exports, req, m);
  return m.exports;
}
const c = (n) => load(path.join(root, 'content', n + '.ts'));
const out = {
  site: c('site').site, themes: c('site').themes,
  essays: [...c('essays').essays, ...c('essays-more').moreEssays, ...c('context-engineering').contextEngineeringEssays],
  notes: [...c('essays').notes, ...c('essays-more').moreNotes],
  playbooks: c('playbooks').playbooks, initiatives: c('initiatives').initiatives,
};
fs.writeFileSync(process.argv[3], JSON.stringify(out, (k, v) => v instanceof RegExp ? String(v) : v, 1));
console.log(Object.fromEntries(Object.entries(out).map(([k, v]) => [k, Array.isArray(v) ? v.length : typeof v])));
