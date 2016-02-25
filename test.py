x = 1

def f():
    global x
    x += 1
    print(x)
    return

def main():
    for i in range (0,11):
        f()
