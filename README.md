# AC6309
Minimalistic industrial computer based on Hitachi 6309 (Motorola 6809).

## Purpose
Proof of concept industrial custom computer with minimal implementation of the latest iteration of 6809 - Hitachi 6309!

## Mainboard
The main board contains the following:
* CPU: Hitachi 63B09P running at 2MHz
* RAM: 32KB Winbond W24257A at 25ns refresh
* ROM: 32KB Atmel 28C256 EEPROM on a ZIP socket
* UART: Toshiba TMP6861 double-channel (up to 1.5 MBps)
* Address decoders: 74HCT00 and 74HCT138



## Communication
The double UART chip is selected to provide a constant connection to a PC together with a "free" channel to communicate to other devices (via RS-232).

## Software
Initially bare metal test applications. Eventually running NitrOS-9 or CP/M variant for 6809. 

## Toolchain
TBA

## Future use
Possible use cases:
* Basis of a flight control computer, providing some navigational calculations and control signals (keywords: ARINC429, AM9511, Airdata)
* Basis of a fictional "Pravetz-8N" computer
* Basis of a custom gaming console (double dragon 6309)
* Basis of a custom industrial computer

- - - 

#### References
* Minimal chip count 6809 computer by Grant Searle
* HB6809 by Lindoran