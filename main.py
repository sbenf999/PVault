import getpass
import hashlib
import json
import os, os.path
import random
import requests
import secrets
import string
import stdiomask
import socket
import sys
import time

from time import sleep
from visualUtils import *

#Miscellaneous Functions
def reminder_exit():
	moving_ellipsis("\n Exiting program")

def get_help(given_list):
	print("\n Help:")
	lens = []
	
	for i in range(len(given_list)):
		for j in range(len(given_list[i])):
			lens.append(len(given_list[i][0]))

	for i in range(len(given_list)):
		output2 = []

		for j in range(len(given_list[i])):
			output = f"{given_list[i][j]}"
			output2.append(output)

		calc = ((max(lens)+min(lens))-len(given_list[i][0]))
		dots = '.'*calc
		info = f'{dots}: '.join(output2)

		print(f"   {info}") 

def get_input(string: str, valid_options: list) -> str:
    while True:
        user_input = input(string)
        if user_input == '':
        	continue
        else:
	        capitalized = user_input[0].upper() + user_input[1:len(user_input)]

        options = []
        for i in range(len(valid_options)):

            for j in range(len(valid_options[i])):
                option = f'{valid_options[i][j-1]}'
            options.append(option)

        if user_input in options or capitalized in options:
            return capitalized

        elif capitalized == 'Help':
        	return get_help(valid_options)

        print(f" -Please select from: {', '.join(options)} or Help-")

def generate_token(size=15):
    return secrets.token_urlsafe(size)[:size]

def does_exist(file_name):
	return os.path.isfile(file_name)

#Make hashes for comparisons and storing in .txt file 'accountfile.txt
def make_hash(data):
	return hashlib.sha256(str.encode(data)).hexdigest()

def check_hash(data, hash):
	if make_hash(data) == hash:
		return True

	return False

#Functions that deal with creation, authorisation and login process of the user
def get_existing_users():
    if does_exist('accountfile.txt'):
        with open('accountfile.txt', 'r') as fp:
            for line in fp.readlines():
                (username, password) = line.split()
                yield (username, password)
    else:

        f = open('accountfile.txt', 'a')
        f.close()
        get_existing_users()

def is_authorized(username, password):
    spinner()
    return any(check_hash(username, user[0]) and check_hash(password, user[1]) for user in get_existing_users())

def check_user(username):
    return any(check_hash(username, user[0]) for user in get_existing_users())

def get_user(data_needed):
	if data_needed == "Username":
		username = input("\n Username: ")

		return username

	else:
		username = input("\n Username: ")
		password = stdiomask.getpass(prompt=" Password: ")

		return username, password

def make_user():
	new_username = input("\n New Username: ")

	while any(check_hash(new_username, user[0]) for user in get_existing_users()):
		if not any(check_hash(new_username, user[0]) for user in get_existing_users()):
			break

		print(" > Username already taken")
		new_username = input("\n New Username: ")

	new_password = input(" New Password: ")

	while stdiomask.getpass(prompt=" Confirm Password: ") != new_password:
		print("\n > Passwords do not match. Try again")
		stdiomask.getpass(prompt=" Confirm Password: ")
		
	moving_ellipsis("\n > Your Passwords Match. Continuing process")

		
	#hash usernames and passwords before writing to .txt file
	with open("accountfile.txt","a") as file:
		file.write(make_hash(new_username))
		file.write(" ")
		file.write(make_hash(new_password))
		file.write("\n")

	if is_authorized(new_username, new_password):
		try:
			moving_ellipsis("\n Redirecting to login process")
			authorisation()
		except Exception as e:
			print(f" Fail encountered during sub-process {make_user.__name__}. Error: {e}")
	else:
		print(" Something went wrong. Try again later :D")

	return False

def authorisation():
	if len(list(get_existing_users())) == 0:
		print(" No exisiting users in account file")

		moving_ellipsis("\n Redirecting to user creation process")
		make_user()

	else:
		username, password = get_user("Both")

		if is_authorized(username, password):
			time.sleep(1)
			print(f"\n <Welcome back {username}>")
			return (True, username)

		else:
			time.sleep(1)
			print("\n Incorrect login details")
			return (False, username)

def vault_menu(name):
	while True:
		choice2 = get_input(f'\n {name}@Vault_Menu\n → ', [["Initialise", "Create your password vault"], ["Load", "Load your password vault connected to your account"], ["Audit", "Edit data in your password vault"], ["Erase", "Delete the entire password vault - requires password"]])

		if choice2 == "Load":
			pass

		elif choice2 == "Audit":
			pass

		elif choice2 == "Erase":
			username = name

			if check_user(username) and does_exist(username+".txt"):
				print(f" File associated with your username is: {username}.txt")
				
				while True:
					choice3 = get_input(f'\n Do you wish to delete it?\n → ', [["y", "yes"], ["n", "no"]])
					if choice3 == "Y":
						spinner(" Deleting password vault: ", "Deleted")

						try:
							os.remove(username+".txt")
							break

						except Exception:
							print(" The file is unable to be deleted")
							break

			else:
				print(f"\n A vault tied to your username, {username}, does not exist.")


#Main menu loop!!!
def main():
	menu_art(1)
	screen_line()

	while True:
		choice = get_input(f'\n mainMenu\n → ', 
			[["Login", "Login to a pre-existing account"], ['New User', 'Create a new user - found in "accountfile.txt" '], ["Exit", "Exit the program - will give 3s warning"]])

		if choice == "Login":
			authorise = authorisation()
			if authorise[0]:
				vault_menu(authorise[1])
				
			else:
				reminder_exit()
				break

		elif choice == "New User":
			make_user()

		elif choice == "Exit":
			reminder_exit()
			break

main()