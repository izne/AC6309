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

		ORG $0000

ACIA_C 	EQU $A000 				; ACIA control register address
ACIA_D 	EQU $A001 				; ACIA data register address

A_CPU3	EQU "6309"
A_CPU8  EQU "6809"
D_CPU	RMB 1					; equ "6309"
D_SPD 	RMB 2					; equ "-.-"
D_BPS	EQU "115200"
D_ACIA	EQU "$A000"

		ORG		$1000

Start	
ChkCPU 							; Check CPU type
		PSHS    D               ; Save Reg-D
		FDB     $1043           ; 6309 COMD instruction (COMA on 6809)
		CMPB    1,S             ; not equal if 6309
		BNE     Is6309          ; Branch to Is6309 if not equal

Is6809  
		LDA		#33
		STA 	D_CPU
		BRA 	ChkCPU_End

Is6309  
        LDA 	#33
        STA 	D_CPU
	
ChkCPU_End
		PULS    D,PC


ChkSpeed						; Check the available memory. Zero out each checked cell.
ChkSpeedEnd

ChkMem							; Check the available memory. Zero out each checked cell.
ChkMemEnd


PrintM	ldx 	#BOOTMSG 			; Load address of the message
MsgLoop    lda 	,x 					; Load the next character from the message
        beq 	Done 				; If it's the null terminator, we're done
        sta 	ACIA_D 				; Otherwise, send the character to ACIA
        jsr 	Delay 				; Introduce a delay
        leax 	1, x 				; Move to the next character in the message
        bra 	MsgLoop 				; Repeat for the next character
		
Done    RTS 						; Stop execution

Delay   LDA 	#100 				; Delay between character output 
Delay_Loop
        SUBA	#1					; Decrement the counter
        BNE 	Delay_Loop 			; Repeat until the counter is zero
        RTS 						; Return from subroutine
		
BOOTMSG FCC 	"AC6309/AC29 rev.1, December 2023", $0A, $0D
		FCC		"CPU: ", D_CPU , " at ", D_SPD, " MHz", $0A, $0D
		FCC		"RAM: 32K $0000 - $7FFF", $0A, $0D
		FCC		"ROM: 16K $C000 - $FFFF", $0A, $0D
		FCC		"ACIA: ", D_BPS, " baud at ", D_ACIA, $0A, $0D, 0		