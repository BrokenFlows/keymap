# Usage

## Requirements
This repository creates keymap SVG image using python.
As such, you must have `python3` installed to use this tool.

## Editing Keymap Files
The keymaps are defined in python files following this structure:
- Layer 1
    - Left Block
        - Row 1
        - Row 2
        - ...
    - Right Block
        - Rows ...
    - Thumbs
        - Left
        - Right
- More Layers ...

Keys are defined within pairs of double quotes, like `"q"`. 

There are various functions for affecting the appearance of a key:
- `hl()` for denoting that a key is being held
- `cm()` for denoting that a key is part of a combo
- `ch()` for denoting that a key is part of a combo which must be held
- `nm()` for denoting that a key is in the number row
- `ph()` for hiding a key that is used as a blank space for formatting

These functions are used as wrappers around keys, like `nm("1")` or `hl('shift")`.

## Image Generation
This is a command line tool, it is intended to be used in the terminal.
The command for creating a keymap takes the following form:

`python3 draw.py {keymap_directory}.{keymap_filename} > {keymap_directory}/{image_filename}.svg`

For example:

`python3 draw.py keys_36.keymap_36 > keys_36/keymap-36.svg`

