# 1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.

def first():
    with open('assignment6.txt', mode='w') as file:
        more = True
        while more:
            print('1 to input and 2 to quit ')
            choice = input('Enter input ')
            if choice == '1':
                data = input('Enter input to save ')
                file.write(data)
            else:
                more = False
# 2) Add another option to your user interface: The user should be able to output the data stored in the file in the terminal.
def second():
            more = True
            while more:
                print('1 to input, 2 to print file and 3 to quit')
                choice = input('Enter input ')
                if choice == '1':
                    data = input('Enter input to save ')
                    with open('assignment6.txt', mode='w') as file:
                        file.write(data)
                elif choice == '2':
                    with open('assignment6.txt', mode='r') as f:
                        contents = f.readlines()
                        for line in contents:
                            print(line)
                else:
                    more = False


# 3) Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.
import json
import pickle

def jjssoonn():
    more = True
    data = []
    while more:
        print('1 to input, 2 to print file and 3 to quit')
        choice = input('Enter input ')
        if choice == '1':
            data.append(input('Enter input to save '))
            with open('assignment6.txt', mode='w') as file:
                file.write(json.dumps(data))
        elif choice == '2':
            with open('assignment6.txt', mode='r') as f:
                contents = f.read()
                values = json.loads(contents)
                for line in values:
                    print(line)
        else:
            more = False

def ppiicckkllee():
    more = True
    data = []
    while more:
        print('1 to input, 2 to print file and 3 to quit')
        choice = input('Enter input ')
        if choice == '1':
            data.append(input('Enter input to save '))
            with open('assignment6.p', mode='wb') as file:
                file.write(pickle.dumps(data))
        elif choice == '2':
            with open('assignment6.p', mode='rb') as f:
                contents = f.reads()
                values = pickle.loads(contents)
                for line in values:
                    print(line)
        else:
            more = False

# 4) Adjust the logic to load the file content to work with pickled/ json data.
