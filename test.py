str1 = input('Первое значение: ')
str2 = input('Второе значение: ')
try:
    str1 = int(str1)
except ValueError:
    print(str1 + str2)
else:
    try:
        str2 = int(str2)
    except ValueError:
        print(str(str1) + str2)
    else:
        print(str1 + str2)
