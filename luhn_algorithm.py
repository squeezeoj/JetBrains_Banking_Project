import random


def get_cc_number():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    return sys.argv[1]


def sum_digits(digit):
    if digit < 10:
        return digit
    else:
        sum = (digit % 10) + (digit // 10)
        return sum


def validate(cc_num):
    # reverse the credit card number
    cc_num = cc_num[::-1]
    # convert to integer list
    cc_num = [int(x) for x in cc_num]
    # double every second digit
    doubled_second_digit_list = list()
    digits = list(enumerate(cc_num, start=1))
    for index, digit in digits:
        if index % 2 == 0:
            doubled_second_digit_list.append(digit * 2)
        else:
            doubled_second_digit_list.append(digit)

    # add the digits if any number is more than 9
    doubled_second_digit_list = [sum_digits(x) for x in doubled_second_digit_list]
    # sum all digits
    sum_of_digits = sum(doubled_second_digit_list)
    # return True or False
    return sum_of_digits % 10 == 0


# Generate 16-digit visa-style credit card number
def generate_card_number():
    temp = randint(1, 9999999999)
    temp = temp + 10000000000
    temp = str(temp)
    temp = temp[1:11]
    temp = "400000" + temp
    return str(temp)


# Generate Luhn-valid 16-digit credit card number...
# https://atufashireen.medium.com/luhn-algorithm-67c62e081238
first_6=400000 # IIN For Banking Industry(6 digits)
def luhn():
    global first_6  
    card_no = [int(i) for i in str(first_6)]  # To find the checksum digit on
    card_num = [int(i) for i in str(first_6)]  # Actual account number
    seventh_15 = random.sample(range(9), 9)  # Acc no (9 digits)
    for i in seventh_15:
        card_no.append(i)
        card_num.append(i)
    for t in range(0, 15, 2):  # odd position digits
        card_no[t] = card_no[t] * 2
    for i in range(len(card_no)):
        if card_no[i] > 9:  # deduct 9 from numbers greater than 9
            card_no[i] -= 9
    s = sum(card_no)
    mod = s % 10
    check_sum = 0 if mod == 0 else (10 - mod)
    card_num.append(check_sum)
    card_num = [str(i) for i in card_num]
    return ''.join(card_num)


# Find valid card number using random generation...
valid = False
while not valid:
    # test_card_number = generate_card_number()
    test_card_number = luhn()
    print("Checking:", test_card_number)
    if validate(test_card_number):
        valid = True
        print(test_card_number,"is valid!")
    else:
        valid = False
        print(test_card_number,"is not valid!")
    print()
    
