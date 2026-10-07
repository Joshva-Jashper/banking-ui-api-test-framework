class UserContact:
    def __init__(self,apiClient):
        self.apiClient = apiClient

    def AddContacts(self,UserId):
        return self.apiClient.post(endpoint = "/contacts", data = {"contactUserId" : UserId})

    def GetContacts(self,UserName):
        return self.apiClient.get(endpoint = f"/contacts/{UserName}")    

    def DeleteContacts(self,ContactId):
        return self.apiClient.delete(endpoint = f"/contacts/{ContactId}")    