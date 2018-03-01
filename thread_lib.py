from threading import Thread
from threading import Event 
################################################################################
# DESCRIPTION:
# This class allow you to thread multiple operations called instruction
# Each operation will be done time by time
# The instruction format is:
#     inst = [func, is_finished, param, ...]
# Instruction must be unique
# While the instruction isn't started to execute the is_finshed = -1
# During execution of the function, is_finished = 0
# After the end of the executionm is_finished = 1
################################################################################


class Threader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__instructions = []
        self.__is_running = False
        self.__pause = Event()

    def addInstruction(self, instruction):
        instruction[1] = -1
        self.__instructions.append(instruction)
        self.__pause.set()

    def cancelInstruction(self, instruction):
        for i in range(len(self.__instructions)):
            if self.__instructions[i] is instruction:
                del self.__instructions[i]
                break

    def isRunning():
        return self.__is_running

    def __exec(self, inst):
        inst[1] = 0
# This is a trick to update correctly the instruction
        param = inst[2:]
        inst[0](param)
        inst[2:] = param
        inst[1] = 1

    def run(self):
        self.__pause.clear()
        while (1):
            while(len(self.__instructions) != 0):
                self.__is_running = True
                instruction = self.__instructions.pop(0)
                self.__exec(instruction)        
            self.__pause.wait(100)
        self.__is_running = False

