# AC6309
Minimalistic industrial computer based on Hitachi 6309 (Motorola 6809).

## Purpose
Proof of concept industrial custom computer with minimal implementation of the latest iteration of 6809 - Hitachi 6309!

## Mainboard
The main board contains the following:
* CPU: Hitachi 63B09P running at 2MHz
* RAM: 32KB Winbond W24257A
* ROM: 32KB Atmel 28C256 EEPROM on a ZIP socket
* UART: Toshiba TMP6861 double-channel (up to 1.5 MBps)
* Address decoders: 74HCT00 (and/or 74HCT138)

## Memory map
0x0000-0x7FFF: RAM
0x8000-0xFFFF: ROM
0xA000-0xA003: UART


## Communication
As the computer does not have keyboard or screen intended, a double UART chip is used. The idea is that one "channel" (through FTDI adapter) will always be occupied for the connection to a PC, therefore the other one is to be used to communicate with other devices.

## Software
Initially bare metal test applications. Eventually running NitrOS-9 or CP/M variant for 6809. The goal is to use high level language, like C via CMOS project.

## Toolchain
* AS09 
* LWTOOLS-4.20
* CMOC


## Future use
Possible use cases:
* Basis of a custom industrial computer
* Basis of a flight control computer, providing some navigational calculations and control signals (ARINC429, AM9511)
* Basis of a fictional "Pravetz-8N" computer
* Basis of a custom gaming console (double dragon 6309)


- - - 

#### References
* Minimal chip count 6809 computer by Grant Searle
* HB6809 by Lindoran