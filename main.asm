MOV   N  ,   R0 		; R0 = 7 address 0
XOR R1, R1 				; R1 = 0 address 2
MOV #20, R3 			; R3 = 20 address 3
						; memory is word addressable, so there isno
						; problem in having odd addresses, why?
Label3: 				; address 5
MOV -(R3), M 			; M = 5 , R3= 19 address 5
X: DEC R0 					; R0 = 6 address 7
Y:CMP #18, @R3 			; C=1,N=1 address 8
BHI Label1				; Not taken address 10
MOV #18,@R3 			; M=18 address 11
Label1: 				; address 13
DEC R0 					; R0=5 address 13
BEQ Label2 				; not taken address 14
INC R3 					; R3=20 address 15
Label2: 				; address 16
BR Label3 				; address 16
HLT 					; address 17
Define N 7,8, 9, 11	  	; address 18
Define M 5 				; address 19
