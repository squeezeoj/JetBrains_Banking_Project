# ----------------------------------------------------------------------
# JetBrains - Simple Banking Program
# January 2021
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# Practice Cards
# ----------------------------------------------------------------------

# Card 1:
# 4000005218374602
# 5333
#
# Card 2:
# 4000007650183426
# 4565


# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------

# Randomization...
from random import randint, sample

# SQL Lite...
import sqlite3


# ----------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------

# Returns random 4-digit PIN, fully-padded with leading zeros...
def generate_random_pin_number():
    temp = randint(0, 9999)
    temp = temp + 10000
    temp = str(temp)
    temp = temp[1:5]
    return str(temp)

# Returns Luhn-valid 16-digit visa-style credit card...
# Source: https://atufashireen.medium.com/luhn-algorithm-67c62e081238
first_6=400000 # IIN For Banking Industry(6 digits)
def generate_luhn_card_number():
    global first_6
    card_no = [int(i) for i in str(first_6)]  # To find the checksum digit on
    card_num = [int(i) for i in str(first_6)]  # Actual account number
    seventh_15 = sample(range(9), 9)  # Acc no (9 digits)
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

# Returns true if card number is valid against Luhn algorithm...
# Source: https://dev.to/anuragrana/python-script-validating-credit-card-number-luhn-s-algorithm-2f7c
def sum_digits(digit):
    if digit < 10:
        return digit
    else:
        sum = (digit % 10) + (digit // 10)
        return sum

def validate_luhn_card_number(cc_num):
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

# Returns true if card number and pin validate against card database...
def check_login(prm_card_number, prm_pin_number):
    cur.execute("SELECT id, number, pin, balance FROM card WHERE number = {} AND pin = {}".format(prm_card_number, prm_pin_number))
    result = cur.fetchone()
    if result != None:
        return True
    else:
        return False

# Returns true if card number exists in database...
def check_card_exists(prm_card_number):
    cur.execute("SELECT id, number FROM card WHERE number = {}".format(prm_card_number))
    result = cur.fetchone()
    if result != None:
        return True
    else:
        return False

# Returns integer balance for specified card...
def get_balance(prm_card_number):
    cur.execute("SELECT id, number, pin, balance FROM card WHERE number = {}".format(prm_card_number))
    result = cur.fetchone()
    if result != None:
        return result[3]
    else:
        return 0

# Returns true after adding income to specified card...
def add_income(prm_card_number, prm_income):
    current_balance = get_balance(prm_card_number)
    new_balance = int(current_balance) + int(prm_income)
    cur.execute("UPDATE card SET balance = {} WHERE number = {}".format(new_balance, prm_card_number))
    conn.commit()
    return True

# Returns true after transferring amount from one card to the other...
def transfer_to_another_card(prm_from_card_number, prm_to_card_number, prm_transfer_amount):
    # Take transfer amount off FROM card
    current_balance = get_balance(prm_from_card_number)
    new_balance = int(current_balance) - int(prm_transfer_amount)
    cur.execute("UPDATE card SET balance = {} WHERE number = {}".format(new_balance, prm_from_card_number))
    # Add transfer amount to TO card
    result = add_income(prm_to_card_number, prm_transfer_amount)
    return True

# Returns true after deleting the specified card from the database...
def close_account(prm_card_number):
    cur.execute("DELETE FROM card WHERE number = {}".format(prm_card_number))
    conn.commit()
    return True


# ----------------------------------------------------------------------
# Create Database / Initialize Connection and Create Table if Necessary
# ----------------------------------------------------------------------

# Open Database Connection and Set Cursor (Creates DB if it doesn't exist)...
conn = sqlite3.connect("card.s3db")
cur = conn.cursor()

# Create Database Table...
cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
conn.commit()


# ----------------------------------------------------------------------
# Main Program Loop
# ----------------------------------------------------------------------

# Generate main menu...
main_logout = False
while not main_logout:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")

    choice = int(input())

    if choice == 1:
        # Create an account...
        new_card_number = generate_luhn_card_number()
        new_pin_number = generate_random_pin_number()
        new_balance = 0
        cur.execute("INSERT INTO card (number, pin, balance) VALUES ({}, {}, {})".format(new_card_number, new_pin_number, new_balance))
        conn.commit()
        print("Your card has been created")
        print("Your card number:")
        print(new_card_number)
        print("Your card PIN:")
        print(new_pin_number)
        main_logout = False
        
    elif choice == 2:
        # Log into account...
        print("Enter your card number:")
        card_number = int(input())
        print("Enter your PIN:")
        pin_number = int(input())
        if check_login(card_number, pin_number):
            print("You have successfully logged in!")

            # Generate sub menu...
            sub_logout = False
            while not sub_logout:
                print("1. Balance")
                print("2. Add income")
                print("3. Do transfer")
                print("4. Close account")
                print("5. Log out")
                print("0. Exit")

                sub_choice = int(input())

                if sub_choice == 1:
                    print(get_balance(card_number))
                    sub_logout = False
                    
                elif sub_choice == 2:
                    print("Enter income:")
                    new_income = input()
                    result = add_income(card_number, new_income)
                    if result:
                        print("Income was added!")
                    sub_logout = False
                    
                elif sub_choice == 3:
                    print("Transfer")
                    print("Enter card number:")     # Transfer TO this card
                    to_card_number = input()

                    transfer_error = False
                    if (str(card_number) == str(to_card_number)) and (transfer_error == False):
                        print("You cannot transfer money to the same account!")
                        transfer_error = True
                        sub_logout = False

                    if transfer_error == False:
                        if validate_luhn_card_number(to_card_number):
                            # print("Luhn is valid - proceed")
                            transfer_error = False
                        else:
                            print("Probably you made a mistake in the card number. Please try again!")
                            transfer_error = True
                            sub_logout = False

                    if transfer_error == False:
                        if check_card_exists(to_card_number):
                            # print("Card exists - proceed")
                            transfer_error = False
                        else:
                            print("Such a card does not exist.")
                            transfer_error = True
                            sub_logout = False

                    if transfer_error == False:
                        print("Enter how much money you want to transfer:")
                        transfer_amount = int(input())       # Amount to transfer

                        if get_balance(card_number) >= transfer_amount:
                            # print("Balance is high enough - proceed")
                            transfer_error = False
                        else:
                            print("Not enough money!")
                            transfer_error = True
                            sub_logout = False
                        
                    if transfer_error == False:
                        result = transfer_to_another_card(card_number, to_card_number, transfer_amount)
                        if result:
                            print("Success!")
                        transfer_error = False
                        sub_logout = False
                    
                elif sub_choice == 4:
                    result = close_account(card_number)
                    if result:
                        print("The account has been closed!")
                    sub_logout = True
                    main_logout = False
                    break
                
                elif sub_choice == 5:
                    print("You have successfully logged out!")
                    sub_logout = True
                    main_logout = False
                    break
                
                else:
                    sub_logout = True
                    main_logout = True
                    break
                
            # ...end of sub menu

        else:
            print("Wrong card number or PIN!")
            main_logout = False
            
    else:
        # Exit...
        main_logout = True
        break

# Exit...
print("Bye!")
