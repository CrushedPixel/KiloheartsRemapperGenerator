import struct

def float_to_hex(f):
    return struct.pack('<f', f)

def generate_music_curve(chord_intervals, steps=12):
    magic_bytes = bytes.fromhex('6B487352656D6170')
    num_keyframes = len(chord_intervals) * 2
    header = magic_bytes + bytes.fromhex('000001000000') + struct.pack('<I', num_keyframes)
    keyframes = []

    delta_x = 2.0 / len(chord_intervals)
    step_value = 2.0 / steps

    chord_intervals = sorted(chord_intervals)
    for idx, n in enumerate(chord_intervals):
        x_start = -1 + idx * delta_x
        x_end = x_start + delta_x
        y = -1 + n * step_value  

        x_start_hex = float_to_hex(x_start)
        x_end_hex = float_to_hex(x_end)
        y_hex = float_to_hex(y)

        keyframe_start = x_start_hex + y_hex + x_start_hex + y_hex + bytes.fromhex('03000000')
        keyframe_end = x_end_hex + y_hex + x_end_hex + y_hex + bytes.fromhex('03000000')

        keyframes.extend([keyframe_start, keyframe_end])

    return header + b''.join(keyframes)

def save_music_curve(chord_intervals, filename):
    if max(chord_intervals) > 12:
        steps = 24
    else:
        steps = 12

    curve = generate_music_curve(chord_intervals, steps)
    print(f"Saving {filename}:", curve.hex())
    with open(filename, "wb") as f:
        f.write(curve)

# Chord definitions
base_chords = {
    "Major": [0, 4, 7],
    "Major6": [0, 4, 7, 9],
    "Major7": [0, 4, 7, 11],
    "Minor": [0, 3, 7],
    "Minor6": [0, 3, 7, 9],
    "Minor7": [0, 3, 7, 10],
    "MinorMajor7": [0, 3, 7, 11],
    "Dominant7": [0, 4, 7, 10],
    "Diminished": [0, 3, 6],
    "Diminished7": [0, 3, 6, 9],
    "HalfDiminished": [0, 3, 6, 10],
    "Augmented": [0, 4, 8],
    "Augmented7": [0, 4, 8, 10],
    "Sus2": [0, 2, 7],
    "Sus4": [0, 5, 7],
    "7Sus4": [0, 5, 7, 10],
    "Add9": [0, 4, 7, 14],
    "Major69": [0, 4, 7, 9, 14],
    "Major9": [0, 4, 7, 11, 14],
    "Major11": [0, 4, 7, 11, 14, 17],
    "Minor9": [0, 3, 7, 10, 14],
    "Minor11": [0, 3, 7, 10, 14, 17],
    "Dominant9": [0, 4, 7, 10, 14],
    "Dominant11": [0, 4, 7, 10, 14, 17],
    "Dominant13": [0, 4, 7, 10, 14, 17, 21],
    "Add11": [0, 4, 7, 17]
}

chords = {}

for name, intervals in base_chords.items():
    # Add the original chord
    chords[name + ".remap"] = intervals
    
    # Add the octave for chords that don't have it
    if 12 not in intervals:
        chords[name + "WithOctave.remap"] = intervals + [12]
    
    # Double the intervals for chords that don't exceed an octave
    if max(intervals) <= 12:
        chords[name + "TwoOctaves.remap"] = intervals + [i+12 for i in intervals]

for filename, intervals in chords.items():
    save_music_curve(intervals, filename)
