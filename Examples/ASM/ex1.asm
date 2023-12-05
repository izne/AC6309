* Set up the ACIA control registers
ACIA_CTRL equ $A000   ; ACIA control register address
ACIA_DATA equ $A001   ; ACIA data register address

* Define a string to be printed
MSG     fcc "Hello, World!",0

* Start of the program
        org $E000   ; You can choose any address for your program

START   ldx #MSG    ; Load address of the message
LOOP    lda ,x+     ; Load the next character from the message
        beq DONE    ; If it's the null terminator, we're done
        sta ACIA_DATA ; Otherwise, send the character to ACIA
        jsr DELAY    ; Introduce a delay (optional)
        bra LOOP    ; Repeat for the next character

DONE    swi         ; Stop execution

* Optional delay subroutine
DELAY   lda #5000    ; You may need to adjust the delay count
DELAY_LOOP
        dec         ; Decrement the counter
        bne DELAY_LOOP ; Repeat until the counter is zero
        rts         ; Return from subroutine
