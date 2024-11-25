a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))

def calc(a,b):
    try:
        c = a/b
        print(c)
    except ZeroDivisionError:
        print("Error!")

calc(a,b)