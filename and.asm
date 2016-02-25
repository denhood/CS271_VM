@256 //put base address of stack in SP (we don't need this in general)
D=A
@SP
M=D

@5  //value to be pushed on stack
D=A //D=5
@SP //load RAM[0]
A=M //put value at RAM[0] in A register
M=D //put 5 in RAM[256]
@SP
M=M+1 //increment stackpointer

@6  //value to be pushed on stack
D=A //D=5
@SP //load RAM[0]
A=M //put value at RAM[0] in A register
M=D //put 5 in RAM[256]
@SP
M=M+1 //increment stackpointer
//-------start of and-------
@SP //get value at stack pointer
M=M-1 //decrement
A=M
D=M  //put last value in D register
@SP
M=M-1
A=M
A=M //put next to last value in A register
D=D&A
@SP
A=M
M=D