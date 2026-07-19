def uppercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase

    return wrapper

def say_hi():
    return 'hello there'

say_hi = uppercase_decorator(say_hi)
print(say_hi())

# Following is an alternate way of writing it which does the same thing
# by just putting the @ symbol with the name of the decorator
# (metafunction) on line before the function
@uppercase_decorator
def say_hi():
    return 'hello there'

print(say_hi())

#%%
from datetime import datetime
def log_datetime(func):
    '''Log the date and time of a function'''
    def wrapper():
        print(f'Function: {func.__name__}\nRun on: {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'{"-"*30}')
        func()
    return wrapper

@log_datetime
def daily_backup():
    print('Daily backup job has finished.')

daily_backup()

#%%
def count(aClass):
    aClass.numInstances = 0
    print(aClass.numInstances)
    return aClass

@count
class Spam:
    def __init__(self):
        print('New spam object created...')
        Spam.numInstances = Spam.numInstances+1
        print(Spam.numInstances)

@count
class Other:
    pass

print('==========')
a = Spam()
b = Spam()
c = Spam()
d = Spam()
count(Spam)

aa = Other()
bb = Other()
count(aa)
count(Other)
