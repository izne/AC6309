# AC6309
A minimalistic industrial computer based on Hitachi 6309 (Motorola 6809).

## Purpose
Proof of concept custom industrial computer with minimal implementation.

## Mainboard
The main board contains the following:
* CPU: Hitachi 63B09P running at 2MHz
* RAM: 32KB (only 16KB addressed) Winbond W24257A
* ROM: 32KB Atmel 28C256 EEPROM on a ZIF socket
* UART: Toshiba TMP6861 double-channel (up to 1MBps)
* Address decoders: 74HCT00 and 74HCT138

## Memory map
The current design has the following address space:
* RAM: 0x0000-0x7FFF
* ROM: 0x8000-0xFFFF
* UART: 0xA000-0xA003
* Extension slot #1: 0xB000 - 
* Extension slot #2: 0xC000 - 
* Extension slot #3: 0xD000 - 

Implementation of address decoder using 74HCT138 is in progress.

In consideration: memory banking with 74HCT00 to enable two 32K RAM chips.


## Communication
As the computer does not have keyboard or screen intended, a double UART chip is used. 
* UART#1 provides FTDI header (for FT232) to connect to a PC via USB.
* UART#2 is used to produce an I2C bus

## Software
Bare metal test applications, at first. Eventually running NitrOS-9. The goal is to use C via CMOC project.

## Toolchain
* AS09 
* LWTOOLS-4.20 
* CMOC 


## Future use
Possible use cases:
* Basis of a custom industrial computer
* Basis of a flight control computer (ARINC429, AM9511)
* Basis of a fictional "Pravetz-8N" computer
* Basis of a custom gaming console (double dragon 6309)


- - - 

#### References
* Minimal chip count 6809 computer by Grant Searle
* HB6809 by Lindoran