print("""AminoLab by Kek
my telegram t.me/two_brothers_2""")
from functools import reduce
from time import timezone,time
import requests,base64,json,objects,os
from typing import BinaryIO, Union
from hmac import new
from json_minify import json_minify
from hashlib import sha1
from locale import getdefaultlocale as locale
from base64 import b64encode, b64decode
class Client():
    def __init__(self,proxy:dict=None):
        self.proxies=proxy
        self.headers = {"Accept-Language": "en-US","Content-Type": "application/x-www-form-urlencoded", "Host": "service.narvii.com","Accept-Encoding": "gzip","Connection": "Upgrade"}
        self.secret = None
        self.sid = None
        self.userId = None        
        self.api ="https://service.narvii.com/api/v1"
    def devgener(self):
    	identifier = os.urandom(20)
    	return ("19" + identifier.hex() + new(bytes.fromhex("E7309ECC0953C6FA60005B2765F99DBBC965C8E9"), b"\x19" + identifier, sha1).hexdigest()).upper()
    def headers_lib(self):
    	self.headers["NDCDEVICEID"]=self.devgener()
    	return self.headers
    def sig(self, data:str):
    	self.headers["NDC-MSG-SIG"] =b64encode(bytes.fromhex("19") + new(bytes.fromhex("DFA5ED192DDA6E88A12FE12130DC6206B1251E44"), data.encode("utf-8"), sha1).digest()).decode("utf-8")
    	return self.headers["NDC-MSG-SIG"]
    def get_user_visitors(self,userId,comId:int=None):
    	if comId:response=requests.get(f"{self.api}/x{comId}/s/user-profile/{userId}/visitors",headers=self.headers_lib())
    	else: response=requests.get(f"{self.api}/g/s/user-profile/{userId}/visitors",headers=self.headers_lib())
    	if response.status_code != 200:            	print(response.json()["api:message"])
    	else:return response.json()["visitors"]
    def search_by_nickname(self,nickname,start:int=0,size:int=100,comId:int=None):
    	if comId:response=requests.get(f"{self.api}/x{comId}/s/user-profile?type=name&q={nickname}&start={start}&size={size}",headers=self.headers_lib())
    	else: response=requests.get(f"{self.api}/g/s/user-profile?type=name&q={nickname}&start={start}&size={size}",headers=self.headers_lib())
    	if response.status_code != 200:            	print(response.json()["api:message"])
    	else:return objects.MembersList(response.json()["userProfileList"]).MembersList
    def apply_avatar_frame(self,frameId,comId:int=None):
    	data =json.dumps({"frameId": frameId,"deviceID": self.devgener(),"timestamp": int(time()  * 1000)})
    	self.sig(data)
    	if comId:response=requests.post(f"{self.api}/x{comId}/s/avatar-frame/apply",headers=self.headers_lib(),data=data)
    	else: response=requests.post(f"{self.api}/g/s/avatar-frame/apply",headers=self.headers_lib(),data=data)
    	if response.status_code != 200:            	print(response.json()["api:message"])
    	else:return response.json()
    def generate_bubble(self,file,comId:int=None):
    	if comId:response=requests.post(f"{self.api}/x{comId}/s/chat/chat-bubble/templates/107147e9-05c5-405f-8553-af65d2823457/generate",headers=self.headers_lib(),proxies=self.proxies,data=file)
    	else:response=requests.post(f"{self.api}/g/s/chat/chat-bubble/templates/107147e9-05c5-405f-8553-af65d2823457/generate",headers=self.headers_lib(),proxies=self.proxies,data=file)
    	if response.status_code != 200:            	print(response.json()["api:message"])
    	else:return response.json()['chatBubble']['bubbleId']
    def get_bubbles_list(self,comId:int=None):
        if comId:response = requests.get(f"{self.api}/x{comId}/s/chat/chat-bubble",headers=self.headers_lib())
        else:response = requests.get(f"{self.api}/g/s/chat/chat-bubble",headers=self.headers_lib())
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()
    def get_bubbles_templates_list(self,start:int=0,size:int=100,comId:int=None):
        if comId:response = requests.get(f"{self.api}/x{comId}/s/chat/chat-bubble/templates?start={start}&size={size}",headers=self.headers_lib())
        else:response = requests.get(f"{self.api}/g/s/chat/chat-bubble/templates?start={start}&size={size}",headers=self.headers_lib())
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()["templateList"]
    def get_avatar_frames_list(self,comId:int=None,start: int = 0, size: int = 10):
        if comId:response = requests.get(f"{self.api}/x{comId}/s/avatar-frame?start={start}&size={size}",headers=self.headers_lib())
        else: response = requests.get(f"{self.api}/g/s/avatar-frame?start={start}&size={size}",headers=self.headers_lib())
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()
    def upload_bubble(self,bubbleId,comId:int=None):
    	if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/chat-bubble/{bubbleId}", headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.post(f"{self.api}/g/s/chat/chat-bubble/{bubbleId}", headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:            	print(response.json()["api:message"])
    	else:return response.json()
    def create_shared_folder(self, title: str,comId:str):
        data = json.dumps({"title": title,"timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/shared-folder/folders", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else: return response.json()
    def websocket_url(self):
    	return requests.get("https://aminoapps.com/api/chat/web-socket-url", headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36","content-type": "application/json","x-requested-with": "xmlhttprequest","cookie": f"sid={self.sid}"}).json()["result"]["url"]
    def register(self,email,password,nickname,verification_code):
        data = json.dumps({"secret": f"0 {password}","deviceID": self.devgener(),"email": email,"clientType": 100,"nickname": nickname,"latitude": 0,"longitude": 0,"address": None,"clientCallbackURL": "narviiapp://relogin","validationContext": {"data": {"code": verification_code},"type": 1,"identity": email},"type": 1,"identity": email,"timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/g/s/auth/register", data=data, headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()
    def activate_account(self, email: str, code: str):
        data = json.dumps({"type": 1,"identity": email,"data": {"code": code},"deviceID": self.devgener()})
        self.sig(data)
        response = requests.post(f"{self.api}/g/s/auth/activate-email",headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()
    def request_security_validation(self,email: str,reset_password: bool = False):
        data = {"identity": email,"type": 1,"deviceID":self.devgener()}
        if reset_password is True:
            data["level"] = 2
            data["purpose"] = "reset-password"
        data = json.dumps(data)
        self.sig(data)
        response = requests.post(f"{self.api}/g/s/auth/request-security-validation", headers=self.headers_lib(),proxies=self.proxies, data=data)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()
    def auth(self, email: str = None, phone: str = None, password: str = None):
    	data ={"v":2,"secret": f"0 {password}","deviceID": self.devgener(),"clientType": 100,"action": "normal","timestamp": int(time()  * 1000)}
    	if email:data["email"]=email
    	elif phone:data["phoneNumber"]=phone
    	data = json.dumps(data)
    	self.sig(data)
    	response=requests.post(f"{self.api}/g/s/auth/login",data=data,headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:
            if response.json()["api:message"]=="Please verify your account before logging in on a new device.":
            	print(response.json()["api:message"])
            	return response.json()["url"]
            else:print(response.json()["api:message"])		
    	else:
    		self.sid = response.json()["sid"]
    		self.secret = response.json()["secret"]
    		self.userId = response.json()["auid"]
    		self.headers["NDCAUTH"] = f"sid={self.sid}"
    def get_chat_thread(self, chatId: str,comId:int=None):
        if comId: response = requests.get(f"{self.api}/x{comId}/s/chat/thread/{chatId}", headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.get(f"{self.api}/g/x/s/chat/thread/{chatId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["thread"]
    def join_chat(self, chatId: str,comId: int=None):
        if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/member/{self.userId}", headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/member/{self.userId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return response.json()

    def leave_chat(self, chatId: str=None,chatsId:str=None,comId: int=None):
        if chatsId:
        	if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread/leave?threadIds=" + '%2C'.join(chatsId), headers=self.headers_lib(),proxies=self.proxies)
        	else: response = requests.post(f"{self.api}/g/s/chat/thread/leave?threadIds=" + '%2C'.join(chatsId), headers=self.headers_lib(),proxies=self.proxies)
        else:
        	if comId:response = requests.delete(f"{self.api}/x{comId}/s/chat/thread/{chatId}/member/{self.userId}", headers=self.headers_lib(),proxies=self.proxies)
        	else:response = requests.delete(f"{self.api}/g/s/chat/thread/{chatId}/member/{self.userId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return response.json()
    def get_from_code(self, code: str):
        response = requests.get(f"{self.api}/g/s/link-resolution?q={code}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return objects.FromCode(response.json()["linkInfoV2"]).FromCode
    def sub_clients(self):
        response = requests.get(f"{self.api}/g/s/community/joined?v=1&start=0&size=100", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return objects.CommunityList(response.json()["communityList"]).CommunityList
    def join_community(self, comId: int, invitationId: str = None):
        data = {"deviceID": self.devgener(),"timestamp": int(time()  * 1000)}
        if invitationId: data["invitationId"] = invitationId
        data = json.dumps(data)
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/community/join", data=data, headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()
    def request_join_community(self, comId: int, message: str = None):
        data = json.dumps({"message": message, "timestamp": int(time()  * 1000),"deviceID": self.devgener()})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/community/membership-request", data=data, headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()
    def leave_community(self, comId: str):
        response = requests.post(f"{self.api}/x{comId}/s/community/leave", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()
    def get_user_info(self, userId: str,comId: int=None):
        if comId:response = requests.get(f"{self.api}/x{comId}/s/user-profile/{userId}",headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.get(f"{self.api}/g/s/user-profile/{userId}",headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return objects.UserInfo(response.json()["userProfile"]).UserInfo
    def get_chat_threads(self,size: int = 100,comId: str=None):
        if comId:response = requests.get(f"{self.api}/x{comId}/s/chat/thread?type=joined-me&start=0&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.get(f"{self.api}/g/s/chat/thread?type=joined-me&start=0&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return objects.ChatThreads(response.json()["threadList"]).ChatThreads
    def get_chat_messages(self, chatId: str, size: int = 25,comId: int=None):
    	if comId:url = f"{self.api}/x{comId}/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}"
    	else: url = f"{self.api}/g/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}"
    	response = requests.get(url, headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else:return response.json()
    def get_message_info(self, chatId: str, messageId: str,comId: int=None):
        if comId: response = requests.get(f"{self.api}/x{comId}/s/chat/thread/{chatId}/message/{messageId}", headers=self.headers_lib(),proxies=self.proxies)
        else: response = requests.get(f"{self.api}/g/s/chat/thread/{chatId}/message/{messageId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return response.json()["message"]
    def get_community_info(self, comId: str):
        response = requests.get(f"{self.api}/g/s-x{comId}/community/info?withInfluencerList=1&withTopicList=true&influencerListOrderStrategy=fansCount", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return response.json()["community"]
    def get_user_following(self, userId: str, start: int = 0, size: int = 25,comId: int=None):
        if comId: response = requests.get(f"{self.api}/x{comId}/s/user-profile/{userId}/joined?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        else: response = requests.get(f"{self.api}/g/s/user-profile/{userId}/joined?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return objects.MembersList(response.json()["userProfileList"]).MembersList
    def get_user_followers(self, userId: str, start: int = 0, size: int = 25,comId: int=None):
        if comId: response = requests.get(f"{self.api}/x{comId}/s/user-profile/{userId}/member?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        else: response = requests.get(f"{self.api}/g/s/user-profile/{userId}/member?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return objects.MembersList(response.json()["userProfileList"]).MembersList
    def get_account_info(self):
        response = requests.get(f"{self.api}/g/s/account",headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:
            return response.json()["account"]
    def upload_media(self, file: BinaryIO, fileType: str):
        if fileType == "audio":
            t = "audio/aac"
        elif fileType == "image":
            t = "image/jpg"
        data = file.read()
        sigdata=json.dumps({"timestamp": int(time()  * 1000),"deviceID": self.devgener()})
        self.sig(data=sigdata)
        self.headers["Content-Type"]=t
        response = requests.post(f"{self.api}/g/s/media/upload", data=data, headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return response.json()["mediaValue"]
    def delete_account(self, password: str):
        data = json.dumps({"deviceID": self.devgener(),"secret": f"0 {password}"})
        response = requests.post(f"{self.api}/g/s/account/delete-request", headers=self.headers_lib(),proxies=self.proxies, data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return response.json()
    def block_full_list(self):
        response = requests.get(f"{self.api}/g/s/block/full-list", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:
            return response.json()
    def get_invitationId(self, code: str):
        response = requests.get(f"{self.api}/g/s/community/link-identify?q=http%3A%2F%2Faminoapps.com%2Finvite%2F{code}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()["invitationId"]
    def get_public_communities(self, language: str = "ru", size: int = 25):
        response = requests.get(f"{self.api}/g/s/topic/0/feed/community?language={language}&type=web-explore&categoryKey=recommendation&size={size}&pagingType=t", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return objects.CommunityList(response.json()["communityList"]).CommunityList
    def get_all_users(self, type: str = "recent", start: int = 0, size: int = 25,comId:int=None):
        if type == "recent":
        	if comId:response = requests.get(f"{self.api}/x{comId}/s/user-profile?type=recent&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        	else:response = requests.get(f"{self.api}/g/s/user-profile?type=recent&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        elif type == "banned": response = requests.get(f"{self.api}/x{comId}/s/user-profile?type=banned&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        elif type == "featured": response = requests.get(f"{self.api}/x{comId}/s/user-profile?type=featured&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        elif type == "leaders": response = requests.get(f"{self.api}/x{comId}/s/user-profile?type=leaders&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        elif type == "curators": response = requests.get(f"{self.api}/x{comId}/s/user-profile?type=curators&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        elif type=="online":
        	if comId:response = requests.get(f"{self.api}/x{comId}/s/live-layer?topic=ndtopic:x{comId}:online-members&size={size}&start={start}", headers=self.headers_lib(),proxies=self.proxies)
        	else:response = requests.get(f"{self.api}/g/s/user-profile?type=online&size={size}&start={start}",headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return objects.MembersList(response.json()["userProfileList"]).MembersList
    def activity_status(self, status: str,comId:str):
        if "on" in status.lower(): status = 1
        elif "off" in status.lower(): status = 2
        data = json.dumps({"onlineStatus": status,"duration": 86400,"timestamp": int(time()  * 1000)})
        self.sig(data)
        response =requests.post(f"{self.api}/x{comId}/s/user-profile/{self.userId}/online-status", headers=self.headers_lib(), data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def edit_chat(self, chatId: str, pinChat: bool = None, title: str = None, icon: str = None, content: str = None, viewOnly: str=None,comId:int=None,announcement: str = None,pinAnnouncement:str=None):
        data = {"timestamp": int(time()  * 1000)}
        if title: data["title"] = title
        if content: data["content"] = content
        if icon: data["icon"] = icon
        if announcement: data["extensions"] = {"announcement": announcement,"pinAnnouncement": True}
        data=json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}", headers=self.headers_lib(),proxies=self.proxies, data=data)
        else:response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}", headers=self.headers_lib(),proxies=self.proxies, data=data)
        if response.status_code != 200:            	print(response.json()["api:message"])
        if viewOnly==200:self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/view-only/enable",headers=self.headers_lib(),proxies=self.proxies, data=data)
        else:response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/view-only/enable",headers=self.headers_lib(),proxies=self.proxies, data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: response.status_code
    def send_message(self, chatId: str, message: str = None, messageType: int = 0, file: BinaryIO = None, fileType: str = None, replyTo: str = None, mentionUserIds: list = None, stickerId: str = None, embedId: str = None, embedType: int = None, embedLink: str = None, embedTitle: str = None, embedContent: str = None, embedImage: BinaryIO = None,comId:int=None):
        if message is not None and file is None:
            message = message.replace("<$", "‎‏").replace("$>", "‬‭")
        mentions = []
        if mentionUserIds:
            for mention_uid in mentionUserIds:
                mentions.append({"uid": mention_uid})
        if embedImage:
            embedImage = [[100, self.upload_media(embedImage, "image"), None]]
        data = {"deviceID": self.devgener(),"type": messageType,"content": message,"clientRefId": int(time()  / 10 % 1000000000),"attachedObject": {"objectId": embedId,"objectType": embedType,"link": embedLink,"title": embedTitle,"content": embedContent,"mediaList": embedImage},"extensions": {"mentionedArray": mentions},"timestamp": int(time()  * 1000)}
        if replyTo: data["replyMessageId"] = replyTo
        if stickerId:
            data["content"] = None
            data["stickerId"] = stickerId
            data["type"] = 3

        if file:
            data["content"] = None
            if fileType == "audio":
                data["type"] = 2
                data["mediaType"] = 110

            elif fileType == "image":
                data["mediaType"] = 100
                data["mediaUploadValueContentType"] = "image/jpg"
                data["mediaUhqEnabled"] = True

            elif fileType == "gif":
                data["mediaType"] = 100
                data["mediaUploadValueContentType"] = "image/gif"
                data["mediaUhqEnabled"] = True
            data["mediaUploadValue"] = base64.b64encode(file.read()).decode()
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/message", headers=self.headers_lib(),proxies=self.proxies, data=data)
        else:response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/message", headers=self.headers_lib(),proxies=self.proxies, data=data)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else: return response.json()
    def start_chat(self, userId: Union[str, list], message: str, title: str = None, content: str = None, isGlobal: bool = False, publishToGlobal: bool = False,comId: int=None):
        if isinstance(userId, str): userIds = [userId]
        elif isinstance(userId, list):userIds = userId
        data = {"title": title,"inviteeUids": userIds,"initialMessageContent": message,"content": content,"timestamp": int(time()  * 1000)}
        if isGlobal is True: data["type"] = 2; data["eventSource"] = "GlobalComposeMenu"
        else: data["type"] = 0
        if publishToGlobal is True: data["publishToGlobal"] = 1
        else: data["publishToGlobal"] = 0
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread", headers=self.headers_lib(),proxies=self.proxies, data=data)
        else:response = requests.post(f"{self.api}/g/s/chat/thread", headers=self.headers_lib(),proxies=self.proxies, data=data)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else: return response.json() 
    def login_sid(self, sid: str):
    	data =json.loads(b64decode(reduce(lambda a, e: a.replace(*e), ("-+", "_/"), sid + "=" * (-len(sid) % 4)).encode())[1:-20].decode())
    	self.sid = sid
    	self.userId = data["2"]
    	self.headers["NDCAUTH"] = f"sid={self.sid}"
    	return data
    def follow(self, userId: Union[str, list],comId:int=None):
            if isinstance(userId, str):
            	if comId:response = requests.post(f"{self.api}/x{comId}/s/user-profile/{userId}/member", headers=self.headers_lib(),proxies=self.proxies)
            	else:response = requests.post(f"{self.api}/g/s/user-profile/{userId}/member", headers=self.headers_lib(),proxies=self.proxies)
            elif isinstance(userId, list):
            	data = json.dumps({"targetUidList": userId,"deviceID": self.devgener(), "timestamp": int(time()  * 1000)})
            	self.sig(data)
            	if comId:response = requests.post(f"{self.api}/x{comId}/s/user-profile/{self.userId}/joined", headers=self.headers_lib(),proxies=self.proxies,data=data)
            	else:response = requests.post(f"{self.api}/g/s/user-profile/{self.userId}/joined", headers=self.headers_lib(),proxies=self.proxies,data=data)
            if response.status_code != 200:print(response.json()["api:message"])
            else: return response.json()
    def unfollow(self, userId: str,comId:int=None):
        if comId:response = requests.delete(f"{self.api}/x{comId}/s/user-profile/{self.userId}/joined/{userId}", headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.delete(f"{self.api}/g/s/user-profile/{self.userId}/joined/{userId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def add_influencer(self, userId: str, monthlyFee: int,comId: int):
        data = json.dumps({"monthlyFee": monthlyFee,"timestamp": int(time()  * 1000)})
        self.sig(data)
        response =requests.post(f"{self.api}/x{comId}/s/influencer/{userId}", headers=self.headers_lib(),proxies=self.proxies, data=data)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else: return response.json()
    def remove_influencer(self, userId: str,comId: int):
        response =requests.delete(f"{self.api}/x{comId}/s/influencer/{userId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else: return response.json()
    def like_blog(self, blogId:str = None,blogsId:str=None, wikiId: str = None,comId: int=None):
        data = {"value": 4,"timestamp": int(time()  * 1000),"deviceID": self.devgener()}
        if blogId:data["eventSource"] = "UserProfileView"
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/blog/{blogId}/vote?cv=1.2", data=data, headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/blog/{blogId}/vote?cv=1.2", data=data, headers=self.headers_lib(),proxies=self.proxies)
        if blogsId:data["targetIdList"] = blogsId
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/feed/vote", data=data, headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/feed/vote", data=data, headers=self.headers_lib(),proxies=self.proxies)
        if wikiId:data["eventSource"] = "PostDetailView"
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/item/{wikiId}/vote?cv=1.2", data=data, headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/item/{wikiId}/vote?cv=1.2", data=data, headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else: return response.json()
    def comment(self, message: str, userId: str = None, blogId: str = None, wikiId: str = None, replyTo: str = None, isGuest: bool = False,comId: int=None):
        data = {"content": message,"stickerId": None,"type": 0,"deviceID": self.devgener(),"timestamp": int(time()  * 1000)}
        if replyTo: data["respondTo"] = replyTo
        if isGuest: comType = "g-comment"
        else: comType = "comment"
        if userId:data["eventSource"] = "UserProfileView"
        data = json.dumps(data)
        self.sig(data )
        if comId:response = requests.post(f"{self.api}/x{comId}/s/user-profile/{userId}/{comType}", data=data, headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/user-profile/{userId}/{comType}", data=data, headers=self.headers_lib(),proxies=self.proxies)
        if blogId:data["eventSource"] = "PostDetailView"
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/blog/{blogId}/{comType}", data=data, headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/blog/{blogId}/{comType}", data=data, headers=self.headers_lib(),proxies=self.proxies)
        if wikiId:data["eventSource"] = "PostDetailView"
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/item/{wikiId}/{comType}", data=data, headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/item/{wikiId}/{comType}", data=data, headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_recent_blogs(self,start: int = 0, size: int = 25,comId: int=None):
        if comId:response = requests.get(f"{self.api}/x{comId}/s/feed/blog-all?pagingType=t&start={start}&size={size}",headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.get(f"{self.api}/g/s/feed/blog-all?pagingType=t&start={start}&size={size}",headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.BlogsList(response.json()["blogList"]).BlogsList
    def get_public_chat_threads(self, comId: int=None , type: str = "recommended", start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.ChatThreads(response.json()["threadList"]).ChatThreads
    def get_user_blogs(self, comId:str, userId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/blog?type=user&q={userId}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.BlogsList(response.json()["blogList"]).BlogsList
    def play_quiz_raw(self, quizId: str, quizAnswerList: list, quizMode: int = 0,comId: int=None):
        data = json.dumps({"mode": quizMode,"quizAnswerList": quizAnswerList,"deviceID": self.devgener(),"timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/blog/{quizId}/quiz/result", headers=self.headers_lib(),proxies=self.proxies, data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def send_active_object(self,comId:int , startTime: int = None, endTime: int = None, optInAdsFlags: int = 2147483647, tz: int = -timezone // 1000, timers: list = None, timestamp: int = int(time()  * 1000)): 
        data = {"userActiveTimeChunkList": [{"start": startTime, "end": endTime}], "timestamp": timestamp,"deviceID": self.devgener(), "optInAdsFlags": optInAdsFlags, "timezone": tz} 
        if timers: data["userActiveTimeChunkList"] = timers 
        data = json_minify(json.dumps(data))  
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/community/stats/user-active-time", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"]) 
        else: return response.json()
    def unlike_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None,comId: int=None):
        if userId:
        	if comId:response = requests.delete(f"{self.api}/x{comId}/s/user-profile/{userId}/comment/{commentId}/g-vote?eventSource=UserProfileView", headers=self.headers_lib(),proxies=self.proxies)
        	else:response = requests.delete(f"{self.api}/g/s/user-profile/{userId}/comment/{commentId}/g-vote?eventSource=UserProfileView", headers=self.headers_lib(),proxies=self.proxies)
        if blogId:
        	if comId:response = requests.delete(f"{self.api}/x{comId}/s/blog/{blogId}/comment/{commentId}/g-vote?eventSource=PostDetailView", headers=self.headers_lib(),proxies=self.proxies)
        	else:response = requests.delete(f"{self.api}/g/s/blog/{blogId}/comment/{commentId}/g-vote?eventSource=PostDetailView", headers=self.headers_lib(),proxies=self.proxies)
        if wikiId:
        	if comId:response = requests.delete(f"{self.api}/x{comId}/s/item/{wikiId}/comment/{commentId}/g-vote?eventSource=PostDetailView", headers=self.headers_lib(),proxies=self.proxies)
        	else:response = requests.delete(f"{self.api}/g/s/item/{wikiId}/comment/{commentId}/g-vote?eventSource=PostDetailView", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def like_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None,comId: int=None):
        data = {"value": 1,"deviceID": self.devgener(),"timestamp": int(time()  * 1000)}
        if userId:data["eventSource"] = "UserProfileView"
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/user-profile/{userId}/comment/{commentId}/vote?cv=1.2&value=1", headers=self.headers_lib(),proxies=self.proxies,data=data)
        else:response = requests.post(f"{self.api}/g/s/user-profile/{userId}/comment/{commentId}/vote?cv=1.2&value=1", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if blogId:data["eventSource"] = "PostDetailView"
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/blog/{blogId}/comment/{commentId}/vote?cv=1.2&value=1", headers=self.headers_lib(),proxies=self.proxies,data=data)
        else:response = requests.post(f"{self.api}/g/s/blog/{blogId}/comment/{commentId}/vote?cv=1.2&value=1", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if wikiId:data["eventSource"] = "PostDetailView"
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/item/{wikiId}/comment/{commentId}/g-vote?cv=1.2&value=1", headers=self.headers_lib(),proxies=self.proxies,data=data)
        else:response = requests.post(f"{self.api}/g/s/item/{wikiId}/comment/{commentId}/g-vote?cv=1.2&value=1", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def unlike_blog(self, blogId: str = None, wikiId: str = None,comId: int=None):
        if blogId:
        	if comId:response = requests.delete(f"{self.api}/x{comId}/s/blog/{blogId}/vote?eventSource=UserProfileView", headers=self.headers_lib(),proxies=self.proxies)
        	else:response = requests.delete(f"{self.api}/g/s/blog/{blogId}/vote?eventSource=UserProfileView", headers=self.headers_lib(),proxies=self.proxies)
        elif wikiId:
        	if comId:response = requests.delete(f"{self.api}/x{comId}/s/item/{wikiId}/vote?eventSource=PostDetailView", headers=self.headers_lib(),proxies=self.proxies)
        	else:response = requests.delete(f"{self.api}/g/s/item/{wikiId}/vote?eventSource=PostDetailView", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def post_blog(self, title: str, content: str, imageList: list = None, captionList: list = None, categoriesList: list = None, backgroundColor: str = None, fansOnly: bool = False, extensions: dict = None, crash: bool = False,comId: int=None):
        mediaList = []
        if captionList is not None:
            for image, caption in zip(imageList, captionList):
                mediaList.append([100, self.upload_media(image, type="image"), caption])
        else:
            if imageList is not None:
                for image in imageList:
                    print(self.upload_media(image, "image"))
                    mediaList.append([100, self.upload_media(image, "image"), None])
        data = {"address": None,"content": content,"title": title,"deviceID": self.devgener(),"mediaList": mediaList,"extensions": extensions,"latitude": 0,"longitude": 0,"eventSource": "GlobalComposeMenu","timestamp": int(time()  * 1000)}
        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if categoriesList: data["taggedBlogCategoryIdList"] = categoriesList
        data = json.dumps(data)
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/blog", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def post_wiki(self, title: str, content: str, icon: str = None, imageList: list = None, keywords: str = None, backgroundColor: str = None, fansOnly: bool = False,comId: int=None):
        mediaList = []
        for image in imageList:
            mediaList.append([100, self.upload_media(image, "image"), None])
        data = {"label": title,"content": content,"mediaList": mediaList,"deviceID": self.devgener(),"eventSource": "GlobalComposeMenu","timestamp": int(time()  * 1000)}
        if icon: data["icon"] = icon
        if keywords: data["keywords"] = keywords
        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        data = json.dumps(data)
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/item", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def edit_profile(self, nickname: str = None, content: str = None, icon: BinaryIO = None, backgroundColor: str = None, backgroundImage: str = None, defaultBubbleId: str = None,comId: int=None):
        data = {"address": None,"latitude": 0,"longitude": 0,"mediaList": None,"eventSource": "UserProfileView","timestamp": int(time()  * 1000)}
        if nickname: data["nickname"] = nickname
        if icon: data["icon"] = self.upload_media(icon, "image")
        if content: data["content"] = content
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if backgroundImage: data["extensions"] = {"style": {"backgroundMediaList": [[100, backgroundImage, None, None, None]]}}
        if defaultBubbleId: data["extensions"] = {"defaultBubbleId": defaultBubbleId}
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/user-profile/{self.userId}", headers=self.headers_lib(),proxies=self.proxies,data=data)
        else:response = requests.post(f"{self.api}/g/s/user-profile/{self.userId}", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()
    def get_invite_codes(self,comId: int, status: str = "normal", start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/g/s-x{comId}/community/invitation?status={status}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["communityInvitation"]
    def generate_invite_code(self,comId:int, duration: int = 0, force: bool = True):
        data = json.dumps({"duration": duration,"force": force,"timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/g/s-x{comId}/community/invitation", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["communityInvitation"]
    def review_quiz_questions(self,comId: int, quizId: str):
        response = requests.get(f"{self.api}/x{comId}/s/blog/{quizId}?action=review", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.QuizQuestionList(response.json()["blog"]["quizQuestionList"]).QuizQuestionList
    def get_recent_quiz(self, comId: int,start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/blog?type=quizzes-recent&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.BlogsList(response.json()["blogList"]).BlogsList
    def get_trending_quiz(self, comId: int,start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/feed/quiz-trending?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.BlogsList(response.json()["blogList"]).BlogsList
    def get_best_quiz(self, comId: int,start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/feed/quiz-best-quizzes?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.BlogsList(response.json()["blogList"]).BlogsList
    def ban(self, comId: int,userId: str, reason: str, banType=2):
        data = json.dumps({"reasonType": banType,"note": {"content": reason},"timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/user-profile/{userId}/ban", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()

    def unban(self, userId: str, reason: str,comId: int):
        data = json.dumps({"note": {"content": reason},"deviceID": self.devgener(),"timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/user-profile/{userId}/unban", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_chat_users(self, comId: int,chatId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.UserProfileList(response.json()["memberList"]).UserProfileList
    def get_public_chat_threads(self, comId: int,type: str = "recommended", start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.ChatThreads(response.json()["threadList"]).ChatThreads
    def play_quiz_raw(self,comId: int, quizId: str, quizAnswerList: list, quizMode: int = 0):
        data = json.dumps({"mode": quizMode,"quizAnswerList": quizAnswerList,"deviceID": self.devgener(),"timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/blog/{quizId}/quiz/result", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def play_quiz(self, quizId: str,comId: int, questionIdsList: list, answerIdsList: list, quizMode: int = 0):
        quizAnswerList = []
        for question, answer in zip(questionIdsList, answerIdsList):
            part = json.dumps({"optIdList": [answer],"quizQuestionId": question,"timeSpent": 0.0})
            quizAnswerList.append(json.loads(part))
        data = json.dumps({"mode": quizMode,"quizAnswerList": quizAnswerList,"deviceID": self.devgener(),"timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/blog/{quizId}/quiz/result", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def delete_invite_code(self, inviteId: str,comId: int):
        response = requests.delete(f"{self.api}/g/s-x{comId}/community/invitation/{inviteId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def edit_blog(self, comId: int,blogId: str, title: str = None, content: str = None, imageList: list = None, categoriesList: list = None, backgroundColor: str = None, fansOnly: bool = False):
        mediaList = []
        for image in imageList:
            mediaList.append([100, self.upload_media(image, "image"), None])
        data = {"address": None,"mediaList": mediaList,"latitude": 0,"longitude": 0,"eventSource": "PostDetailView","timestamp": int(time()  * 1000)}
        if title: data["title"] = title
        if content: data["content"] = content
        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if categoriesList: data["taggedBlogCategoryIdList"] = categoriesList
        data = json.dumps(data)
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/blog/{blogId}", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def delete_blog(self, comId: int,blogId: str):
        response = requests.delete(f"{self.api}/x{comId}/s/blog/{blogId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def delete_wiki(self,comId: int, wikiId: str):
        response = requests.delete(f"{self.api}/x{comId}/s/item/{wikiId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def repost_blog(self, comId: int,content: str = None, blogId: str = None, wikiId: str = None):
        if blogId is not None: refObjectId, refObjectType = blogId, 1
        elif wikiId is not None: refObjectId, refObjectType = wikiId, 2
        else: raise exceptions.SpecifyType()
        data = json.dumps({"content": content,"refObjectId": refObjectId,"refObjectType": refObjectType,"type": 2,"timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/blog", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def check_in(self, comId: int,tz: int = -timezone // 1000):
        data = json.dumps({"timezone": tz,"timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/check-in", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def lottery(self, comId: int,tz: int = -timezone // 1000):
        data = json.dumps({"timezone": tz,"timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/check-in/lottery", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()

    def vote_poll(self, blogId: str,comId: int, optionId: str):
        data = json.dumps({"value": 1,"eventSource": "PostDetailView","timestamp": int(time()  * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/blog/{blogId}/poll/option/{optionId}/vote", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()   
    def delete_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None,comId: int=None):
        if userId:
        	if comId:response = requests.delete(f"{self.api}/x{comId}/s/user-profile/{userId}/g-comment/{commentId}", headers=self.headers_lib(),proxies=self.proxies)
        	else:response = requests.delete(f"{self.api}/g/s/user-profile/{userId}/g-comment/{commentId}", headers=self.headers_lib(),proxies=self.proxies)
        elif blogId:
        	if comId:response = requests.delete(f"{self.api}/x{comId}/s/blog/{blogId}/g-comment/{commentId}", headers=self.headers_lib(),proxies=self.proxies)
        	else:response = requests.delete(f"{self.api}/g/s/blog/{blogId}/g-comment/{commentId}", headers=self.headers_lib(),proxies=self.proxies)
        elif wikiId:
        	if comId:response = requests.delete(f"{self.api}/x{comId}/s/item/{wikiId}/g-comment/{commentId}", headers=self.headers_lib(),proxies=self.proxies)
        	else:response = requests.delete(f"{self.api}/g/s/item/{wikiId}/g-comment/{commentId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def subscribe(self, userId: str,comId: int,autoRenew: str = False, transactionId: str = None):
        if transactionId is None: transactionId = str(UUID(hexlify(urandom(16)).decode('ascii')))
        data = json.dumps({"paymentContext": {"transactionId": transactionId,"isAutoRenew": autoRenew},"timestamp": int(time()  * 1000),"deviceID": self.devgener()})       
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/influencer/{userId}/subscribe", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def add_linked_community(self, comId: str):
        response = requests.post(f"{self.api}/g/s/user-profile/{self.userId}/linked-community/{comId}",headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()

    def invite_to_chat(self, userId: Union[str, list], chatId: str,comId:int=None):
        if isinstance(userId, str): userIds = [userId]
        elif isinstance(userId, list): userIds = userId
        data = json.dumps({"uids": userIds,"timestamp": int(time()  * 1000)})
        if comId:
        	self.sig(data)
        	response =requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/member/invite",headers=self.headers_lib(),proxies=self.proxies,data=data)
        else:
        	self.sig(data)
        	response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/member/invite", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else:return response.json()
    def remove_linked_community(self, comId: str):
        response = requests.delete(f"{self.api}/g/s/user-profile/{self.userId}/linked-community/{comId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:            	print(response.json()["api:message"])
        else:return response.json()
    def create_community(self, name: str, tagline: str, path, themeColor: str, joinType: int = 0, primaryLanguage: str = "ru"):
        data = json.dumps({
            "icon": {
                "height": 512.0,
                "imageMatrix": [1.6875, 0.0, 108.0, 0.0, 1.6875, 497.0, 0.0, 0.0, 1.0],
                "path": path,
                "width": 512.0,
                "x": 0.0,
                "y": 0.0
            },
            "joinType": joinType,
            "name": name,
            "primaryLanguage": primaryLanguage,
            "tagline": tagline,
            "templateId": 9,
            "themeColor": themeColor,
            "timestamp": int(time()  * 1000)
        })
        self.sig(data)
        response = requests.post(f"{self.api}/g/s/community", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()

    def delete_community(self, comId:str,email: str, password: str, verificationCode: str):
        data = json.dumps({"secret": f"0 {password}","validationContext": {"data": {"code": verificationCode},"type": 1,"identity": email},"deviceID": self.devgener()})
        self.sig(data)
        response = requests.post(f"{self.api}/g/s-x{comId}/community/delete-request", headers=self.headers_lib(),proxies=self.proxies,data=data)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()

    def get_user_wikis(self, comId:str,userId: str, start: int = 0, size: int = 25):
        response =requests.get(f"{self.api}/x{comId}/s/item?type=user-all&start={start}&size={size}&cv=1.2&uid={userId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.BlogsList(response.json()["itemList"]).BlogsList
    def get_wall_comments(self, userId: str, sorting: str, start: int = 0, size: int = 25,comId:int=None):
        if sorting.lower() == "newest": sorting = "newest"
        elif sorting.lower() == "oldest": sorting = "oldest"
        elif sorting.lower() == "top": sorting = "vote"
        if comId:response = requests.get(f"{self.api}/x{comId}/s/user-profile/{userId}/g-comment?sort={sorting}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.get(f"{self.api}/g/s/user-profile/{userId}/g-comment?sort={sorting}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else:
            return objects.CommentList(response.json()["commentList"]).CommentList
    def edit_community(self, comId,name: str = None, description: str = None, aminoId: str = None, primaryLanguage: str = None, themePackUrl: str = None):
        data = {"timestamp": int(time()  * 1000)}
        if name: data["name"] = name
        if description: data["content"] = description
        if aminoId: data["endpoint"] = aminoId
        if primaryLanguage: data["primaryLanguage"] = primaryLanguage
        if themePackUrl: data["themePackUrl"] = themePackUrl
        data = json.dumps(data)
        self.sig(data)
        response =  requests.post(f"{self.api}/x{comId}/s/community/settings", data=data, headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_from_device_id(self, deviceId: str):
    	response = requests.get(f"{self.api}/g/s/auid?deviceId={deviceId}",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def accept_host(self,chatId: str,comId: int=None):
    	data = json.dumps({"timestamp": int(time() * 1000)})
    	self.sig(data)
    	if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/accept-organizer",data=data,headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/accept-organizer",data=data,headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def get_notifications(self, comId: int=None, start: int = 0, size: int = 10):
    	if comId:response = requests.get(f"{self.api}/x{comId}/s/notification?start={start}&size={size}",headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.get(f"{self.api}/g/s/notification?start={start}&size={size}",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def check_deviceId(self, deviceId: str):
        data = json.dumps({"deviceID": deviceId,"bundleID": "com.narvii.amino.master","clientType": 100,"timezone": -int(timezone) // 1000,"systemPushEnabled": True,"locale": locale()[0],"timestamp": int(time() * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/g/s/device",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_wallet_info(self):
        response = requests.get(f"{self.api}/g/s/wallet",headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_wallet_history(self,start: int = 0,size: int = 25):
    	response = requests.get(f"{self.api}/g/s/wallet/coin/history?start={start}&size={size}",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def transfer_host(self,chatId: str,userIds: list,comId: int=None):
        data = json.dumps({"uidList": userIds,"timestamp": int(time() * 1000)})
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/transfer-organizer",data=data,headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/transfer-organizer",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def create_sticker_pack(self,comId: int,name: str,stickers: list):
        data = json.dumps({"collectionType": 3,"description": "sticker_pack","iconSourceStickerIndex": 0,"name": name,"stickerList": stickers,"timestamp": int(time() * 1000)})
        self.sig(data)
        response= requests.post(f"{self.api}/x{comId}/s/sticker-collection",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def search_user_chat(self,userId: str,comId: int=None):
    	if comId:response = requests.get(f"{self.api}/x{comId}/s/chat/thread?type=exist-single&cv=1.2&q={userId}",headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.get(f"{self.api}/g/s/chat/thread?type=exist-single&cv=1.2&q={userId}",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return objects.MembersList(response.json()["userProfileList"]).MembersList
    def change_vc_permission(self,chatId: str,permission: int,comId: int=None):
        data = json.dumps({"vvChatJoinType": permission,"timestamp": int(time() * 1000)})
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/vvchat-permission",data=data,headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/vvchat-permission",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_moderation_history(self,comId:int,userId:str=None,wikiId:str=None,blogId:str=None,quizId:str=None,fileId:str=None,size:int=100):
    	if fileId:response = requests.get("{self.api}/x{comId}/s/admin/operation?objectId={fileId}&objectType=109&pagingType=t&size={size}",headers=self.headers_lib(),proxies=self.proxies)
    	if userId:response = requests.get(f"{self.api}/x{comId}/s/admin/operation?objectId={userId}&objectType=0&pagingType=t&size={size}",headers=self.headers_lib(),proxies=self.proxies)
    	if blogId:response =requests.get(f"{self.api}/x{comId}/s/admin/operation?objectId={blogId}&objectType=1&pagingType=t&size={size}",headers=self.headers_lib(),proxies=self.proxies)
    	if quizId:response = requests.get(f"{self.api}/x{comId}/s/admin/operation?objectId={quiz_id}&objectType=1&pagingType=t&size={size}",headers=self.headers_lib(),proxies=self.proxies)
    	if wikiId:response = requests.get(f"{self.api}/x{comId}/s/admin/operation?objectId={wikiId}&objectType=2&pagingType=t&size={size}",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def moderation_history_community(self, comId: int, size: int = 25):
    	response = requests.get(f"{self.api}/x{comId}/s/admin/operation?objectId={wikiId}&objectType=2&pagingType=t&size={size}",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def repost_blog(self,comId: int,content: str = None,blogId: str = None,wikiId: str = None):
        if blogId:
            ref_object_id = blogId
            ref_object_type = 1
        elif wikiId:
            ref_object_id = wikiId,
            ref_object_type = 2
        data = json.dumps({"content": content,"refObjectId": ref_object_id,"refObjectType": ref_object_type,"type": 2,"timestamp": int(time() * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/blog",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def change_password(self,password: str,new_password: str):
        data = json.dumps({"secret": f"0 {password}","updateSecret": f"0 {new_password}","validationContext": None,"deviceID": self.devgener()})
        self.sig(data)
        response = requests.post(f"{self.api}/g/s/auth/change-password",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_blog_info(self,blogId: str,wikiId:str,comId: int):
    	if comId:
    		if blogId:response = requests.get(f"{self.api}/x{comId}/s/blog/{blogId}",headers=self.headers_lib(),proxies=self.proxies)
    		if wikiId:response = requests.get(f"{self.api}/x{comId}/s/item/{wikiId}",headers=self.headers_lib(),proxies=self.proxies)
    	else:
    		if blogId:response = requests.get(f"{self.api}/g/s/blog/{blogId}",headers=self.headers_lib(),proxies=self.proxies)
    		if wikiId:response = requests.get(f"{self.api}/x{comId}/s/item/{wikiId}",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def report(self,reason: str,flag_Type: int,userId: str = None,blogId: str = None,wikiId: str = None,chatId: str = None,comId:int=None):
    	data={"flagType": flag_Type,"message": reason,"timestamp": int(time() * 1000)}
    	if userId:data["objectId"] = userId;data["objectType"] = 0
    	if blogId:data["objectId"] = blogId;data["objectType"] = 1
    	if wikiId:data["objectId"] = wikiId;data["objectType"] = 2
    	if chatId:data["objectId"] = chatId;data["objectType"] = 12
    	else:data["objectId"] = comId;data["objectType"] = 16
    	data = json.dumps(data)
    	self.sig(data)
    	if comId:response = requests.post(f"{self.api}/x{comId}/s/flag", data=data,headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.post(f"{self.api}/g/s/flag", data=data,headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def read_only_mode(self, userId: str, comId:int,time: int, title: str = None, reason: str = None):
    	if time == 1: time = 86400
    	elif time == 2: time = 10800
    	elif time == 3: time = 21600
    	elif time == 4: time = 43200
    	elif time == 5: time = 86400
    	data = json.dumps({"uid": userId,"title": title,"content": reason,"attachedObject": {"objectId": userId,"objectType": 0},"penaltyType": 1,"penaltyValue": time,"adminOpNote": {},"noticeType": 4,"timestamp": int(time() * 1000)})
    	self.sig(data)
    	response = requests.post(f"{self.api}/x{comId}/s/notice",data=data,headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def reject_join_request(self, userId: str,comId:int):
    	data=json.dumps({})
    	self.sig(data)
    	response = requests.post(f"{self.api}/x{comId}/s/community/membership-request/{userId}/reject",data=data,headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def accept_join_request(self, userId: str,comId:int):
    	data=json.dumps({})
    	self.sig(data)
    	response = requests.post(f"{self.api}/x{comId}/s/community/membership-request/{userId}/accept",data=data,headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def block_user(self,userId: str):
    	response = requests.post(f"{self.api}/g/s/block/{userId}",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def unblock_user(self,userId: str):
    	response = requests.delete(f"{self.api}/g/s/block/{userId}",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def promote(self, userId: str, rank: str,comId:int):
    	rank = rank.lower().replace("agent", "transfer-agent")
    	response = requests.post(f"{self.api}/x{comId}/s/user-profile/{userId}/{rank}",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def get_join_requests(self, comId:int,start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/community/membership-request?status=pending&start={start}&size={size}",headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def warn(self, userId: str,comId:int,reason: str = None):
    	data = json.dumps({"uid": userId,"title": "Custom","content": reason,"attachedObject": {"objectId": userId,"objectType": 0},"penaltyType": 0,"adminOpNote": {},"noticeType": 7,"timestamp": int(time() * 1000)})
    	self.sig(data)
    	response = requests.post(f"{self.api}/x{comId}/s/notice",data=data,headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def link_translation(self,comId:int=None,userId: str = None,blogId: str = None,wikiId: str = None,chatId: str = None):
        data ={"targetCode": 1,"timestamp": int(time() * 1000)}
        if userId:
            data["objectId"] = userId
            data["objectType"] = 0
        if blogId:
            data["objectId"] = blogId
            data["objectType"] = 1
        if wikiId:
            data["objectId"] = wikiId
            data["objectType"] = 2
        if chatId:
            data["objectId"] = chatId
            data["objectType"] = 12
        data = json.dumps(data)
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/g/s-x{comId}/link-resolution",data=data,headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/link-resolution",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def watch_ad(self):
        response = requests.post(f"{self.api}/g/s/wallet/ads/video/start",headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def upload_themepack_raw(self,comId:int, file: BinaryIO):
    	self.sig(json.dumps({"timestamp": int(time()  * 1000),"deviceID": self.devgener()}))
    	response = requests.post(f"{self.api}/x{comId}/s/media/upload/target/community-theme-pack", data=file.read(), headers=self.headers_lib,proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def reject_wiki_request(self, requestId: str,comId:int):
        data = json.dumps({})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/knowledge-base-request/{requestId}/reject",data=data,headers=self.headers_lib,proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def visit_user(self,userId: str,comId:int=None):
    	if comId:response=requests.get(
            f"{self.api}/x{comId}/s/user-profile/{userId}?action=visit",headers=self.headers_lib(),proxies=self.proxies)
    	else:response=requests.get(
            f"{self.api}/g/s/user-profile/{userId}?action=visit",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def get_user_checkins(self, comId:int,userId: str):
        response = requests.get(f"{self.api}/x{comId}/s/check-in/stats/{userId}?timezone={-timezone // 1000}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def claim_vc_reputation(self,chatId: str,comId:int=None):
        if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/avchat-reputation", headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/avchat-reputation", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_user_visitors(self,userId: str,comId:int=None, start: int = 0, size: int = 25):
        if comId:response = requests.get(f"{self.api}/x{comId}/s/user-profile/{userId}/visitors?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.get(f"{self.api}/g/s/user-profile/{userId}/visitors?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def mark_as_read(self, chatId: str, messageId: str,comId:int=None):
    	data = json.dumps({"messageId": messageId,"timestamp": int(time() * 1000)})
    	self.sig(data)
    	if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/mark-as-read",data=data,headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/mark-as-read", data=data,headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def buy_bubble(self, bubbleId: str,comId: int=None):
    	data = json.dumps({"objectId": bubbleId,"objectType": 116,"v": 1,"timestamp": int(time() * 1000)})
    	self.sig(data)
    	if comId:response = requests.post(f"{self.api}/x{comId}/s/store/purchase", data=data,headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.post(f"{self.api}/g/s/store/purchase", data=data,headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def invite_to_vc(self,chatId: str,userId: str,comId: int=None):
        data = json.dumps({"uid": userId})
        self.sig(data)
        if comId:response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/vvchat-presenter/invite",data=data, headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/vvchat-presenter/invite",data=data, headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def delete_notification(self,notificationId: str,comId: int=None):
    	if comId:response=requests.delete(f"{self.api}/x{comId}/s/notification/{notificationId}",headers=self.headers_lib(), proxies=self.proxies)
    	else: response=requests.delete(f"{self.api}/g/s/notification/{notificationId}",headers=self.headers_lib(), proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def get_vip_users(self,comId):
        response = requests.get(f"{self.api}/{comId}/s/influencer", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.MembersList(response.json()["userProfileList"]).MembersList
    def clear_notifications(self,comId:int=None):
    	if comId:response = requests.delete(f"{self.api}/x{comId}/s/notification",headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.delete(f"{self.api}/g/s/notification",headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def delete_chat(self, chatId: str,comId:int=None):
    	if comId:response = requests.delete(f"{self.api}/x{comId}/s/chat/thread/{chatId}", headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.delete(f"{self.api}/g/s/chat/thread/{chatId}", headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def get_leaderboard_info(self, comId:int,type: str, start: int = 0, size: int = 25):
        if "24" in type or "hour" in type: response = requests.get(f"{self.api}/g/s-x{comId}/community/leaderboard?rankingType=1&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        elif "7" in type or "day" in type: response = requests.get(f"{self.api}/g/s-x{comId}/community/leaderboard?rankingType=2&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        elif "rep" in type: response = requests.get(f"{self.api}/g/s-x{comId}/community/leaderboard?rankingType=3&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        elif "check" in type: response = requests.get(f"{self.api}/g/s-x{comId}/community/leaderboard?rankingType=4", headers=self.headers_lib(),proxies=self.proxies)
        elif "quiz" in type: response = requests.get(f"{self.api}/g/s-x{comId}/community/leaderboard?rankingType=5&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.MembersList(response.json()["userProfileList"]).MembersList
    def get_blog_comments(self, comId:int,blogId: str = None, wikiId: str = None, fileId: str = None, sorting: str = "newest", start: int = 0, size: int = 25):
        if sorting == "newest": sorting = "newest"
        elif sorting == "oldest": sorting = "oldest"
        elif sorting == "top": sorting = "vote"
        if blogId:response = requests.get(f"{self.api}/x{comId}/s/blog/{blogId}/comment?sort={sorting}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        elif wikiId: response = requests.get(f"{self.api}/x{comId}/s/item/{wikiId}/comment?sort={sorting}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        elif fileId: response = requests.get(f"{self.api}/x{comId}/s/shared-folder/files/{fileId}/comment?sort={sorting}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.CommentList(response.json()["commentList"]).CommentList
    def hide(self, comId:int,userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None,fileId: str = None, reason: str = None):
        data = {"adminOpNote": {"content": reason},"timestamp": int(time() * 1000)}
        if userId:
            data["adminOpName"] = 18
            data = json.dumps(data)
            self.sig(data)
            response =  requests.post(f"{self.api}/x{comId}/s/user-profile/{userId}/admin",data=data, headers=self.headers_lib(),proxies=self.proxies)
        elif blogId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
            data = json.dumps(data)
            self.sig(data)
            response =  requests.post(f"{self.api}/x{comId}/s/blog/{blogId}/admin",data=data, headers=self.headers_lib(),proxies=self.proxies)
        elif wikiId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
            data = json.dumps(data)
            self.sig(data)
            response = requests.post(f"{self.api}/x{comId}/s/item/{wikiId}/admin",data=data, headers=self.headers_lib(),proxies=self.proxies)
        elif chatId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
            data = json.dumps(data)
            self.sig(data)
            response =  requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/admin",data=data, headers=self.headers_lib(),proxies=self.proxies)
        elif fileId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 9
            data = json.dumps(data)
            self.sig(data)
            response =  requests.post(f"{self.api}/x{comId}/s/shared-folder/files/{fileId}/admin",data=data, headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_blogs_by_category(self, categoryId: str,comId:int,start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/blog-category/{categoryId}/blog-list?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.BlogsList(response.json()["blogList"]).BlogsList
    def unhide(self, comId:int, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None, fileId: str = None, reason: str = None):
        data = {"adminOpNote": {"content": reason},"timestamp": int(time() * 1000)}
        if userId:
            data["adminOpName"] = 19
            data = json.dumps(data)
            self.sig(data)
            response =  requests.post(f"{self.api}/x{comId}/s/user-profile/{userId}/admin",data=data, headers=self.headers_lib(),proxies=self.proxies)
        elif blogId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0
            data = json.dumps(data)
            self.sig(data)
            response =  requests.post(f"{self.api}/x{comId}/s/blog/{blogId}/admin",data=data, headers=self.headers_lib(),proxies=self.proxies)
        elif wikiId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0
            data = json.dumps(data)
            self.sig(data)
            response =  requests.post(f"{self.api}/x{comId}/s/item/{wikiId}/admin",data=data, headers=self.headers_lib(),proxies=self.proxies)
        elif chatId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0
            data = json.dumps(data)
            self.sig(data)
            response =  requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/admin",data=data, headers=self.headers_lib(),proxies=self.proxies)
        elif fileId:
            data["adminOpName"] = 110
            data["adminOpValue"] = 0
            data = json.dumps(data)
            self.sig(data)
            response =  requests.post(f"{self.api}/x{comId}/s/shared-folder/files/{fileId}/admin",data=data, headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def change_sidepanel_color(self,comId:int,color: str):
        data = json.dumps({"path": "appearance.leftSidePanel.style.iconColor","value": color,"timestamp": int(time() * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/community/configuration",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def apply_bubble(self,comId:int, bubbleId: str, chatId: str, applyToAll: bool = False):
        data = {"applyToAll": 0,"bubbleId": bubbleId,"threadId": chatId,"timestamp": int(time() * 1000)}
        if applyToAll is True:
            data["applyToAll"] = 1
        data = json.dumps(data)
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/chat/thread/apply-bubble",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_wiki_submissions(self, comId:int, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/knowledge-base-request?type=all&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["knowledgeBaseRequestList"]
    def get_vc_reputation_info(self, comId:int, chatId: str):
    	if comId:response = requests.get(f"{self.api}/x{comId}/s/chat/thread/{chatId}/avchat-reputation", headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.get(f"{self.api}/g/s/chat/thread/{chatId}/avchat-reputation", headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def accept_wiki_request(self, comId:int, requestId: str, destinationCategoryIdList: list):
    	data = json.dumps({"destinationCategoryIdList": destinationCategoryIdList,"actionType": "create","timestamp": int(time() * 1000)})
    	self.sig(data)
    	response = requests.post(f"{self.api}/x{comId}/s/knowledge-base-request/{requestId}/approve",data=data,headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()
    def submit_to_wiki(self, comId:int, wikiId: str, message: str):
        data = json.dumps({"message": message,"itemId": wikiId,"timestamp": int(time() * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/knowledge-base-request",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def search_users(self, nickname: str,comId:int=None ,start: int = 0, size: int = 25):
    	if comId:response = requests.get(f"{self.api}/x{comId}/s/user-profile?type=name&q={nickname}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.get(f"{self.api}/g/s/user-profile?type=name&q={nickname}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return objects.MembersList(response.json()["userProfileList"]).MembersList
    def get_tipped_users(self, comId: int, blogId: str = None, wikiId: str = None,chatId: str = None, start: int = 0, size: int = 25):
        if blogId:response = requests.get(f"{self.api}/x{comId}/s/blog/{blogId}/tipping/tipped-users-summary?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if wikiId:response = requests.get(f"{self.api}/x{comId}/s/item/{wikiId}/tipping/tipped-users-summary?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if chatId:response = requests.get(f"{self.api}/x{comId}/s/chat/thread/{chatId}/tipping/tipped-users-summary?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def create_wiki_category(self, comId: int, title: str, parentCategoryId: str, content: str = None):
        data = json.dumps({"content": content,"icon": None,"label": title,"mediaList": None,"parentCategoryId": parentCategoryId,"timestamp": int(time() * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/item-category",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def add_poll_option(self, blogId: str, question: str):
        data = json.dumps({"mediaList": None,"title": question,"type": 0,"timestamp": int(time() * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/blog/{blogId}/poll/option",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def feature(self, time: int, comId:int,userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None):
        if chatId:
            if time == 1: time = 3600
            if time == 1: time = 7200
            if time == 1: time = 10800
        else:
            if time == 1: time = 86400
            elif time == 2: time = 172800
            elif time == 3: time = 259200
        data = {"adminOpName": 114,"adminOpValue": {"featuredDuration": time},"timestamp": int(time() * 1000)}
        if userId:
            data["adminOpValue"] = {"featuredType": 4}
            data = json.dumps(data)
            self.sig(data)
            response = requests.post(f"{self.api}/x{comId}/s/user-profile/{userId}/admin",data=data,headers=self.headers_lib(),proxies=self.proxies)
        elif blogId:
            data["adminOpValue"] = {"featuredType": 1}
            data = json.dumps(data)
            self.sig(data)
            response = requests.post(f"{self.api}/x{comId}/s/blog/{blogId}/admin",data=data,headers=self.headers_lib(),proxies=self.proxies)
        elif wikiId:
            data["adminOpValue"] = {"featuredType": 1}
            data = json.dumps(data)
            self.sig(data)
            response = requests.post(f"{self.api}/x{comId}/s/item/{wikiId}/admin",data=data,headers=self.headers_lib(),proxies=self.proxies)
        elif chatId:
            data["adminOpValue"] = {"featuredType": 5}
            data = json.dumps(data)
            self.sig(data)
            response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/admin",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def unfeature(self, comId:int, userId: str = None, chatId: str = None, blogId: str = None, wikiId: str = None):
        data = {"adminOpName": 114,"adminOpValue": {},"timestamp": int(time() * 1000)}
        if userId:
            data["adminOpValue"] = {"featuredType": 0}
            data = json.dumps(data)
            self.sig(data)
            response = requests.post(f"{self.api}/x{comId}/s/user-profile/{userId}/admin",data=data,headers=self.headers_lib(),proxies=self.proxies)
        elif blogId:
            data["adminOpValue"] = {"featuredType": 0}
            data = json.dumps(data)
            self.sig(data)
            response = requests.post(f"{self.api}/x{comId}/s/blog/{blogId}/admin",data=data,headers=self.headers_lib(),proxies=self.proxies)
        elif wikiId:
            data["adminOpValue"] = {"featuredType": 0}
            data = json.dumps(data)
            self.sig(data)
            response = requests.post(f"{self.api}/x{comId}/s/item/{wikiId}/admin",data=data,headers=self.headers_lib(),proxies=self.proxies)
        elif chatId:
            data["adminOpValue"] = {"featuredType": 0}
            data = json.dumps(data)
            self.sig(data)
            response = requests.post(f"{self.api}/x{comId}/s/chat/thread/{chatId}/admin",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_hidden_blogs(self, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/feed/blog-disabled?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.BlogsList(response.json()["blogList"]).BlogsList
    def get_sticker_collection(self, collectionId: str,comId:int=None):
        if comId:response = requests.get(f"{self.api}/x{comId}/s/sticker-collection/{collectionId}?includeStickers=true", headers=self.headers_lib(),proxies=self.proxies)
        else:response = requests.get(f"{self.api}/g/s/sticker-collection/{collectionId}?includeStickers=true", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["stickerCollection"]
    def get_shared_folder_files(self, comId:int, type: str = "latest", start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/shared-folder/files?type={type}&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["fileList"]
    def edit_titles(self, userId: str, comId:int, titles: list, colors: list):
        tlt = []
        for titles, colors in zip(titles, colors):
            tlt.append({"title": titles, "color": colors})
        data = json.dumps({"adminOpName": 207,"adminOpValue": {"titles": tlt},"timestamp": int(time() * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/user-profile/{userId}/admin",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_shared_folder_info(self,comId:int):
        response = requests.get(f"{self.api}/x{comId}/s/shared-folder/stats", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["stats"]
    def add_to_favorites(self, comId:int, userId: str):
        response = requests.post(f"{self.api}/x{comId}/s/user-group/quick-access/{userId}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_promotion(self, comId:int, noticeId: str, type: str = "accept"):
        response = requests.post(f"{self.api}/x{comId}/s/notice/{noticeId}/{type}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_user_achievements(self, comId: int, userId: str):
        response = requests.get(f"{self.api}/x{comId}/s/user-profile/{userId}/achievements", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["achievements"]
    def get_influencer_fans(self, comId:int,userId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/influencer/{userId}/fans?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def reorder_featured_users(self,comId:int, userIds: list):
        data = json.dumps({"uidList": userIds,"timestamp": int(time() * 1000)})
        self.sig(data)
        response = requests.post(f"{self.api}/x{comId}/s/user-profile/featured/reorder",data=data,headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_saved_blogs(self,comId:int,start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/bookmark?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["bookmarkList"]
    def get_community_stickers(self,comId:int):
        response = requests.get(f"{self.api}/x{comId}/s/sticker-collection?type=community-shared", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_store_stickers(self, comId:int, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/store/items?sectionGroupId=sticker&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_store_chat_bubbles(self, comId:int, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/store/items?sectionGroupId=chat-bubble&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_recent_wiki_items(self, comId:int,start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/item?type=catalog-all&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return objects.BlogsList(response.json()["itemList"]).BlogsList
    def get_wiki_categories(self, comId:int, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/item-category?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["itemCategoryList"]
    def get_wiki_category(self, comId: int, categoryId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/item-category/{categoryId}?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_notifications(self, comId: int=None, start: int = 0, size: int = 25):
    	if comId:response = requests.get(f"{self.api}/x{comId}/s/notification?pagingType=t&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
    	else:response = requests.get(f"{self.api}/g/s/notification?pagingType=t&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
    	if response.status_code != 200:print(response.json()["api:message"])
    	else: return response.json()["notificationList"]
    def get_blog_categories(self, comId: int, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/blog-category?size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["blogCategoryList"]
    def get_quiz_rankings(self, comId: int, quizId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/blog/{quizId}/quiz/result?start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()
    def get_notices(self, comId: int, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/x{comId}/s/notice?type=usersV2&status=1&start={start}&size={size}", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["noticeList"]
    def get_sticker_pack_info(self, comId: int, sticker_pack_id: str):
        response = requests.get(f"{self.api}/x{comId}/s/sticker-collection/{sticker_pack_id}?includeStickers=true", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["stickerCollection"]
    def get_sticker_packs(self, comId: int):
        response = requests.get(f"{self.api}/x{comId}/s/sticker-collection?includeStickers=false&type=my-active-collection", headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()["stickerCollection"]
    def claim_new_user_coupon(self):
        response = requests.post(f"{self.api}/g/s/coupon/new-user-coupon/claim",headers=self.headers_lib(),proxies=self.proxies)
        if response.status_code != 200:print(response.json()["api:message"])
        else: return response.json()