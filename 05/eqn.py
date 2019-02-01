#! /usr/bin/env python

import numpy as np
import sys, re

def main(input):
     with open(input) as file:
        data = file.readlines()
        coeficients, constants, letters = process_data(data)
        rank_coef = np.linalg.matrix_rank(coeficients)
        rank_aug = np.linalg.matrix_rank(np.column_stack((coeficients,constants)))
        if rank_coef != rank_aug:
            print("no solution")
        elif rank_coef != len(letters):
            print("solution space dimension: " + str(len(letters)-rank_coef))
        else:
            result = np.linalg.solve(coeficients, constants)
            output = "solution:"
            for i in range(len(letters)):
                output = output + " "  + str(letters[i]) + " = " + str(result[i]) + ","
            print(output[:-1])

def process_data(data):
    coeficients = []
    constants = []
    letters = []
    regex = re.compile(r"(\+ *[a-z,A-Z]{1}[0-9]*)|(\- *[a-z,A-Z]{1}[0-9]*)|(\- *[0-9]*[a-z,A-Z]{1})|([a-z,A-Z]{1}[0-9]*)|([0-9]*[a-z,A-Z]{1})|(\+ *[0-9]*[a-z,A-Z]{1})")
    regex_expr = re.compile(r"([a-z,A-Z]?)([0-9]*)([a-z,A-Z]?)")
    for line in data:
        splitted = re.split("=", line)
        constants.append(float(splitted[1].strip()))
        match = regex.finditer(splitted[0])
        dictionary = {}
        for group in match:
            sign = "+"
            expression = group.group()
            expression =  expression.replace(" ", "")
            if expression[0] == "-":
                sign = "-"
            match_expr = regex_expr.findall(expression)
            for prefix, number, suffix in match_expr:
                letter = prefix + suffix
                if letter not in letters and letter != '':
                    letters.append(letter)
                if number == '':
                    number = "1.0"
                number = sign + number
                if letter != '':
                    dictionary[letter] = float(number)
        coeficients.append(dictionary)
    matrix = create_matrix(coeficients, letters)
    return matrix, constants, letters

def create_matrix(coeficients, letters):
    matrix = []
    letters = sorted(letters)
    for line in coeficients:
        row = []
        for letter in letters:
            if letter not in line:
                row.append(float(0.0))
            else:
                row.append(line[letter])
        matrix.append(row)
    return matrix

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Wrong number of arguments!")
    else:
        main(sys.argv[1])
