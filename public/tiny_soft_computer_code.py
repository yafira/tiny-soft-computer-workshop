# tiny soft computer
# press the button for a little something
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


# MESSAGES + ASCII ART: add, remove, or change these freely.
content = [
    "you can rest now",
    "you are doing enough",
    "it's okay to slow down",
    "you don't have to earn rest",
    "you are allowed to take up space",
    "this moment is enough",
    "be gentle with yourself today",
    "you are not behind",
    "know when to fold 'em",
    "ready...set...go....",
    "small steps still count",
    "inhale.....exhale.......",
    "you have what you need already",
    "things do come back around",
    "anything can be a poem - even this",
    "you deserve softness too",
    "you are allowed to change your mind",
    "it's okay to ask for help",
    "you don't have to be productive right now",
    "your feelings make sense",
    "you can start again tomorrow",
    "you are worth taking care of",
    "it's okay to not know yet",
    "you can let this be easy",
    "you are allowed to say no",
    "you did not have to be perfect today",
    "this is a good place to pause",
    "you are allowed to feel proud",
    "you can trust yourself here",
    "it's okay to take up less than everything today",
    "you are still growing",

    # expressive faces
    "(^_^)",
    "(._.)",
    "(o_o)",
    "(>_<)",
    "(^.^)",
    "(*_*)",
    "(>.<)",
    "(^o^)",
    "(-_-)",
    "(u_u)",
    "(. .)",
    "(^-^)",

    # tiny sun
    [
        " \\ | / ",
        "-- * --",
        " / | \\ ",
    ],
]


print("starting up")

displayio.release_displays()


# BUTTON SETUP
# one button to keep the build simple

button = digitalio.DigitalInOut(board.A2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


# DISPLAY SETUP
# auto-detect Feather RP2040 ThinkInk pins

spi = busio.SPI(
    board.EPD_SCK,
    MOSI=board.EPD_MOSI,
    MISO=None
)

epd_cs = board.EPD_CS
epd_dc = board.EPD_DC
epd_reset = board.EPD_RESET
epd_busy = board.EPD_BUSY

display_bus = FourWire(
    spi,
    command=epd_dc,
    chip_select=epd_cs,
    reset=epd_reset,
    baudrate=1000000
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
print("time_to_refresh:", display.time_to_refresh, "seconds")


# tracks when the next safe refresh is allowed
next_refresh_time = 0


def draw_screen(lines):
    global next_refresh_time

    g = displayio.Group()

    # white background
    main_bitmap = displayio.Bitmap(
        display.width,
        display.height,
        2
    )

    main_palette = displayio.Palette(2)
    main_palette[0] = 0xFFFFFF
    main_palette[1] = 0x000000

    main_sprite = displayio.TileGrid(
        main_bitmap,
        pixel_shader=main_palette
    )

    g.append(main_sprite)

    # add text
    # lines is a list of (text, scale, y_offset)

    for text_content, scale, y_offset in lines:

        text_area = label.Label(
            terminalio.FONT,
            text=text_content,
            scale=scale,
            color=0x000000
        )

        text_area.anchor_point = (0.5, 0.5)

        text_area.anchored_position = (
            display.width // 2,
            display.height // 2 + y_offset
        )

        g.append(text_area)

    display.root_group = g

    now = time.monotonic()

    if now < next_refresh_time:

        remaining = int(next_refresh_time - now)

        print(
            "display still resting:",
            remaining,
            "seconds remaining"
        )

        return False

    try:

        print("refreshing display...")

        display.refresh()

        print("refresh complete")

        # follow the display's recommended refresh timing
        next_refresh_time = (
            time.monotonic()
            + display.time_to_refresh
            + 5
        )

        print(
            "next refresh in approximately:",
            int(next_refresh_time - time.monotonic()),
            "seconds"
        )

        return True

    except RuntimeError as error:

        print("couldn't refresh yet:", error)

        next_refresh_time = (
            time.monotonic()
            + display.time_to_refresh
            + 5
        )

        return False


def show_message(message):

    print("showing:", message)

    # ASCII art can contain multiple lines.
    if isinstance(message, list):

        lines = []

        # center the three-line sun
        start_y = -14

        for line in message:

            lines.append(
                (line, 1, start_y)
            )

            start_y += 14

        return draw_screen(lines)

    # regular message or face
    return draw_screen([
        (message, 1, 0)
    ])


def show_intro():

    return draw_screen([
        ("tiny soft computer", 1, -14),
        ("press the button\nto begin", 1, 18),
    ])


def wait_for_next_refresh():
    # sleep exactly until the display says it's ready again
    remaining = next_refresh_time - time.monotonic()
    if remaining > 0:
        print("waiting", int(remaining), "seconds before the next one")
        time.sleep(remaining)


def run_full_loop():
    # one press goes through everything, in a random order,
    # pacing itself to the display's real refresh limit
    order = list(content)
    random.shuffle(order)

    print("starting a full loop through", len(order), "items")

    for item in order:
        show_message(item)
        wait_for_next_refresh()

    print("loop complete")
    show_intro()


# STARTUP

show_intro()

print("ready, press the button to begin")


# MAIN LOOP
# one press starts a full randomized loop through everything

while True:

    if not button.value:

        print("BUTTON PRESSED")

        # wait for the physical button to be released before starting,
        # so a long press doesn't retrigger anything
        while not button.value:
            time.sleep(0.01)

        print("BUTTON RELEASED")

        if time.monotonic() >= next_refresh_time:
            run_full_loop()
        else:
            remaining = int(next_refresh_time - time.monotonic())
            print(
                "display is resting.",
                remaining,
                "seconds until it can start."
            )

    time.sleep(0.05)