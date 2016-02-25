@256 //put base address of stack in SP (we don't need this in general)
D=A
@SP
M=D

@24  //value to be pushed on stack
D=A //D=5
@SP //load RAM[0]
A=M //put value at RAM[0] in A register
M=D //put 5 in RAM[256]
@SP
M=M+1 //increment stackpointer


//-------start of not-------
@SP //get value at stack pointer
M=M-1 //decrement
A=M
D=M  //put last value in D register
D=!M
M=D //put not result to last value in RAM