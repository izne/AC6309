# AC6309
A minimalistic industrial computer based on Hitachi 6309 (Motorola 6809).

## Purpose
Proof of concept custom industrial computer with minimal device count implementation. Modular, low-power design, allowing easy expansion and customization per use case.

## Mainboard
The main board contains the following:
* CPU: Hitachi 63B09P running at 1.8MHz 
* RAM: 32KB Winbond W24257A
* ROM: 16KB Atmel 28C256 EEPROM on a ZIF socket
* UART: Hitachi 63B50P (up to 1MBps) with FT23 header
* Address decoding: 74HCT00 and 74HCT138
* 2x20-pin expansion port with addres, data and control lines
* Power over USB or expansion port

## System memory map
|Address range|Device|Size|
|-------------|------|----|
|$0000-$7FFF|RAM|32KB|
|$8000-$8FFF|UART|4KB|
|$9000-$9FFF|Device 1|4KB|
|$A000-$AFFF|Device 2|4KB|
|$B000-$BFFF|Device 3|4KB|
|$C000-$FFFF|ROM|16KB|

The entire 32KB of RAM is allocated from the beginning of the address range $0000 to $7FFF.
The ROM is allocated at the last 16KB of the address space between $C000 and $FFFF.
The remaining 16KB of address space in the middle, $8000 to $BFFF is used for four I/O devices, each with a 4KB address space (work in progress for using only 4KB for the entire I/O).


## Communication
As the computer does not have a keyboard or screen devices intended, a UART chip is used as a built-in communication device, coupled with a FTDI header (for FT232) to connect to a PC via USB.

## Software
Bare metal test applications at first. Eventually running NitrOS-9 from BIOS. The goal is to use high level C code.

## Toolchain
* [AS09](https://gitlab.com/dfffffff/as09)
* [LWTOOLS-4.20](http://www.lwtools.ca/)
* [CMOC](http://perso.b2b2c.ca/~sarrazip/dev/cmoc.html)
* [MillFork](https://github.com/KarolS/millfork)

## Emulators
* [6809 online assembler](http://6809.uk/)
* [XRoar](https://www.6809.org.uk/xroar/)
* [XRoar Online](https://www.6809.org.uk/xroar/online/)


## Future use
Possible use cases:
* Basis of a custom industrial controller
* Basis of a flight control computer
* Basis of a fictional "Pravetz-8N" computer
* Basis of a custom gaming console (see MAME for 6309 games)


- - - 

#### References and inspiration:
* [Minimal chip count 6809 computer by Grant Searle](http://searle.x10host.com/6809/Simple6809.html)
* [HB6809 by Lindoran](https://github.com/lindoran/HB6809)
* [OMEN Kilo](https://github.com/omenmicro/kilo)