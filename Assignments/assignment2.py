# 1) Create a list of names and use a for loop to output the length of each name (len()).
def len_of_names():
    list = []
    while True:
        value = input('Enter list of names one by one. Use q to exit \n')
        if value == 'q':
            break
        else:
            list.append(value)
            continue

    for name in list:
        #1 Answer) print("The length of {} is {}".format(name, len(name)-1))

# 2) Add an if check inside the loop to only output names longer than 5 characters.
        #if len(name) > 5:
        #    print("The length of {} is {} which is greater than 5".format(name, len(name) - 1))
# 3) Add another if check to see whether a name includes a “n” or “N” character.
        for i in range(len(name)):
            if (name[i] == 'n' or name[i] == 'N') and len(name) > 5:
                print("The length of {} is {} which is greater than 5 and contains the letter N".format(name, len(name)-1))
                break
            else:
                continue

# 4) Use a while loop to empty the list of names (via pop())
    empty = False
    while not empty:
        list.pop()
        if len(list) == 0:
            empty = True
            print('List is empty ')

len_of_names()