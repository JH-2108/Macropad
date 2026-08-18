import board 
import displayio 
import i2cdisplaybus 
import adafruit_displayio_ssd1306 

from kmk.kmk_keyboard import KMKKeyboard 
from kmk.scanners.keypad import KeysScanner  
from kmk.keys import KC  

displayio.release_displays() 

i2c = board.I2C() 

display_bus = i2cdisplaybus.I2CDisplayBus(
    i2c, 
    device_address=0x3C
)

display = adafruit_displayio_ssd1306.SSD1306( 
    display_bus, 
    width=128, 
    height=32 
)

bitmap = displayio.Bitmap(128, 32, 2) 

palette = displayio.Palette(2) 
palette[0] = 0x000000
palette[1] = 0xFFFFFF 

def draw_art(art, start_x, start_y): 
    for y, row in enumerate(art): 
        for x, pixel in enumerate(row): 
            if pixel == "X": 
                px = start_x + x 
                py = start_y + y 

                if 0 <= px < 128 and 0 <= py < 32: 
                    bitmap[px, py] = 1 

penguin_art = [ 
    "          XXXXXXXXXX          ",
    "        XXX        XXX        ",
    "      XXX            XXX      ",
    "     XX                XX     ",
    "    XX                  XX    ",
    "   XX      XX    XX      XX   ",
    "   X       XX    XX       X   ",
    "  XX         XXXX         XX  ",
    "  XX          XX          XX  ",
    " XX                       XX  ",
    " XX    XX           XX     XX ",
    "XX    XXX           XXX     XX",
    "XX    XXX           XXX     XX",
    "XX     XX           XX      XX",
    "XX      XX         XX       XX",
    " XX      XXXXXXXXXXX       XX ",
    " XX       XXXXXXXXX        XX ",
    "  XX       XXXXXXX        XX  ",
    "  XX        XXXXX        XX   ",
    "   XX                 XX      ",
    "    XX               XX       ",
    "     XXX           XXX        ",
    "       XXX       XXX          ",
    "         XXXXXXXXX            ",
    "       XXX       XXX          ",
    "      XXXX       XXXX         ",
]

snowflake_big = [ 
    "  X  ",
    " XXX ",
    "XXXXX",
    " XXX ",
    "  X  ",
]

snowflake_small = [ 
    " X ",
    "XXX",
    " X ",
]

snow_dots = [ 
    (4, 4),
    (27, 8), 
    (16, 18), 
    (6, 27), 

    (102, 5),
    (120, 9),
    (111, 18), 
    (123, 27),
]

draw_art(
    penguin_art, 
    49,
    3
)

draw_art(
    snowflake_small,
    25, 
    3 
)

draw_art( 
    snowflake_big, 
    119,
    10
)

draw_art(
    snowflake_small,
    100,
    3
)

draw_art(
    snowflake_small,
    108,
    23
)

for x, y in snow_dots: 
    bitmap[x, y] = 1 

screen = displayio.Group() 

penguing = displayio.TileGrid(
    bitmap, 
    pixel_shader=palette
)

screen.append(penguin) 

display.root_group = screen 

keyboard = KMKKeyboard() 

keyboard.matrix = KeysScanner(
    pins = [
        board.D0,
        board.D1, 
        board.D2, 
        board.D3, 
        board.D6, 
        board.D10,
        board.D9,
        board.D8,
        board.D7,
    ],
    value_when_pressed=False, 
    pull = True,
)

GOOGLE = KC.MACRO(
    KC.LGUI(KC.R),
    KC.MACRO_SLEEP_MS(300),
    "https://www.google.com",
    KC.ENT,
)

SPOTIFY = KC.MACRO( 
    KC.LGUI(KC.R),
    KC.MACRO_SLEEP_MS(300), 
    "spotify",
    KC.ENT,
)

ROBLOX = KC.MACRO( 
    KC.LGUI(KC.R), 
    KC.MACRO_SLEEP_MS(300), 
    "roblox",
    KC.ENT,
)

keyboard.keymap = [ 
    [ 
        GOOGLE, 
        #opens google 

        KC.LCTL(KC.C), 
        #ctrl c 

        KC.LCTL(KC.V),
        #ctrl v 

        SPOTIFY,
        #opens spotify

        KC.LCTL(KC.X),
        #ctrl x

        ROBLOX, 
        #opens roblox

        KC.LATL(KC.TAB),
        #alt tab

        KC.LGUI(KC.LSFT(KC.S)),
        #screenshot
        
        KC.LCTL(KC.LSFT(KC.ESC)),
        #task manager
    ]
]

if __name__ == '__main__': 
    keyboard.go()