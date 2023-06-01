# AC6309
A minimalistic industrial computer based on Hitachi 6309 (Motorola 6809).

## Purpose
Proof of concept custom industrial computer with minimal device count implementation. Modular, low-power design, allowing easy expansion and customization per use case.

## Mainboard
The main board contains the following:
* CPU: Hitachi 63B09P running at 1.8MHz 
* RAM: 32KB Winbond W24257A
* ROM: 16KB Atmel AT28C256 EEPROM
* UART: Hitachi 63B50P (up to 1MBps) on FT23 header with hardware handshake
* Address decoding: 74HCT00 and 74HCT138
* 2x20-pin expansion port with address, data and control lines
* Power over USB or expansion port

## System memory map
|Address range|Device|Size|
|-------------|------|----|
|$0000-$7FFF|RAM|32KB|
|$8000-$8FFF|Extension port #1|4KB|
|$9000-$9FFF|Extension port #2|4KB|
|$A000-$AFFF|UART|4KB|
|$B000-$BFFF|Extension port #3|4KB|
|$C000-$FFFF|ROM|16KB|

The entire 32KB of RAM is allocated from the bottom of the address range $0000 to $7FFF.
The ROM is allocated at top 16KB of the address space starting $C000 to $FFFF.

The I/O mapping is temporary and to allow compatibility with existing BIOS images having ACIA on address 0xA000. 

### Work in progress: I/O update
|Address range|Device|Size|
|-------------|------|----|
|$0000-$7FFF|RAM|32KB|
|$8000-$8FFF|Unallocated|4KB|
|$9000-$9FFF|Unallocated|4KB|
|$A000-$AFFF|I/O|4KB|
|$B000-$BFFF|Unallocated|4KB|
|$C000-$FFFF|ROM|16KB|

The I/O being split into four pieces is forming the ACIA and the 3 extension port SELECT lines with the following addressing:
|Address range|Device|Size|
|-------------|------|----|
|$A000-$A3FF|UART|1KB|
|$A400-$A7FF|Extension port #1|1KB|
|$A800-$ABFF|Extension port #2|1KB|
|$AC00-$AFFF|Extension port #3|1KB|

## Writing the ROM image
Using the combination ROM image in Intel HEX format it needs first be turned into a binary image to be written to the EEPROM.
> objcopy -I ihex -O binary ExBasROM.hex ExBasROM.bin

Write the resulting .bin file using the specially created EEPROM programmer for AT28C-series EEPROMs. Or any other.
> promdude.exe -wExBasROM.bin

## Communication
The system communicates with a host computer via USB serial connection using the included ACIA device and its UART capability, coupled with an FT23 header. Host computer serial port settings: 115200 baud, 8n1, no hardware handshake.

## Software
Main goals for the first runs of the project:
- ASSIST09 and Extended BASIC
- Use of high level C code (the CMOC project)
- Cross-compile on host machine
- No continuous burning of EEPROM for program deployment (instead paste S19 in ASSIST09 console and run)



## Toolchain
* [AS9](http://home.hccnet.nl/a.w.m.van.der.horst/m6809.html)
* [AS09](https://gitlab.com/dfffffff/as09)
* [LWTOOLS-4.20](http://www.lwtools.ca/)
* [CMOC](http://perso.b2b2c.ca/~sarrazip/dev/cmoc.html)
* [MillFork](https://github.com/KarolS/millfork)

## Emulators
* [6809 online assembler](http://6809.uk/)
* [XRoar](https://www.6809.org.uk/xroar/online/)


## Future use
Possible use cases:
* Basis of a custom industrial controller
* Basis of a flight control computer
* Basis of a fictional "Pravetz-8N" computer
* Basis of a custom gaming console (see MAME for 6309 games)


- - - 

#### References and inspiration:
* [sbc689 by Jeff Tranter](https://github.com/jefftranter/6809)
* [6809 computer by Grant Searle](http://searle.x10host.com/6809/Simple6809.html)
* [HB6809 by Lindoran](https://github.com/lindoran/HB6809)
* [OMEN Kilo](https://github.com/omenmicro/kilo)
* [Chip Labels by Grant Searle](http://searle.x10host.com/labels/ChipLabels.pdf)