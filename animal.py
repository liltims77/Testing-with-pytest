# animals = ['cat', 'dog', 'cow', 'hen', 'goat' ]

# my_list = []

# for animal in animals:
#     if len(animal)==3:
#         my_list.append(animal.upper())

#     else:
#         print(f"'{animal}' has a different length, not 3")

# print(my_list)


animals = ['cat', 'dog', 'cow', 'hen']

my_list = []

if len(animals) == 4:
    for animal in animals:
        my_list.append(animal.upper())
else:
    print('wrong')

print(my_list)
