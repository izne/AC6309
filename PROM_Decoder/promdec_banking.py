# Generate truth table and .bin file for 28C16 EEPROM (64x8)
# Inputs: A14, A13, A12, E, RW, BANK (6 bits)
# Outputs: BANK_EN, BANK1, BANK0, RAM_CS, EXT1_CS, EXT2_CS, UART_CS, ROM_CS (8 bits, active-low CS)

def not_(x): return 1 if x == 0 else 0
def and_(*args): return 1 if all(args) else 0

# TRUT table (and the ROM content)
rom_data = []
print("A14 A13 A12 E RW BANK | BANK_EN BANK1 BANK0 RAM_CS EXT1_CS EXT2_CS UART_CS ROM_CS")
print("-" * 70)
for i in range(2**6):  # 64 adresa?
    # Inputs load
    A14 = (i >> 5) & 1
    A13 = (i >> 4) & 1
    A12 = (i >> 3) & 1
    E = (i >> 2) & 1
    RW = (i >> 1) & 1
    BANK = i & 1

    # Output logic
    RAM_CS = and_(not_(A14), not_(A13), E)           # $0000-$7FFF
    EXT1_CS = and_(A14, not_(A13), not_(A12), E)     # $8000-$8FFF
    EXT2_CS = and_(A14, not_(A13), A12, E)           # $9000-$9FFF
    UART_CS = and_(A14, A13, not_(A12), E)           # $A000-$AFFF
    EXT3_CS = and_(A14, A13, A12, E)                 # $B000-$BFFF
    ROM_CS = and_(A14, A13, E)                       # $C000-$FFFF
    BANK_EN = and_(A14, A13, not_(A12), E, not_(RW)) # Write to $AFFE
    BANK1 = and_(not_(A14), not_(A13), E, BANK)      # Bank bit 1 (A16) for RAM
    BANK0 = and_(not_(A14), not_(A13), E, BANK)      # Bank bit 0 (A15) for RAM

    # Pack outputs (active-low CS)
    byte = (BANK_EN << 7) | \
           (BANK1 << 6) | \
           (BANK0 << 5) | \
           (not_(RAM_CS) << 4) | \
           (not_(EXT1_CS) << 3) | \
           (not_(EXT2_CS) << 2) | \
           (not_(UART_CS) << 1) | \
           not_(ROM_CS)

    # Store resulting byte for the ROM
    rom_data.append(byte)
    
    print(f"{A14}   {A13}   {A12}   {E}  {RW}  {BANK}   | "
          f"{(byte>>7)&1}       {(byte>>6)&1}     {(byte>>5)&1}     {(byte>>4)&1}      {(byte>>3)&1}       {(byte>>2)&1}       {(byte>>1)&1}       {byte&1}")

# Write binary file
with open('prom_decoder_ac6309.bin', 'wb') as f:
    f.write(bytes(rom_data))
