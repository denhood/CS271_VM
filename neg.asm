@256 //load base address of stack in SP (we don't need this in general)
D=A  //put base address in D register
@SP  //load address of SP RAM[0]
M=D  //write address of stack to SP

//----PUSH-------------------------//
@5   //value to be pushed on stack(arbitrary)
D=A  //D=5
@SP  //load RAM[0]
A=M  //put value at RAM[0] in A register
M=D  //put 5 in RAM[256]
@SP
M=M+1 //increment stackpointer

//----neg-------------------------//
@SP
M=M-1
A=M
M=-M
@SP
M=M+1
