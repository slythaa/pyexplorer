import os
import shutil
import shlex

import pyperclip


#print("Welcome to PyExplorer! Simple CLI Python file explorer. Not really practical, just made for fun")

# Get user directory
home_directory = os.path.expanduser( '~' )
#print(home_directory)

# Gets current directory (crazy)
current_directory = os.getcwd()
#print(current_directory)

def create_directory(name):
    pass

# Move files!! |:O its a bit weird
# Can't handle folder/file names with spaces in em, something to do with the .split(), fix later, works fine otherwise
# Doesn't work for directories, but then again it's not supposed to anyways
def move_files(file, destination):
    #file = current_directory + "\\" + file

    #file = file.replace(" ", "\\")
    #destination = destination.replace(" ", "\\")

    if os.path.isfile(file):
        if os.path.isdir(destination):
            # Using shutil to move file, os.rename() just wouldn't work
            shutil.move(file, destination)
            print("Moved file successfully!")
        else:
            print("Invalid destination")
    else:
        file = current_directory + "\\" + file
        if os.path.isfile(file):
            if os.path.isdir(destination):
                shutil.move(file,destination)
            else:
                print("Invalid destination")
        else:
            print("Not a file in current directory")

# TODO create file, not hard do now
def create_file(file):

    isfile = os.path.isfile(file)
    if isfile:
        print("Cannot create, file already exists.")
    else:
        try:
            with open(file, 'w') as f:
                pass
            print(f"File '{file}' has been created!")
        except:
            print(file)
            print("Failed")

# List all files in a directory
def list_files(directory):

    # List of files and folder in current directory
    file_list = []
    if directory == 'cwd':
        for file_path in os.listdir(current_directory):
            # check if current file_path is a file
            if os.path.isfile(os.path.join(current_directory, file_path)):
                # add filename to list
                file_list.append("{FILE}: " + file_path)
            else:
                file_list.append("{FOLDER}: " + file_path)

        modified_list = str(file_list).replace('[', '').replace(']', '')
        print(modified_list)

    # List of files and folders in specified directory
    else:
        if os.path.isdir(directory):
            for file_path in os.listdir(directory):
                # check if current file_path is a file
                if os.path.isfile(os.path.join(directory, file_path)):
                    # add filename to list
                    file_list.append("{FILE}: " + file_path)
                else:
                    file_list.append("{FOLDER}: " + file_path)

            modified_list = str(file_list).replace('[', '').replace(']', '')
            print(modified_list)
        else:
            print("Directory doesn't exist...")


def cmds():
    print("""
        Commands:
        'move': Move file 
        'delete': Delete file
        'copy': Copy file
        'create': Create file
        'createdir': Create folder in current folder or somewhere else
        'cd': Change directory, or when used without an argument, prints out current working directory
        'list': List all files in current directory   
        'quit': Exit script
        'c': Copy current directory to clipboard to get by faster
        
        [TIP]: Make sure to wrap paths with spaces in quotes!
    """)

# DON'T CHANGE THE ORDER
command_list = ["move", "delete", "copy", "createdir", "cd", "cmds", "list", "quit", "..","c", "create"]


# Used fo the 'changedir' command, used to go up one directory
go_up_one = command_list[8]
copy_chdir = command_list[9]

while True:
    user_input = input(f"{current_directory} ")

    # Check if user_input is empty and keep asking for input if empty
    while user_input.strip() == "":
        user_input = input(f"{current_directory} ")

    user_input = user_input.replace('\\', '/')

    # Split user input using shlex
    # I think it just finds quotes in a string and combines it into one string, useful for what I'm doing
    user_list = shlex.split(user_input)
    command_entered = user_list[0]


    #print(user_list[0])
    # Check if first word is a command
    if command_entered in command_list:
    # MOVE COMMAND
        if command_entered == command_list[0]:
            if len(user_list) == 3:
                move_files(user_list[1], user_list[2])
            else:
                print("The move command requires 2 arguments.")
    # DELETE COMMAND
        elif command_entered == command_list[1]:

            if len(user_list) > 1:
                if os.path.isfile(user_list[1]):
                    os.remove(user_list[1])
                    print("File deleted!")
                else:
                    # If not recognised as a file, do one last check then exit
                    file = current_directory + "\\" + user_list[1]
                    if os.path.isfile(file):
                        os.remove(file)
                        print("File deleted!")
                    else:
                        print("Not a file")
            else:
                print("Delete command requires a file to be deleted.")
    # COPY COMMAND
        elif command_entered == command_list[2]:
            if len(user_list) > 2:
                # TODO make file copy
                if os.path.isfile(user_list[1]) and os.path.isdir(user_list[2]):
                    cmd = f'copy "{user_list[1]}" "{"2" + user_list[1]}"'
                    os.system(cmd)
            else:
                print("The 'copy' command must have 2 arguments: file and destination")
    # CREATE DIRECTORY COMMAND
        elif command_entered == command_list[3]:
            print("Create directory")
    # CHANGE DIRECTORY COMMAND
        # Change directory or print working directory
        elif command_entered == command_list[4]:
            if len(user_list) > 1:
                if os.path.isdir(user_list[1]):
                    change = os.path.abspath(user_list[1])
                    current_directory = str(change)
                else:
                    user_list[1] = current_directory + "\\" + user_list[1]
                    if os.path.isdir(user_list[1]):
                        current_directory = user_list[1]
                    else:
                        print("Not a directory! We can't move to nowhere!\nMake sure to wrap filenames or paths with spaces in double quotes!")

            else:
                print(f"\nCurrent directory: {current_directory}\n")
    # LIST COMMAND
        # List all commands
        elif command_entered == command_list[5]:
            cmds()

    # LIST ITEMS COMMAND
        # List all items in directory
        elif command_entered == command_list[6]:
            # Check if user_input has an argument
            if len(user_list) > 1:
                if user_list[1]:
                    list_files(user_list[1])
            # If not, default to listing all items within current directory
            else:
                list_files("cwd")

        # Copy to clipboard current working directory
        elif command_entered == copy_chdir:
            pyperclip.copy(current_directory)
            print("Copied current directory!")

    # CREATE FILE
        elif command_entered == command_list[10]:
            create_file(user_list[1])

        elif command_entered == command_list[7]:
            print("Exiting...")
            break
    else:
        print(f"Invalid command '{command_entered}', enter 'cmds' for list of commands.")






