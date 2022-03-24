#! /usr/bin/env python3

from sys import argv
from importlib import import_module

# check for arguments, and use the first one as a keymap if possible
if len(argv) > 1:
    KEYMAP = import_module(argv[1]).KEYMAP
else:
    from keys_34.keymap_34 import KEYMAP

# define key-related dimensions
KEY_W = 55
KEY_H = 45
KEY_RX = 6
KEY_RY = 6
INNER_PAD_W = 2
INNER_PAD_H = 2
OUTER_PAD_W = KEY_W / 2
OUTER_PAD_H = KEY_H / 2
LINE_SPACING = 18

STYLE = """
    svg {
        font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
        font-size: 14px;
        font-kerning: normal;
        text-rendering: optimizeLegibility;
        fill: #24292e;
    }

    rect {
        fill: #f6f8fa;
    }

    .hold {
        fill: #ff8080;
    }

    .combo_hold {
        fill: #ff8080;
    }

    .combo {
        fill: #79f2f2;
    }
    
    .number{
        fill: #bfc2c7
    }

    .invisible{
        opacity: 0;
    }
"""


# count the number of layers in the keymap
layers = 0

for layer in KEYMAP:
    layers += 1

padding = layers + 1


# count the number of rows in a layer
rows = 1

for layer in KEYMAP:
    for row in layer["left"]:
        rows += 1
    break

cols = 5

# define dimensions for svg components
KEYSPACE_W = KEY_W + 2 * INNER_PAD_W
KEYSPACE_H = KEY_H + 2 * INNER_PAD_H
HAND_W = cols * KEYSPACE_W
HAND_H = rows * KEYSPACE_H
LAYER_W = 2 * HAND_W + OUTER_PAD_W
LAYER_H = HAND_H
BOARD_W = LAYER_W + 2 * OUTER_PAD_W
BOARD_H = layers * LAYER_H + padding * OUTER_PAD_H


def print_key(x, y, key, combo_flag):
    key_class = "" # placeholder for class value
    if type(key) is dict:
        key_class = key["class"]
        key = key["key"]

    # print key shape
    print(
        f'<rect rx="{KEY_RX}" ry="{KEY_RY}" x="{x + INNER_PAD_W}" y="{y + INNER_PAD_H}" width="{KEY_W}" height="{KEY_H}" class="{key_class}" />'
    )

    if "invisible" in key_class:
        key = ""

    # prepare text
    words = key.split()
    y += (KEYSPACE_H - (len(words) - 1) * LINE_SPACING) / 2

    # prints text on key
    for word in key.split():
        print(
            f'<text text-anchor="middle" dominant-baseline="middle" x="{x + KEYSPACE_W / 2}" y="{y}">{word}</text>'
        )
        y += LINE_SPACING

    # print combo arc if past two keys are combos
    if "combo" in key_class:
        if combo_flag:
            print(
                f'<path fill="none" stroke="#5656A8" stroke-width="4" stroke-linecap="round" d="M{x+OUTER_PAD_W},{y-KEY_H+INNER_PAD_H*6} A{KEY_W},{KEY_W*1} 0,0,0 {x-OUTER_PAD_W},{y-KEY_H+INNER_PAD_H*6}" />'
            )


def print_row(x, y, row):
    for index,key in enumerate(row):

        now_combo = False # flag when the current key is a combo
        combo_flag = False # flag when th current and previous keys are combos
        
        # placeholders for class values
        key_class = ""
        prev_class = ""
        
        # if there's a key class, get it
        if type(key) is dict:
            key_class = key["class"]
        
        # flag if the key is a sort of combo
        if "combo" in key_class:
            if index > 0:
                prev = row[index-1]
                now_combo = True
        
        # check if the previous keys is also a combo key
        if now_combo:
            if type(prev) is dict:
                prev_class = prev["class"]
            if "combo" in prev_class:
                combo_flag = True

        # print the key and track space
        print_key(x, y, key, combo_flag)
        x += KEYSPACE_W


def print_block(x, y, block):
    for row in block:
        print_row(x, y, row)
        y += KEYSPACE_H


def print_layer(x, y, layer):
    # print left then right blocks
    print_block(x, y, layer["left"])
    print_block(
        x + HAND_W + OUTER_PAD_W, y, layer["right"],
    )

    # count the number of rows in the blocks
    rows = 0

    for row in layer["left"]:
        rows += 1

    # print the thumbs below the main blocks
    # account for thumb count and row count in thumb placement
    print_row(
        x + (cols-len(layer["thumbs"]["left"])) * KEYSPACE_W, y + rows * KEYSPACE_H, layer["thumbs"]["left"],
    )
    print_row(
        x + HAND_W + OUTER_PAD_W, y + rows * KEYSPACE_H, layer["thumbs"]["right"],
    )


def print_board(x, y, keymap):
    x += OUTER_PAD_W
    for layer in keymap:
        y += OUTER_PAD_H
        print_layer(x, y, layer)
        y += LAYER_H


print(
    f'<svg width="{BOARD_W}" height="{BOARD_H}" viewBox="0 0 {BOARD_W} {BOARD_H}" xmlns="http://www.w3.org/2000/svg">'
)
print(f"<style>{STYLE}</style>")
print_board(0, 0, KEYMAP)
print("</svg>")

