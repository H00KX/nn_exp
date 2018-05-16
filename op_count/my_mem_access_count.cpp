#include <stdio.h>
#include "pin.H"


FILE * trace;
static UINT64 MemReadCount = 0;
static UINT64 MemWriteCount = 0;


VOID Instruction(INS ins, VOID *v)
{
    UINT32 memOperands = INS_MemoryOperandCount(ins);

    // Iterate over each memory operand of the instruction.
    for (UINT32 memOp = 0; memOp < memOperands; memOp++)
    {
        if(INS_MemoryOperandIsRead(ins, memOp)) MemReadCount++;
        if(INS_MemoryOperandIsWritten(ins, memOp)) MemWriteCount++;
    }
}


VOID Fini(INT32 code, VOID *v)
{
    fprintf(trace, "mem read: %llu\n", MemReadCount);
    fprintf(trace, "mem write: %llu\n", MemReadCount);
    fclose(trace);
}

   
INT32 Usage()
{
    PIN_ERROR( "This Pintool prints a trace of memory addresses\n" 
              + KNOB_BASE::StringKnobSummary() + "\n");
    return -1;
}


int main(int argc, char *argv[])
{
    if (PIN_Init(argc, argv)) return Usage();
    printf("main initialized\n");
    trace = fopen("my_mem_access_count.out", "w");


    INS_AddInstrumentFunction(Instruction, 0);

    PIN_AddFiniFunction(Fini, 0);
    printf("Finished\n");

    // Never returns
    PIN_StartProgram();
    
    return 0;
}
