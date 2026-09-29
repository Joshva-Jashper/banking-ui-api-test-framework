class ClientUser:
    def __init__(self,apiClient):
        self.apiClient = apiClient

    def CreateUser(self,body):
        return self.apiClient.post(endpoint = "/users", data = body)
