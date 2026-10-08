class BankAccount:

    def __init__(self,apiClient):
        self.apiClient = apiClient

    def AddBankAccount(self,bankBody):
        return self.apiClient.post(endpoint = "/bankAccounts", data = bankBody)

    def GetAllBankAccount(self):
        return self.apiClient.get(endpoint = "/bankAccounts")

    def GetbankAccountWithId(self,BankId):
        return self.apiClient.get(endpoint = f"/bankAccounts/{BankId}")    
    
    def DeleteBankAccountWithId(self,BankId):
        return self.apiClient.delete(endpoint = f"/bankAccounts/{BankId}")

    