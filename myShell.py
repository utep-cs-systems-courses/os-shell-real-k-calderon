import os, sys

env = os.environ
for key in os.environ:
    print(key, "=", os.environ.get(key))

userName = os.environ.get("USERNAME")
computerName = os.environ.get("HOSTNAME") or os.environ.get("COMPUTERNAME")
currentDir = os.getcwd()
print(f"{userName}@{computerName}:{currentDir}")


while True:
        print(f"{userName}@{computerName}:{currentDir}")
        print(f"$ ", end = "")

        command = input().strip().split()

        if command[0] == "exit":
            sys.exit(0)

        elif command[0] == "cd":
            if len(command) > 1:
                newPath = command[1]
                if os.path.isdir(newPath):
                    currentDir = newPath
                else:
                    print(f"cd: no such directory: {newPath}")
            else:
                print("cd: path not specified")

        else:
            #TODO: handle commands
            print(f"Command not recognized: {command[0]}")