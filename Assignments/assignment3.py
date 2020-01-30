# 1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.
persons = [{
    'name':'Batman',
    'age':21,
    'hobby': 'MMA'
    },
    {
    'name': 'Spiderman',
    'age': 19,
    'hobby': 'Slinghshot'
    },
    {
    'name':'Superman',
    'age':65,
    'hobby': 'Fly'
    }
]

# 2) Use a list comprehension to convert this list of persons into a list of names (of the persons).
names = [x['name'] for x in persons]
print(names)

# 3) Use a list comprehension to check whether all persons are older than 20.
ages_older =all([a['age'] > 20 for a in persons])
print(ages_older)

# 4) Copy the person list such that you can safely edit the name of the first person (without changing the original list).
copied_persons = [x.copy() for x in persons]     #[:] wont deep copt it
copied_persons[0]['name'] = 'Joker'
print(copied_persons)
print(persons)

# 5) Unpack the persons of the original list into different variables and output these variables.
name = ''
age = ''
hobby = ''
for each in persons:
    for (k,v) in each.items():
        if k == 'name':
            name = name + ' ' + v
        elif k == 'age':
            age = age + ' ' + str(v)
        else:
            hobby = hobby + ' ' +v

print('Names:{}, Ages:{}, Hobbies:{}'.format(name,age,hobby))