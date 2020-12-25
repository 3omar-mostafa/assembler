mov r1, r2
jsr nono ; jsr opcode + address of label nono in memory  

br nono ; غلطة البروجرامر يستحمل


hlt

nono:
	mov r1, r3
	rts  ; opcode of rts

; INTERRUPT:
	mov r1, r4
	iret ; opcode of iret

