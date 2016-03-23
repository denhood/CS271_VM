"""
Title: vm_to_hack1
Author: Harold Smith, Denny Hood, Brad Thompson
Class: CS 271
Description: This program will translate commands for memory allocation and
             perform arithmetic operations of add, subtract and negate. Also,
             the translator can perform boolean logic such as AND, OR, NOT. The
             output file will be stored as the input file with a .HACK extension.
"""
################################################################################
#                        GLOBAL VARIABLE ALERT!                                #
labelCount = 0 #need this global variable to handle address labels in eq
################################################################################

def open_file():
    fileName = input("filename: ")
    fileInList = fileName.split(".",2)
    if fileInList[1] == 'vm':
        try:
            filePtr = open(fileName,"r") #we don't want to modify .vm file
            return filePtr
        except IOError:
            print ("Error: ",fileName," does not exist.")
            return -1
    elif fileInList[1] == "asm":
        try:
            filePtr = open(fileName,"w") #we want to modify .asm file
            return filePtr
        except IOError:
            print ("Error: ",fileName," could not be created.")
            return -1
    else:
        print("Error: ",fileName," does not appear to be a valid file name.")
        return -2
    
def write_to_file(string, fileObj):
    fileObj.write(string)
    return

def close_file(fileName): #create an infinite assembly loop and close file
    fileName.write("\n(END)\n@END\n0;JMP")
    fileName.close()
    return

def setup(fileName): #setup puts starting address of stack in SP
    fileName.write("@256\n"+\
                   "D=A\n"+\
                   "@SP\n"+\
                   "M=D\n"+\
                   "@300\n"+\
                   "D=A\n"+\
                   "@LCL\n"+\
                   "M=D\n"+\
                   "@16\n"+\
                   "D=A\n"+\
                   "@static\n"+\
                   "M=D\n")
    return
    
def push(memSeg, offset): #NOTE: only complete segment is constant
    if memSeg == 'constant': #write the value of offset to the stack
        #offset is a value to put on stack
        return('\n@'+offset+\
               '\nD=A'+\
               '\n@SP'+\
               '\nA=M'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'static': #base address IS RAM[16]
        #get the value at static
        return('\n@'+str(offset)+\
               '\nD=A'+\
               '\n@static'+\
               '\nA=A+D'+\
               '\nD=M'+\
               '\n@SP'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'that': #base address of area in heap stored in RAM[4]
        #get the value at THAT
        return('\n@'+str(offset)+\
               '\nD=A'+\
               '\n@THAT'+\
               '\nA=A+D'+\
               '\nD=M'+\
               '\n@SP'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'this': #base address of area in heap stored in RAM[3]
        #get the value at THIS
        return('\n@'+str(offset)+\
               '\nD=A'+\
               '\n@THIS'+\
               '\nA=A+D'+\
               '\nD=M'+\
               '\n@SP'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'argument': #base address of area in heap stored in RAM[2]
        #get the value at ARG
        return('\n@'+str(offset)+\
               '\nD=A'+\
               '\n@ARG'+\
               '\nA=A+D'+\
               '\nD=M'+\
               '\n@SP'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'local': #base address of area in heap stored in RAM[1]
        #get the value of LCL
        return('\n@'+str(offset)+\
               '\nD=A'+\
               '\n@LCL'+\
               '\nA=A+D'+\
               '\nD=M'+\
               '\n@SP'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'pointer': #base address of area in heap stored in RAM[?]
        #get the value of LCL
        return('\n@'+offset+\
               '\nD=A'+\
               '\n@SP'+\
               '\nA=M'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'temp': #Hold the contents of temp segment in RAM[5]
        #get the value of LCL
        return('\n@'+offset+\
               '\nD=A'+\
               '\n@SP'+\
               '\nA=M'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    else:
        return ('seg not found')

def pop(memSeg, offset):
    memorySeg = {'static': 'static', 'that': 'THAT', 'this': 'THIS', 'argument': 'ARG', 'local': 'LCL'}
    if memSeg == 'constant':
        return('\n@SP'+\
               '\nM=M-1')
    elif memSeg in memorySeg:
        return('\n@SP'+\
               '\nM=M-1'+\
               '\n@'+memorySeg[memSeg]+\
               '\nD=M'+\
               '\n@'+str(offset)+\
               '\nD=A+D'+\
               '\n@R15'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nA=M'+\
               '\nD=M'+\
               '\n@R15'+\
               '\nA=M'+\
               '\nM=D')
    elif memSeg == 'pointer' or memSeg == 'temp':
        pass
    else:
        return 'Non-valid memory segment'
               
    

def add():
    #add the last two values on the stack
    string =  ""
    #decrement the stack pointer to last value that was pushed on
    string += "\n@SP"+\
              "\nM=M-1"
    #load that value in D register
    string += "\nA=M"+\
              "\nD=M"
    #decrement the stack pointer to next to last value
    string += "\n@SP"+\
              "\nM=M-1"
    #load that value in the A register
    string += "\nA=M"+\
              "\nA=M"
    #add two values and put in D register
    string += "\nD=D+A"
    #write D register contents to memory and advance stack pointer
    string += "\n@SP"+\
              "\nA=M"+\
              "\nM=D"+\
              "\n@SP"+\
              "\nM=M+1"
    return string

def sub():
    string = ""
    #load the stack pointer and decrement to last value pushed and put in D register
    string = "\n@SP"+\
             "\nM=M-1"+\
             "\nA=M"+\
             "\nD=M"
    #load next to last value and put in A register
    string += "\n@SP"+\
              "\nM=M-1"+\
              "\nA=M"+\
              "\nA=M"
    #subtract D register from A register and store in D register
    string += "\nD=A-D"
    #put result in location of memory addressed by SP
    string += "\n@SP"+\
              "\nA=M"+\
              "\nM=D"+\
              "\n@SP"+\
              "\nM=M+1"
    return string

def neg():
    string = ""
    #load the SP and decrement to last value
    string = "\n@SP"+\
             "\nM=M-1"+\
             "\nA=M"
    #negate value
    string += "\nM=-M"
    #advance SP
    string += "\n@SP"+\
              "\nM=M+1"
    return string

def eq():
    global labelCount #forgive me Batman for I have sinned
    labelCount += 1   #NEED TO HAVE AN INCREMENTING VARIABLE AND CONCATENATE WITH ADDRESS LABELS ex:(AROUND1)
    string = ""
    #load last two values off stack into D and A registers
    string = "\n@SP"+\
             "\nM=M-1"+\
             "\nA=M"+\
             "\nD=M"+\
             "\n@SP"+\
             "\nM=M-1"+\
             "\nA=M"+\
             "\nA=M"
    #subtract the two registers, if D=A then D-A=0
    string += "\nD=D-A"
    #check to see if this is zero if it is, jump to (AROUND), else set memory to FALSE (0)
    string += "\n@AROUND"+str(labelCount)+\
              "\nD;JEQ"+\
              "\n@SP"+\
              "\nA=M"+\
              "\nM=0"+\
              "\n@END_COMP"+str(labelCount)+\
              "\n0;JMP"
    #set value in memory to TRUE (-1)
    string += "\n(AROUND"+str(labelCount)+")"+\
              "\n@SP"+\
              "\nA=M"+\
              "\nM=-1"
    #after setting memory to TRUE or FALSE, JUMP here to increment SP
    string += "\n(END_COMP"+str(labelCount)+")"+\
              "\n@SP"+\
              "\nM=M+1"
    return string

def gt():
    global labelCount #forgive me Batman for I have sinned
    labelCount += 1#NEED TO HAVE AN INCREMENTING VARIABLE AND CONCATENATE WITH ADDRESS LABELS ex:(AROUND1)
    string = ""
    #load last value of stack in D register
    string = "\n@SP"+\
             "\nM=M-1"+\
             "\nA=M"+\
             "\nD=M"
    #load second to last value in A register
    string += "\n@SP"+\
              "\nM=M-1"+\
              "\nA=M"+\
              "\nA=M"
    #if A>D then A-D must be positive
    string += "\nD=A-D"
    #if A-D is NOT greater than 0, return FALSE (0)
    string += "\n@AROUND"+str(labelCount)+\
              "\nD;JGT"+\
              "\n@SP"+\
              "\nA=M"+\
              "\nM=0"+\
              "\n@END_COMP"+str(labelCount)+\
              "\n0;JMP"
    #if A-D is positive, return TRUE (-1)
    string += "\n(AROUND"+str(labelCount)+")"+\
              "\n@SP"+\
              "\nA=M"+\
              "\nM=-1"
    #increment SP
    string += "\n(END_COMP"+str(labelCount)+")"+\
              "\n@SP"+\
              "\nM=M+1"
    return string

def lt():
    global labelCount #forgive me Batman for I have sinned
    labelCount += 1#NEED TO HAVE AN INCREMENTING VARIABLE AND CONCATENATE WITH ADDRESS LABELS ex:(AROUND1)
    string = ""
    #load last value of stack in D register
    string = "\n@SP"+\
             "\nM=M-1"+\
             "\nA=M"+\
             "\nD=M"
    #load second to last value in A register
    string += "\n@SP"+\
              "\nM=M-1"+\
              "\nA=M"+\
              "\nA=M"
    #if A<D then A-D must be negative
    string += "\nD=A-D"
    #if A-D is NOT less than 0, return FALSE (0)
    string += "\n@AROUND"+str(labelCount)+\
              "\nD;JLT"+\
              "\n@SP"+\
              "\nA=M"+\
              "\nM=0"+\
              "\n@END_COMP"+str(labelCount)+\
              "\n0;JMP"
    #if A-D is negative, return TRUE (-1)
    string = string + "\n(AROUND"+str(labelCount)+")"+\
             "\n@SP"+\
             "\nA=M"+\
             "\nM=-1"
    #increment SP
    string += "\n(END_COMP"+str(labelCount)+")"+\
              "\n@SP"+\
              "\nM=M+1"
    return string

def And():
    string = ""
    #load last value of stack in D register
    string = "\n@SP"+\
             "\nM=M-1"+\
             "\nA=M"+\
             "\nD=M"
    #load next to last value of stack in A register
    string += "\n@SP"+\
              "\nM=M-1"+\
              "\nA=M"+\
              "\nA=M"
    #store result of D&A in D register
    string += "\nD=D&A"
    #load last address of SP and put TRUE or FALSE there
    string += "\n@SP"+\
              "\nA=M"+\
              "\nM=D"
    #increment SP
    string += "\n@SP"+\
              "\nM=M+1"
    return string

def Or():
    string = ""
    #load last value of stack in D register
    string = "\n@SP"+\
             "\nM=M-1"+\
             "\nA=M"+\
             "\nD=M"
    #load next to last value of stack in A register
    string += "\n@SP"+\
              "\nM=M-1"+\
              "\nA=M"+\
              "\nA=M"
    #store result of D&A in D register
    string += "\nD=D|A"
    #load last address of SP and put TRUE or FALSE there
    string += "\n@SP"+\
              "\nA=M"+\
              "\nM=D"
    #increment SP
    string += "\n@SP"+\
              "\nM=M+1"
    return string

def Not():
    string = ""
    #load last value of stack in D register
    string = "\n@SP"+\
             "\nM=M-1"+\
             "\nA=M"+\
             "\nD=M"
    #NOT the result in D register
    string += "\nD=!M"
    #write NOT to memory
    string += "\nM=D"
    #increment SP
    string += "\n@SP"+\
              "\nM=M+1"
    return string

def VM_command_to_HACK(instruction,file):
    templst = instruction.split()
    if templst[0] == 'push':
        write_to_file(push(templst[1],templst[2]),file)
    elif templst[0] == 'pop':
        write_to_file(pop(templst[1],templst[2]),file) 
    elif templst[0] == 'add':
        write_to_file(add(),file)
    elif templst[0] == 'sub':
        write_to_file(sub(),file)
    elif templst[0] == 'neg':
        write_to_file(neg(),file)
    elif templst[0] == 'eq':
        write_to_file(eq(),file)
    elif templst[0] == 'gt':
        write_to_file(gt(),file)
    elif templst[0] == 'lt':
        write_to_file(lt(),file)
    elif templst[0] == 'and':
        write_to_file(And(),file)
    elif templst[0] == 'or':
        write_to_file(Or(),file)
    elif templst[0] == 'not':
        write_to_file(Not(),file)
    elif templst[0] == 'goto':
        pass
    elif templst[0] == 'if-goto':
        pass
    elif templst[0] == 'function':
        pass
    elif templst[0] == 'call':
        pass
    elif templst[0] == 'return':
        pass
    else:
        print("command not found")
    return

def parse_command(fileIn):
    command_list = []
    for line in fileIn:
        line = line.strip()
        if line != "": #make sure line is not empty
            if line[0] != '/': #make sure line is not a comment
                command_list.append(line)    
    return command_list

def remove_labels(listIn, dictIn):
    #remove labels from list and add entry in dictionary with line after label
    for line in listIn:
        if line[0:5] == 'label':
            ProgCount = listIn.index(line)
            listIn.remove(line)
            line = line.split()
            dictIn[line[1]] = ProgCount
    return

def main():
    print("Input ",end="")
    inputfptr = open_file()
    commandList = parse_command(inputfptr)#parse file
    inputfptr.close()
    print("Output ",end="")
    outputfptr = open_file()
    setup(outputfptr) #setup addresses of stack, LCL, ARGS, THIS, THAT
    for line in commandList:
        VM_command_to_HACK(line,outputfptr)
    close_file(outputfptr)
    print("file written")

main()
