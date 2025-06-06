# AC6309 PROM-based address decoder
overview

## Purpose

## How it works
The 28C16 EEPROM (128x8) functions as an address decoder, mapping the CPU’s 16-bit address space ($0000–$FFFF) to specific memory regions using 7 inputs (A14, A13, A12, A11, A10, E, /RW) to generate 8 active-low chip select signals (/RAM_RD, /RAM_WR, /EXT1A_CS, /EXT1B_CS, /EXT2A_CS, /EXT2B_CS, /UART_CS, /ROM_CS). Each input combination, corresponds to a byte in the EEPROM, programmed with the script’s logic to activate the appropriate chip select based on the address range.

For example, /RAM_RD activates for $0000–$7FFF reads (A14=0, A13=0, E=1, /RW=1), outputting 0x7F, while /EXT1A_CS activates for $8000–$83FF (A14=1, A13=0, A12=0, A11=0, E=1), outputting 0xDF. The script generates these 128 bytes, stored in decode.bin, which are loaded into the 28C16 to enable precise memory region selection during CPU operation.

### Key features
- E Clock Integration - Gates all outputs with the E clock, preventing spurious activations during invalid bus cycles
- Active-Low Outputs - Inverts all chip select signals using not_() function
- No Address Conflicts - Each memory region is uniquely decoded with no overlaps
Proper /RW Handling; RAM correctly distinguishes read vs write operations

### Mapping
28C16 Pinout (Unchanged)
Inputs:
A0 (pin 1): /RW
A1 (pin 2): E
A2 (pin 3): A10
A3 (pin 4): A11
A4 (pin 5): A12
A5 (pin 6): A13
A6 (pin 7): A14
A7–A10 (pins 8, 9, 11, 23): GND
Outputs:
D7 (pin 21): /RAM_RD
D6 (pin 20): /RAM_WR
D5 (pin 19): /EXT1A_CS
D4 (pin 17): /EXT1B_CS
D3 (pin 16): /EXT2A_CS
D2 (pin 15): /EXT2B_CS
D1 (pin 14): /UART_CS
D0 (pin 13): /ROM_CS

### Output Logic
- RAM (32KB): $0000 - $7FFF - Splits read/write based on /RW signal
- EXT1A: $8000 - $83FF (1KB)
- EXT1B: $8400 - $87FF (1KB)
- EXT2A: $9000 - $93FF (1KB)
- EXT2B: $9400 - $95FF (512B) - Uses A10=0 for partial decode
- UART: $A000 - $AFFF (4KB) - Onboard I/O space
- ROM: $C000 - $FFFF (16KB)

``` python
    RAM_RD = and_(not_(A14), not_(A13), E, RW)       # $0000 - $7FFF read  (/RW = 1)
    RAM_WR = and_(not_(A14), not_(A13), E, not_(RW)) # $0000 - $7FFF write (/RW = 0)
    EXT1A_CS = and_(A14, not_(A13), not_(A12), not_(A11), E) # $8000 - $83FF
    EXT1B_CS = and_(A14, not_(A13), not_(A12), A11, E)       # $8400 - $87FF
    EXT2A_CS = and_(A14, not_(A13), A12, not_(A11), E)       # $9000 - $93FF
    EXT2B_CS = and_(A14, not_(A13), A12, A11, not_(A10), E)  # $9400 - $95FF
    UART_CS = and_(A14, A13, not_(A12), E)                   # $A000 - $AFFF
    ROM_CS = and_(A14, A13, A12, E)                          # $C000 - $FFFF
```

### Output truth table
``` ruby
Addr    Region        A14 A13 A12 A11 A10 E   /RW |/RAM_RD   /RAM_WR   /EXT1A_CS /EXT1B_CS /EXT2A_CS /EXT2B_CS /UART_CS  /ROM_CS   
-----------------------------------------------------------------------------------------------------------------------------------
0x02    $0000-$7FFF W    0   0   0   0   0   1   0|         1         0         1         1         1         1         1         1
0x03    $0000-$7FFF R    0   0   0   0   0   1   1|         0         1         1         1         1         1         1         1
0x06    $0000-$7FFF W    0   0   0   0   1   1   0|         1         0         1         1         1         1         1         1
0x07    $0000-$7FFF R    0   0   0   0   1   1   1|         0         1         1         1         1         1         1         1
0x0a    $0000-$7FFF W    0   0   0   1   0   1   0|         1         0         1         1         1         1         1         1
0x0b    $0000-$7FFF R    0   0   0   1   0   1   1|         0         1         1         1         1         1         1         1
0x0e    $0000-$7FFF W    0   0   0   1   1   1   0|         1         0         1         1         1         1         1         1
0x0f    $0000-$7FFF R    0   0   0   1   1   1   1|         0         1         1         1         1         1         1         1
0x12    $0000-$7FFF W    0   0   1   0   0   1   0|         1         0         1         1         1         1         1         1
0x13    $0000-$7FFF R    0   0   1   0   0   1   1|         0         1         1         1         1         1         1         1
0x16    $0000-$7FFF W    0   0   1   0   1   1   0|         1         0         1         1         1         1         1         1
0x17    $0000-$7FFF R    0   0   1   0   1   1   1|         0         1         1         1         1         1         1         1
0x1a    $0000-$7FFF W    0   0   1   1   0   1   0|         1         0         1         1         1         1         1         1
0x1b    $0000-$7FFF R    0   0   1   1   0   1   1|         0         1         1         1         1         1         1         1
0x1e    $0000-$7FFF W    0   0   1   1   1   1   0|         1         0         1         1         1         1         1         1
0x1f    $0000-$7FFF R    0   0   1   1   1   1   1|         0         1         1         1         1         1         1         1
0x42    $8000-$83FF      1   0   0   0   0   1   0|         1         1         0         1         1         1         1         1
0x43    $8000-$83FF      1   0   0   0   0   1   1|         1         1         0         1         1         1         1         1
0x46    $8000-$83FF      1   0   0   0   1   1   0|         1         1         0         1         1         1         1         1
0x47    $8000-$83FF      1   0   0   0   1   1   1|         1         1         0         1         1         1         1         1
0x4a    $8400-$87FF      1   0   0   1   0   1   0|         1         1         1         0         1         1         1         1
0x4b    $8400-$87FF      1   0   0   1   0   1   1|         1         1         1         0         1         1         1         1
0x4e    $8400-$87FF      1   0   0   1   1   1   0|         1         1         1         0         1         1         1         1
0x4f    $8400-$87FF      1   0   0   1   1   1   1|         1         1         1         0         1         1         1         1
0x52    $9000-$93FF      1   0   1   0   0   1   0|         1         1         1         1         0         1         1         1
0x53    $9000-$93FF      1   0   1   0   0   1   1|         1         1         1         1         0         1         1         1
0x56    $9000-$93FF      1   0   1   0   1   1   0|         1         1         1         1         0         1         1         1
0x57    $9000-$93FF      1   0   1   0   1   1   1|         1         1         1         1         0         1         1         1
0x5a    $9400-$95FF      1   0   1   1   0   1   0|         1         1         1         1         1         0         1         1
0x5b    $9400-$95FF      1   0   1   1   0   1   1|         1         1         1         1         1         0         1         1
0x62    $A000-$AFFF      1   1   0   0   0   1   0|         1         1         1         1         1         1         0         1
0x63    $A000-$AFFF      1   1   0   0   0   1   1|         1         1         1         1         1         1         0         1
0x66    $A000-$AFFF      1   1   0   0   1   1   0|         1         1         1         1         1         1         0         1
0x67    $A000-$AFFF      1   1   0   0   1   1   1|         1         1         1         1         1         1         0         1
0x6a    $A000-$AFFF      1   1   0   1   0   1   0|         1         1         1         1         1         1         0         1
0x6b    $A000-$AFFF      1   1   0   1   0   1   1|         1         1         1         1         1         1         0         1
0x6e    $A000-$AFFF      1   1   0   1   1   1   0|         1         1         1         1         1         1         0         1
0x6f    $A000-$AFFF      1   1   0   1   1   1   1|         1         1         1         1         1         1         0         1
0x72    $C000-$FFFF      1   1   1   0   0   1   0|         1         1         1         1         1         1         1         0
0x73    $C000-$FFFF      1   1   1   0   0   1   1|         1         1         1         1         1         1         1         0
0x76    $C000-$FFFF      1   1   1   0   1   1   0|         1         1         1         1         1         1         1         0
0x77    $C000-$FFFF      1   1   1   0   1   1   1|         1         1         1         1         1         1         1         0
0x7a    $C000-$FFFF      1   1   1   1   0   1   0|         1         1         1         1         1         1         1         0
0x7b    $C000-$FFFF      1   1   1   1   0   1   1|         1         1         1         1         1         1         1         0
0x7e    $C000-$FFFF      1   1   1   1   1   1   0|         1         1         1         1         1         1         1         0
0x7f    $C000-$FFFF      1   1   1   1   1   1   1|         1         1         1         1         1         1         1         0
```

### Output .bin image contents
```cs
FF FF BF 7F FF FF BF 7F FF FF BF 7F FF FF BF 7F FF FF BF 7F FF FF BF 7F FF FF BF 7F FF FF BF 7F FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF DF DF FF FF DF DF FF FF EF EF FF FF EF EF FF FF F7 F7 FF FF F7 F7 FF FF FB FB FF FF FF FF FF FF FD FD FF FF FD FD FF FF FD FD FF FF FD FD FF FF FE FE FF FF FE FE FF FF FE FE FF FF FE FE
```


