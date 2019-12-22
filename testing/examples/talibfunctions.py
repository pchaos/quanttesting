import os

FONTNAME = "~/.local/share/fonts/HanyiSentyTang.ttf"

def getFontName(fname=FONTNAME):
    return os.path.expanduser(fname)