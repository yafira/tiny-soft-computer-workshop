# tiny soft computer
# press the button once, then it runs on its own
# Feather RP2040 ThinkInk + 2.13" 212x104 Flexible Monochrome eInk (IL0373)

import time
import random
import gc
import board
import busio
import displayio
import terminalio
import digitalio
from fourwire import FourWire
import adafruit_il0373
from adafruit_display_text import label


# MESSAGES + ASCII ART
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
        "you are a beam of light",
    ],
]


# The display should not be updated more often than every
# 180 seconds, according to the display datasheet.
# This is the single source of truth for timing in this file.

CONTENT_INTERVAL = 180


print("starting up")

displayio.release_displays()


# One button starts the computer.
# The button uses a pull-up resistor.
# False means pressed and True means not pressed.

button = digitalio.DigitalInOut(board.A2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


# Everything below this is already wired up and working,
# feel free to skim it or skip ahead.

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


# Tracks when the display last actually refreshed, so we always
# know the real gap, including the very first refresh from the
# intro screen, not just the gap between messages.

last_refresh_time = None


def draw_screen(lines):
    # Draws one screen and refreshes the display.
    # Waits here, if needed, so the display never refreshes
    # sooner than CONTENT_INTERVAL since the last real refresh,
    # including the very first one from the intro screen.

    global last_refresh_time

    if last_refresh_time is not None:

        elapsed = time.monotonic() - last_refresh_time
        remaining = CONTENT_INTERVAL - elapsed

        if remaining > 0:
            wait_with_countdown(remaining)

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
        last_refresh_time = time.monotonic()
        return True

    except RuntimeError as error:
        # This is a safety net. It shouldn't normally trigger
        # because draw_screen waits for the real elapsed time.

        print("display wasn't ready:", error)
        last_refresh_time = time.monotonic()
        return False


# Tracks whether we've shown a message yet, so the very first
# one says "showing:" and every one after says "showing next:".

first_message_shown = False


def show_message(message):
    # Show one message or drawing on the screen.

    global first_message_shown

    label = "showing next:" if first_message_shown else "showing:"
    first_message_shown = True

    print("")
    print("--------------------------------")

    if isinstance(message, list):

        print(label)

        for line in message:
            print(line)

    else:

        print(label, message)

    print("--------------------------------")

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
        ("press button\ngive it a moment ...", 1, 18),
    ])


def shuffle_list(items):
    # Put the messages into a random order.
    # This uses the Fisher-Yates shuffle, a simple way to make
    # sure every possible order is equally likely.

    for i in range(len(items) - 1, 0, -1):

        j = random.randint(0, i)

        items[i], items[j] = (
            items[j],
            items[i]
        )


# Add special messages here.
# The number is the number of seconds into the wait.
#
# The Serial Monitor will still show every 10 seconds.
# These messages can happen at any time.

waiting_messages = {
    20: "still here",
    35: "a little more patience",
    50: "taking its sweet time",
    60: "thinking....",
    70: "still thinking",
    90: "halfway there",
    110: "a little longer",
    130: "nearly there",
    145: "just hanging out",
    160: "almost there",
    170: "so little time",
}


def wait_with_countdown(total_seconds):
    # Waits while showing progress in the Serial Monitor.
    # A regular update appears every 10 seconds.
    # Special messages can appear at other times.
    # The button is also checked while waiting.

    start_time = time.monotonic()

    next_ten_second_update = 10
    printed_messages = []

    button_was_pressed = False

    while True:

        elapsed = time.monotonic() - start_time

        # Check the button frequently while waiting.

        if not button.value:

            if not button_was_pressed:
                print("button pressed, just a few seconds...")
                button_was_pressed = True

        else:
            button_was_pressed = False

        # Stop when the full wait is complete.

        if elapsed >= total_seconds:
            break

        # Print every 10 seconds.

        if elapsed >= next_ten_second_update:

            if next_ten_second_update in waiting_messages:
                print(
                    next_ten_second_update,
                    "seconds -",
                    waiting_messages[next_ten_second_update]
                )

            else:
                print(
                    next_ten_second_update,
                    "seconds"
                )

            next_ten_second_update += 10

        # Print special messages that happen between
        # the regular 10-second updates.

        for message_time in waiting_messages:

            if (
                message_time not in printed_messages
                and elapsed >= message_time
                and message_time % 10 != 0
            ):

                print(
                    message_time,
                    "seconds -",
                    waiting_messages[message_time]
                )

                printed_messages.append(message_time)

        time.sleep(0.05)


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

        # Show every item once before making
        # a new random order.

        for item in order:

            show_message(item)

            # Tidy up memory now and then, since this loop
            # runs for a very long time without ever restarting.

            gc.collect()

        # Once everything has been shown,
        # shuffle everything and start again.

        print("finished this set, reshuffling...")


# Show the intro when the computer starts.

show_intro()

print("")
print("ready, press the button to begin")
print("")


# The button only needs to be pressed once.
# After that run_forever() takes over.

while True:

    if not button.value:

        print("button pressed, just a few seconds...")

        time.sleep(0.5)

        run_forever()

    time.sleep(0.05)