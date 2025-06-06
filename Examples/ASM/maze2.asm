	ORG $1000          ; Starting address in memory
	
START
	JSR INIT_RANDOM    ; Initialize random number generator

LOOP1
	JSR GET_RANDOM     ; Get random number in A (0 or 1)
	CMPA #1            ; Compare A with 1
	BEQ PRINT_SLASH    ; If A = 1, print "/"
        
PRINT_DOT
	LDA #'.'           ; Load ASCII value for "."
	JSR PRINT_CHAR     ; Print the character
	BRA NEXT           ; Go to next iteration

PRINT_SLASH
	LDA #'/'           ; Load ASCII value for "/"
	JSR PRINT_CHAR     ; Print the character

NEXT BRA LOOP1           ; Repeat the loop indefinitely

; Subroutine: Initialize random generator
INIT_RANDOM
	LDA #$55           ; Example seed value
	STA RANDOM_SEED    ; Store it in RANDOM_SEED
	RTS

; Subroutine: Generate random number (0 or 1)
GET_RANDOM
	LDA RANDOM_SEED    ; Load current seed
	ASL                ; Shift left (basic LFSR randomization)
	EORA #$A5          ; XOR with a constant (pseudo-random)
	STA RANDOM_SEED    ; Store back as new seed
	ANDA #1            ; Keep only the least significant bit
	RTS

; Subroutine: Print character in A
PRINT_CHAR
	LDX #$A001         ; ACIA/Console output (adjust for your system)
	STAA ,X            ; Output character to console
	RTS

; Variables
RANDOM_SEED FCB 0         ; Byte to store random seed

	END START
