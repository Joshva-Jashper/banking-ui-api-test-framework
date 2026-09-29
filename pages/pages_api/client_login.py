class UserLogin:
    def __init__(self,api_client):
        self.api_client = api_client

    def CreateLogin(self,UserName,Password,remember = False):
        return self.api_client.post(endpoint = "/login",params = {"username" : UserName,"password" : Password,"remember" : remember})