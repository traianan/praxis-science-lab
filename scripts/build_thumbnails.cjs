/* Optional authoring step: SHARP_MODULE may point to an installed Sharp module. */
const fs = require('node:fs');
const path = require('node:path');
const sharp = require(process.env.SHARP_MODULE || 'sharp');
const root = path.resolve(__dirname, '..');
async function main() {
  const apps = JSON.parse(fs.readFileSync(path.join(root, 'scripts/apps.json'), 'utf8'));
  let count = 0;
  for (const app of apps) {
    const folder = path.join(root, 'apps', app.slug, 'media');
    const source = ['app-icon.png', 'icon.png', 'app-icon.svg'].find(name => fs.existsSync(path.join(folder, name)));
    if (!source) continue;
    await sharp(path.join(folder, source)).resize(112, 112, {fit: 'contain', background: '#00000000'}).webp({quality: 85}).toFile(path.join(folder, 'card-icon.webp'));
    count++;
  }
  console.log(`Generated ${count} catalog thumbnails; original artwork preserved.`);
}
main().catch(error => { console.error(error); process.exitCode = 1; });
