//put 123 in memory
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
//put 456 in memory
@456
D=A
@SP
A=M
M=D
@SP
M=M+1
//---sub---//
@SP
M=M-1 
A=M
D=M //put last value in D register
@SP
M=M-1
A=M
A=M
D=A-D
@SP
A=M
M=D //put result in location of SP
@SP
M=M+1