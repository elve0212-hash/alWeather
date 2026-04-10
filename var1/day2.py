#Data Types

#String

print('123' + '456')

#Integer

print(123 + 456)

#Float

3.14159

#Boolean

True
False

num_char = len(input('what is your name?'))
#print('your name has' + num_char + 'characters.')

print(type(num_char))

num_char = len(input('what is your name?'))

new_num_char = str(num_char)

print('Your name has' + new_num_char + 'characters')

a = str(123)
print(type(a))

a = float(123)
print(type(a))

print(70 + float('100.5'))

print(str(70)+ str(100))

two_digit_number = input('type a two digit number: ')
print(type(two_digit_number))

first_digit = two_digit_number[0]
second_digit = two_digit_number[1]

result = int(first_digit) + int(second_digit)
print(result)

3 + 5
7 - 4
3 * 5
6 / 3
print(6 / 3)

#exponent
2 ** 3
print(2 ** 3)

#PEMDAS
print(3 * (3 + 3) / 3 - 3)

#BMI
#BMI = weight(kg)/height ** 2(m ** 2)
height = input('enter your height in m: ')
weight = input('enter your weight in kg: ')

bmi = int(weight) / float(height) ** 2
print(bmi)

bmi_as_int= int(bmi)
print(bmi_as_int)

print(round(bmi))

print(round(bmi, 2))

print(round(2.6666666666666666, 2))

print(8//3)

score = 100
height = 1.8
weight = 78
isWinning = True
#f-string
print(f"Your score is: {score}, your height is: {height}, you are winning is: {isWinning}")


