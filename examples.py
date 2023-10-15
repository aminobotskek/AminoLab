#login
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")

#login with phonenumber
import AminoLab
client = AminoLab.Client()
client.auth(phone="phone_number", password="password")

#login with email input
import AminoLab
client = AminoLab.Client()
client.auth(email = input("Email >> "), password = input("Password >> "))

#login with phonenumber input
import AminoLab
client = AminoLab.Client()
client.auth(phone=input("Phone Number >> "), password=input("Password >> "))
#follow user
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
client.follow_user(comId="comId", userId="userId")

#unfollow_user
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
client.unfollow(comId="comId", userId="userId")

#get public communities list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
clients = client.get_public_communities(language="en", size=100)
for name, comId in zip(clients.name, clients.comId):
	print(f"{name} >> {comId}")
	
#get joined communities list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
clients = client.sub_clients()
for name, comId in zip(clients.name, clients.comId):
	print(f"{name} >> {comId}")

#get public chats list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
chats = client.get_public_chat_threads(comId="comId", size="size")
for title, chatId in zip(chats.title, chats.chatId):
	print(f"{title} >> {chatId}")

#get joined chats list
import AminoLab
client = AminoLab.Client()
client.auth(email="email", password="password")
chats = client.get_chat_threads(comId="comId", size="size")
for title, chatId in zip(chats.title, chats.chatId):
	print(f"{title} >> {chatId}")

#p.s. if you do not specify comId in functions, the script will work in the global