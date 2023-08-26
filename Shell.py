from _interpreter import *
print('To execute script: write filename with no "')
print('To execute line: write line"')
print('To exit: write end"')

user_input = None
f = open("ExecutionFile.flux","w")
f.close()
while user_input != "END":
    user_input = input("Shell> ")
    if user_input[0:3]=="RUN":
        filename = user_input[4:]
        INT = Interpreter(filename)
        INT.RUN( )
    else:
        f = open("ExecutionFile.flux","a")
        f.writelines(user_input+"\n")
        f.close()

        f = open("ExecutionFile.flux","r")
        INT = Interpreter("ExecutionFile.flux")
        INT.RUN()
        f.close()

f = open("ExecutionFile.flux","w")
f.close()