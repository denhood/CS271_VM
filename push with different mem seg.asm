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
M=M+1 //SP++

//----ANOTHER PUSH----------------//
@5   //value to be pushed on stack(arbitrary)
D=A  //D=5
@SP  //load RAM[0]
A=M  //put value at RAM[0] in A register
M=D  //put 5 in RAM[256]
@SP
M=M+1 //increment stackpointer

//put 8 in static[0]
@8
D=A
@19
M=D //now we have 8 in RAM[16]

//getting value from static

@3 //value of offset
D=A
@16 //value of static
A=D+A //goto memlocation static+offset
D=M //get value at static+offset

//now that we have located 8 in RAM[19] (static+3)
@SP  //load RAM[0]
A=M  //put value at RAM[0] in A register
M=D  //put 5 in RAM[256]
@SP
M=M+1 //increment stackpointer