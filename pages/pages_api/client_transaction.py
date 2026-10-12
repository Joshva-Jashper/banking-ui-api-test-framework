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
    
    def UpdateTransaction(self,TransactionId,Body):
        return self.apiClient.patch(endpoint = f"/transactions/{TransactionId}",data = Body)
    
    def GetOneTransaction(self, TransactionId):
        return self.apiClient.get(endpoint = f"/transactions/{TransactionId}")
    
    def GetTransactionFilterSatus(self,Status):
        return self.apiClient.get(endpoint = f"/transactions?status={Status}")
    
    def GetTransactionFilterRequestStatus(self,RequestStatus):
        return self.apiClient.get(endpoint = f"/transactions?reqestStatus={RequestStatus}")
    
    def GetTransactionFilterAmount(self,AmountMin,AmountMax):
        return self.apiClient.get(endpoint = f"/transactions?amountMin={AmountMin}&amountMax={AmountMax}")
    
    
