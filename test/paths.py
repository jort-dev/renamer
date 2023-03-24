import os
path = os.getcwd()
base = os.path.basename(path)
x = path[:-len(base)]
print(x)