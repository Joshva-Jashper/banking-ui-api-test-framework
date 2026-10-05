class ClientUser:
    def __init__(self,apiClient):
        self.apiClient = apiClient

    def CreateUser(self,body):
        return self.apiClient.post(endpoint = "/users", data = body)

    def GetUser(self,UserId):
        return self.apiClient.get(endpoint=f"/users/{UserId}")

    def GetCheckAuth(self):
        return self.apiClient.get(endpoint = "/checkAuth")

    