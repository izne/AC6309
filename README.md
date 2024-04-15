# AC6309
A minimalistic industrial computer core, based on Motorola 6809 platform.

## Purpose
Proof of concept custom industrial computer with minimal device count implementation. Modular, low-power design, allowing easy expansion and customization per use case.

## Configuration AC29
![AC29 Config](Images/AC29_config.PNG)

## Prototype build 
* CPU: Hitachi HD63B09 @ 1.8MHz
* RAM: 32KB Winbond W24257A
* ROM: 16KB Atmel 28C256 EEPROM (half)
* UART: Hitachi HD63B50 (1MBps) on FT23 USB Serial
* Address decoding: 74HCT00
* Power over USB

![AC29 Breadboard](Images/AC29_Breadboard.jpg)

![AC29 BASIC](Images/AC29_BASIC.jpg)

## Layout
![AC29 Layout](Images/AC29_layout.PNG)

## PCB Updates
Current state of PCB design:
![AC29 PCB](Renders/PCB.png)
![AC29 TOP](Renders/TOP.png)
![AC29 BTM](Renders/BTM.png)

## Dedication
AC29 is dedicated to my beloved father.

![BAUS](Images/bauscii.png)

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

Currently it looks like this:

|Address range|Device|Size|
|-------------|------|----|
|$0000-$7FFF|RAM|32KB|
|$8000-$8FFF|Unallocated|4KB|
|$9000-$9FFF|Unallocated|4KB|
|$A000-$AFFF|I/O|4KB|
|$B000-$BFFF|Unallocated|4KB|
|$C000-$FFFF|ROM|16KB|

### AC29
The A000 I/O address being split into four pieces (another 74138) is forming the ACIA and adding 3 extension port select lines with the following addressing:
|Address range|Device|Size|
|-------------|------|----|
|$A000-$A3FF|UART|1KB|
|$A400-$A7FF|Extension port #1|1KB|
|$A800-$ABFF|Extension port #2|1KB|
|$AC00-$AFFF|Extension port #3|1KB|

### AC219
The addressing can be "A" - internal devices, "B" - external devices:
|Address range|Device|Size|
|-------------|------|----|
|$A000-$A3FF|UART|1KB|
|$A400-$A7FF|Internal device #1|1KB|
|$A800-$ABFF|Internal device #2|1KB|
|$AC00-$AFFF|Internal device #3|1KB|

|Address range|Device|Size|
|-------------|------|----|
|$B000-$B3FF|Extension port #1|1KB|
|$B400-$B7FF|Extension port #2|1KB|
|$B800-$BBFF|Extension port #3|1KB|
|$BC00-$BFFF|Extension port #4|1KB|

For even more external devices:
$8000-$8FFF - another 4 ports
$9000-$9FFF - and another 4 ports


## Decoding logic and CS lines
ROM: When ROM_CS is LOW (active low). The signal is produced by one NAND gate fed with A14 and A15 lines.

RAM: When A15 signal is LOW (the second half (16KBytes) of the address space).

ACIA: Using A13, A14 and A15 for the CS0, CS1 and CS2 registers respectively.


## Writing the ROM image
Using the combination ROM image in Intel HEX format it needs first be turned into a binary image to be written to the EEPROM.
> objcopy -I ihex -O binary combined.hex combined.bin

Write the resulting .bin file using the specially created EEPROM programmer for AT28C-series EEPROMs. Or any other.
> promdude.exe -combined.bin

As a note, burning the combined.bin (16K) onto 32K 28C256 has to be at the correct half. Optionally, a copy of combined.bin twice into the chip will do as well.

## ROM switching
As the firmware is 16K and 28C256 chips are nowadays more accesible, two firmwares could be stored in the 32K. A possible rom switching key can be implemented on the board, to switch the higher or lower part of the chip to be "visible"  (A15).

## Communication
The system communicates with a host computer via USB serial connection using the included ACIA device and its UART capability, coupled with an FT23 header. Host computer serial port settings: 115200 baud, 8n1, no hardware handshake.

## Software
Main goals for the first runs of the project:
- [x] Run ASSIST09 and Extended BASIC
- [x] Write basic program (asm)
- [x] Cross-compile on host machine
- [x] Easy program transer via ASSIST09 Load (S19)
- [ ] Use of high level C code (CMOC)

## Hardware
Main goals for the fabrication part:
- [x] Breadboard prototype running
- [ ] Extended addressing with 74138
- [ ] Expansion board with easy coupling
- [ ] Revision 1 completion and PCB fabrication
- [ ] Expansion card: TMP68681 (2x6350) / 2x RS232
- [ ] Expansion card: Ethernet adapter (ENC28J60)
- [ ] Expansion card: SAA1099+amp audio interface
- [ ] Expansion card: Am9511 card
- [ ] Expansion card: Tape interface
- [ ] Expansion card: VGA and PS/2 (Arduino)
- [ ] Expansion card: VGA and PS/2 (MC6845/HD6321)

## Toolchain
* [A09](https://github.com/Arakula/A09)
* [AS09](https://gitlab.com/dfffffff/as09)
* [LWTOOLS-4.20](http://www.lwtools.ca/)
* [CMOC](http://perso.b2b2c.ca/~sarrazip/dev/cmoc.html)
* [MillFork](https://github.com/KarolS/millfork)

## Emulators
* [6809 online assembler](http://6809.uk/)
* [XRoar](https://www.6809.org.uk/xroar/online/)


- - - 
#### Prerequisites
The schematics and PCB design is made with [KiCad](http://kicad.org)


#### References and inspiration:
* [sbc689 by Jeff Tranter](https://github.com/jefftranter/6809)
* [6809 computer by Grant Searle](http://searle.x10host.com/6809/Simple6809.html)
* [HB6809 by Lindoran](https://github.com/lindoran/HB6809)
* [OMEN Kilo](https://github.com/omenmicro/kilo)
* [Chip Labels by Grant Searle](http://searle.x10host.com/labels/ChipLabels.pdf)

### Some great oldschool books:

* [![6809 Assembly Programming](Images/book_6809_programming.PNG)](https://colorcomputerarchive.com/repo/Documents/Books/6809%20Assembly%20Language%20Programming%20(Lance%20Leventhal).pdf)


* [![6809 Assembly Subroutines](Images/book_6809_subroutines.PNG)](https://colorcomputerarchive.com/repo/Documents/Books/6809%20Assembly%20Language%20Subroutines%20(Lance%20Leventhal).pdf)

* [![6809 Microcomputer Programming and Interfacing with Experiments](Images/book_6809_experiments.PNG)](https://colorcomputerarchive.com/repo/Documents/Books/6809%20Microcomputer%20Programming%20and%20Interfacing%20with%20Experiments%20(Andrew%20C.%20Staugaard%20Jr.).pdf)

* [![Programming the 6809](Images/book_6809_programming_the.PNG)](https://colorcomputerarchive.com/repo/Documents/Books/Programming%20the%206809%20(Rodney%20Zaks%20and%20William%20Labiak).pdf)

* [The 6309 Book](https://colorcomputerarchive.com/repo/Documents/Books/The%206309%20Book%20(Burke%20&%20Burke).pdf)


https://colorcomputerarchive.com/repo/Documents/Books/Programming%20the%206809%20(Rodney%20Zaks%20and%20William%20Labiak).pdf

https://www.chibiakumas.com/6809/
