import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import all_func
import enter

class __Normal__:
    dict = {}
    cdn = []

class __No_Dependent__:
    dict = {}
    cdn = []

class Func():
    normal = __Normal__
    no_dep = __No_Dependent__

for function in [func for func in all_func.normal]:
    if function.__doc__:
        for key in function.__doc__.split(','):
            Func.normal.dict[key.strip()] = function
    else:
        Func.normal.cdn.append(function)

for function in [func for func in all_func.no_dependent]:
    if function.__doc__:
        for key in function.__doc__.split(','):
            Func.no_dep.dict[key.strip()] = function
    else:
        Func.no_dep.cdn.append(function)

def match_enter():
    global Func
    for key in Func.normal.dict:
        if key in enter.raw:
            Func.normal.dict[key]()
            return 1
    for func in Func.normal.cdn:
        if func():
            return 1
    for key in Func.no_dep.dict:
        if key in enter.raw:
            Func.normal.dict[key]()
            return 1
    for func in Func.no_dep.cdn:
        if func():
            return 1
    return 0


if __name__ == '__main__':
    print(Func.normal.dict)
    print(Func.normal.cdn)
    print(Func.no_dep.dict)
    print(Func.no_dep.cdn)
    while 1:
        enter.set_raw(input(": "))
        if not match_enter():
            print("key not found")