#! /usr/bin/env python3

import os, sys, time, re

for key in os.environ:
    print(key, "=", os.environ.get(key))
userName = os.environ.get("USERNAME") or os.environ.get("USER")
computerName = os.environ.get("HOSTNAME") or os.environ.get("COMPUTERNAME") or os.environ.get("NAME")
currentDir = os.getcwd()
print(f"{userName}@{computerName}:{currentDir}")


def redirect(command):
    tempDisplayFD = -1
    # check for redirects
    # https://stackoverflow.com/questions/13160564/python-index-of-item-in-list-without-error
    try:
        targetIndex = command.index(">") + 1
        print("targetIndex", targetIndex)
    except ValueError:
        targetIndex = -1

    if targetIndex > -1:
        targetOutput = command[targetIndex]
        print("targetOutput", targetOutput)
        tempDisplayFD = os.dup(1)
        # disconnect FD1
        os.close(1)
        # connect the output file to FD1
        os.open(targetOutput, os.O_CREAT | os.O_WRONLY)
        # Dr F says this needs to be here
        os.set_inheritable(1, True)
        # print("Redirect Complete")
        command = command[:(targetIndex - 1)]
        print("command", command)
    return (command, tempDisplayFD)

def restore(tempDisplayFD):
    if tempDisplayFD > -1:
        os.close(1)
        os.open(tempDisplayFD, os.O_CREAT | os.O_WRONLY)

while True:
        print(f"{userName}@{computerName}:{currentDir}")
        print(f"$ ", end = "")

        command = input().strip().split()
        print("command", command)

        if command[0] == "exit":
            sys.exit(0)

        elif command[0] == "cd":
            if len(command) > 1:
                newPath = command[1]
                if os.path.isdir(newPath):
                    currentDir = newPath
                    os.chdir(newPath)
                else:
                    print(f"cd: no such directory: {newPath}")
            else:
                print("cd: path not specified")

        else:
            print(f"Command not recognized: {command[0]}")
            pid = os.getpid()

            os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

            rc = os.fork()

            if rc < 0:
                os.write(2, ("fork failed, returning %d\n" % rc).encode())
                sys.exit(1)

            elif rc == 0:                   # child
                os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                            (os.getpid(), pid)).encode())
                


                for dir in re.split(":", os.environ['PATH']): # try each directory in the path
                    program = "%s/%s" % (dir, command[0])
                    os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
                    if os.path.isfile(program):
                        try:
                            command, tempDisplayFD = redirect(command)  
                            print("command", command)
                            os.execve(program, command, os.environ) # try to exec program
                            # process terminates after succesfully invoking execve
                        except FileNotFoundError:             # ...expected
                            pass                              # ...fail quietly

                os.write(2, ("Child:    Could not exec %s\n" % command[0]).encode())
                sys.exit(1)                 # terminate with error

            else:                           # parent (forked ok)
                os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                            (pid, rc)).encode())
                childPidCode = os.wait()
                os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                            childPidCode).encode())