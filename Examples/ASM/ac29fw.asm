; AC6309/AC29 Rev. 1
;
; Firmware version 1.0
;
; http://github.com/izne/AC6309
;
; 2023 Dimitar Angelov <info@DimitarAngelov.com>
;
; Compile:
; asm6809 -3 -S -v -o ac29fw.s19 ac29fw.asm

		 ORG     $1100
D_CPU	RMB 1
ACIA_C  EQU $A000
ACIA_D  EQU $A001
RAM_S   EQU $0000
RAM_E   EQU $7FFF

        ORG     $1500
Start
        LDX     #BootMsg
        JSR     PrintMsg
        LDX     #CopyMsg
        JSR     PrintMsg
		JSR		ChkCPU
        JSR     PrintCPU
Ending  SWI
                                ; Check if 6309
ChkCPU
        LDA     #8              ; Assume 6809 at start
        STA     D_CPU           ; Store 8 to indicate 6809
        TFR     CC,DP           ; TFR CC,DP is valid only on 6309, illegal on 6809
        BCS     Is6809          ; Branch if illegal instruction (6809)

Is6309
        LDA     #3
        STA     D_CPU           ; Store 3 to indicate 6309

Is6809
EndChkCPU
        RTS

PrintCPU
        LDX     #CPU_MSG        ; Point X to the start of the "CPU Type:" message
        JSR     PrintMsg        ; Print the "CPU Type:" message
        LDX     #MSG_6809       ; Default to 6809 message
        LDA     D_CPU           ; Load the CPU type value
        CMPA    #3              ; Compare it to 3 (6309)
        BEQ     Print6309       ; If 3, change pointer to 6309 message
        BRA     PrintMsg        ; Jump to print message loop

Print6309
        LDX     #MSG_6309       ; Load message for 6309

PrintMsg
        LDA    ,X+              ; Load a character from pointed message
        BEQ     PrintDone       ; Check for end of message
        STA     ACIA_D          ; Output character to ACIA
        JSR     Delay           ; Introduce a delay
        BRA     PrintMsg        ; Loop to print next character
PrintDone
        RTS                     ; Return from subroutine

Delay
        LDA     #100            ; Delay between character output 
Delay_Loop
        SUBA    #1              ; Decrement the counter
        BNE     Delay_Loop      ; Repeat until the counter is zero
        RTS                     ; Return from subroutine
		

CPU_MSG  FCC    "CPU: ",0
RAM_MSG  FCC    "RAM: ",0
MSG_6309 FCC    "Hitachi 6309", $0A, $0D, 0
MSG_6809 FCC    "Motorola 6809", $0A, $0D, 0
BootMsg  FCC    "AC6309/AC29, Rev. 1", $0A, $0D, 0
CopyMsg  FCC    "(c) 2023 Dimitar Angelov", $0A, $0D, 0