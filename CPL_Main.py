import os
import sys
import time
import random
import datetime
import math
import threading
import IDE_2 as IDE
import subprocess
if os.name != "nt":
    import pwd
else:
    pass
import warnings
import textwrap

try:
    from tkinter import *
except:
    print("Graphics library could not be imported,  graphics features cannot be used.")

global file_lines_list
global variables
global functions
global running
global repeat_count
global repeat_count_import
global import_run
global button_command

interpreter = False

calcmem = {}

#math syntax extension for CPL (msyx)

def msyx(com):
    com_spl = com.split(" ")

    try:
                    if com_spl[0] == "add":
                        return float(com_spl[1]) + float(com_spl[2])
                    elif com_spl[0] == "sub":
                        return float(com_spl[1]) - float(com_spl[2])
                    elif com_spl[0] == "mul":
                        return float(com_spl[1]) * float(com_spl[2])
                    elif com_spl[0] == "div":
                        return float(com_spl[1]) / float(com_spl[2])
                    elif com_spl[0] == "sin":
                        return math.sin(float(com_spl[1]))
                    elif com_spl[0] == "cos":
                        return math.cos(float(com_spl[1]))
                    elif com_spl[0] == "tan":
                        return math.tan(float(com_spl[1]))
                    elif com_spl[0] == "sinh":
                        return math.sinh(float(com_spl[1]))
                    elif com_spl[0] == "cosh":
                        return math.cosh(float(com_spl[1]))
                    elif com_spl[0] == "tanh":
                        return math.tanh(float(com_spl[1]))
                    elif com_spl[0] == "asin":
                        return math.asin(float(com_spl[1]))
                    elif com_spl[0] == "acos":
                        return math.acos(float(com_spl[1]))
                    elif com_spl[0] == "atan":
                        return math.atan(float(com_spl[1]))
                    elif com_spl[0] == "asinh":
                        return math.asinh(float(com_spl[1]))
                    elif com_spl[0] == "acosh":
                        return math.acosh(float(com_spl[1]))
                    elif com_spl[0] == "atanh":
                        return math.atanh(float(com_spl[1]))
                    elif com_spl[0] == "mdefl": #loud memory address definition (returns memory address name)
                        calcmem[com_spl[1]] = 0.0
                        return f"Memory address created ({com_spl[1]})"
                    elif com_spl[0] == "mdefs": #silent memory address definition
                        calcmen[com_spl[1]] = 0.0
                        return "NIL_CPL_ENC"
                    elif com_spl[0] == "msavl": #loud save
                        calcmem[com_spl[1]] = msyx(' '.join(com_spl[2:]))
                        return f"Value {calcmem[com_spl[1]]} saved to memory address ({com_spl[1]})"
                    elif com_spl[0] == "msavs": #silent save
                        calcmem[com_spl[1]] = msyx(' '.join(com_spl[2:]))
                        return "NIL_CPL_ENC"
                    elif com_spl[0] == "mret":
                        return calcmem[com_spl[1]]
    except:
        print("Math Domain Error")
            
    return "NIL_CPL_ENC"

"""
ERROR DICTIONARY

"ERROR 0x" - String Error
"ERROR 1x" - Integer Error
"ERROR 2x" - Boolean Error
"ERROR 3x" - Date-Based Error
"ERROR 4x" - Time-Based Error
"ERROR 5x" - Variable-Based Error
"ERROR 6x" - Math-Based Error
"ERROR 7x" - Random-Based Error
"ERROR 8x" - File-Based Error
"ERROR 9x" - If-Statement-Based Error
"""

#NIL_CPL_ENC (Null CPL Encoded) is the token that makes it so a command doesn't return anything
#RTC means "Run Terminal Command"
#RPC means "Run Python Command"

running = True
file_lines_list = [] #this is the list of what commands are executed if a file is dragged and dropped onto the console
variables = {}
functions = {}
objects = {}

file_count = 0
repeat_count = 0
repeat_count_import = 0
import_run = False

os.system("title CPL v1.6")
def program_exit(exit_code):
    input("Program Ended With Exit Code: " + exit_code)
    sys.exit()
    
def run_input():
    inp = input()
    return inp

def run_input_args(args):
    inp = input(args)
    return inp

def open_win(width, height):
    window = Tk()
    window.geometry(f"{width}x{height}")
    window.mainloop()
    return window


def execute_command(command):
    command = command.strip() #removes any excess blank space
    cmdlist = command.split(" ") #splits all words in a command into a list

    for i in range(len(cmdlist)): 
        if cmdlist[i] in variables:
            cmdlist[i] = str(variables[cmdlist[i]])

        if cmdlist[i] == "object":
            if cmdlist[i+1] == "new":
                pass
            if cmdlist[i+1] == "create":
                if cmdlist[i+2] == "list":
                    objects[cmdlist[i+3]] = []
                elif cmdlist[i+2] == "file":
                    global file
                    global file_count
                    
                    file_name = ' '.join(cmdlist[i+3:])
                    file = open(str(file_name), 'r')
                    file_count += 1
                    objects[' '.join(cmdlist[i+3:])] = str(file.read())
                    
            elif cmdlist[i+1] == "remove":
                del objects[cmdlist[i+2]]
                
            elif cmdlist[i+1] == "modify":
                if cmdlist[i+2] == "list":
                    if cmdlist[i+4] == "append":
                        objects[cmdlist[i+3]].append(str(' '.join(cmdlist[i+5:])))
                    elif cmdlist[i+4] == "remove":
                        objects[cmdlist[i+3]].remove(str(' '.join(cmdlist[i+5:])))
                else:
                    pass
            elif cmdlist[i+1] == "return":
                if cmdlist[i+2] == "list":
                    pos_to_return = cmdlist[i+4]
                    return objects[cmdlist[i+3]][int(cmdlist[i+4])]
                if cmdlist[i+2] == "file":
                    return objects[' '.join(cmdlist[i+3:])]
                else:
                    pass
            return "NIL_CPL_ENC"

        
        if cmdlist[i] == "display_objects":
            return objects
        
        if cmdlist[i] == "import":
            import_list = []
            with open(str(cmdlist[i+1]), 'r') as file:
                for a in file:               
                    import_list.append(a.replace("\n", ""))
        
            repeat_count_import = len(import_list)

            for imp in range(len(import_list)):
                repeat_count_import -= 1
                return_val_imp = execute_command(import_list[imp])

                if return_val_imp == "NIL_CPL_ENC":
                    pass
                elif return_val_imp == "ERROR 5x3 - Invalid Type For A Variable":
                    pass
                else:
                    print(return_val_imp)
                

            import_run = True
            return "NIL_CPL_ENC"
        if cmdlist[i] == "run":
            if cmdlist[i+1] in functions:
                cmd_split = functions[cmdlist[i+1]].split(';')
    
                for j in range(len(cmd_split)):
                    return_val = execute_command(cmd_split[j])
                    
                    if return_val == "NIL_CPL_ENC":
                        pass
                    elif return_val == "ERROR 5x3 - Invalid Type For A Variable":
                        pass
                    else:
                        print(return_val)

            return "NIL_CPL_ENC"
        
        if cmdlist[i] == "function":
            if cmdlist[i+1] == "remove":
                function_to_remove = cmdlist[i+2]

                del functions[function_to_remove]
                return "NIL_CPL_ENC"
            
            if cmdlist[i+1] == "define":
                func_name = cmdlist[i+2]
                command_to_run = cmdlist[i+3:]

                functions[func_name] = str(' '.join(command_to_run))
                return "NIL_CPL_ENC"
            else:
                return "NIL_CPL_ENC"

        if cmdlist[i] == "remove_all_functions":
            for i in range(len(functions)):
                del functions[i]

            return "NIL_CPL_ENC"
        
        if cmdlist[i] == "set":
            try:
                var_name = cmdlist[i+1]
                var_type = cmdlist[i+2]
                var_contents = ' '.join(cmdlist[i+3:])
                
                if var_type == 'num':
                    variables[var_name] = float(var_contents)
                    return "NIL_CPL_ENC"
                if var_type == 'str':
                    variables[var_name] = str(var_contents)
                    return "NIL_CPL_ENC"
                if var_type == 'cmd':
                    variables[var_name] = str(execute_command(var_contents))
                    var_contents = variables[var_name]
                    print("DEPRACATION WARNING: Default cmd argument is deprecated,  please use the new cmd-str or cmd-float arguments for your variables")
                    return "NIL_CPL_ENC"
                if var_type == 'cmd-float':
                    variables[var_name] = str(execute_command(var_contents))
                    var_contents = float(variables[var_name])
                    return "NIL_CPL_ENC"
                if var_type == 'cmd-str':
                    variables[var_name] = str(execute_command(var_contents))
                    var_contents = str(variables[var_name])
                    return "NIL_CPL_ENC"   
                else:
                    return "ERROR 5x3 - Invalid Type For A Variable"
            
            except ValueError:
                try:
                    var_name = cmdlist[i+1]
                    var_value = cmdlist[i+2]
                    variables[var_name] = var_value
                    return ""
                except IndexError:
                    return "ERROR 5x1 - Missing value for variable assignment"

        if cmdlist[i] == "var_modify":
            var_to_append = cmdlist[i+1]
            amount_to_set = cmdlist[i+2]

            if var_to_append in variables:
                variables[f"{var_to_append}"] = amount_to_set
                return ""
            else:
                return "ERROR 5x2 - Variable Not Found"

        if cmdlist[i] == "if":
            type_of_variable = cmdlist[i+1]
            variable = cmdlist[i+2]
            operand = cmdlist[i+3]
            value_to_check = cmdlist[i+4]
            command_to_execute = ' '.join(cmdlist[i+5:])

            if variable in variables and type_of_variable == "num":
                if operand == "=":
                    if float(variables[variable]) == float(value_to_check):
                        return str(execute_command(command_to_execute))
                    else:
                        pass
                    pass
                elif operand == "!=":
                    if float(variables[variable]) != float(value_to_check):
                        return str(execute_command(command_to_execute))
                    else:
                        pass
                    pass
                elif operand == ">":
                    if float(variables[variable]) > float(value_to_check):
                        return str(execute_command(command_to_execute))
                    else:
                        pass
                    pass
                elif operand == "<":
                    if float(variables[variable]) < float(value_to_check):
                        return str(execute_command(command_to_execute))
                    else:
                        pass
                    pass
                elif operand == ">=":
                    if float(variables[variable]) >= float(value_to_check):
                        return str(execute_command(command_to_execute))
                    else:
                        pass
                    pass
                elif operand == "<=":
                    if float(variables[variable]) <= float(value_to_check):
                        return str(execute_command(command_to_execute))
                    else:
                        pass
                    pass
                else:
                    return "ERROR 9x1 - Invalid operand or variable type for the If statement"          
            elif variable in variables and type_of_variable == "str":
                if operand == "=":
                    if str(variables[variable]) == str(value_to_check):
                        print(execute_command(command_to_execute))
                    else:
                        pass
                    pass
                if operand == "!=":
                    if str(variables[variable]) == str(value_to_check):
                        print(execute_command(command_to_execute))
                    else:
                        pass
                    pass
                
                pass

            pass
            return "NIL_CPL_ENC"

        if cmdlist[i] == "remove_all_variables":
            for i in range(len(variables)):
                del variables[i]
            
            return "NIL_CPL_ENC"

        if cmdlist[i] == "remove_variable":
            var_to_remove = cmdlist[i+1]

            try:
                del variables[var_to_remove]
                return "NIL_CPL_ENC"
            except:
                return "ERROR 5x4 - Variable doesn't exist"

            return "NIL_CPL_ENC"
        
        if cmdlist[i] == "RTC":
            command_to_run = ' '.join(cmdlist[i+1:])
            os.system(command_to_run)

            return "NIL_CPL_ENC"

        if cmdlist[i] == "RPC":
            command_to_run = ' '.join(cmdlist[i+1:])
            exec(command_to_run)

            return "NIL_CPL_ENC"
        if cmdlist[i] == "for":
            global anything_after
            
            repeat_count = cmdlist[i+1]
            action = cmdlist[i+2]
            anything_after = ' '.join(cmdlist[i+3:])

            try:
                repeat_count = float(repeat_count)
            except:
                return "ERROR 1x1 - Invalid repeat count"
            
            if action == "execute":
                repeat_count -= 1
                print(execute_command(anything_after))
            elif action == "print":
                return str(anything_after * repeat_count)
            else:
                return "ERROR 0x1 - Invalid paramaters for the ""\"for""\" command"

        if cmdlist[i] == "until_break":
            command_to_exec = ' '.join(cmdlist[i+1:])
            
            try:
                while True:
                    executed_command = execute_command(command_to_exec)
                    if executed_command == "NIL_CPL_ENC":
                        pass
                    else:
                        print(executed_command)
            except KeyboardInterrupt:
                return "NIL_CPL_ENC"
            
            return "NIL_CPL_ENC"
        if cmdlist[i] == "show_vars":
            return variables
        

        if cmdlist[i] == "//":
            return "NIL_CPL_ENC"

        if cmdlist[i] == "win":
             thread = threading.Thread(target=open_win, args=(int(cmdlist[i+1]), (cmdlist[i+2])))
             thread.start()
             return "NIL_CPL_ENC"
        
        if cmdlist[i] == "win_label":
            label_text = cmdlist[i+1:]
            
            label = Label(text=label_text)
            label.pack()
            return "NIL_CPL_ENC"
        
        if cmdlist[i] == "win_button_test":
            button_text = "testing"
            button = Button(text=button_text,  command=execute_command("wtln \"hi\""))
            button.pack()
            return "NIL_CPL_ENC"
        
        if cmdlist[i] == "win_textbox_test":
            textbox = Text()
            textbox.pack()
            return "NIL_CPL_ENC"
        
        if cmdlist[i] == "wtln":
            wtln_r = ' '.join(cmdlist[i+1:])
            if "\"" in wtln_r:
                wtln_r = wtln_r.replace("\"", "")
                return wtln_r
            else:
                if wtln_r in variables:
                    return variables[wtln_r]
                else:
                    return f"ERROR 5x2 - Variable Not Found"


        if cmdlist[i] == "sleep":
            try:
                sleep_r = float(cmdlist[i+1])
                time.sleep(sleep_r)
                return "NIL_CPL_ENC"
            except ValueError:
                return "ERROR 4x1 - Invalid range for the sleep function"
            
            return "NIL_CPL_ENC"

        if cmdlist[i] == "pause":
            if os.name == 'nt':
                os.system("pause>nul")
            else:
                os.system("read")
            
            return "NIL_CPL_ENC"
        
        if cmdlist[i] == "evaluate":
            line_to_eval = ' '.join(cmdlist[i+1:])

            for var in variables:
                line_to_eval = line_to_eval.replace(var, str(variables[var]))

            evaluated = eval(f"{line_to_eval}")
            return evaluated


        if cmdlist[i] == "file_read":
            try:
                with open(cmdlist[i+1].replace("\"", ""), 'r') as file:
                    return file.read()
            except FileNotFoundError:
                return "ERROR 8x1 - File not found"
                                            
        if cmdlist[i] == "help":
            return textwrap.dedent(r"""
            Available commands:

            STRING BASED:
            - wtln "text" or wtln (variable): Prints text
            - concat "string1" "string2" ... : Concatenates strings
            - reverse "text" : Reverses a string
            - upper "text" : Converts text to uppercase
            - lower "text" : Converts text to lowercase
            - length "text" : Gets the length of a string
            - contains (var or str) "string" "substring" : Checks if a string contains a specified substring.  Example: contains str HelloWorld Hello (returns True). Example 2: contains var x y (returns True or False depending on if the string contains the substring).
            - datetime : Returns the current date
            - time : Returns the current time
            - repeat : Returns text repeated multiple times in one string.  Example: repeat 3 CPL (returns "CPLCPLCPL")
            - isPalindrome : Checks if the string inputted is a palindrome.  Example: isPalindrome racecar (returns True).

            VARIABLE BASED:
            - set (var_name) (var_type) (value) : Defines a new variable.  The 3 possible types of variables are: num, str, and cmd.  Example: set x num 5
            - var_modify (variable) (value) : Modifies the value of a variable
            - show_vars : Displays all variables
            - remove_variable (variable) : Removes a variable from the current instance of CPL
            - remove_all_variables : Removes all variables from the current instance of CPL

            CONDITION BASED:
            - if (variable type) (variable) (operand) (value) (command to execute if true) : Executes a command based off specific conditions.  Example: if num x = 5 wtln "X is equal to 5" (returns X is equal to 5).  Example 2: if str y = Hello! wtln x (returns 5 if y is already defined as "Hello!")
            - until_break (command) : Runs the inputted command until the user manually pressed Ctrl-C to break out of the loop
            - for (amount) (action type) (command or text) : Runs any command or prints out text after the action type (execute or print)

            FUNCTION BASED:
            - function (define or remove) (function name) (command to execute) : Command to define functions in a program.  Example: function define func wtln "Hello!"; pause (returns Hello! and pauses the program if run using "run func").  Example 2: function remove func (removes the function func)            
            - remove_all_functions : Removes all functions in the current instance of CPL

            MATH BASED:
            - evaluate (expression) : Evaluates an expression
            - factorial (condition) (num or var) : Calculates the factorial of the given number
            - power (condition) (base) (exponet) : Calculates the power of a number.  Conditions: num, var
            - sqrt (condition) (num or var) : Calculates the square root of a given number.  Conditions: num, var
            - abs (condition) (num or var) : Calculates the absolute value of a given number.  Conditions: num, var
            - neg (condition) (num or var) : Turns a positive number into a negative number.  Conditions: num, var
            - round (condition) (num or var) : Rounds a given number to the nearest integer.  Conditions: num, var
            - ceil (condition) (num or var) : Rounds a number up to the nearest integer.  Conditions: num, var
            - floor (condition) (num or var) : Rounds a number down to the nearest integer.  Conditions: num, var
            - gcd (condition) (num or var 1) (num or var 2) : Finds the greatest common denominator of 2 given numbers.  Conditions: num, var
            - lcm (condition) (num or var 1) (num or var 2) : Finds the least common multiple of 2 given numbers.  Conditions: num, var
            - is_prime (condition) (value) : Checks whether the given number is prime.  Conditions: num, var
            - is_even (condition) (value) : Checks if a given number is even based off the conditions given.  Conditions: num, var
            - is_odd (condition) (value) : Checks if a given number is odd based off the conditions given.  Conditions: num, var
            - sin (condition) (value) : Sine calculation.  Conditions: num, var
            - cos (condition) (value) : Cosine calculation.  Conditions: num, var
            - tan (condition) (value) : Tangent calculation.  Conditions: num, var
            - asin (condition) (value) : Arcsine calculation.  Conditions: num, var
            - acos (condition) (value) : Arccosine calculation.  Conditions: num, var
            - atan (condition) (value) : Arctangent calculation.  Conditions: num, var
            - sinh (condition) (value) : Hyperbolic sine calculation.  Conditions: num, var
            - cosh (condition) (value) : Hyperbolic cosine calculation.  Conditions: num, var
            - tanh (condition) (value) : Hyperbolic tangent calculation.  Conditions: num, var
            - asinh (condition) (value) : Inverse hyperbolic tangent calculation.  Conditions: num, var
            - acosh (condition) (value) : Inverse hyperbolic cosine calculation.  Conditions: num, var
            - log (condition) (value) : Logarithmic calculation.  Conditions: num, var
            - log10 (condition) (value) : Logarithmic(10) calculation.  Conditions: num, var
            - log2 (condition) (value) : Logarithmic(2) calculation.  Conditions: num, var
            - atanh (condition) (value) : Inverse hyperbolic tangent calculation.  Conditions: num, var

            GRAPHICS (currently only in testing):
            - win_test : Opens a test window
            - win_label (text) : Places a label with certain text on it.  Example: win_label Hello!
            - win_button_test : Places a test button in the defined window
            - win_textbox_test : Places a textbox in the defined window
            NOTE: THESE ARE STILL ONLY IN TESTING PHASE,  THEY CANNOT BE USED FOR ANYTHING AT THE MOMENT.

            TERMINAL-BASED COMMANDS:
            - RTC (command) : Runs a terminal command
            - list_dir : Runs the terminal command for reading the directory inputted in the command.  Example: list_dir C:\Windows\System32 (Windows).  list_dir /usr/lib/ (Linux).
            - get_os : Returns the type of operating system the user is running on
            - get_user : Returns the current user running the instance of CPL
            - uptime : Returns the uptime of the system (Linux), Returns the date and time the system was turned on (Windows).

            MISC:
            - RPC (command) : Runs a python command
            - import (file_to_import) : Imports an external file's variables,  functions,  and commands to be used in the program
            - inp : Creates an input box for the user to enter something and returns the input that was inputted into the box
            - jump (line) : Jumps to a line in the program and starts executing commands line by line from that line
            - exec_line (line) : Executes a certain line of code in a program
            - confirm (value) : a Yes/No input box.  If the input returned is "y" or "yes",  it returns True,  otherwise it returns false.  Example: confirm "Do you want to continue?: " (returns true if y or yes is inputted into the box)
            - random (condition) (min) (max) : Generates a random number between the minimum value provided and the maximum value provided.  Conditions: num, var
            - clear : Clears the console screen
            - sleep (seconds) : Pauses the execution for a specified number of seconds
            - help : Displays this help message
            - error_dictionary : Displayes the legend for errors
            - // (text) - Comment
            - object_documentation : Displays the documentation for the object command
            - version : Displays the version
            - IDE : Opens the CPL IDE
            - exit : Exits the program
            """)

            
        if cmdlist[i] == "reverse":
            text = cmdlist[i+1].replace("\"", "")
            text_mod = text[::-1]
            return text_mod


        if cmdlist[i] == "upper":
            text = cmdlist[i+1].replace("\"", "")
            text_mod = text.upper()
            return text_mod


        if cmdlist[i] == "lower":
            text = cmdlist[i+1].replace("\"", "")
            text_mod = text.lower()
            return text_mod
        

        if cmdlist[i] == "length":
            text = cmdlist[i+1].replace("\"", "")
            text_mod = len(text)
            return text_mod
        

        if cmdlist[i] == "clear":
            if os.name == "nt":
                os.system('cls')
                return "NIL_CPL_ENC"
            else:
                os.system("clear")
                return "NIL_CPL_ENC"

            return "NIL_CPL_ENC" 

        if cmdlist[i] == "concat":
            if "\"" in " ".join(cmdlist[i+1:]):
                result = "".join(cmdlist[i+1:])
                result = result.replace("\"", "")
                return result
            
            else:
                result = "".join(cmdlist[i+1:])
                
                for var in variables:
                    result = result.replace(var, str(variables[var]))

                return result
            
            return result

        if cmdlist[i] == "inp":
            out = run_input()
            return out
        
        if cmdlist[i] == "datetime":
            datetime_str = datetime.datetime.now().strftime("%m-%d-%Y")
            return datetime_str

        if cmdlist[i] == "time":
            time_str = datetime.datetime.now().strftime("%H:%M:%S")
            return time_str
        
        if cmdlist[i] == "is_prime":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    if num <= 1:
                        return "False"
                    else:
                        for i in range(2, int(num ** 0.5) + 1):
                            if num % i == 0:
                                return "False"
                                break
                        else:
                            return "True"
                elif cmdlist[i+1] == "var":
                    num = str(cmdlist[i+2])

                    for var in variables:
                        num = num.replace(var,  str(variables[var]))

                    num = float(num)
                    
                    if num <= 1:
                        return "False"
                    else:
                        for i in range(2, int(num ** 0.5) + 1):
                            if num % i == 0:
                                return "False"
                                break
                        else:
                            return "True"
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x2 - Invalid number for primality test"


        if cmdlist[i] == "factorial":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    result = 1
                    for num_range in range(1, num + 1):
                        result *= num_range
                    return result
                elif cmdlist[i+1] == "var":
                    num = str(cmdlist[i+2])

                    for var in variables:
                        num = num.replace(var,  str(variables[var]))
                    
                    num = float(num)
                    result = 1
                    
                    for num_range in range(1, num + 1):
                        result *= num_range
                        
                    return result
            except ValueError:
                return "ERROR 6x4 - Invalid number for factorial calculation"


        if cmdlist[i] == "sqrt":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    if num < 0:
                        return "ERROR 6x5 - Cannot calculate the square root of a negative number"
                    else:
                        result = num ** 0.5
                        return result
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]
                    
                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    if num < 0:
                        return "ERROR 6x5 - Cannot calculate the square root of a negative number"
                    else:
                        result = num ** 0.5
                        return result
                else:
                    return "NIL_CPL_ENC"
            except ValueError:
                return "ERROR 6x10 - Invalid number for square root calculation"
            
        if cmdlist[i] == "abs":
            val_to_check = cmdlist[i+2]

            try:
                if cmdlist[i+1] == "var":
                    for var in variables:
                         val_to_check = val_to_check.replace(var, str(variables[var]))
                    
                    val_to_check = int(val_to_check)
                    
                    val = abs(val_to_check)
                    return val
                
                elif cmdlist[i+1] == "num":
                    val_to_check = cmdlist[i+2]
                    val_to_check = int(val_to_check)
                    
                    val = abs(val_to_check)
                    return val
                else:
                    return "NIL_CPL_ENC"
            except ValueError:
                return "ERROR 6x11 - Invalid value for the abs function"
            
            return "NIL_CPL_ENC"
        
        if cmdlist[i] == "neg":
            val_to_check = cmdlist[i+2]

            try:
                if cmdlist[i+1] == "var":
                    for var in variables:
                        val_to_check = val_to_check.replace(var, str(variables[var]))

                    val_to_check = int(val_to_check)
                    
                    neg_val = -value_to_check
                    return neg_val
                if cmdlist[i+1] == "num":
                    val_to_check = int(val_to_check)
                    
                    neg_val = -value_to_check
                    return neg_val
            except ValueError:
                return "ERROR 6x12 - Invalid value for the neg function"
            
            return "NIL_CPL_ENC"
        if cmdlist[i] == "sign":
            val_to_check = cmdlist[i+2]

            try:
                if cmdlist[i+1] == "var":
                    for var in variables:
                        val_to_check = val_to_check.replace(var, str(variables[var]))

                    val_to_check = int(val_to_check)

                    if val_to_check > 0:
                        return 1
                    elif val_to_check < 0:
                        return -1
                    elif val_to_check == 0:
                        return 0

                elif cmdlist[i+1] == "num":
                    val_to_check = int(val_to_check)

                    if val_to_check > 0:
                        return 1
                    elif val_to_check < 0:
                        return -1
                    elif val_to_check == 0:
                        return 0
            except ValueError:
                return "ERROR 6x13 - Invalid value for the sign function"

            return "NIL_CPL_ENC"


        if cmdlist[i] == "round":
            val_to_check = cmdlist[i+2]

            try:
                if cmdlist[i+1] == "var":
                    for var in variables:
                        val_to_check = val_to_check.replace(var, str(variables[var]))

                    val_to_check = float(val_to_check)

                    rounded = round(val_to_check)
                    return rounded

                elif cmdlist[i+1] == "num":
                    val_to_check = int(val_to_check)

                    rounded = round(val_to_check)
                    return rounded
            except ValueError:
                return "ERROR 6x14 - Invalid value for the round function"
            
            return "NIL_CPL_ENC"

        if cmdlist[i] == "ceil":
            val_to_check = cmdlist[i+2]

            try:
                if cmdlist[i+1] == "var":
                    for var in variables:
                        val_to_check = val_to_check.replace(var, str(variables[var]))

                    val_to_check = float(val_to_check)

                    final_val = math.ceil(val_to_check)
                    return final_val
                elif cmdlist[i+1] == "num":
                    val_to_check = float(val_to_check)

                    final_val = math.ceil(val_to_check)
                    return final_val
            except ValueError:
                return "ERROR 6x15 - Invalid value for the ceiling function"
            
            return "NIL_CPL_ENC"

        if cmdlist[i] == "floor":
            val_to_check = cmdlist[i+2]

            try:
                if cmdlist[i+1] == "var":
                    for var in variables:
                        val_to_check = val_to_check.replace(var, str(variables[var]))

                    val_to_check = float(val_to_check)

                    final_val = math.floor(val_to_check)
                    return final_val
                elif cmdlist[i+1] == "num":
                    val_to_check = float(val_to_check)

                    final_val = math.floor(val_to_check)
                    return final_val
            except ValueError:
                return "ERROR 6x18 - Invalid value for the floor function"
            
            return "NIL_CPL_ENC"
        
        if cmdlist[i] == "gcd":
            val_1 = cmdlist[i+2]
            val_2 = cmdlist[i+3]

            try:
                if cmdlist[i+1] == "var":
                    for var in variables:
                        val_1 = val_1.replace(var, str(variables[var]))
                        val_2 = val_2.replace(var, str(variables[var]))

                    val_1 = float(val_1)
                    val_2 = float(val_2)

                    final_val = math.gcd(val_1, val_2)
                    return final_val
                elif cmdlist[i+1] == "num":
                    val_1 = float(val_1)
                    val_2 = float(val_2)

                    final_val = math.gcd(val_1, val_2)
                    return val_3

                return "NIL_CPL_ENC"
            except ValueError:
                return "ERROR 6x17 - Invalid value for the gcd function"

        if cmdlist[i] == "lcm":
            try:
                val_1 = cmdlist[i+2]
                val_2 = cmdlist[i+3]

                if cmdlist[i+1] == "var":
                    for var in variables:
                        val_1 = val_1.replace(var, str(variables[var]))
                        val_2 = val_2.replace(var, str(variables[var]))

                    val_1 = float(val_1)
                    val_2 = float(val_2)
                    
                    final_val = math.lcm(val_1, val_2)
                    return final_val
                elif cmdlist[i+1] == "num":
                    val_1 = float(val_1)
                    val_2 = float(val_2)
                    
                    final_val = math.lcm(val_1, val_2)
                    return final_val
            except ValueError:
                return "ERROR 6x18 - Invalid value for the lcm function"
            
            return "NIL_CPL_ENC"
        
        if cmdlist[i] == "power":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    exponent = float(cmdlist[i+3])
                    result = num ** exponent
                    return result      
                elif cmdlist[i+1] == "var":
                    num = str(cmdlist[i+2])
                    exponet = str(cmdlist[i+3])
                        
                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                            
                    num = float(num)
                            
                    for var in variables:
                        exponet = exponet.replace(var, str(variables[var]))

                    exponet = float(exponet)

                    result = num ** exponet
                    return result
                else:
                    return "NIL_CPL_ENC"
            except Exception as e:
                return "ERROR 6x6 - Invalid number or exponent for power operation"


        if cmdlist[i] == "is_even":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    if num % 2 == 0:
                        return "True"
                    else:
                        return "False"
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)

                    if num % 2 == 0:
                        return "True"
                    else:
                        return "False"
                else:
                    return "NIL_CPL_ENC"
            except ValueError:
                return "ERROR 6x7 - Invalid number for even check"


        if cmdlist[i] == "is_odd":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    if num % 2 != 0:
                        return "True"
                    else:
                        return "False"
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)

                    if num % 2 != 0:
                        return "True"
                    else:
                        return "False"

                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x8 - Invalid number for odd check"
                
        if cmdlist[i] == "sin":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.sin(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                    return math.sin(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x9 - Invalid number for sine calculation"

        if cmdlist[i] == "cos":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.cos(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.cos(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x10 - Invalid number for cosine calculation"

        if cmdlist[i] == "tan":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.tan(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.tan(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x11 - Invalid number for tangent calculation"

        if cmdlist[i] == "asin":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.asin(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.asin(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x12 - Invalid number for Arcsine calculation"

        if cmdlist[i] == "acos":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.acos(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.acos(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x13 - Invalid number for Arccosine calculation"

        if cmdlist[i] == "atan":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.atan(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.atan(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x14 - Invalid number for Arctangent calculation"

        if cmdlist[i] == "sinh":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.sinh(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.sinh(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x15 - Invalid number for Hyperbolic Sine calculation"

        if cmdlist[i] == "cosh":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.cosh(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.cosh(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x16 - Invalid number for Hyperbolic Cosine calculation"

        if cmdlist[i] == "tanh":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.tanh(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.tanh(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x17 - Invalid number for Hyperbolic Tangent calculation"

        if cmdlist[i] == "asinh":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.asinh(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.asinh(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x18 - Invalid number for Inverse Hyperbolic Sine calculation"

        if cmdlist[i] == "acosh":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.acosh(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.acosh(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x19 - Invalid number for Inverse Hyperbolic Cosine calculation"

        if cmdlist[i] == "atanh":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.atanh(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.atanh(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x20 - Invalid number for Inverse Hyperbolic Tangent calculation"

        if cmdlist[i] == "log":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.log(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.log(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x21 - Invalid number for a Logarithmic calculation"

        if cmdlist[i] == "log10":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.log10(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.log10(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x21 - Invalid number for a Logarithmic calculation"

        if cmdlist[i] == "log2":
            try:
                if cmdlist[i+1] == "num":
                    num = float(cmdlist[i+2])
                    return math.log2(num)
                
                elif cmdlist[i+1] == "var":
                    num = cmdlist[i+2]

                    for var in variables:
                        num = num.replace(var, str(variables[var]))
                        num = float(num)
                        
                    return math.log2(float(num))
                else:
                    return "NIL_CPL_ENC"
                
            except ValueError:
                return "ERROR 6x21 - Invalid number for a Logarithmic calculation"
        
        if cmdlist[i] == "contains":
            type_of_str = cmdlist[i+1]
            string = cmdlist[i+2].replace("\"", "")
            substring = cmdlist[i+3].replace("\"", "")

            if type_of_str == "var":
                for var in variables:
                    string = string.replace(var,  str(variables[var]))
                    substring = substring.replace(var, str(variables[var]))
            elif type_of_str == "str":
                pass
            else:
                return "ERROR 0x2 - Invalid paramaters for the contains command"
            
            if substring in string:
                return "True"
            else:
                return "False"
        

        if cmdlist[i] == "random":
             try:
                 if cmdlist[i+1] == "num":
                    min_val = int(cmdlist[i+2])
                    max_val = int(cmdlist[i+3])
                    result = random.randint(min_val, max_val)
                    return result
                 elif cmdlist[i+1] == "var":
                    min_val = str(cmdlist[i+2])
                    max_val = str(cmdlist[i+3])

                    for var in variables:
                        min_val = min_val.replace(var, str(variables[var]))
                    min_val = int(min_val)

                    for var in variables:
                        max_val = max_val.replace(var, str(variables[var]))
                    max_val = int(max_val)
                    
                    result = random.randint(min_val, max_val)
                    return result
                
             except ValueError:
                return "ERROR 7x1: Invalid range for the random function"

        if cmdlist[i] == "isPalindrome":
            pal_check = ' '.join(cmdlist[i+1:])
            reversed_text = pal_check[::-1]
            
            if pal_check.lower() == reversed_text.lower():
                return True
            else:
                return False

        if cmdlist[i] == "repeat":
            amount_to_repeat = int(cmdlist[i+1])
            letters_to_repeat = ' '.join(cmdlist[i+2:])
            string_repeated = ""
            for i in range(amount_to_repeat):
                string_repeated = string_repeated + letters_to_repeat

            return string_repeated

        if cmdlist[i] == "list_dir":
            dir_to_check = ' '.join(cmdlist[i+1:])
            if os.name == 'nt':
                return os.system(f"dir \"{dir_to_check}\"")
            else:
                return os.system(f"ls \"{dir_to_check}\"")

        if cmdlist[i] == "get_os":
            return os.name

        if cmdlist[i] == "get_user":
            if os.name == "nt":
                return os.getlogin()
            else:
                return pwd.getpwuid(os.getuid()).pw_name

        if cmdlist[i] == "uptime":
            if os.name == "nt":
                return os.system("systeminfo | find \"System Boot Time\"")
            else:
                return os.system("uptime")

        if cmdlist[i] == "confirm":
            response = run_input_args(' '.join(cmdlist[i+1:]))
            if response.lower() == "y" or "yes":
                return True
            else:
                return False

        if cmdlist[i] == "jump":
            if interpreter == False:
                jump_arg = cmdlist[i+1]
                jump_arg = int(jump_arg)

                list_before_place_to_jump = []

                for lines in range(jump_arg-1, len(file_lines_list)):
                    list_before_place_to_jump.append(file_lines_list[lines])
                
                for a in range(len(list_before_place_to_jump)):
                    executed = execute_command(list_before_place_to_jump[a])
                    if executed != "NIL_CPL_ENC":
                        print(executed)
                    else:
                        pass

                return "NIL_CPL_ENC"
            else:
                return "ERROR 10x0 - Unable to run jump command in the interpreter"

        if cmdlist[i] == "exec_line":
            if interpreter == False:
                jump_arg = cmdlist[i+1]
                jump_arg = int(jump_arg)

                executed = execute_command(file_lines_list[jump_arg-1])
                
                if executed != "NIL_CPL_ENC":
                    print(executed)
                else:
                    pass

                return "NIL_CPL_ENC"
            else:
                return "ERROR 10x1 - Unable to run exec_line command in the interpreter"
        
        if cmdlist[i] == "error_dictionary":
            return """
                    ERROR DICTIONARY

                    "ERROR 0x" - String Error
                    "ERROR 1x" - Integer Error
                    "ERROR 2x" - Boolean Error
                    "ERROR 3x" - Date-Based Error
                    "ERROR 4x" - Time-Based Error
                    "ERROR 5x" - Variable-Based Error
                    "ERROR 6x" - Math-Based Error
                    "ERROR 7x" - Random-Based Error
                    "ERROR 8x" - File-Based Error
                    "ERROR 9x" - If-Statement-Based Error
                    "ERROR 10x" - Jump-Based Error
                    """
        
        if cmdlist[i] == "object_documentation":
            return """
EXAMPLE COMMAND:
(1) object create list List
(2) object remove List
(3) object modify list List append a
(4) object modify list List remove a
(5) object return list List 0

(1)
This command creates a list object called "List",  to simplify,  we will break it down word for word.

"object" is the command to start using objects
"create" is the keyword to create a new object
"list" is the type of object to create
"List" is the name of the object

(2)
This command removes an object called "List",  to simplify,  we will break it down word for word.

"object" is the command to start using objects
"remove" is the keyword to delete an object
"List" is the name of the object to delete

(3)
This command modifies the list List and adds an A to the list.  to simplify,  we will break it down word for word.

"object" is the command to start using objects
"modify" is the keyword to modify an object
"list" is the type of object to modify
"List" is the name of the object to modify
"append" is the command for lists to append something to its contents
"a" is the value to append the list by


(4)
This command modifies the list List and removes an A from the list.  to simplify,  we will break it down word for word.

"object" is the command to start using objects
"modify" is the keyword to modify an object
"list" is the type of object to modify
"List" is the name of the object to modify
"remove" is the command for lists to remove something from its contents
"a" is the value to remove from the list

(5)
This command modifies the list List and removes an A from the list.  to simplify,  we will break it down word for word.

"object" is the command to start using objects
"return" is the keyword to return one of the values of an object
"list" is the type of object to modify
"List" is the name of the object to modify
"0" is the position of the list to return
                      """
        if cmdlist[i] == "version":
            return "Casiero Programming Language (CPL) Version 1.6.  CHANGE LOG: Fixed bug where the cmd-str command only executed with cmd-string;  Fixed bug where when using quotes in the concat command it would not detect them and instead would try and print variables instead;  Fixed problem with new lines and white spaces in programs;  Fixed issue with win_label not adding anything after a space;  Added log, log10, log2 commands;  Added isPalindrome, repeat, list_dir, get_os, get_user, uptime, confirm, jump commands; "
            
        if cmdlist[i] == "exit":
            sys.exit()
        if cmdlist[i] == "IDE":
            IDE.ide()
        try: 
            while repeat_count != 0 and action == "execute":
                repeat_count -= 1
                print(execute_command(anything_after))
        except:
            pass
        
    try:
        if sys.argv[1] == "":
            return "NIL_CPL_ENC"
        else:
            pass
    except:
        return "NIL_CPL_ENC"

    return "NIL_CPL_ENC"
        
def cmdinp():
    cmd_inp = input(">>> ")
    try:
        cmd_inp_split = cmd_inp.split()
        if "set" in cmd_inp_split[0]:
            execute_command(cmd_inp)
        else:
            return_value = execute_command(cmd_inp)
            if return_value == "NIL_CPL_ENC":
                pass
            else:
                print(return_value)
    except IndexError:
        return


if __name__ == "__main__":
    try:
        args = sys.argv[1]
        running = False
        with open(args, 'r') as file:
            for a in file:
                file_lines_list.append(a.replace("\n", ""))
        if file_lines_list[0] != "#using msyx":
            for i in range(len(file_lines_list)):
                print(f"executing {file_lines_list[i]}")
                if file_lines_list[i] != '':
                    i_str = file_lines_list[i]
                    i_str_split = i_str.split()
                    
                    if "set" in i_str_split[0]:
                        execute_command(file_lines_list[i])
                    else:
                        
                        return_val = execute_command(file_lines_list[i])

                        if return_val == "NIL_CPL_ENC":
                            print("here")
                        else:
                            print(return_val)
                else:
                    pass
                
            program_exit("0x1") #CPL program end call
        
        else:
            for i in range(len(file_lines_list)):
                if file_lines_list[i] != '':
                    a = msyx(file_lines_list[i])
                    
                    if a == "NIL_CPL_ENC":
                        pass
                    else:
                        print(a)
                else:
                    pass
            program_exit("0x2") #msyx program end call

    except:
        if running == True:
            interpreter = True
            print("Casiero Programming Language v1.6")
            print("Type \"help\" to get a list of commands")
            print("Tyle \"version\" to get the version of CPL you are on and the change logs")

            cmdinp()
        
    while running == True:
        cmdinp()
else:
    pass
