@256 //put base address of stack in SP (we don't need this in general)

@5  //value to be pushed on stack
D=M //D=5
@SP //load RAM[0]
A=M //put value at RAM[0] in A register
M=D //put 5 in RAM[256]
