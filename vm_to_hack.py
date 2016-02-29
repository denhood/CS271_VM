def open_file(fileName):
    fileObj = open(fileName,'w')
    return fileObj
    
def write_to_file(string, fileObj):
    fileObj.write(string)
    return

def close_file(fileName):
    fileName.close()
    return
def setup(fileName):
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

def eq(count):#NEED TO HAVE AN INCREMENTING VARIABLE AND CONCATENATE WITH ADDRESS LABELS (AROUND_1)...
    string = ""
    #load last two values off stack into D and A registers
    string = "\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nA=M"
    #subtract the two registers, if D=A then D-A=0
    string = string + "\nD=D-A"
    #check to see if this is zero if it is, jump to (AROUND), else set memory to FALSE
    string = string + "\n@AROUND"+count+"\nD;JEQ\n@SP\nA=M\nM=0\n@END_COMP"+count+"\n0;JMP"
    #set value in memory to TRUE
    string = string + "\n(AROUND"+count+")\n@SP\nA=M\nM=-1"
    #after setting memory to TRUE or FALSE, JUMP here to increment SP
    string = string + "\n(END_COMP"+count+")\n@SP\nM=M+1"
    return string

def gt():
    pass

def lt():
    pass

def And():
    pass

def Or():
    pass

def Not():
    pass

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
    VM_command_to_HACK("push constant 123",fptr)
    VM_command_to_HACK("push constant 456",fptr)
    VM_command_to_HACK("add",fptr)
    VM_command_to_HACK("push constant 421",fptr)
    VM_command_to_HACK("sub",fptr)
    VM_command_to_HACK("neg",fptr)
    VM_command_to_HACK("push constant 421",fptr)
    VM_command_to_HACK("eq",fptr)
    VM_command_to_HACK("push constant 3",fptr)
    VM_command_to_HACK("push constant 6",fptr)
    VM_command_to_HACK("eq",fptr)
    close_file(fptr)
    print("file written")
