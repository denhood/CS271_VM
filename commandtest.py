################################################################################
#                        MEMORY SEGMENT ALERT!                                 #
# This module only uses the constant memory segment to write directly to stack #
################################################################################

import vm_to_hack1 as VM

def test():
    #run this function to test features of VM_command_to_HACK
    #note: separate files are written per vm command
    addfptr = VM.open_file("vmoutadd.asm")
    subfptr = VM.open_file("vmoutsub.asm")
    negfptr = VM.open_file("vmoutneg.asm")
    eqfptr = VM.open_file("vmouteq.asm")
    gtfptr = VM.open_file("vmoutgt.asm")
    ltfptr = VM.open_file("vmoutlt.asm")
    andfptr = VM.open_file("vmoutand.asm")
    orfptr = VM.open_file("vmoutor.asm")
    notfptr = VM.open_file("vmoutnot.asm")
    
    VM.setup(addfptr) #setup address of stack
    VM.setup(subfptr) #setup address of stack
    VM.setup(negfptr) #setup address of stack
    VM.setup(eqfptr) #setup address of stack
    VM.setup(gtfptr) #setup address of stack
    VM.setup(ltfptr) #setup address of stack
    VM.setup(andfptr) #setup address of stack
    VM.setup(orfptr) #setup address of stack
    VM.setup(notfptr) #setup address of stack
    #add
    VM.VM_command_to_HACK("push constant 123",addfptr)
    VM.VM_command_to_HACK("push constant 456",addfptr)
    VM.VM_command_to_HACK("add",addfptr)
    #sub
    VM.VM_command_to_HACK("push constant 99",subfptr)
    VM.VM_command_to_HACK("push constant 100",subfptr)
    VM.VM_command_to_HACK("sub",subfptr)
    #neg
    VM.VM_command_to_HACK("push constant 42",negfptr)
    VM.VM_command_to_HACK("neg",negfptr)
    #test for equality (false)
    VM.VM_command_to_HACK("push constant 421",eqfptr)
    VM.VM_command_to_HACK("eq",eqfptr)
    #test for equality (true)
    VM.VM_command_to_HACK("push constant 3",eqfptr)
    VM.VM_command_to_HACK("push constant 3",eqfptr)
    VM.VM_command_to_HACK("eq",eqfptr)
    #AND
    VM.VM_command_to_HACK("push constant 21",andfptr) #21 = 10101B
    VM.VM_command_to_HACK("push constant 10",andfptr) #10 = 01010B
    VM.VM_command_to_HACK("and",andfptr) #21&10 = 0
    #OR
    VM.VM_command_to_HACK("push constant 21",orfptr) #21 = 10101B
    VM.VM_command_to_HACK("push constant 10",orfptr) #10 = 01010B
    VM.VM_command_to_HACK("or",orfptr) #21|10 = 31
    #NOT
    VM.VM_command_to_HACK("push constant 341",notfptr) #341 = 101010101B
    VM.VM_command_to_HACK("not",notfptr) #!341 = -342
    #lt 8!<7 return FALSE
    VM.VM_command_to_HACK("push constant 8",ltfptr)
    VM.VM_command_to_HACK("push constant 7",ltfptr)
    VM.VM_command_to_HACK("lt",ltfptr)
    #gt 8>7 return TRUE
    VM.VM_command_to_HACK("push constant 8",gtfptr)
    VM.VM_command_to_HACK("push constant 7",gtfptr)
    VM.VM_command_to_HACK("gt",gtfptr)
    VM.close_file(addfptr)
    VM.close_file(subfptr)
    VM.close_file(negfptr)
    VM.close_file(eqfptr)
    VM.close_file(gtfptr)
    VM.close_file(ltfptr)
    VM.close_file(andfptr)
    VM.close_file(orfptr)
    VM.close_file(notfptr)
    print("files written")

test() #this will automatically run test
