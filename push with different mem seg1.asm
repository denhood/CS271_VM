//ESTABLISH POINTER LOCATIONS IN AREA OF HEAP--------------------------------//
//SET LOCATION OF STACK POINTER------------------------------------------------
	@256 //load base address of stack in SP (we don't need this in general)
	D=A  //put base address in D register
	@SP  //load address of SP RAM[0]
	M=D  //write address of stack to SP
//SET LOCATION OF STATIC-------------------------------------------------------
	@16
	D=A
	@STATIC
	M=D
//SET LOCATION OF LOCAL--------------------------------------------------------
	@300//create an area in heap for base address of LCL
	D=A
	@LCL
	M=D
//SET LOCATION OF ARGUMENT-----------------------------------------------------
	@400//create an area in heap for base address of ARG
	D=A
	@ARG
	M=D
//SET LOCATION OF THIS----------------------------------------------------------
	@3000//create an area in heap for base address of THIS
	D=A
	@THIS
	M=D
//SET LOCATION OF THAT----------------------------------------------------------
	@3010//create an area in heap for base address of THAT
	D=A
	@THAT
	M=D
//----------------------------------------------------------------------------//

//----ASSIGN VALUES TO STATIC------------------------------------------------//
@5   //arbitrary value to be put in static
D=A  //D=5
@STATIC  //load address of STATIC
A=M  //put value at RAM[0] in A register
M=D  //put 5 in RAM[STATIC]
@11  //arbitrary value to put in static
D=A
@STATIC
A=A+1
M=D  //put 11 in RAM[STATIC+1]


//----"push static 1"----------------//
//calculate address of STATIC+1
@STATIC
A=A+1 //where 1 is OFFSET
D=M
//push value onto stack via SP
@SP
A=M
M=D //should push 11 onto stack
@SP
M=M+1 //increment SP