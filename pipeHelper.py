import os, sys, time, re

def executeCommand(program, command):
    os.execve(program, command, os.environ)

def hookupPipe(program, command, readIndex, writeIndex, pipeIndex):
    r, w = os.pipe()
    pid = os.fork()

    if pid > 0:
        print("pipe parent")
        #parent
        os.close(r)
        os.dup2(w, 1)
        os.close(w)
        executeCommand(program, command[:pipeIndex])
    else:
        print("pipe child")
        # child
        os.close(w)
        os.dup2(r, 0)
        os.close(r)
        executeCommand(program, command[readIndex:len(command)])


def handler(program, command):
    marker = len(command)
    if "|" in command:
        readIndex = command.index("|") + 1
        writeIndex = command.index("|") - 1
        pipeIndex = command.index("|")
        # marker = min(hookupPipe(program, command, readIndex, writeIndex, pipeIndex), marker)
        hookupPipe(program, command, readIndex, writeIndex, pipeIndex)
    command = command[:marker]
    return command