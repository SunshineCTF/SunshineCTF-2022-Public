# Tool to generate JXL bitmap images

import pyperclip    

pixel_size = 10
text_color = 1000
bkgd_color = 0

data = {
    "a": [
        [False, True, False],
        [True, False, True],
        [True, True, True],
        [True, False, True],
        [True, False, True]
    ],
    "b": [
        [True, True, False],
        [True, False, True],
        [True, True, True],
        [True, False, True],
        [True, True, False]
    ],
    "c": [
        [True, True, True],
        [True, False, False],
        [True, False, False],
        [True, False, False],
        [True, True, True]
    ],
    "d": [
        [True, True, False],
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, True, False]
    ],
    "e": [
        [True, True, True],
        [True, False, False],
        [True, True, False],
        [True, False, False],
        [True, True, True]
    ],
    "f": [
        [True, True, True],
        [True, False, False],
        [True, True, False],
        [True, False, False],
        [True, False, False]
    ],
    "g": [
        [True, True, True],
        [True, False, False],
        [True, False, True],
        [True, False, True],
        [True, True, False]
    ],
    "h": [
        [True, False, True],
        [True, False, True],
        [True, True, True],
        [True, False, True],
        [True, False, True]
    ],
    "i": [
        [True, True, True],
        [False, True, False],
        [False, True, False],
        [False, True, False],
        [True, True, True]
    ],
    "j": [
        [False, False, True],
        [False, False, True],
        [False, False, True],
        [True, False, True],
        [True, True, True]
    ],
    "k": [
        [True, False, True],
        [True, False, True],
        [True, True, False],
        [True, False, True],
        [True, False, True]
    ],
    "l": [
        [True, False, False],
        [True, False, False],
        [True, False, False],
        [True, False, False],
        [True, True, True]
    ],
    "m": [
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True, False, True, False, True],
        [True, False, False, False, True],
        [True, False, False, False, True]
    ],
    "n": [
        [True, True, True],
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, False, True]
    ],
    "o": [
        [True, True, True],
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, True, True]
    ],
    "p": [
        [True, True, True],
        [True, False, True],
        [True, True, True],
        [True, False, False],
        [True, False, False]
    ],
    "q": [
        [True, True, True],
        [True, False, True],
        [True, True, True],
        [False, False, True],
        [False, False, True]
    ],
    "r": [
        [True, True, True],
        [True, False, True],
        [True, True, False],
        [True, False, True],
        [True, False, True]
    ],
    "s": [
        [True, True, True],
        [True, False, False],
        [True, True, True],
        [False, False, True],
        [True, True, True]
    ],
    "t": [
        [True, True, True],
        [False, True, False],
        [False, True, False],
        [False, True, False],
        [False, True, False]
    ],
    "u": [
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, True, True]
    ],
    "v": [
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [False, True, False]
    ],
    "w": [
        [True, False, False, False, True],
        [True, False, False, False, True],
        [True, False, True, False, True],
        [True, True, False, True, True],
        [True, False, False, False, True]
    ],
    "x": [
        [True, False, True],
        [True, False, True],
        [False, True, False],
        [True, False, True],
        [True, False, True]
    ],
    "y": [
        [True, False, True],
        [True, False, True],
        [True, True, True],
        [False, False, True],
        [True, True, True]
    ],
    "z": [
        [True, True, True],
        [False, False, True],
        [False, True, False],
        [True, False, False],
        [True, True, True]
    ],
    "0": [
        [False, True, False],
        [True, False, True],
        [True, False, True],
        [True, False, True],
        [False, True, False]
    ],
    "1": [
        [False, True, False],
        [True, True, False],
        [False, True, False],
        [False, True, False],
        [True, True, True]
    ],
    "2": [
        [True, True, False],
        [False, False, True],
        [False, True, False],
        [True, False, False],
        [True, True, True]
    ],
    "3": [
        [True, True, False],
        [False, False, True],
        [True, True, False],
        [False, False, True],
        [True, True, False]
    ],
    "4": [
        [True, False, True],
        [True, False, True],
        [True, True, True],
        [False, False, True],
        [False, False, True]
    ],
    "5": [
        [True, True, True],
        [True, False, False],
        [True, True, False],
        [False, False, True],
        [True, True, False]
    ],
    "6": [
        [True, True, True],
        [True, False, False],
        [True, True, True],
        [True, False, True],
        [True, True, True]
    ],
    "7": [
        [True, True, True],
        [False, False, True],
        [False, True, False],
        [False, True, False],
        [False, True, False]
    ],
    "8": [
        [True, True, True],
        [True, False, True],
        [True, True, True],
        [True, False, True],
        [True, True, True]
    ],
    "9": [
        [True, True, True],
        [True, False, True],
        [True, True, True],
        [False, False, True],
        [True, True, True]
    ],
    "{": [
        [False, False, True],
        [False, True, False],
        [True, True, False],
        [False, True, False],
        [False, False, True]
    ],
    "}": [
        [True, False, False],
        [False, True, False],
        [False, True, True],
        [False, True, False],
        [True, False, False]
    ],
    "-": [
        [False, False, False],
        [False, False, False],
        [True, True, True],
        [False, False, False],
        [False, False, False]
    ],
    "_": [
        [False, False, False],
        [False, False, False],
        [False, False, False],
        [False, False, False],
        [True, True, True]
    ],
    "!": [
        [True, False],
        [True, False],
        [True, False],
        [False, False],
        [True, False]
    ],
    "?": [
        [False, True, False],
        [True, False, True],
        [False, True, False],
        [False, False, False],
        [False, True, False]
    ],
    ".": [
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [True, False]
    ],
    "@": [
        [False, True, True, False],
        [True, False, False, True],
        [True, True, False, True],
        [True, False, True, False],
        [False, True, True, False]
    ],
    " ": [
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [False, False]
    ],
    "$": [
        [False, True, True],
        [True, True, False],
        [True, True, True],
        [False, True, True],
        [True, True, False]
    ],
    "+": [
        [False, False, False],
        [False, True, False],
        [True, True, True],
        [False, True, False],
        [False, False, False]
    ],
    "=": [
        [False, False, False],
        [True, True, True],
        [False, False, False],
        [True, True, True],
        [False, False, False]
    ],
    "/": [
        [False, False, True],
        [False, False, True],
        [False, True, False],
        [True, False, False],
        [True, False, False]
    ],
    "\\": [
        [True, False, False],
        [True, False, False],
        [False, True, False],
        [False, False, True],
        [False, False, True]
    ],
    "(": [
        [False, True],
        [True, False],
        [True, False],
        [True, False],
        [False, True]
    ],
    "[": [
        [True, True],
        [True, False],
        [True, False],
        [True, False],
        [True, True]
    ],
    ")": [
        [True, False],
        [False, True],
        [False, True],
        [False, True],
        [True, False]
    ],
    "]": [
        [True, True],
        [False, True],
        [False, True],
        [False, True],
        [True, True]
    ],
    "%": [
        [True, False, True],
        [False, False, True],
        [False, True, False],
        [True, False, False],
        [True, False, True]
    ],
    ":": [
        [False, False],
        [True, False],
        [False, False],
        [True, False],
        [False, False]
    ],
    ";": [
        [False, False],
        [True, False],
        [False, False],
        [True, False],
        [True, False]
    ],
    "^": [
        [False, False, False],
        [False, True, False],
        [True, False, True],
        [False, False, False],
        [False, False, False]
    ],
    ">": [
        [True, False, False],
        [False, True, False],
        [False, False, True],
        [False, True, False],
        [True, False, False]
    ],
    "<": [
        [False, False, True],
        [False, True, False],
        [True, False, False],
        [False, True, False],
        [False, False, True]
    ]
}

def get_text(text):
    out = [
        [],
        [],
        [],
        [],
        []
    ]

    for i in range(len(text)):
        letter = text[i].lower()

        out[0] = out[0] + [False] + data.get(letter)[0]
        out[1] = out[1] + [False] + data.get(letter)[1]
        out[2] = out[2] + [False] + data.get(letter)[2]
        out[3] = out[3] + [False] + data.get(letter)[3]
        out[4] = out[4] + [False] + data.get(letter)[4]

    out[0] = out[0] + [False]
    out[1] = out[1] + [False]
    out[2] = out[2] + [False]
    out[3] = out[3] + [False]
    out[4] = out[4] + [False]

    blank_line = []
    for i in out[0]:
        blank_line.append(False)

    out.insert(0, blank_line)
    out.append(blank_line)

    return out

def generate_line(axis="x", value=0, yes=f"", no=f""):
    return f"if {axis} > {value}\n{yes}\n{no}\n"

# This only deals with the X axis!
def print_line(img_line):
    return print_line_text_color_helper(img_line, 0)

def print_line_text_color_helper(img_line, carat, last_state=False):
    buf = ""

    for pixel in img_line[carat:]:
        if pixel == last_state:
            carat += 1
        else:
            # buf += print_line_text_color_helper(axis="x", value=(carat * pixel_size), yes=f"- Set {text_color}")
            buf += f"if x > {(carat * pixel_size) - 1}\n"
            buf += print_line_text_color_helper(img_line, carat + 1, not last_state)

            if (last_state):
                buf += f"- Set {text_color}\n"
            else:
                buf += f"- Set {bkgd_color}\n"

            return buf

    buf += f"- Set {bkgd_color}\n"
    return buf

def print_pattern(img):
    if (len(img[0]) * pixel_size > 1024):
        print("WARN: Image exeeds 1024-width limit.")

    buf = f"Width {len(img[0]) * pixel_size}\n"
    buf += f"Height {len(img) * pixel_size}\n"
    buf += "RCT 1\n\n"

    buf += print_pattern_text_color_helper(img, len(img) - 1)

    return buf

def print_pattern_text_color_helper(img, line_number):
    if line_number >= len(img) or line_number < 0:
        return f"- Set {bkgd_color}\n"

    buf = ""
    buf += f"if y > {(line_number * pixel_size) - 1}\n"
    buf += print_line(img[line_number])
    buf += print_pattern_text_color_helper(img, line_number - 1)

    return buf


if __name__ == '__main__':
    text = input("Input desired text: ")

    print("\n\n")

    # Test image:
    #  ____________
    # |    X       |
    # | XXX X X XX |
    # |X X         |
    # --------------
    _test = [
        [False, False, False, False, True, False, False, False, False, False, False, False],
        [False, True, True, True, False, True, False, True, False, True, True, False],
        [True, False, True, False, False, False, False, False, False, False, False, False]
    ]

    text_arr = get_text(text)

    output = print_pattern(text_arr)

    print(output)

    pyperclip.copy(output)
