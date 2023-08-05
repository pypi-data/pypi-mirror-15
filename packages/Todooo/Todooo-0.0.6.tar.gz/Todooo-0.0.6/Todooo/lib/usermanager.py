import random
import os
class User(object):

	def __init__(self):
		self.usr={}
		self.id_num=set()
		self.id={}
		
	def add_user(self):
		while True:
			name= input("Please enter your username: ")
			if name in self.usr:
				print("We have already has this username ~")
				continue
			else:
				passwd=input("Please enter Your Password: ")
				self.usr[name]=passwd
				while True:
					num=random.randint(10000,99999)
					if num not in self.id_num:
						self.id_num.add(num)
						break
				self.id[name]=num
				print("Congrats!Your account has been successfully established!\nYour user data id is %d"%num)
				if os.path.exists(os.path.join(os.path.dirname(__file__),'../data/usr/%s'%num)):
					pass
				else:
					os.mkdir(os.path.join(os.path.dirname(__file__),'../data/usr/%s'%num))
				break
	def user_login(self,name_input):
		while True:
			counter = 0
			
			if name_input in self.usr:
				while True:
					attempt=0
					passwd_input=input("Please Enter your password: ")
					if passwd_input==self.usr[name_input]:
						return True
					else:
						print("Invaild Password, try again please!")
						attempt+=1
					if attempt>3:
						print("You have run out of your choice!Break Anyway")
						break
				break
			else:
				print("User not exists, try again please!")
			counter+=1
			if counter >3:
				print("You have run out of your choice!Break Anyway")
				break
			return False

	def delete_user(self):
		print("For your account protection, we need to verify your information")
		while True:
			counter = 0
			name_attempt=input("Please Enter your username: ")
			if name_attempt in self.usr:
				while True:
					attempt=0
					passwd_attempt=input("Please Enter your password: ")
					if passwd_attempt==self.usr[name_attempt]:
						del self.usr[name_attempt]
						del self.id[name_attempt]
						del name_attempt
						del passwd_attempt
						input("You account has been successfully canceled, welcome back any time!\nPress Enter to continue..")
						break
					else:
						print("Invaild Password, try again please!")
						attempt+=1
						if attempt>3:
							print("You have run out of your choice!Break Anyway")
							break
						continue
				break
			else:	
				print("User not exists, try again please!")
			
				if counter >3:
					print("You have run out of your choice!Break Anyway")
					break

	def modify_user(self):
		print("For your account protection, we need to verify your information")
		while True:
			name_attempt=input("Please Enter your username: ")
			if name_attempt in self.usr:
				while True:
					attempt=0
					passwd_attempt=("Please Enter your password: ")
					if passwd_attempt==self.usr[name_attempt]:
						passwd=("Please enter your new password: ")
						self.usr[name_attempt]=passwd
						del passwd_attempt
						print("You account has been successfully canceled, welcome back any time!")
						break
					else:
						print("Invaild Password, try again please!")
						attempt+=1
						if attempt>3:
							print("You have run out of your choice!Break Anyway")
							break
				break
			else:
				print("User not exists, try again please!")
				counter+=1
				if counter >3:
					print("You have run out of your choice!Break Anyway")
				break

