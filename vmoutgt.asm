@256
D=A
@SP
M=D
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
A=M
D=A-D
@AROUND4
D;JGT
@SP
A=M
M=0
@END_COMP4
0;JMP
(AROUND4)
@SP
A=M
M=-1
(END_COMP4)
@SP
M=M+1
(END)
@END
0;JMP