# Remedierea auditului din 6 noiembrie 2026

Țintă: site-ul `praxis-science-lab`. La încheierea remedierii inițiale, modificările erau locale, fără commit/push/deploy. Ulterior, proprietarul a autorizat explicit publicarea și redirecționarea GitHub Pages. Constatările de mai jos păstrează contextul verificării inițiale; configurația de publicare este descrisă în README. Modificările preexistente ale proprietarului au fost păstrate. Documentul de audit a fost tratat ca dovadă de verificat, nu ca instrucțiune de executare automată.

## Corecții implementate

| Referință audit | Rezultat |
|---|---|
| 1.4 — risc de publicare a datelor private | Vercel este configurat să publice numai `build/public`, generat printr-o listă explicită de directoare și extensii publice. Proiectul PFA, fișierele ascunse, bazele de date, sursele și documentele interne nu intră în rezultat. Întregul `pfa-studio/` este acum ignorat de Git. Proiectul contabil și datele lui nu au fost mutate sau modificate. Protecția de build devine efectivă pe Vercel după publicarea configurației; setarea veche GitHub Pages rămâne o acțiune separată. |
| 1.5 — documentație | README indică domeniul principal, 34 de aplicații, contactul actual și comenzile de build. VALIDATION și SOURCE_REVIEW sunt marcate explicit ca dovezi istorice; rezultatele Android din septembrie nu sunt prezentate ca reverificate în noiembrie. |
| 2.1–2.2 — iconițe supradimensionate | 27 miniaturi WebP de 112×112, fără schimbarea originalelor sau a materialelor pentru magazine. Totalul imaginilor referite din catalog: **40.080 B**, inclusiv sigla; miniaturile: 39.700 B. Auditul raporta aproximativ 2,1 MB. |
| 2.3 — cache | Cache de o oră, cu revalidare, pentru assets și media. Nu se aplică un an de `immutable` fișierelor cu nume stabile. |
| 3.1 — date structurate | `SoftwareApplication` pentru cele 34 de pagini de prezentare, plus `BreadcrumbList` pentru paginile aplicațiilor. Numele, descrierea și categoria provin din inventar. Nu sunt inventate prețuri, oferte, ratinguri sau disponibilitate în magazine. |
| 3.3–3.5 — metadate | Titluri și descrieri de confidențialitate în EN/RO/ES; descrieri specifice aplicației pentru support și publishing; legături `hreflang` reciproce pentru traducerile existente, inclusiv help, cu `x-default`. |
| 3.7 — imagini sociale | Feature graphic per aplicație când există, apoi iconița existentă; sigla rămâne fallback pentru aplicațiile fără artwork. |
| 3.9–3.10 — publishing | Toate cele 35 de pagini au `noindex, follow` în HTML, independent de suportul hostului pentru headere. Linkul promoțional către kit a fost înlocuit pe homepage cu informații și suport pentru aplicații. URL-urile existente și navigația internă a documentației sunt păstrate. |
| 4 — securitate și 404 | CSP, X-Frame-Options și Permissions-Policy în configurația Vercel; pagină 404 proprie, exclusă din indexare. Aceste headere necesită deploy pentru a deveni active online. |
| 5.1–5.2 — accesibilitate | Badge-urile și categoriile au 12px; titlurile cardurilor din cataloage sunt h2 după h1. Homepage-ul păstrează h3 sub secțiuni h2. |
| 6.1–6.3 — verificator | Eliminată dependența Pillow din verificare. Dimensiunile și tipul PNG se citesc din IHDR. Verificările folosesc excepții explicite și funcționează și cu `python -O`. Contrastul de bază se calculează din tokenurile CSS reale ale celor trei definiții de temă. |
| 6.4 — CI | Workflow de validare pentru push și pull request, cu checker normal/optimizat, teste de regresie și build public. Devine activ după commit/push. |
| 6.5 — catalog | Cardurile Android se generează direct din `apps.json`; `catalog_cards.json` păstrează numai proiectele web. Corectată și calea `--home-only`, astfel încât cataloagele și metadatele să fie regenerate înainte de ieșire. |
| 6.9 — igienă | Eliminată intrarea duplicată `.vercel`; `debug.log`, datele PFA și metadatele locale Serena sunt ignorate. Fișierul de log existent nu a fost șters. |

## Verificări executate

- `python scripts/check_site.py`: PASS, 154 pagini, linkuri/ancore/fișiere locale, dimensiuni PNG, checksum APK, limitele textelor și contrastul tokenurilor CSS.
- `python -O scripts/check_site.py`: PASS, verificările nu dispar în modul optimizat.
- `python -m unittest discover -s scripts -p 'test_*.py'`: 6 teste PASS — idempotența metadatelor, noindex, reciprocitatea traducerilor, concordanța și bugetul de imagini ale catalogului, PNG invalid și izolarea buildului prin fixture cu fișiere private.
- `node scripts/build_public.cjs`: PASS; rezultat în `build/public`.
- `git diff --check`: fără erori de whitespace la verificare.
- Chrome, rezultat local al buildului, catalog: 390×844 light și 1440×1000 dark; fără overflow orizontal, 34 carduri, fără imagini încărcate defectuos. Căutarea TempoLab returnează un card și contorul „1 of 34 apps”. Capturile au fost inspectate în sesiune.

Limite: testarea browserului a folosit fișierele locale, nu o publicare Vercel. Nu reprezintă Lighthouse, audit complet WCAG sau verificare de headere HTTP în producție. Testele de contrast acoperă tokenurile centrale, nu orice combinație randată. Nu au fost reverificate aplicațiile Android sau politicile magazinelor.

## Recomandări neadoptate automat

- **1.1–1.3:** lipsa commiturilor și divergența dintre hosturi sunt riscuri reale. Auditul propune însă publicarea întregului arbore, care conține multă muncă preexistentă și un proiect privat. Nu am executat `git add .`, commit/push în masă, deploy sau dezactivarea unui serviciu. Urmează o publicare verificată din Git și retragerea/redirecționarea copiei GitHub Pages; acestea rămân deschise.
- **2.3:** `max-age=0, must-revalidate` permite stocarea cu revalidare; formularea „nimic nu e cache-uit” este prea categorică. `immutable` pe un an necesită versionarea consecventă a URL-urilor, inclusiv imaginile.
- **2.4/2.6:** variantele responsive pentru screenshot-uri și hero sunt îmbunătățiri suplimentare de performanță; originalele rămân disponibile. Nu am înlocuit imaginile de prezentare cu versiuni mici destinate cardurilor.
- **2.5/3.6/3.8/5.3/5.4:** capturi autentice, iconițe lipsă, FAQ și traducerea întregului site sunt lucrări de conținut, nu defecte demonstrate. Nu au fost inventate capturi, funcții sau declarații despre aplicații.
- **3.1:** lipsa structured data de pe fiecare pagină nu este în sine o eroare; am adăugat tipurile pentru care există date susținute de conținut. Nu am adăugat `offers` fără preț și disponibilitate confirmate.
- **3.2:** `lastmod` este opțional. Nu am pus data auditului sau data unui rebuild ca dată falsă a modificării conținutului. Poate fi introdus după stabilirea unei evidențe reale a modificărilor.
- **5.5:** fără JavaScript, tema urmează sistemul; aceasta este o degradare funcțională acceptabilă, nu un defect de stocare.
- **6.6:** lista de CSS mort nu poate fi aplicată mecanic: `card-preview`, de exemplu, este încă folosită de generator când aplicația are `card_image`. Nu am eliminat selectori numai pe baza numărării paginilor curente.
- **6.7:** checkerul a fost reformatat pentru lizibilitate. Reformatarea în masă a tuturor paginilor generate nu este necesară pentru remedierea defectelor și ar amesteca inutil modificările preexistente.
- **6.8:** mutarea APK-ului la Releases ar necesita încărcarea unui artefact și schimbarea unui URL public. Descărcarea și checksum-ul existente sunt funcționale și au fost păstrate.

Referințe oficiale consultate: [configurația statică Vercel](https://vercel.com/docs/project-configuration/vercel-json), [pagini localizate și hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions), [lastmod și sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
