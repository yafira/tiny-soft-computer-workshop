# tiny soft computer (OLED version)
# press the button, get a random message, instantly
# Feather RP2040 ThinkInk + Monochrome 0.96" 128x64 OLED (STEMMA QT)

import time
import random
import board
import displayio
import terminalio
import digitalio
import i2cdisplaybus
import adafruit_displayio_ssd1306
from adafruit_display_text import label


# Why this file looks different from the eInk version:
# the eInk display can only redraw once every 180 seconds, so that
# version is built around a shuffle-and-wait loop to work around that.
# this OLED has no such limit, it refreshes instantly, so none of that
# complexity is needed here. press the button, see something new,
# right away. same idea, simpler code, because the hardware allows it.


# MESSAGES + ASCII ART
# Copy your own list from the eInk version's code.py, or start here.
# Add, remove, or change these to make the computer your own.

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

    # Little faces
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
    "(*_.)",
    "(^-^)",

    # A tiny sun
    [
        " \\ | / ",
        "-- * --",
        " / | \\ ",
        "you are a beam of light",
    ],
]


print("starting up")

displayio.release_displays()


# One button, same as the eInk version.
# The button uses a pull-up resistor.
# False means pressed and True means not pressed.

button = digitalio.DigitalInOut(board.A2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


# Set up the OLED over the board's built-in STEMMA QT connector.
# This is I2C, not SPI, so there's no busy pin and no FourWire setup,
# just plug the STEMMA QT cable in and go.

i2c = board.STEMMA_I2C()

display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

display = adafruit_displayio_ssd1306.SSD1306(
    display_bus,
    width=128,
    height=64,
)

print("display ready")


def wrap_text(text, max_chars=20):
    # Break a long message into multiple lines so it fits
    # on this smaller 128px-wide screen.

    words = text.split(" ")
    lines = []
    current = ""

    for word in words:

        if len(current) + len(word) + 1 <= max_chars:
            current = (
                current + " " + word
                if current
                else word
            )

        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return "\n".join(lines)


def draw_screen(lines):
    # Draws one screen. No waiting here, and no refresh() call
    # either, this display auto-refreshes the instant root_group
    # is set. That's the whole benefit of OLED over eInk.

    g = displayio.Group()

    # Create a white background.

    main_bitmap = displayio.Bitmap(
        display.width,
        display.height,
        2
    )

    main_palette = displayio.Palette(2)
    main_palette[0] = 0x000000
    main_palette[1] = 0xFFFFFF

    main_sprite = displayio.TileGrid(
        main_bitmap,
        pixel_shader=main_palette
    )

    g.append(main_sprite)

    # Add each piece of text to the screen.

    for text_content, scale, y_offset in lines:

        text_area = label.Label(
            terminalio.FONT,
            text=text_content,
            scale=scale,
            color=0xFFFFFF
        )

        text_area.anchor_point = (0.5, 0.5)

        text_area.anchored_position = (
            display.width // 2,
            display.height // 2 + y_offset
        )

        g.append(text_area)

    display.root_group = g


def show_message(message):
    # Show one message or drawing on the screen.

    print("")
    print("--------------------------------")

    if isinstance(message, list):

        print("showing:")

        for line in message:
            print(line)

    else:

        print("showing:", message)

    print("--------------------------------")

    # A list means the content has multiple lines,
    # like the little sun. this screen is shorter than the eInk
    # one, so lines are spaced a bit tighter (12px instead of 14px).

    if isinstance(message, list):

        lines = []
        start_y = -18

        for line in message:

            lines.append(
                (line, 1, start_y)
            )

            start_y += 12

        return draw_screen(lines)

    # Regular messages are wrapped automatically if too long.

    wrapped = wrap_text(message)

    return draw_screen([
        (wrapped, 1, 0)
    ])


def show_intro():
    # This is the screen shown before the button is pressed.

    return draw_screen([
        ("tiny soft computer", 1, -12),
        ("press the button", 1, 8),
    ])


# Show the intro when the computer starts.

show_intro()

print("")
print("ready, press the button")
print("")


# Every press shows a new random message, right away.
# No shuffling, no waiting, no forever-loop needed, the display
# can keep up with however fast someone wants to press it.

while True:

    if not button.value:

        print("button pressed")

        # Wait for the button to be released, so holding it down
        # doesn't trigger the computer more than once.

        while not button.value:
            time.sleep(0.01)

        message = random.choice(content)
        show_message(message)

    time.sleep(0.05)
