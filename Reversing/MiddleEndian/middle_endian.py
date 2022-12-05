import io, math

# ~ A special thanks to Oreomeister, for helping come up with this shitpost of an idea. ~

# Get file name
fn = input("Enter file name to middle-endify: ")

byte_array = []
file_array = []

with open(fn, "rb") as f:
    while (byte := f.read(1)):
        # Do stuff with byte.
        byte_array.append(byte)
        file_array.append(bytes([0x99]))


lower = math.floor(len(byte_array) / 2)
upper = math.ceil(len(byte_array) / 2)

is_even = False

while lower >= 0 and upper < len(file_array):
    if (is_even):
        is_even = False

        file_array[lower] = byte_array[lower]
        file_array[upper] = byte_array[upper]
    else:
        is_even = True

        file_array[upper] = byte_array[lower]
        file_array[lower] = byte_array[upper]

    lower -= 1
    upper += 1

# failure check
if file_array[lower] == bytes([0x99]):
    file_array[lower] = byte_array[lower]

with open(fn + ".me", "wb") as f:
    for byte in file_array:
        f.write(byte)