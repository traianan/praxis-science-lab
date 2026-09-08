# Praxis Science Lab

Public documentation, legal policies, and support portal for apps developed by Praxis Science Lab.

Website: https://traianan.github.io/praxis-science-lab/

## Current scope

An English homepage and app-specific information, privacy, support and Google Play preparation pages for five Android apps. Scientific Calculator is first in the release order. Public support: traiananghel@gmail.com. No app is represented as already available on Google Play.

Plain HTML and CSS with a small local script that updates the copyright year on page load: `2026` in the founding year, then `2026–current year`. A Light / Dark / System group of icon buttons (sun, moon, monitor) highlights the active preference, defaults to System, follows device changes and saves only the theme preference in localStorage. Dark uses a true black background; its internal `black` value is retained for compatibility with saved preferences. If storage is blocked, selection still works for the current page; without JavaScript the device theme is followed. No external fonts, analytics, cookies or runtime dependencies added by this site. GitHub Pages provides hosting and has its own infrastructure practices.

## Publishing

GitHub Pages publishes `main` from the repository root. `.nojekyll` keeps the site as static files. All local asset links are relative so the site works at the project URL, including its `/praxis-science-lab/` prefix. No package installation or build command is required.

To preview locally, run `python -m http.server 8000` from this directory. Run `python scripts/check_site.py` for static integrity checks. Browser layout/interaction testing is not claimed by that check.

## App documentation

Each app uses `apps/<slug>/` with `privacy/`, `support/`, `publishing/`, English store text and `media/`. The shared guide is at `publishing/`; website privacy is at `privacy/`.

Reviewed source inventories live in `scripts/apps.json`. Regenerate pages with `python scripts/build_documents.py`; feature graphics with `python scripts/build_media.py` (Pillow and Windows Arial). `scripts/build_icons.cjs` uses the bundled Sharp runtime and also synchronizes three Android projects' launcher PNGs; run it only when intentionally updating those app icons. The calculator and terminology icon exports preserve existing app designs. No medical learning content was created.

Run `python scripts/check_site.py` to validate all pages, local links, listing lengths, graphic dimensions and text contrast. This does not establish Google Play approval, legal identity verification, provider-specific Data safety answers, a completed closed test or device QA.

The terminology app's current release contains no production dataset and must not be submitted as a functioning learning app. Its governed embedded-policy/URL update remains a separate tracked release item. Ceas Atomic's network-provider Data safety review remains open. All final declarations must match the exact uploaded artifact and all active variants.

## Brand assets

- `assets/logo.svg`: horizontal vector wordmark, for light backgrounds.
- `assets/logo.png`: transparent 4× raster version of that wordmark.
- `assets/logo-mark.svg` and `assets/logo-mark.png`: square brand symbol, raster 512×512.
- `assets/logo-symbol.svg`: white symbol for blue backgrounds, used in the homepage brand panel.
- `assets/favicon.svg` and `assets/favicon.ico`: browser icons; ICO contains 16, 32 and 48px sizes.
- `assets/apple-touch-icon.png`: 180×180 touch icon.

The original geometric P pairs a strong vertical stem with a yellow point: a compact mark for ideas put into practice. Primary blue `#1739d6`, ink `#15233b`, accent yellow `#ffe076`, white background. Arial/Helvetica wordmark and interface; Georgia editorial headline. Keep the symbol proportions and clear space, and use the blue square version on an unknown background. No external image or font asset is required.
