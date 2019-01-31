import numpy as np
import sys, re

def main(input):
     with open(input) as file:
         data = file.readlines()
         coeficients, constants = process_data(data)
         #result = np.linalg.solve(coeficients, constants)
         return 0

def process_data(data):
    coeficients = [[]]
    constants = []
    regex = re.compile(r"([a-z,A-Z]{1}[0-9]*)|([0-9]*[a-z,A-Z]{1})|(\+ *[0-9]*[a-z,A-Z]{1})|(\+ *[a-z,A-Z]{1}[0-9]*)|(\- *[0-9]*[a-z,A-Z]{1})|(\- *[a-z,A-Z]{1}[0-9]*)")
    for line in data:
        splitted = re.split("=", line)
        constants.append(splitted[1].strip())
        print(constants[0])
        match = regex.finditer(splitted[0])
        for group in match:
            print(group.group())
    return [], []


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Wrong number of arguments!")
    else:
        main(sys.argv[1])
