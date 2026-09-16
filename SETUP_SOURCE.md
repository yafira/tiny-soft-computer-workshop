# tiny soft computer — setup guide
### draft documentation, for the future workshop website

---

## what you'll need

- Adafruit RP2040 Feather ThinkInk for 24-pin E-Paper Displays (STEMMA QT)
- 2.13" 212x104 Flexible Monochrome / 4-Gray eInk display (ILI0373 chipset)
- USB-C cable
- a computer to program from

**Backup on hand, not in use yet:** Monochrome 0.96" 128x64 OLED Graphic Display (STEMMA QT) — same Feather board can drive this too, either via STEMMA QT or direct wiring, if we need a fallback.

---

## step 1: install CircuitPython on your board

**Before you start: disconnect the eInk display from the Feather.** Having it connected can interfere with the board entering bootloader mode. Reconnect it after CircuitPython is installed.

1. Unplug the board completely.
2. Press and hold the **BOOTSEL** button on the board.
3. While still holding it, plug in the USB-C cable to your computer.
4. Wait a second or two, then release the button. (This "boot on start" method is more reliable than double-pressing reset while already powered on, since there's no timing to get right.)
5. A drive named `RPI-RP2` should appear.
6. Go to [circuitpython.org](https://circuitpython.org), search for your exact board: **"Adafruit Feather RP2040 ThinkInk"**. Don't pick a generic RP2040 file, other Feather RP2040 variants have different pin mappings and won't work correctly with this display.
7. Choose the **stable** release (10.x, not alpha/beta), and download the single `.uf2` file (not a folder or zip).
8. Drag that `.uf2` file onto the `RPI-RP2` drive.
9. The board will restart automatically, and the drive will now be named `CIRCUITPY`. That means CircuitPython is installed.
10. Now you can reconnect the eInk display.

**If the `RPI-RP2` drive never appears:**
- Confirm the eInk display is disconnected (see above).
- Try a different USB-C cable. Some cables are charge-only and don't carry data.
- Try a different USB port, avoid hubs if possible.
- Unplug fully and retry the BOOTSEL sequence from the start.

---

## step 2: add the required libraries

CircuitPython needs a few extra library files to talk to the display and render text. These come from the official Adafruit CircuitPython Library Bundle.

1. Go to [circuitpython.org/libraries](https://circuitpython.org/libraries) and download the **Bundle matching your CircuitPython version** (check the version number in `boot_out.txt` on your CIRCUITPY drive if unsure).
2. Unzip the bundle.
3. On your CIRCUITPY drive, create a folder called `lib` if one doesn't already exist.
4. From the unzipped bundle's `lib` folder, copy these into your CIRCUITPY `lib` folder:
   - `adafruit_il0373.mpy`
   - `adafruit_display_text` (folder)
5. Double check the names match exactly — no typos, no hyphens where there should be underscores. A mismatched name is the most common reason a library fails to import.

---

## step 3: add the test code

1. Copy the provided `code.py` onto your CIRCUITPY drive (see attached test script).
2. The board should auto-run it. If it doesn't, press the reset button once.
3. Watch the serial console (via the REPL) as it runs. The script prints its progress at each step ("starting up", "displays released", "pins set up", etc.), so if something goes wrong you'll see exactly how far it got.
4. After "about to refresh, this takes a couple seconds" prints, **wait, and don't look at the screen yet.** E-ink flickers through intermediate frames during a refresh, this can look like scrambled smudges or blur mid-transition, which is completely normal and not a sign of a problem.
5. Only judge what's on screen once "refresh complete, check the screen" has printed. At that point you should see the words **"tiny soft computer"** appear, centered, on a white background.

**Key parameters this specific display needs** (found through testing, not obvious from generic e-ink examples):
- Library: `adafruit_il0373`, not `adafruit_ssd1680` (that's for a different, rigid display)
- Rotation: `90`
- Must include `black_bits_inverted=False, color_bits_inverted=True, swap_rams=True` when creating the display object.
- Bitmaps must be created with `value_count=2` (a real 2-color bitmap), not `value_count=1`. Using `1` technically creates a zero-bit bitmap that can silently fail to render or composite correctly, even though the code runs with no error. This was the root cause of a lot of confusing "it's not working" testing, not faulty hardware.
- Text color must be explicitly set to black (`color=0x000000`). The default text color is white, invisible against a light background.
- **Do a single refresh, not a separate clear-then-draw double refresh.** An earlier version of this script did a full clear cycle before drawing, which seemed to cause more inconsistent results (smudging, blank screens) on some units. Going straight from display setup to drawing your final content in one refresh has been the more reliable approach.

**A red herring to know about:** if you see a `SyntaxError: invalid syntax` referencing `<stdin>` in the REPL, that's not a problem with your code, it usually means a stray keypress (like an arrow key) got sent into the REPL prompt directly. Press **Ctrl+D** to reload, or press the physical reset button, and try again.

---

## troubleshooting notes (from our own testing)

- CircuitPython version and library bundle version must match exactly (e.g. both 10.x). Mismatched versions cause import errors.
- Folder and file names must be exact: `adafruit_display_text` (underscore, not hyphen), `adafruit_il0373.mpy`.
- This display is genuinely flexible. Don't flex it during a screen refresh, and don't flex near where the ribbon cable connects, since that connection is delicate. Mount it to a stable backing (this is where the soft enclosure comes in) to reduce ongoing stress on the panel.
- The eInk display connected during bootloader mode can prevent the `RPI-RP2` drive from appearing at all. Always disconnect it before flashing CircuitPython, reconnect after.
- Code running with no errors does not mean the display is showing anything. Bitmaps must use `value_count=2`, not `1`, see step 3 for why.
- Don't judge the screen while it's mid-refresh. E-ink flickers through intermediate frames that look like smudges or blur, this is normal, not a fault. Only judge the final result after the code confirms the refresh is complete.
- A single refresh (straight to final content) has been more reliable than a separate clear-then-draw double refresh.
- The display holds its image with no power needed. Once it shows text, you can even unplug it and the image will remain.

**Batch-testing tip:** when testing multiple units, keep a simple tally of which ones passed cleanly versus needed extra troubleshooting (and what fixed it). This becomes real data for estimating per-kit setup time for the actual workshop. Also worth noting: if a display seems to fail, re-test it with the latest known-good code before assuming it's faulty hardware, an earlier bug in our own test script caused some units to look broken when they weren't.

---

## test script

See `eink_test.py` — displays "tiny soft computer" centered on the 2.13" monochrome eInk display.

---

*This is a living draft. Update as we test more units and encounter new issues, so the final version is accurate for attendees building their own kit.*
