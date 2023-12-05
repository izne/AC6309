		ORG 	$1000

ACIA_C 	EQU 	$A000 				; ACIA control register address
ACIA_D 	EQU 	$A001 				; ACIA data register address	

* Set up memory locations for temporary variables
SEED_HI EQU $FFEB
SEED_LO EQU $FFEC

* Initial seed for the random number generator
INITIAL_SEED EQU $1234

Start	LDX 	#SEED_HI
Loop    JSR RNG           ; Call the random number generator
        STB SEED_HI       ; Update seed_hi for the next iteration
        LDB SEED_LO       ; Load the low byte of the seed
        ANDA #$3F         ; Mask all bits except the lowest 6 bits (0-63)
        BEQ PrintSlash    ; If the result is zero, print '/'

PrintBackslash
        LDA #'\'          ; Load ASCII code for '\'
        BRA OutputChar

PrintSlash
        LDA #'/'          ; Load ASCII code for '/'
        BRA OutputChar

OutputChar
        STA ACIA_D        ; Send the character to ACIA_D
        JSR Delay         ; Introduce a delay
        BRA Loop          ; Repeat for the next iteration

Delay   LDA 	#100 				; Delay between character output 
Delay_Loop
        SUBA	#1					; Decrement the counter
        BNE 	Delay_Loop 			; Repeat until the counter is zero
        RTS 						; Return from subroutine

RNG     LDX #SEED_HI     ; Load address of high byte of seed
        LDA SEED_HI,X    ; Load high byte of seed
        ADDA #17          ; Add a constant value for randomness (adjust as needed)
        STA SEED_HI,X   ; Store back in high byte of seed

        LDX #SEED_LO     ; Load address of low byte of seed
        LDA SEED_LO,X    ; Load low byte of seed
        ADDA #19          ; Add another constant value for more randomness (adjust as needed)
        STA SEED_LO,X   ; Store back in low byte of seed

        RTS               ; Return from subroutine

NO_OVERFLOW
        RTS               ; Return from subroutine
