/* Publish only reviewed static file types from explicit public directories. */
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'build', 'public');
const allowed = new Set(['.html', '.css', '.js', '.png', '.webp', '.svg', '.ico', '.apk', '.zip', '.txt']);
const roots = ['assets', 'apps', 'privacy', 'publishing', 'contact', 'legal', 'terms', 'projects'];
function copy(source, target) {
  const stat = fs.lstatSync(source);
  if (stat.isSymbolicLink()) throw new Error('Symlinks are not publishable');
  if (stat.isDirectory()) {
    fs.mkdirSync(target, {recursive: true});
    for (const name of fs.readdirSync(source)) {
      if (name.startsWith('.') || name === 'developer-profile' || name === 'node_modules') continue;
      copy(path.join(source, name), path.join(target, name));
    }
  } else if (allowed.has(path.extname(source))) {
    fs.copyFileSync(source, target);
  }
}
// The destination is fixed beneath this repository; never remove arbitrary paths.
if (fs.existsSync(output) && fs.lstatSync(output).isSymbolicLink()) throw new Error('Unsafe output link');
if (fs.existsSync(path.dirname(output)) && fs.lstatSync(path.dirname(output)).isSymbolicLink()) throw new Error('Unsafe build link');
fs.rmSync(output, {recursive: true, force: true});
fs.mkdirSync(output, {recursive: true});
for (const name of roots) copy(path.join(root, name), path.join(output, name));
for (const name of ['index.html', '404.html', 'robots.txt', 'sitemap.xml', '.nojekyll']) {
  fs.copyFileSync(path.join(root, name), path.join(output, name));
}
console.log('Public build created in build/public (private projects and source files excluded).');
