# tiny soft computer

Website for the "tiny soft computer" workshop by alannabean × electrocute,
part of the SOFTER residency in Denmark.

Built with [Astro](https://astro.build) — a static site generator, no
client-side framework, ships zero JS by default.

## structure

- `src/layouts/Layout.astro` — shared nav + footer, used by every page
- `src/pages/index.astro` — homepage, with a live simulated e-ink hero
- `src/pages/setup.astro` — step-by-step hardware/CircuitPython setup guide
- `src/pages/code.astro` — reads `public/tiny_soft_computer_code.py` directly
  at build time and displays it, so the page can never drift out of sync
  with the real code file
- `src/pages/about.astro` — pedagogy, references (The Embroidered Computer,
  1-Bit Symphony)
- `src/styles/global.css` — shared styles
- `public/script.js` — hero animation only
- `public/tiny_soft_computer_code.py` — the actual code file, served for
  download and read directly by code.astro
- `SETUP_SOURCE.md` — original working notes the setup guide was built from

## local development

```
npm install
npm run dev
```

Visit `http://localhost:4321`.

## building

```
npm run build
```

Outputs a static site to `dist/`. This was verified to build cleanly.

## deploying

**Vercel** (recommended): connect the GitHub repo, Vercel auto-detects
Astro, no config needed. Every push to `main` redeploys automatically.

**GitHub Pages**: needs `@astrojs/github-pages` adapter or a manual
static export via `npm run build` + publish the `dist/` folder. Vercel
is simpler for this project.

## still to do

- [ ] add real photos of the build (kit, enclosure, working display)
- [ ] add the mini zine / pedagogy handout as a downloadable PDF
- [ ] confirm final button wiring diagram, add a diagram image
- [ ] add Alanna's soft-fabrication instructions once finalized
- [ ] swap placeholder Instagram links if handles change
- [ ] add real facilitator bios
