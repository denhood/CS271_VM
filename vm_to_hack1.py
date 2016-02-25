labelCount = 0 #need this global variable to handle address labels in eq

def open_file(fileName):
    fileObj = open(fileName,'w')
    return fileObj
    
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
                   "M=D")
    return
    
def push(memSeg, offset):
    if memSeg == 'constant':
        #offset is a value to put on stack
        return('\n@'+offset+\
               '\nD=A'+\
               '\n@SP'+\
               '\nA=M'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'static': #RAM[16]
        #get the value at static
        return('\n@'+offset+\
               '\nD=A'+\
               '\n@SP'+\
               '\nA=M'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'that': #RAM[4]
        #get the value at THAT
        return('\n@'+offset+\
               '\nD=A'+\
               '\n@SP'+\
               '\nA=M'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeAg == 'this': #RAM[3]
        #get the value at THIS
        return('\n@'+offset+\
               '\nD=A'+\
               '\n@SP'+\
               '\nA=M'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'argument': #RAM[2]
        #get the value at ARG
        return('\n@'+offset+\
               '\nD=A'+\
               '\n@SP'+\
               '\nA=M'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'local': #RAM[1]
        #get the value of LCL
        return('\n@'+offset+\
               '\nD=A'+\
               '\n@SP'+\
               '\nA=M'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'pointer': #RAM[1]
        #get the value of LCL
        return('\n@'+offset+\
               '\nD=A'+\
               '\n@SP'+\
               '\nA=M'+\
               '\nM=D'+\
               '\n@SP'+\
               '\nM=M+1')
    elif memSeg == 'temp': #RAM[1]
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

def add():
    #add the last two values on the stack
    string =  ""
    #decrement the stack pointer to last value that was pushed on
    string = string + "\n@SP\nM=M-1"
    #load that value in D register
    string = string + "\nA=M\nD=M"
    #decrement the stack pointer to next to last value
    string = string + "\n@SP\nM=M-1"
    #load that value in the A register
    string = string + "\nA=M\nA=M"
    #add two values and put in D register
    string = string + "\nD=D+A"
    #write D register contents to memory and advance stack pointer
    string = string + "\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    return string

def sub():
    string = ""
    #load the stack pointer and decrement to last value pushed and put in D register
    string = "\n@SP\nM=M-1\nA=M\nD=M"
    #load next to last value and put in A register
    string = string + "\n@SP\nM=M-1\nA=M\nA=M"
    #subtract D register from A register and store in D register
    string = string + "\nD=A-D"
    #put result in location of memory addressed by SP
    string = string + "\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    return string

def neg():
    string = ""
    #load the SP and decrement to last value
    string = "\n@SP\nM=M-1\nA=M"
    #negate value
    string = string + "\nM=-M"
    #advance SP
    string = string + "\n@SP\nM=M+1"
    return string

def eq():
    global labelCount #forgive me Batman for I have sinned
    labelCount += 1#NEED TO HAVE AN INCREMENTING VARIABLE AND CONCATENATE WITH ADDRESS LABELS ex:(AROUND1)
    string = ""
    #load last two values off stack into D and A registers
    string = "\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nA=M"
    #subtract the two registers, if D=A then D-A=0
    string = string + "\nD=D-A"
    #check to see if this is zero if it is, jump to (AROUND), else set memory to FALSE (0)
    string = string + "\n@AROUND"+str(labelCount)+"\nD;JEQ\n@SP\nA=M\nM=0\n@END_COMP"+str(labelCount)+"\n0;JMP"
    #set value in memory to TRUE (-1)
    string = string + "\n(AROUND"+str(labelCount)+")\n@SP\nA=M\nM=-1"
    #after setting memory to TRUE or FALSE, JUMP here to increment SP
    string = string + "\n(END_COMP"+str(labelCount)+")\n@SP\nM=M+1"
    return string

def gt():
    global labelCount #forgive me Batman for I have sinned
    labelCount += 1#NEED TO HAVE AN INCREMENTING VARIABLE AND CONCATENATE WITH ADDRESS LABELS ex:(AROUND1)
    string = ""
    #load last value of stack in D register
    string = "\n@SP\nM=M-1\nA=M\nD=M"
    #load second to last value in A register
    string = string + "\n@SP\nM=M-1\nA=M\nA=M"
    #if A>D then A-D must be positive
    string = string + "\nD=A-D"
    #if A-D is NOT greater than 0, return FALSE (0)
    string = string + "\n@AROUND"+str(labelCount)+"\nD;JGT\n@SP\nA=M\nM=0\n@END_COMP"+str(labelCount)+"\n0;JMP"
    #if A-D is positive, return TRUE (-1)
    string = string + "\n(AROUND"+str(labelCount)+")\n@SP\nA=M\nM=-1"
    #increment SP
    string = string + "\n(END_COMP"+str(labelCount)+")\n@SP\nM=M+1"
    return string

def lt():
    global labelCount #forgive me Batman for I have sinned
    labelCount += 1#NEED TO HAVE AN INCREMENTING VARIABLE AND CONCATENATE WITH ADDRESS LABELS ex:(AROUND1)
    string = ""
    #load last value of stack in D register
    string = "\n@SP\nM=M-1\nA=M\nD=M"
    #load second to last value in A register
    string = string + "\n@SP\nM=M-1\nA=M\nA=M"
    #if A<D then A-D must be negative
    string = string + "\nD=A-D"
    #if A-D is NOT less than 0, return FALSE (0)
    string = string + "\n@AROUND"+str(labelCount)+"\nD;JLT\n@SP\nA=M\nM=0\n@END_COMP"+str(labelCount)+"\n0;JMP"
    #if A-D is negative, return TRUE (-1)
    string = string + "\n(AROUND"+str(labelCount)+")\n@SP\nA=M\nM=-1"
    #increment SP
    string = string + "\n(END_COMP"+str(labelCount)+")\n@SP\nM=M+1"
    return string

def And():
    string = ""
    #load last value of stack in D register
    string = "\n@SP\nM=M-1\nA=M\nD=M"
    #load next to last value of stack in A register
    string = string+"\n@SP\nM=M-1\nA=M\nA=M"
    #store result of D&A in D register
    string = string+"\nD=D&A"
    #load last address of SP and put TRUE or FALSE there
    string = string+"\n@SP\nA=M\nM=D"
    #increment SP
    string = string+"\n@SP\nM=M+1"
    return string

def Or():
    string = ""
    #load last value of stack in D register
    string = "\n@SP\nM=M-1\nA=M\nD=M"
    #load next to last value of stack in A register
    string = string+"\n@SP\nM=M-1\nA=M\nA=M"
    #store result of D&A in D register
    string = string+"\nD=D|A"
    #load last address of SP and put TRUE or FALSE there
    string = string+"\n@SP\nA=M\nM=D"
    #increment SP
    string = string+"\n@SP\nM=M+1"
    return string

def Not():
    string = ""
    #load last value of stack in D register
    string = "\n@SP\nM=M-1\nA=M\nD=M"
    string = string + "\nD=!M"
    string = string + "\nM=D\n"
    #increment SP
    string = string+"\n@SP\nM=M+1"
    return string

def VM_command_to_HACK(instruction,file):
    templst = instruction.split()
    if templst[0] == 'push':
        write_to_file(push(templst[1],templst[2]),file)
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
    else:
        print("command not found")

def main():
    fptr = open_file("vmout.asm")
    setup(fptr) #setup address of stack
    '''
    #add
    VM_command_to_HACK("push constant 123",fptr)
    VM_command_to_HACK("push constant 456",fptr)
    VM_command_to_HACK("add",fptr)
    #sub
    VM_command_to_HACK("push constant 421",fptr)
    VM_command_to_HACK("sub",fptr)
    #neg
    VM_command_to_HACK("neg",fptr)
    #test for equality (false)
    VM_command_to_HACK("push constant 421",fptr)
    VM_command_to_HACK("eq",fptr)
    #test for equality (true)
    VM_command_to_HACK("push constant 3",fptr)
    VM_command_to_HACK("push constant 3",fptr)
    VM_command_to_HACK("eq",fptr)
    #AND
    VM_command_to_HACK("push constant 21",fptr) #21 = 10101B
    VM_command_to_HACK("push constant 10",fptr) #10 = 01010B
    VM_command_to_HACK("and",fptr) #21&10 = 0
    #OR
    VM_command_to_HACK("push constant 21",fptr) #21 = 10101B
    VM_command_to_HACK("push constant 10",fptr) #10 = 01010B
    VM_command_to_HACK("or",fptr) #21|10 = 31
    #NOT
    VM_command_to_HACK("push constant 341",fptr) #341 = 101010101B
    VM_command_to_HACK("not",fptr) #!341 = -342
    '''
    #lt 8!<7 return FALSE
    VM_command_to_HACK("push constant 8",fptr)
    VM_command_to_HACK("push constant 7",fptr)
    VM_command_to_HACK("lt",fptr)
    #gt 8>7 return TRUE
    VM_command_to_HACK("push constant 8",fptr)
    VM_command_to_HACK("push constant 7",fptr)
    VM_command_to_HACK("gt",fptr)
    close_file(fptr)
    print("file written")
