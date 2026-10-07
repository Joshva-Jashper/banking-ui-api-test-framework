class ClientUser:
    def __init__(self,apiClient):
        self.apiClient = apiClient

    def CreateUser(self,body):
        return self.apiClient.post(endpoint = "/users", data = body)

    def GetUser(self,UserId):
        return self.apiClient.get(endpoint=f"/users/{UserId}")

    def GetCheckAuth(self):
        return self.apiClient.get(endpoint = "/checkAuth")

    def GetUserBySearch(self,keyword):
        return self.apiClient.get(endpoint = "/users/search",params={"q" : f'"{keyword}"'})

    def GetUserbySearchWithNoKeyWord(self): 
        return self.apiClient.get(endpoint = "/users/search")

    def UpdateUser(self,UserBody,UserId):
        return self.apiClient.patch(endpoint = f"/users/{UserId}", data = UserBody)
    
    def GetPublicUserProfile(self,UserName):
        return self.apiClient.get(endpoint = f"users/profile/{UserName}")
    