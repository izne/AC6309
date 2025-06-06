# Generate TRUT table and .bin file for 28C16 EEPROM (128x8)
# for the AC6309 single board computer
# 
# Inputs: A14, A13, A12, A11, A10, E, /RW (7 bits)
# Outputs: RAM_RD, RAM_WR, EXT1A_CS, EXT1B_CS, EXT2A_CS, EXT2B_CS, UART_CS, ROM_CS (8 bits, active-low)

# Device 28C16 DIP24
# Inputs:
# A0 (pin 1): /RW
# A1 (pin 2): E
# A2 (pin 3): A11
# A3 (pin 4): A12
# A4 (pin 5): A13
# A5 (pin 6): A14
# A6 (pin 7): A15
# A7–A10 (pins 8, 9, 11, 23): GND
# Outputs:
# D7 (pin 21): RAM_RD
# D6 (pin 20): RAM_WR
# D5 (pin 19): EXT1A_CS
# D4 (pin 17): EXT1B_CS
# D3 (pin 16): EXT2A_CS
# D2 (pin 15): EXT2B_CS
# D1 (pin 14): UART_CS
# D0 (pin 13): ROM_CS


def not_(x): return 1 if x == 0 else 0
def and_(*args): return 1 if all(args) else 0

showAll = False
rom_data = []
header = "{:8}{:14}{:4}{:4}{:4}{:4}{:4}{:4}{:4}|{:10}{:10}{:10}{:10}{:10}{:10}{:10}{:10}".format(
    "Addr", "Region", "A15", "A14", "A13", "A12", "A11", "E", "/RW",
    "/RAM_RD", "/RAM_WR", "/EXT1A_CS", "/EXT1B_CS", "/EXT2A_CS", "/EXT2B_CS", "/UART_CS", "/ROM_CS"
)
print(header)
print("-" * len(header))
for i in range(2**7):  # 128 addresses
    # Extract inputs
    A15 = (i >> 6) & 1
    A14 = (i >> 5) & 1
    A13 = (i >> 4) & 1
    A12 = (i >> 3) & 1
    A11 = (i >> 2) & 1
    E = (i >> 1) & 1
    RW = i & 1  # /RW from CPU: 1=read, 0=write

    # Output logic (active-low)
    RAM_RD = and_(not_(A15), not_(A14), not_(A13), not_(A12), not_(A11), E, RW)        # $0000-$7FFF read (/RW=1)
    RAM_WR = and_(not_(A15), not_(A14), not_(A13), not_(A12), not_(A11), E, not_(RW))  # $0000-$7FFF write (/RW=0)
    EXT1A_CS = and_(A15, not_(A14), not_(A13), not_(A12), not_(A11), E)                # $8000-$83FF
    EXT1B_CS = and_(A15, not_(A14), not_(A13), not_(A12), A11, E)                      # $8400-$87FF
    EXT2A_CS = and_(A15, not_(A14), not_(A13), A12, not_(A11), E)                      # $9000-$93FF
    EXT2B_CS = and_(A15, not_(A14), not_(A13), A12, A11, E)                            # $9400-$97FF
    UART_CS = and_(A15, not_(A14), A13, not_(A12), not_(A11), E)                       # $A000-$A7FF
    ROM_CS = and_(A15, A14, E)                                                         # $C000-$FFFF

    # Pack outputs
    byte = (not_(RAM_RD) << 7) | \
           (not_(RAM_WR) << 6) | \
           (not_(EXT1A_CS) << 5) | \
           (not_(EXT1B_CS) << 4) | \
           (not_(EXT2A_CS) << 3) | \
           (not_(EXT2B_CS) << 2) | \
           (not_(UART_CS) << 1) | \
           (not_(ROM_CS))

    outputs = [
        ((byte>>7)&1, "$0000-$7FFF R"),    # /RAM_RD
        ((byte>>6)&1, "$0000-$7FFF W"),    # /RAM_WR
        ((byte>>5)&1, "$8000-$83FF"),      # /EXT1A_CS
        ((byte>>4)&1, "$8400-$87FF"),      # /EXT1B_CS
        ((byte>>3)&1, "$9000-$93FF"),      # /EXT2A_CS
        ((byte>>2)&1, "$9400-$97FF"),      # /EXT2B_CS
        ((byte>>1)&1, "$A000-$A7FF"),      # /UART_CS
        (byte&1,      "$C000-$FFFF")       # /ROM_CS
    ]
    
    region = next((r for v, r in outputs if v == 0), "DontCare")
    rom_data.append(byte)
    if showAll or region != "DontCare":
        row = "{:8}{:14}{:4}{:4}{:4}{:4}{:4}{:4}{:4}|{:10}{:10}{:10}{:10}{:10}{:10}{:10}{:10}".format(
            f"0x{i:02x}", region, A15, A14, A13, A12, A11, E, RW,
            (byte>>7)&1, (byte>>6)&1, (byte>>5)&1, (byte>>4)&1, (byte>>3)&1, (byte>>2)&1, (byte>>1)&1, byte&1
        )
        print(row)

with open('decoder.bin', 'wb') as f:
    f.write(bytes(rom_data))
