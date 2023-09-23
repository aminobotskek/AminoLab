class ChatThreads:
    def __init__(self, data):
        self.json = data
        self.title = []
        self.content = []
        self.chatId = []
        self.comId = []

    @property
    def ChatThreads(self):
        for thread in self.json:
        	try:	self.title.append(thread["title"])
        	except (KeyError, TypeError):	self.title.append(None)
        	try:	self.content.append(thread["content"])
        	except (KeyError, TypeError):	self.content.append(None)
        	try:	self.chatId.append(thread["threadId"])
        	except (KeyError, TypeError):	self.chatId.append(None)
        	try:	self.comId.append(thread["ndcId"])
        	except (KeyError, TypeError): self.comId.append(None)
        
        return self

class CommunityList:
    def __init__(self, data):
        self.json = data
        self.comId = []
        self.name = []
        self.link = []
        self.aminoId = []

    @property
    def CommunityList(self):
        for x in self.json:
            self.comId.append(x["ndcId"])
            self.name.append(x["name"])
            self.link.append(x["link"])
            self.aminoId.append(x["endpoint"])
            
        return self

class MembersList:
    def __init__(self, data):
        self.json = data
        self.nickname = []
        self.userId = []
        self.createdTime = []
        self.icon = []

    @property
    def MembersList(self):
        for x in self.json:
        	try:	self.nickname.append(x["nickname"])
        	except (KeyError, TypeError):	pass
        	try:	self.userId.append(x["uid"])
        	except (KeyError, TypeError):	pass
        	try:	self.createdTime.append(x["createdTime"])
        	except (KeyError, TypeError):	pass
        	try:	self.icon.append(x["icon"])
        	except (KeyError, TypeError):	pass

        return self

class FromCode:
	def __init__(self, data):
		self.json = data
		self.path=[]
		self.object_type=None
		self.short_code=None
		self.full_path=None
		self.target_code=None
		self.objectId=None
		self.short_url=None
		self.full_url=None
		self.comId=None
		self.ndcId=None

	@property
	def FromCode(self):
		try:	self.path = self.json["path"] 
		except (KeyError, TypeError): 	pass		
		try:	self.object_type = self.json["extensions"]["linkInfo"]["objectType"]
		except (KeyError, TypeError): 	pass
		try: 	self.short_code = self.json["extensions"]["linkInfo"]["shortCode"]
		except (KeyError, TypeError): 	pass
		try:	self.full_path = self.json["extensions"]["linkInfo"]["fullPath"]
		except (KeyError, TypeError):	pass
		try:	self.target_code = self.json["extensions"]["linkInfo"]["targetCode"]
		except (KeyError, TypeError):	pass
		try: 	self.objectId = self.json["extensions"]["linkInfo"]["objectId"]
		except (KeyError, TypeError):	pass
		try:	self.short_url = self.json["extensions"]["linkInfo"]["shareURLShortCode"]
		except (KeyError, TypeError):	pass
		try:	self.full_url = self.json["extensions"]["linkInfo"]["shareURLFullPath"]
		except (KeyError, TypeError):	pass
		try:self.ndcId=self.json["extensions"]["linkInfo"]["ndcId"]
		except (KeyError, TypeError): pass
		try: self.comId = self.ndcId or self.json["extensions"]["community"]["ndcId"]
		except (KeyError, TypeError): pass
		return self 

class UserInfo:
	def __init__(self, data):
		self.json = data
		self.aminoId = None 
		self.userId = None
		self.nickname = None
		self.content = None 
		self.icon = None 
		self.web_URL = None
		self.createdTime = None 
		self.modifiedTime = None

	@property
	def UserInfo(self):
		try:	self.aminoId = self.json["aminoId"]
		except (KeyError, TypeError): 	pass 
		try:	self.userId = self.json["uid"]
		except (KeyError, TypeError): 	pass 
		try:	self.nickname = self.json["nickname"]
		except (KeyError, TypeError): 	pass 
		try:	self.content = self.json["content"]
		except (KeyError, TypeError): 	pass 
		try:	self.icon = self.json["icon"]
		except (KeyError, TypeError): 	pass 
		try:	self.web_URL = self.json["webURL"]
		except (KeyError, TypeError): 	pass
		try:	self.createdTime = self.json["createdTime"]
		except (KeyError, TypeError): 	pass 
		try:	self.modifiedTime = self.json["modifiedTime"]
		except (KeyError, TypeError): 	pass 
		
		return self 
		
class BlogsList:
	def __init__(self, data):
		self.json = data
		self.wikiId=[]
		self.blogId = []
		self.title = []
		self.content = []
		self.comments_count = []
		self.createdTime = []
		self.modifiedTime = []
		
	@property
	def BlogsList(self):
		for blog in self.json:
			try: self.wikiId.append(blog["itemId"])
			except (KeyError, TypeError):	pass
			try:	self.blogId.append(blog["blogId"])
			except (KeyError, TypeError):	pass
			try:	self.title.append(blog["title"])
			except (KeyError, TypeError):	pass
			try:	self.content.append(blog["content"])
			except (KeyError, TypeError):	pass
			try:	self.comments_count.append(blog["commentsCount"])
			except (KeyError, TypeError):	pass
			try:	self.createdTime.append(blog["createdTime"])
			except (KeyError, TypeError):	pass
			try:	self.modifiedTime.append(blog["modifiedTime"])
			except (KeyError, TypeError):	pass

		return self
class QuizQuestionList:
    def __init__(self, data):
        _answersList = []

        self.json = data

        for y in data:
            try: _answersList.append(QuizAnswers(y["extensions"]["quizQuestionOptList"]).QuizAnswers)
            except (KeyError, TypeError): _answersList.append(None)

        self.status = []
        self.parentType = []
        self.title = []
        self.createdTime = []
        self.questionId = []
        self.parentId = []
        self.mediaList = []
        self.extensions = []
        self.style = []
        self.backgroundImage = []
        self.backgroundColor = []
        self.answerExplanation = []
        self.answersList = _answersList

    @property
    def QuizQuestionList(self):
        for x in self.json:
            try: self.status.append(x["status"])
            except (KeyError, TypeError): self.status.append(None)
            try: self.parentType.append(x["parentType"])
            except (KeyError, TypeError): self.parentType.append(None)
            try: self.title.append(x["title"])
            except (KeyError, TypeError): self.title.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.questionId.append(x["quizQuestionId"])
            except (KeyError, TypeError): self.questionId.append(None)
            try: self.parentId.append(x["parentId"])
            except (KeyError, TypeError): self.parentId.append(None)
            try: self.mediaList.append(x["mediaList"])
            except (KeyError, TypeError): self.mediaList.append(None)
            try: self.extensions.append(x["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try: self.style.append(x["extensions"]["style"])
            except (KeyError, TypeError): self.style.append(None)
            try: self.backgroundImage.append(x["extensions"]["style"]["backgroundMediaList"][0][1])
            except (KeyError, TypeError, IndexError): self.backgroundImage.append(None)
            try: self.backgroundColor.append(x["extensions"]["style"]["backgroundColor"])
            except (KeyError, TypeError): self.backgroundColor.append(None)
            try: self.answerExplanation.append(x["extensions"]["quizAnswerExplanation"])
            except (KeyError, TypeError): self.answerExplanation.append(None)

        return self

class ItemList:
    def __init__(self, data):
        self.json = data
        self.objectId = []
        self.imageUrl = []
        self.adCampaignId = []
        self.deepLink = []
        self.objectType = []
        self.scenarioType = []
        self.reqId = []
        self.adUnitId = []
        self.uiPos = []
    @property
    def ItemList(self):
        for x in self.json:
            try: self.objectId.append(x["objectId"])
            except (KeyError, TypeError): self.objectId.append(None)
            try: self.imageUrl.append(x["imageUrl"])
            except (KeyError, TypeError): self.imageUrl.append(None)
            try: self.adCampaignId.append(x["adCampaignId"])
            except (KeyError, TypeError): self.adCampaignId.append(None)
            try: self.deepLink.append(x["deepLink"])
            except (KeyError, TypeError): self.deepLink.append(None)
            try: self.objectType.append(x["objectType"])
            except (KeyError, TypeError): self.objectType.append(None)
            try: self.scenarioType.append(x["strategyInfo"]["scenarioType"])
            except (KeyError, TypeError): self.scenarioType.append(None)
            try: self.reqId.append(x["strategyInfo"]["reqId"])
            except (KeyError, TypeError): self.reqId.append(None)
            try: self.uiPos.append(x["strategyInfo"]["uiPos"])
            except (KeyError, TypeError): self.reqId.append(None)
            try: self.adUnitId.append(x["strategyInfo"]["adUnitId"])
            except (KeyError, TypeError): self.reqId.append(None)

        return self
class CommentList:
    def __init__(self, data):

        self.json = data
        self.votesSum = []
        self.votedValue = []
        self.mediaList = []
        self.parentComId = []
        self.parentId = []
        self.parentType = []
        self.content = []
        self.extensions = []
        self.comId = []
        self.modifiedTime = []
        self.createdTime = []
        self.commentId = []
        self.subcommentsCount = []
        self.type = []

    @property
    def CommentList(self):
        for x in self.json:
            try: self.votesSum.append(x["votesSum"])
            except (KeyError, TypeError): self.votesSum.append(None)
            try: self.votedValue.append(x["votedValue"])
            except (KeyError, TypeError): self.votedValue.append(None)
            try: self.mediaList.append(x["mediaList"])
            except (KeyError, TypeError): self.mediaList.append(None)
            try: self.parentComId.append(x["parentNdcId"])
            except (KeyError, TypeError): self.parentComId.append(None)
            try: self.parentId.append(x["parentId"])
            except (KeyError, TypeError): self.parentId.append(None)
            try: self.parentType.append(x["parentType"])
            except (KeyError, TypeError): self.parentType.append(None)
            try: self.content.append(x["content"])
            except (KeyError, TypeError): self.content.append(None)
            try: self.extensions.append(x["extensions"])
            except (KeyError, TypeError): self.extensions.append(None)
            try: self.comId.append(x["ndcId"])
            except (KeyError, TypeError): self.comId.append(None)
            try: self.modifiedTime.append(x["modifiedTime"])
            except (KeyError, TypeError): self.modifiedTime.append(None)
            try: self.createdTime.append(x["createdTime"])
            except (KeyError, TypeError): self.createdTime.append(None)
            try: self.commentId.append(x["commentId"])
            except (KeyError, TypeError): self.commentId.append(None)
            try: self.subcommentsCount.append(x["subcommentsCount"])
            except (KeyError, TypeError): self.subcommentsCount.append(None)
            try: self.type.append(x["type"])
            except (KeyError, TypeError): self.type.append(None)

        return self