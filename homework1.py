#!/usr/bin/python

"""
Homework 1:
Нужно написать класс который будет создавать объект этого же класса если в конструкторе будет присутствовать
str """"А"""" или """"В"""" но не что либо другое. 
Если в конструктор передается ""С"" или с ""В"" также передается ""С"" то должен быть создан простой базовый обьект (object).
"""

import itertools


class Constructor_limit:
    """
    Creates object of Constructor_limit class if input does not contain "C"
    Creates object of base object class if input contains C
    """

    def __new__(self, *args):
        if 'C' in str(args):
            return object            
        else:
            return object.__new__(Constructor_limit)

    
def all_combinations_list(input_list):
    all_combinations = []
    for r in range(len(input_list) + 1):
        combinations_list = list(itertools.combinations(input_list, r))
        all_combinations += combinations_list
    return all_combinations[1:] # removed () from the list

        
if __name__ == "__main__":
    
    input_strs = all_combinations_list(["A", "B", "C"])  # making all possible combinations with A, B, C except ()   
    for obj_num, obj_str in zip(range(len(input_strs)), input_strs): # creating as many objects as it is need for all combinations
        obj_name = "new_object_" + str(obj_num)
        obj_name = Constructor_limit(obj_str)
        print(f"New object {obj_num} was created, input string is {obj_str}".format(obj_num=obj_num, obj_str=obj_str))
        print("This is an object of Constructor_limit class: " + str(isinstance(obj_name, Constructor_limit)))
        print("This is an object of Object class: " + str(isinstance(obj_name, object)))
