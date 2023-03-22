# i want to compile the program but still let the user use a fully fledged python script
# cant just load it each time, needs to stay in memory for variables to work
filename = "dynamic_script.py"
with open(filename, 'r') as file:
    code = file.read()

print(code)
result = eval(code)
print(result)
