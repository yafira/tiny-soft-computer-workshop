# tiny soft computer

Website for the "tiny soft computer" workshop by alannabean × electrocute,
part of the SOFTER residency in Denmark.

## structure

- `index.html` — homepage, with a live simulated e-ink hero
- `setup.html` — step-by-step hardware/CircuitPython setup guide
- `code.html` — the working `code.py`, with a download link
- `about.html` — pedagogy, references (The Embroidered Computer, 1-Bit Symphony)
- `style.css` — shared styles
- `script.js` — hero animation only
- `tiny_soft_computer_code.py` — the actual code file, served for download
- `SETUP_SOURCE.md` — original working notes the setup guide was built from

## deploying

Static site, no build step. Works directly with GitHub Pages:

1. Push this repo to GitHub
2. Repo Settings → Pages → Deploy from branch → `main` → `/ (root)`
3. Site will be live at `https://<username>.github.io/<repo-name>/`

## still to do

- [ ] add real photos of the build (kit, enclosure, working display)
- [ ] add the mini zine / pedagogy handout as a downloadable PDF
- [ ] confirm final button wiring diagram, add a diagram image
- [ ] add Alanna's soft-fabrication instructions once finalized
- [ ] swap placeholder Instagram links if handles change
- [ ] add real facilitator bios
