import os, sys, time, re

def output(command, fileNameIndex):
    # check for redirects
    if fileNameIndex > -1:
        targetOutput = command[fileNameIndex]
        # print("targetOutput", targetOutput)
        # disconnect FD1
        os.close(1)
        # connect the output file to FD1
        os.open(targetOutput, os.O_CREAT | os.O_WRONLY)
        # Dr F says this needs to be here
        os.set_inheritable(1, True)
        # print("Redirect Complete")
        
        
    return fileNameIndex - 1

def input(command, fileNameIndex):
    if fileNameIndex > -1:
        targetInput = command[fileNameIndex]
        os.close(0)
        newFd = os.open(targetInput, os.O_RDONLY)
        # print("newFd", newFd)
        os.set_inheritable(0, True)
        
        
    return fileNameIndex - 1

def handler(command):
    # check for output redirection
    firstRedirectIndex = len(command)
    # print("firstRedirectIndex", firstRedirectIndex)
    try:
        # https://stackoverflow.com/questions/13160564/python-index-of-item-in-list-without-error
        fileNameIndex = command.index(">") + 1
        firstRedirectIndex = output(command, fileNameIndex)
    except ValueError:
        fileNameIndex = -1
    # check for input redirection
    try:
        fileNameIndex = command.index("<") + 1
        firstRedirectIndex = min(input(command, fileNameIndex), firstRedirectIndex)
    except ValueError:
        fileNameIndex = -1
    # print("command after processing redirects", command)
    # print("firstRedirectIndex", firstRedirectIndex)
    command = command[:(firstRedirectIndex)]
    # int("command after slicing", command)
    return command






'''
def restore(tempDisplayFD):
    if tempDisplayFD > -1:
        os.close(1)
        os.open(tempDisplayFD, os.O_CREAT | os.O_WRONLY)
'''