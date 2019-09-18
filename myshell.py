from cmd import Cmd
import os, sys, shlex, subprocess, threading

global file_pos 
global colour 
global ENDC
global bold

class MyShell(Cmd):

    def do_cd(self, args): 
        global file_pos
        
        try:
            directory = os.getcwd()
            if args == "":
                self.do_pwd("")
            else:
                os.chdir(directory + "/" + args)
        except OSError:
            print("bash: cd: " + args + ": No such file or directory")

        file_pos = os.getcwd()


    def do_clr(self, args):
        sys.stdout.write("\033c")


    def sorter(self, name):
        if name[0] == ".":
            return name[1].lower()
        else:
            return name[0].lower()


    def do_dir(self, args): #wrong
        argument = args.split() 
        directory = args
        try:
            if argument[0] == directory:
                result = [files for files in os.listdir(directory) if not files.startswith(".")] 
                for name in sorted(result, key = self.sorter): # This loop is used to list out all the files within the directory that aren't hidden
                    print(name)

            elif argument[0] == "-a":
                result = [files for files in os.listdir(argument[1])]
                for name in sorted(result, key = self.sorter): # This loop is used to list out all the files within the directory including hidden files
                    print(name)  

        except IndexError:
            print("Enter a directory.")

        except FileNotFoundError:
            directory = file_pos.split("/") # This displays files if the directory you entered is the one that you are currently in
            if argument[0] == directory[-1]:
                result = [files for files in os.listdir(".") if not files.startswith(".")] 
                for name in sorted(result, key = self.sorter):
                    print(name)
            elif argument[0] == "-a" and argument[1] == directory[-1]:
                result = [files for files in os.listdir(".")]
                for name in sorted(result, key = self.sorter): # This displays files including hidden files if the directory you entered is the one you are currently in.
                    print(name)  

            else:
                print("Enter a directory that exists.") 


    def do_environ(self, args):
        env = os.environ # this command lists all the environment strings
        for key in env:
            print(key + "=" + env[key])  


    def do_echo(self, args):
        boolean = True # this is to get echo working like what echo normally does in a normal terminal
        while boolean:
            try:

                args = " ".join(shlex.split(args))
            except ValueError:

                sys.stdout.write(">")

                inp = input()

                args += "\n" + inp

            else:
                boolean = False

        print(args)    


    def do_pause(self, args):
        self.do_clr("") # this command just clears the screen and doesnt allow you to do anything until enter is hit.
        print("shell paused, press enter to resume")
        enter = input()
        while enter != "":
            enter = input()

        print("shell is functioning") 


    def do_quit(self, args):
        print("Quitting.") # This command allows you to quit the shell
        raise SystemExit  


    def do_pwd(self, args):
        print(os.getcwd()) # This command prints out the full path of your current directory on screen


    def complete_dir(self, text, line, begidx, endidx):
        comp_file_pos = os.getcwd()
        return [files for files in os.listdir(comp_file_pos) if files.startswith(text)] # This just gets the tab shortcut working to finish the word for dir


    def complete_cd(self, text, line, begidx, endidx):
        comp_file_pos = os.getcwd()
        return [files for files in os.listdir(comp_file_pos) if files.startswith(text)] # This just gets tab shortcut working to finish the word for cd
        


    def complete_python3(self, text, line, begidx, endidx):
        comp_file_pos = os.getcwd()
        return [files for files in os.listdir(comp_file_pos) if files.startswith(text)] # This just gets tab shortcut working to finish the word for python3



    def complete_python(self, text, line, begidx, endidx):
        comp_file_pos = os.getcwd()
        return [files for files in os.listdir(comp_file_pos) if files.startswith(text)] # This just gets tab shortcut working to finish the word for python


    def do_python3(self, args):
        if len(args) == 0: # This command allows me to run the python3 interpreter within my shell
            p = subprocess.Popen("python3")
        else:
            command_line = args.split()
            if len(command_line) == 1:
                p = subprocess.Popen(["python3", args])
            else:
                p = subprocess.Popen(["python3", command_line[0], command_line[1]])
        p.wait() 


    def do_python(self, args):
        if len(args) == 0: # This command allows me to run the python2 interpreter within my shell
            p = subprocess.Popen("python2")
        else:
            command_line = args.split()
            if len(command_line) == 1:
                p = subprocess.Popen(["python2", args])
            else:
                p = subprocess.Popen(["python2", command_line[0], command_line[1]])
        p.wait()


    def do_javac(self, args):
        if len(args) == 0: # This command allows me to run the java compiler within my shell
            print("Enter file.")
        else:
            p = subprocess.Popen(["javac", args])
        p.wait()


    def do_java(self, args):
        if len(args) == 0: # This command allows me to run java programs within my shell
            print("Enter File.")
        else:
            p = subprocess.Popen(["java", args])
        p.wait()

    def do_more(self, args):
        if args == "more": # This command allows me to view text files within my shell and print them out on screen
            args = sys.argv[1]
        try:
            with open(args, "r") as f:
                file = f.readlines()

            count = 0
            i = 0
            while i < len(file): # This loop is used so it prints 20 lines at a time, to print the next 20, you have to hit space and then enter.
                if count == 20:
                    count = 0
                    inp = input()
                    while inp != " ":
                        inp = input()
                print(file[i].strip("\n"))
                count += 1
                i += 1
            f.close()

        except FileNotFoundError:
            print("Enter valid File.")


    def postcmd(self, stop, line):
        sys.stdout = sys.__stdout__ # This resets standard output to the screen as this is needed as I changed standard output to get output redirection to a file working.
        global bold
        global colour
        global ENDC # These global variables are used to make the colour of the prompt consistent and to display the current pathname as the command line prompt.
        self.prompt = ":{:}{:}~{:}/myshell{:}$ ".format(bold, colour, file_pos, ENDC) # This is how I keep the command line prompt up to date with what directory I am in



    def precmd(self, line):
        arg = line.split() # I use precmd to do my output redirection

        redir = [">", ">>"]
        writing, appending = redir[0], redir[1]

        cmd_redir = ["help", "dir", "echo", "environ"] # List of commands redirection should work with
        indexredir = [i for i in range(len(arg)) if arg[i] in redir] # find index of redirection arrow

        try:
            if arg[0] in cmd_redir and len(indexredir): # if command in list and redirection arrow is present, continue
                
                if arg[indexredir[0]] == writing: # if only one arrow, create new file and write to that file
                    sys.stdout = open(arg[indexredir[0] + 1], "w+")
                    
                elif arg[indexredir[0]] == appending: # if two arrows, append to the name of the file given
                    sys.stdout = open(arg[indexredir[0] + 1], "a+")
                
                return " ".join(arg[:indexredir[0]] + arg[indexredir[0] + 2:]) # return line not including name of file and redirection arrow. This is to ensure echo works correctly as echo works different to every other command when doing output redirection

            else:
                return line # If not doing ouput redirection, just return line as normal

        except:
            return line # just return line as normal if try fails.


    def parseline(self, line):
        background = "&" # signifies a background process

        if not line:
            return None, None, line # if nothing is entered in the command line, just return the line.

        i, n = 0, len(line)
        while i < n and line[i] != " ": # This loop finds where the command is and where the argument is in the line.
            i += 1

        command, arg = line[:i], line[i:].strip() # splitting the line into the command and argument 

        function = command

        if len(line) > 0: # If something was entered
            if line[-1] == background: # If there is an ampersand at the end of the line
                if hasattr(self, "do_{:}".format(function)): # check if such a command exists.
                    try:
                        run = "do_{:}".format(function) # get that command ready to run in thread
                        getter = getattr(self, run) # get that command from myshell class
                        thread = threading.Thread(target = getter, args = (arg.strip(background), ), name = run) # create a thread with the funtion assigned as getter
                        thread.daemon = True # Daemonize thread
                        thread.start() # start thread

                    
                    except:
                        print("There has been an error")

                    return None, None,None # Return nothing as you just want to start the thread, this stops it from throwing an error.
                
                else:
                    return None, None, line # if the function does not exist within myshell class, just return the line
        
        return command, arg, line # These variables get passed to onecmd



    def emptyline(self):
        pass # This function ensures when enter key is pressed when no arguments are present it just returns the command line prompt instead of results from a command previously done.

    def do_batchfile(self, args): # This function is used if a file is passed as a command line argument.
        try:
            fileName = args
            with open(fileName, "r") as file:
                f = file.read().split("\n")

            i = 0
            while i < len(f):
                args = f[i]
                prompt.onecmd(args)
                #print("\n")
                i += 1

            file.close()
            self.do_quit("")

        except FileNotFoundError:
            print("Enter valid file.")


    def help_help(self): # This prints all help files at once.
        print("""\nQ1 Part(VI): 
|""")
        self.help_cd()
        self.help_clr()
        self.help_dir()
        self.help_environ()
        self.help_echo()
        self.help_pause()
        self.help_quit()
        self.help_pwd()
        self.help_batchfile()
        self.help_redirection()
        self.help_processes()
        self.help_python3()
        self.help_python()
        self.help_javac()
        self.help_java()
        self.help_more()


    def help_cd(self): # Helpfile on cd
        print("""\nQ1 part(I): 
|   This is my cd function, it is used to change the shell
|   working directory.
|   Command argument is cd
|   
|   "cd <filename>" :- This is used to change directory 
|                   If directory does not exist, you will
|                   receive an OSError.
|
|   "cd" :- The cd command on its own will print out the
|        full path to your current directory.
|   
|   "cd .." :- This is used to go back into directories 
|            you have already visited.""")    


    def help_clr(self): # helpfile on clr
        print("""\nQ1 part(II): 
|   This is used to clear the screen within the shell. """)


    def help_dir(self): # Helpfile on dir
        print("""\nQ1 part(III): 
|   Display directory stack.
|
|   dir <directory> - It displays a list of current directories 
|   within the directory directory specified.
|   
|   Enter "dir <directory> -a" to reveal hidden files along with 
|   ordinary files. """)


    def help_environ(self): # Helpfile on environ
        print("""\nQ1 Part(IV): 
|   Lists all the environment strings. """)
    


    def help_echo(self): # Helpfile on echo
        print("""\nQ1 part(V):
|   The echo function writes arguments you put after the
|   echo command, e.g. echo <argument>, to standard output. 
|
|   The arguments are seperated by a single whitespace, 
|   unless otherwise stated by quotation marks followed
|   by a newline character. """)


    def help_pause(self): # Helpfile on pause
        print("""\nQ1 part(VII): 
|   The pause command is able to pause the shell until the
|   enter key is hit. """)

    
    def help_quit(self): # Helpfile on quit
        print("""\nQ1 Part(VIII)
|  The command "quit" Quits the program """)


    def help_pwd(self): # Helpfile on pwd
        print("""\nQ1 Part(I)
|   Displays the current full path of the directory you are 
|   in.""") 


    def help_python3(self): # Helpfile on python3
        print("""\nPython3 Interpreter
|   The command "python3" runs the python3 interpreter.
|
|   "python3 <file.py>" executes the py file in python3. """) 


    def help_python(self): # Helpfile on python2
        print("""\nPython2 Interpreter
|   The command "python" runs the python2 interpreter.
|
|   "python <file.py>" executes the py file in python2 """)


    def help_javac(self): # Helpfile on the java compiler
        print("""\nJava Compiler
|  The command "javac" compiles java programs. """)



    def help_java(self): # Helpfile on running java programs
        print("""\nJava
|  The command "java" runs java programs.""")


    def help_redirection(self): # Helpfile on output redirection
        print("""\nQ4, Output Redirection
|   This shell supports output redirection. It works with the commands
|   help, echo, environ and dir. With the symbol ">", this will create 
|   the file if not already created and write the output to that file. 
|   The symbol ">>" will append the output to a file, it will not 
|   overwrite whats already in the file. To use it correctly, you use 
|   it as the following.
|
|   "<command> > outputFile" - this creates a file if it does not 
|   already exist and writes the output to that file.      
|   
|   "<command> >> outputfile" - this appends the output from the command 
|   to the file. It does not overwrite what is already in the file like 
|   what the example above does.
|
|   "echo > outputFile <String>" - You use this when executing the echo command
|   with output redirection. 
|
|   "echo >> outputFile <String>" - Same as before but only if you want to append
|   it to a file.""")


    def help_more(self): # Helpfile on view
        print("""\nView Contents of the readme 
|   This command is used if you want to view contents of the readme manual. 
|   and other files if needed. How it can be used is with the following 
|   format:
|
|   more <filename> - this will open the file and print it on screen 20
|   lines at a time. To display the next 20 lines, you have to hit the spacebar
|   and then the enter key.""")

    def help_batchfile(self):
        print("""\nQ3 Taking input from a file 
|   This is to run commands from a file when executing myshell, to do this
|   it is with the following format:
|
|   python3 myshell.py <FileName> - This will execute the programs within
|   the file and then quit the shell.""")

    def help_processes(self):
        print("""\nQ5
|   Add an ampersand - ("&")  to the end of a command to run it in the background.
|   An example is like the following:
|
|   "python3 test.py&" - this will run the python test file in the background.
|  
|   There cannot be a space between the end of the command and the ampersand
|   otherwise it will not work and also, background processes only works for
|   commands that are defined within the shell.""")


if __name__ == "__main__":
    file_pos = os.getcwd() # This is where I originally state all my global variables
    colour = "\033[92m"
    ENDC = "\033[0m"
    bold = "\033[1m"
    prompt = MyShell()
    prompt.prompt = ":{:}{:}~{:}/myshell{:}$ ".format(bold, colour, file_pos, ENDC) # This is my command line prompt
    arg = sys.argv # This is the beginning of how I run a file of commands from the command line
    if len(arg) == 1: # If there is no batchfile, enter the shell
        prompt.cmdloop("Starting prompt...")
    else: # if there is a batchfile, execute it.
        prompt.do_batchfile(arg[1])

