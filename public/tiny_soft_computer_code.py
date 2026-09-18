# tiny soft computer
# press the button once, then it runs on its own
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


# Messages and drawings that can appear on the screen.
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
    "(. .)",
    "(^-^)",

    # A tiny sun
    [
        " \\ | / ",
        "-- * --",
        " / | \\ ",
    ],
]


# The display should not be updated more often than every
# 180 seconds, according to the display datasheet. this is
# the single source of truth for timing in this file.

CONTENT_INTERVAL = 180


print("starting up")

displayio.release_displays()


# One button starts the computer.
# The button uses a pull-up resistor.
# False means pressed and True means not pressed.

button = digitalio.DigitalInOut(board.A2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


# Set up the connection between the Feather and the e-ink display.

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
print("display refresh time:", display.time_to_refresh, "seconds")


def wrap_text(text, max_chars=26):
    # Break a long message into multiple lines
    # so it fits on the small screen.

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
    # Draws one screen and refreshes the display.
    # Timing between screens is handled entirely by
    # run_forever()'s CONTENT_INTERVAL sleep, this function
    # just draws and refreshes once, whenever it's called.

    g = displayio.Group()

    # Create a white background.

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

    # Add each piece of text to the screen.
    # Each item contains the text, size, and vertical position.

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

    try:
        print("refreshing display...")
        display.refresh()
        print("refresh complete")
        return True

    except RuntimeError as error:
        # this is a safety net, not expected to trigger in normal
        # use, since CONTENT_INTERVAL already paces things correctly
        print("display wasn't ready:", error)
        return False


def show_message(message):
    # Show one message or drawing on the screen.

    print("")
    print("--------------------------------")
    print("changing message")

    # Print the message to the Serial Monitor.

    if isinstance(message, list):

        print("showing:")

        for line in message:
            print(line)

    else:

        print("showing:", message)

    # A list means the content has multiple lines,
    # like the little sun.

    if isinstance(message, list):

        lines = []
        start_y = -14

        for line in message:

            lines.append(
                (line, 1, start_y)
            )

            start_y += 14

        return draw_screen(lines)

    # Regular messages are wrapped automatically
    # if they are too long for one line.

    wrapped = wrap_text(message)

    return draw_screen([
        (wrapped, 1, 0)
    ])


def show_intro():
    # This is the screen shown before the button is pressed.

    return draw_screen([
        ("tiny soft computer", 1, -14),
        ("press the button\nto begin", 1, 18),
    ])


def shuffle_list(items):
    # Put the messages into a random order.
    # This uses the Fisher-Yates shuffle.

    for i in range(len(items) - 1, 0, -1):

        j = random.randint(0, i)

        items[i], items[j] = (
            items[j],
            items[i]
        )


def run_forever():
    # Once the button is pressed, the computer
    # takes over and keeps running by itself.

    print("")
    print("tiny soft computer is running")
    print("changing every", CONTENT_INTERVAL, "seconds")
    print("")

    while True:

        # Make a copy of the content so we can
        # shuffle its order without changing the
        # original list.

        order = list(content)

        shuffle_list(order)

        print(
            "new randomized set of",
            len(order),
            "items"
        )

        # Show every item once before making
        # a new random order.

        for item in order:

            show_message(item)

            print(
                "next message in",
                CONTENT_INTERVAL,
                "seconds"
            )

            time.sleep(CONTENT_INTERVAL)

        # Once everything has been shown,
        # shuffle everything and start again.

        print("finished this set, reshuffling...")


# Show the intro when the computer starts.

show_intro()

print("")
print("ready, press the button to begin")
print("")


# The button only needs to be pressed once.
# After that, run_forever() takes over.

while True:

    if not button.value:

        print("button pressed")

        # Wait for the button to be released.
        # This prevents holding the button down
        # from triggering the computer more than once.

        while not button.value:
            time.sleep(0.01)

        print("button released")

        # Start the computer.
        # This function runs forever, so the button
        # will not be checked again.

        run_forever()

    time.sleep(0.05)