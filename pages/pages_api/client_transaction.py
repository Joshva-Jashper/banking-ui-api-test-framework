class ClientTransaction:
    def __init__(self,apiClient):
        self.apiClient = apiClient
        
    
    def GetAllPublicTransaction(self):
        return self.apiClient.get(endpoint = "/transactions/public");
    
    def GetAllContactTransaction(self):
        return self.apiClient.get(endpoint = "/transactions/contacts")
    
    def GetTransaction(self):
        return self.apiClient.get(endpoint = "/transactions")
    
    def DoTransactionPayment(self,PaymentBody):
        return self.apiClient.post(endpoint = "/transactions",data = PaymentBody)
    
    def DoTransactionRequest(self,PaymentBody):
        return self.apiClient.post(endpoint = "/transactions", data = PaymentBody)
    
