from threading import Thread
from threading import Event 
################################################################################
# DESCRIPTION:
# This class allow you to thread multiple operations called instruction
# Each operation will be done time by time
# The instruction format is:
#     inst = [long_func, start_func, end_func, start_param, param, end_param]
# with func = def func([param]):
# every time a new instruction is executed we got the following scheduling
#    1 - start_func(start_param)
#    2 - long_func(param)
#    3 - end_func(param)
################################################################################


class Threader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__instructions = []
        self.__is_running = False
        self.__pause = Event()

    def addInstruction(self, instruction):
        self.__instructions.append(instruction)
        self.__pause.set()

    def cancelInstruction(self, instruction):
        for i in range(len(self.__instructions)):
            if self.__instructions[i] is instruction:
                del self.__instructions[i]
                break

    def isRunning(self):
        return self.__is_running

    def __exec(self, inst):
        inst[1](inst[3])
# This is a trick to update correctly the instruction
        inst[0](inst[4])
        inst[2](inst[5])

    def run(self):
        self.__pause.clear()
        while (1):
            while(len(self.__instructions) != 0):
                self.__is_running = True
                instruction = self.__instructions.pop(0)
                self.__exec(instruction)
            self.__pause.clear()
            self.__pause.wait(100)
        self.__is_running = False

