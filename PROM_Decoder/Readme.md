# AC6309 Address Decoder EEPROM Programming Script

This script generates a truth table and a binary file (`ac6309_decoder.bin`) for programming an AT28C64 EEPROM (8Kx8) to serve as an address decoder for the AC6309 single board computer. The EEPROM provides active-low chip select signals for various internal devices and expansion slots based on the upper address lines (A15–A8).

## Memory Map

- **0000–7FFF**: 32K RAM (handled by 7400 logic, not controlled by the EEPROM)
- **8000–9FFF**: Unmapped space (not decoded by the EEPROM)
- **A000–A0FF**: UART_CS (internal UART device)
- **A100–A1FF**: PIA_CS (internal PIA device)
- **A200–A2FF**: INT2_CS (internal interrupt 2 device)
- **A300–A3FF**: INT3_CS (internal interrupt 3 device)
- **B000–B0FF**: EXT1_CS (expansion slot 1)
- **B100–B1FF**: EXT2_CS (expansion slot 2)
- **B200–B2FF**: EXT3_CS (expansion slot 3)
- **B300–B3FF**: EXT4_CS (expansion slot 4)
- **C000–FFFF**: 16K ROM (handled by 7400 logic, not controlled by the EEPROM)

The EEPROM's 8K address space (0x0000–0x1FFF) is used to generate chip select outputs for the A000–B3FF range, with each 256-byte block (e.g., A000–A0FF) producing identical output patterns.

## EEPROM AT28C64 DIP28 Pin Mapping

### Inputs (A15–A8)
- A0 (pin 2): A8
- A1 (pin 3): A9
- A2 (pin 4): A10
- A3 (pin 5): A11
- A4 (pin 6): A12
- A5 (pin 7): A13
- A6 (pin 8): A14
- A7 (pin 9): A15
- A8–A12 (pins 10–14): Tied to ground (not used)

### Outputs (Active-Low Chip Selects)
- D7 (pin 23): /UART_CS
- D6 (pin 22): /PIA_CS
- D5 (pin 21): /INT2_CS
- D4 (pin 20): /INT3_CS
- D3 (pin 19): /EXT1_CS
- D2 (pin 1): /EXT2_CS
- D1 (pin 28): /EXT3_CS
- D0 (pin 27): /EXT4_CS

## Script Functionality

### Purpose
The script generates:
- A truth table displaying the first address of each 256-byte block where the EEPROM controls a device.
- A binary file (`ac6309_decoder.bin`) containing 8192 bytes (8K) of data to program the AT28C64 EEPROM.

### Logic
- The script iterates over the EEPROM's 8K address space (0x0000–0x1FFF), extracting A15–A8 bits.
- Chip select outputs are calculated using AND logic based on A15–A8 bit patterns for each 256-byte region (e.g., A000–A0FF for /UART_CS).
- The lower 8 bits (A7–A0) do not affect the EEPROM output, as the chip select remains constant within each 256-byte block.
- Outputs are inverted to active-low and stored in the binary file.

### Output
- **Truth Table**: Displays the address, device name, range, and active-low chip select states for the first address of each controlled region (A000, A100, etc.).
- **Binary File**: `ac6309_decoder.bin` contains 8192 bytes, with each byte representing the inverted chip select pattern for the corresponding 256-byte block in the 6809 address space.

### Notes
- Each 256-byte block (e.g., A000–A0FF) has identical EEPROM outputs, determined by the A15–A8 bits.
- Regions 0000–7FFF (RAM) and C000–FFFF (ROM) are handled by 7400 logic and marked as "not EEPROM-controlled" in the output.
- The unmapped space (8000–9FFF) is also noted but not actively decoded by the EEPROM.

## Usage
1. Run the script: `python script_name.py`
2. Check the console for the truth table output.
3. Use the generated `ac6309_decoder.bin` file to program an PROM of the decoder.

## Example Output
``` python
Address  Device       Range           | /UART_CS /PIA_CS  /INT2_CS /INT3_CS /EXT1_CS /EXT2_CS /EXT3_CS /EXT4_CS
---------------------------------------------------------------------------------------------------------------
$A000    UART         A000-A0FF       |        0        1        1        1        1        1        1        1
$A100    PIA          A100-A1FF       |        1        0        1        1        1        1        1        1
$A200    INT2         A200-A2FF       |        1        1        0        1        1        1        1        1
$A300    INT3         A300-A3FF       |        1        1        1        0        1        1        1        1
$B000    EXT1         B000-B0FF       |        1        1        1        1        0        1        1        1
$B100    EXT2         B100-B1FF       |        1        1        1        1        1        0        1        1
$B200    EXT3         B200-B2FF       |        1        1        1        1        1        1        0        1
$B300    EXT4         B300-B3FF       |        1        1        1        1        1        1        1        0
```