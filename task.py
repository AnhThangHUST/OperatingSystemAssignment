#!/usr/bin/python
import os
from signal import SIGKILL
#import psutil
from prettytable import PrettyTable
import psutil
import operator

class Task:
    def __init__(self):
        self.table = PrettyTable(["PROCNAME", "PROCID","%CPU", "%MEM", "COMMAND"])

    def ListAllProcess(self):
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        for pid in pids:
            try:
                f =  open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
            except FileNotFoundError:
                continue
            if len(f)==0:
                continue
            p = psutil.Process(int(pid))
            proc_name = p.name()
            lst = [proc_name[:10], str(pid),  p.cpu_percent(interval=None), round(p.memory_percent(),2), p.cmdline()[0]]
            self.table.add_row(lst)
        
    # priorities o day la map lay tu gtk "string":"value"
    def KillBasedOnPriority(self, priorities):
        killed_processes = list()
        sorted_priorities = sorted(priorities.items(), key=operator.itemgetter(1))
        for tup in sorted_priorities:
            killed_processes.append(tup[0])
        killed_pid = []
        print ("The Memory Of Operating System is exhausted now")
        print ("Starting To Kill ..............................")
        for based_key in killed_processes:
            for row in self.table:
                if based_key in row.get_string(fields=["COMMAND"]):
                    pid = row.get_string(fields=["PROCID"], border=False).split("\n")[1].strip()
                    name = row.get_string(fields=["PROCNAME"], border=False).split("\n")[1].strip()
                    killed_pid.append([pid,name])
        print (killed_pid)
        for content in killed_pid:
            print ("Process "+content[1]+" with PID "+content[0])
            os.system("kill -9 "+ content[0]) 
            #os.system("killall "+ content[1])
        print ("DONE")
