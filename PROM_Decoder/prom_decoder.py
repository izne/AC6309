# Generate truth table and .bin file for 28C16 EEPROM (64x8)
# Inputs: A14, A13, A12, A11, E, RW (6 bits)
# Outputs: RAM_CS, EXT1A_CS, EXT1B_CS, EXT2A_CS, EXT2B_CS, EXT3A_CS, EXT3B_CS, ROM_CS (8 bits, active-low)

def not_(x): return 1 if x == 0 else 0
def and_(*args): return 1 if all(args) else 0

rom_data = []
print("A14 A13 A12 A11 E RW | RAM_CS EXT1A_CS EXT1B_CS EXT2A_CS EXT2B_CS EXT3A_CS EXT3B_CS ROM_CS")
print("-" * 70)

for i in range(2**6):
    # Inputs
    A14 = (i >> 5) & 1
    A13 = (i >> 4) & 1
    A12 = (i >> 3) & 1
    A11 = (i >> 2) & 1
    E = (i >> 1) & 1
    RW = i & 1

    # Output logic (active-low)
    RAM_CS = and_(not_(A14), not_(A13), E)                    # $0000-$7FFF
    EXT1A_CS = and_(A14, not_(A13), not_(A12), not_(A11), E)  # $8000-$83FF
    EXT1B_CS = and_(A14, not_(A13), not_(A12), A11, E)        # $8400-$87FF
    EXT2A_CS = and_(A14, not_(A13), A12, not_(A11), E)        # $9000-$93FF
    EXT2B_CS = and_(A14, not_(A13), A12, A11, E)              # $9400-$97FF
    EXT3A_CS = and_(A14, A13, A12, not_(A11), E)              # $B000-$B3FF
    EXT3B_CS = and_(A14, A13, A12, A11, E)                    # $B400-$B7FF
    ROM_CS = and_(A14, A13, E)                                # $C000-$FFFF

    # Set Outputs
    byte = (not_(RAM_CS) << 7) | \
           (not_(EXT1A_CS) << 6) | \
           (not_(EXT1B_CS) << 5) | \
           (not_(EXT2A_CS) << 4) | \
           (not_(EXT2B_CS) << 3) | \
           (not_(EXT3A_CS) << 2) | \
           (not_(EXT3B_CS) << 1) | \
           not_(ROM_CS)

    # Append to ROM content
    rom_data.append(byte)
    print(f"{A14}   {A13}   {A12}   {A11}  {E}  {RW}  | "
          f"{(byte>>7)&1}      {(byte>>6)&1}       {(byte>>5)&1}       {(byte>>4)&1}       {(byte>>3)&1}       {(byte>>2)&1}       {(byte>>1)&1}       {byte&1}")

# Write .bin file
with open('decode.bin', 'wb') as f:
    f.write(bytes(rom_data))
