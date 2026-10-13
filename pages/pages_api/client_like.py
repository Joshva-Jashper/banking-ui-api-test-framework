class ClientLike:
    def __init__(self,apiClient):
        self.apiClient = apiClient
        
    def AddLikeWithTransactionId(self,TransactionId):
        return self.apiClient.post(endpoint = f"/likes/{TransactionId}")
    
    def AddCommentWithTransactionId(self,TransactionId,Comment):
        return self.apiClient.post(endpoint = f"/comments/{TransactionId}",data = {"content" : f"{Comment}" })
    
    def AddCommentWithTransactionIdWithInvalidBody(self,TransactionId,Comment):
        return self.apiClient.post(endpoint = f"/comments/{TransactionId}",data = {"comment" : f"{Comment}" })
        