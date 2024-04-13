import os, sys, time, re

def output(command, fileNameIndex):
    # check for redirects
    if fileNameIndex > -1:
        # https://stackoverflow.com/questions/13160564/python-index-of-item-in-list-without-error
        try:
            targetOutput = command[fileNameIndex]
        except IndexError:
            print("No output specified")
            exit(1)
        # print("targetOutput", targetOutput)
        # disconnect FD1
        os.close(1)
        # connect the output file to FD1
        os.open(targetOutput, os.O_CREAT | os.O_WRONLY)
        # Dr F says this needs to be here
        os.set_inheritable(1, True)
        # print("Redirect Complete")
        return fileNameIndex - 1
    return fileNameIndex

def input(command, fileNameIndex):
    if fileNameIndex > -1:
        try:
            targetInput = command[fileNameIndex]
        except IndexError:
            print("No input file specified")
            exit(1)
        os.close(0)
        os.open(targetInput, os.O_RDONLY)
        # print("newFd", newFd)
        os.set_inheritable(0, True)
        
        return fileNameIndex - 1
    return fileNameIndex

def handler(command):
    # check for output redirection
    firstRedirectIndex = len(command)
    # print("firstRedirectIndex", firstRedirectIndex)
    if ">" in command:
        fileNameIndex = command.index(">") + 1
        firstRedirectIndex = min(output(command, fileNameIndex), firstRedirectIndex)
    # check for input redirection
    if "<" in command:
        fileNameIndex = command.index("<") + 1
        firstRedirectIndex = min(input(command, fileNameIndex), firstRedirectIndex)
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