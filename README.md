# tiny soft computer

Website for the "tiny soft computer" workshop by alannabean × electrocute,
part of the SOFTER residency + conference in Denmark.

Built with [Astro](https://astro.build) — a static site generator, no
client-side framework, ships zero JS by default.

## status

- All 20 kits tested, faulty screens identified and replacements requested
  from Adafruit
- Final `code.py` preloaded onto all kits and retested individually
- Website structure and content in progress, more still to add (see
  "still to do" below)
- Zine and presentation not yet started

## structure

- `src/layouts/Layout.astro` — shared nav + footer, used by every page
- `src/pages/index.astro` — homepage, with a live simulated e-ink hero,
  offers two paths: attending the workshop vs. setting up as an educator
- `src/pages/workshop.astro` — attendee-facing page: the three things
  attendees actually do (tweak the code, wire the button, build the
  enclosure). Kits arrive fully preloaded, so this is intentionally short
- `src/pages/educators.astro` — full technical walkthrough for whoever
  preps kits ahead of time: CircuitPython install, libraries, wiring,
  troubleshooting, serial monitor explainer, batch-flashing checklist.
  Opens with an explicit "this is prep work, not the workshop" framing
- `src/pages/fabrication.astro` — soft-fabrication materials and
  technique (placeholder structure, Alanna's content still to come)
- `src/pages/resources.astro` — BOM and classroom-friendly alternatives
  for educators
- `src/pages/code.astro` — reads `public/tiny_soft_computer_code.py`
  directly at build time and displays it, with a copy-to-clipboard
  button, so the page can never drift out of sync with the real code file
- `src/pages/about.astro` — pedagogy, references (The Embroidered
  Computer, 1-Bit Symphony), and the "why 180 seconds" explanation
- `src/styles/global.css` — shared styles (mustard + lavender accent
  palette, IBM Plex Mono + Fraunces type)
- `public/script.js` — hero animation only
- `public/tiny_soft_computer_code.py` — the actual final code file,
  served for download and read directly by code.astro
- `SETUP_SOURCE.md` — original working notes the educators page was
  built from

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
- [ ] add a real pin diagram image (currently a placeholder on the
      educators page)
- [ ] add Alanna's soft-fabrication instructions to fabrication.astro
- [ ] confirm final BOM pricing on resources.astro (currently a
      placeholder)
- [ ] swap placeholder Instagram links if handles change
- [ ] add real facilitator bios
- [ ] finish the zine and presentation
