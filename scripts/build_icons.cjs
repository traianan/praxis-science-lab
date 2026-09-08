const fs=require('fs'),path=require('path');
const sharp=require('C:/Users/traian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=process.cwd();
const svgs={
'atomic-clock':'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108"><rect width="108" height="108" fill="#1739d6"/><circle cx="54" cy="54" r="29" stroke="white" stroke-width="5" fill="none"/><path d="M54 34v20l17 10" stroke="white" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="81" cy="81" r="7" fill="#ffe076"/></svg>',
'frequency-generator':'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108"><rect width="108" height="108" fill="#1739d6"/><path d="M23 54c10-38 21-38 31 0s21 38 31 0" stroke="white" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="81" cy="81" r="7" fill="#ffe076"/></svg>',
'audiolab':'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108"><path fill="#101B24" d="M0 0H108V108H0Z"/><path stroke="#64E5C0" stroke-width="5" stroke-linecap="round" d="M31 48V60M42 36V72M54 27V81M66 38V70M77 47V61"/></svg>',
'medical-terminology-flashcards':'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><path fill="#275D59" d="M0 0h48v48h-48z"/><path fill="#FFFFFF" d="M10 10h22v26h-22z"/><path fill="#275D59" d="M14 16h14v2h-14zM14 22h14v2h-14zM14 28h8v2h-8z"/><path fill="#B8DAD3" d="M34 14h4v26h-24v-2h20z"/></svg>'};
(async()=>{
for(const [slug,svg] of Object.entries(svgs)){
 const dest=path.join(root,'apps',slug,'media');fs.writeFileSync(path.join(dest,'app-icon.svg'),svg);await sharp(Buffer.from(svg)).resize(512,512).png().toFile(path.join(dest,'app-icon.png'));
 const repo={'atomic-clock':'ceas-atomic','frequency-generator':'frequency-generator','audiolab':'audiolab'}[slug];
 if(repo){for(const [density,size] of Object.entries({mdpi:48,hdpi:72,xhdpi:96,xxhdpi:144,xxxhdpi:192}))await sharp(Buffer.from(svg)).resize(size,size).png().toFile(path.join(root,'..',repo,'android/app/src/main/res',`mipmap-${density}`,'ic_launcher.png'));}
}
await sharp(path.join(root,'../calc-stiintific-cn-iorga/assets/icon.png')).resize(512,512).png().toFile(path.join(root,'apps/scientific-calculator/media/app-icon.png'));
console.log('Exported five 512px store icons; replaced Flutter template raster icons in three Android apps.');
})().catch(e=>{console.error(e);process.exitCode=1});
