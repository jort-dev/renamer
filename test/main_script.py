filename = "dynamic_script.py"
with open(filename, 'r') as file:
    code = file.read()

print(code)
result = eval(code)
print(result)
