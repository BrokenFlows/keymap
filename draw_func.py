# signifies that this key is being held
def hl(key):
    return {"key": key, "class": "hold"}

# signifies that this key is part of a combo
def cm(key):
    return {"key": key, "class": "combo"}

# serves as a combination of both hl and cm
def ch(key):
    return {"key": key, "class": "combo_hold"}

# differentiates the number row from the main cluster
def nm(key):
    return {"key": key, "class": "number"}

# placeholder which makes a key invisible
def ph(key):
    return {"key": key, "class": "invisible"}

