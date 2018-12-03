#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h> 
#include "sys/types.h"
#include "sys/sysinfo.h"
#include "iostream"

using namespace std;
int main (void) {  
    while (1) { 
        malloc(1000*sizeof(int)); 
        struct sysinfo memInfo;
        sysinfo (&memInfo);
        if (memInfo.freeram*100/memInfo.totalram <10){
                sleep(1000);
                return 0;  
        }  
    }  
}  
