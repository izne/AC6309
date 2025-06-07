# Generate truth table and .bin file for AT28C64 EEPROM (8Kx8)
# for the AC6309 single board computer address decoder
#
# Memory Map:
# 0000-7FFF: 32K RAM (handled by 7400 logic, not EEPROM)
# 8000-9FFF: Unmapped space
# A000-A0FF: UART_CS (internal device)
# A100-A1FF: PIA_CS (internal device)  
# A200-A2FF: INT2_CS (internal device)
# A300-A3FF: INT3_CS (internal device)
# B000-B0FF: EXT1_CS (expansion slot 1)
# B100-B1FF: EXT2_CS (expansion slot 2)
# B200-B2FF: EXT3_CS (expansion slot 3)
# B300-B3FF: EXT4_CS (expansion slot 4)
# C000-FFFF: 16K ROM (handled by 7400 logic, not EEPROM)
#
# EEPROM AT28C64 DIP28 Pin Mapping:
# Inputs (A15-A8):
# A0 (pin 2): A8,  A1 (pin 3): A9,   A2 (pin 4): A10,  A3 (pin 5): A11
# A4 (pin 6): A12, A5 (pin 7): A13,  A6 (pin 8): A14,  A7 (pin 9): A15
# A8-A12 (pins 10-14): Tie to ground
# Outputs (active-low chip selects):
# D7 (pin 23): /UART_CS, D6 (pin 22): /PIA_CS,  D5 (pin 21): /INT2_CS, D4 (pin 20): /INT3_CS
# D3 (pin 19): /EXT1_CS, D2 (pin 1): /EXT2_CS, D1 (pin 28): /EXT3_CS, D0 (pin 27): /EXT4_CS

def not_(x): 
    return 1 if x == 0 else 0

def and_(*args): 
    return 1 if all(args) else 0

def get_device_info(uart_cs, pia_cs, int2_cs, int3_cs, ext1_cs, ext2_cs, ext3_cs, ext4_cs, A15, A14):
    """Return device name and range based on chip select results"""
    # Check EEPROM-controlled devices first
    if uart_cs:
        return "UART", "A000-A0FF", True
    elif pia_cs:
        return "PIA", "A100-A1FF", True
    elif int2_cs:
        return "INT2", "A200-A2FF", True
    elif int3_cs:
        return "INT3", "A300-A3FF", True
    elif ext1_cs:
        return "EXT1", "B000-B0FF", True
    elif ext2_cs:
        return "EXT2", "B100-B1FF", True
    elif ext3_cs:
        return "EXT3", "B200-B2FF", True
    elif ext4_cs:
        return "EXT4", "B300-B3FF", True
    
    # Address ranges handled by 7400 logic (not EEPROM concern)
    elif not A15:  # 0000-7FFF: RAM
        return "RAM", "0000-7FFF", False
    elif A15 and A14:  # C000-FFFF: ROM  
        return "ROM", "C000-FFFF", False
    else:
        return "UNMAPPED", "----", False

def main():
    rom_data = []
    header = "{:8} {:12} {:15} | {:8} {:8} {:8} {:8} {:8} {:8} {:8} {:8}".format(
        "Address", "Device", "Range", 
        "/UART_CS", "/PIA_CS", "/INT2_CS", "/INT3_CS", "/EXT1_CS", "/EXT2_CS", "/EXT3_CS", "/EXT4_CS"
    )
    print(header)
    print("-" * len(header))

    displayed_ranges = set()
    
    # Generate all 8K entries (full PROM capacity)
    for i in range(8192):  # 2^13 = 8192 entries
        # Load input (A15 - A8)
        A15 = (i >> 7) & 1
        A14 = (i >> 6) & 1  
        A13 = (i >> 5) & 1
        A12 = (i >> 4) & 1
        A11 = (i >> 3) & 1
        A10 = (i >> 2) & 1
        A9 = (i >> 1) & 1
        A8 = i & 1
        
        full_addr = i << 8  # The base address for each 256-byte block
        
        # Output logic
        UART_CS = and_(A15, not_(A14), A13, not_(A12), not_(A11), not_(A10), not_(A9), not_(A8))  # A000-A0FF
        PIA_CS = and_(A15, not_(A14), A13, not_(A12), not_(A11), not_(A10), not_(A9), A8)         # A100-A1FF  
        INT2_CS = and_(A15, not_(A14), A13, not_(A12), not_(A11), not_(A10), A9, not_(A8))        # A200-A2FF
        INT3_CS = and_(A15, not_(A14), A13, not_(A12), not_(A11), not_(A10), A9, A8)              # A300-A3FF
        EXT1_CS = and_(A15, not_(A14), A13, A12, not_(A11), not_(A10), not_(A9), not_(A8))        # B000-B0FF
        EXT2_CS = and_(A15, not_(A14), A13, A12, not_(A11), not_(A10), not_(A9), A8)              # B100-B1FF
        EXT3_CS = and_(A15, not_(A14), A13, A12, not_(A11), not_(A10), A9, not_(A8))              # B200-B2FF
        EXT4_CS = and_(A15, not_(A14), A13, A12, not_(A11), not_(A10), A9, A8)                    # B300-B3FF
        
        # Pack an output byte (still active-high)
        output_byte = (UART_CS << 7) | (PIA_CS << 6) | (INT2_CS << 5) | (INT3_CS << 4) | \
                      (EXT1_CS << 3) | (EXT2_CS << 2) | (EXT3_CS << 1) | EXT4_CS
        
        # Invert to active-low before storing in PROM
        inverted_byte = (~output_byte) & 0xFF
        rom_data.append(inverted_byte)
        
        # Boundary addresses only (display first address of each 256-byte block)
        device_name, device_range, is_eeprom_controlled = get_device_info(
            UART_CS, PIA_CS, INT2_CS, INT3_CS, EXT1_CS, EXT2_CS, EXT3_CS, EXT4_CS, A15, A14
        )
        
        if device_range not in displayed_ranges and is_eeprom_controlled:
            displayed_ranges.add(device_range)
            
            # Display the inverted (active-low) outputs
            outputs = [
                not_((output_byte >> 7) & 1),  # /UART_CS
                not_((output_byte >> 6) & 1),  # /PIA_CS  
                not_((output_byte >> 5) & 1),  # /INT2_CS
                not_((output_byte >> 4) & 1),  # /INT3_CS
                not_((output_byte >> 3) & 1),  # /EXT1_CS
                not_((output_byte >> 2) & 1),  # /EXT2_CS
                not_((output_byte >> 1) & 1),  # /EXT3_CS
                not_(output_byte & 1)          # /EXT4_CS
            ]
            
            row = "{:8} {:12} {:15} | {:8} {:8} {:8} {:8} {:8} {:8} {:8} {:8}".format(
                "${:04X}".format(full_addr), device_name, device_range,
                outputs[0], outputs[1], outputs[2], outputs[3], 
                outputs[4], outputs[5], outputs[6], outputs[7]
            )
            print(row)

    # Write binary file
    binfile = 'ac6309_decoder.bin'
    with open(binfile, 'wb') as f:
        f.write(bytes(rom_data))
    
    print("\nBinary file {0} written ({1} bytes)".format(binfile, len(rom_data)))

if __name__ == "__main__":
    main()
