a = (input('enter the value of a:'))
b = (input('enter the value of b:'))

temp = a
a = b
b = temp

print('The value of a after swapping: {}'.format(a))
print("The value of b after swapping: {}".format(b))