# tiny soft computer
# press the button for a small kind reminder
# Feather RP2040 ThinkInk + 2.13" 212x104 Flexible Monochrome eInk (IL0373)

import time
import random
import board
import busio
import displayio
import terminalio
import digitalio
from fourwire import FourWire
import adafruit_il0373
from adafruit_display_text import label

# ---------------------------------------------------------------
# EDIT ME: add, remove, or change any of these reminders freely.
# keep them short, they need to fit on a small screen.
# ---------------------------------------------------------------
reminders = [
    "you can rest now",
    "you are doing enough",
    "it's okay to slow down",
    "you don't have to earn rest",
    "you are allowed to take up space",
    "this moment is enough",
    "be gentle with yourself today",
    "you are not behind",
    "small steps still count",
    "you deserve softness too",
]

print("starting up")

displayio.release_displays()

# button setup, one button to keep the build simple
button = digitalio.DigitalInOut(board.A0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# auto-detect Feather RP2040 ThinkInk pins
spi = busio.SPI(board.EPD_SCK, MOSI=board.EPD_MOSI, MISO=None)
epd_cs = board.EPD_CS
epd_dc = board.EPD_DC
epd_reset = board.EPD_RESET
epd_busy = board.EPD_BUSY

display_bus = FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)
time.sleep(1)

display = adafruit_il0373.IL0373(
    display_bus,
    width=212,
    height=104,
    rotation=90,
    busy_pin=epd_busy,
    black_bits_inverted=False,
    color_bits_inverted=True,
    swap_rams=True,
)
print("display ready")


def show_message(message):
    g = displayio.Group()

    main_bitmap = displayio.Bitmap(display.width, display.height, 2)
    main_palette = displayio.Palette(2)
    main_palette[0] = 0xFFFFFF  # background
    main_palette[1] = 0x000000  # text
    main_sprite = displayio.TileGrid(main_bitmap, pixel_shader=main_palette)
    g.append(main_sprite)

    text_area = label.Label(terminalio.FONT, text=message, scale=1, color=0x000000)
    text_area.anchor_point = (0.5, 0.5)
    text_area.anchored_position = (display.width // 2, display.height // 2)
    g.append(text_area)

    display.root_group = g
    display.refresh()
    time.sleep(display.time_to_refresh + 5)


# intro sequence
show_message("tiny soft computer")
time.sleep(2)
show_message("starting up")
time.sleep(1.5)
show_message("press the button\nfor a soft reminder")
print("ready, press the button for a reminder")

# main loop: wait for a button press, then show a random reminder
while True:
    if not button.value:  # button pressed
        message = random.choice(reminders)
        print("showing:", message)
        show_message(message)
        time.sleep(1)  # small pause so one press doesn't trigger twice
    time.sleep(0.05)
