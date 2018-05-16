#include <stdio.h>
#include <iostream>
#include "pin.H"

#define MaxOpNum 1024


FILE * trace;
UINT64 myCount[MaxOpNum] = {0};


VOID Instruction(INS ins, VOID *v)
{
    myCount[INS_Opcode(ins)]++;
}


VOID Fini(INT32 code, VOID *v)
{
    for (int i = 0; i < MaxOpNum; i++){
        fprintf(trace, "Opcode-%d: %llu\n", i, myCount[i]);
    }
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
    trace = fopen("my_op_count.out", "w");

    INS_AddInstrumentFunction(Instruction, 0);

    PIN_AddFiniFunction(Fini, 0);

    // Never returns
    PIN_StartProgram();
    
    return 0;
}
