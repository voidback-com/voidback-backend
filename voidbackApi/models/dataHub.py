from django.db import models
from .Account import Account
from .Post import Post





class DataHubAccount(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field="username")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    queries_left = models.BigIntegerField(default=10, blank=True) # 10 queries per day


    class Meta:
        indexes = [
            models.Index(fields=["account", 'created_at', "queries_left"])
        ]


    def __str__(self):
        return str(self.account.username)




class DataHubQuery(models.Model):

    query = models.TextField(default="none", blank=False) # ticker, hashtag, keyword etc...
    query_category = models.TextField(default="symbol", blank=True)
    query_startDate = models.DateField()
    query_endDate = models.DateField()
    includes_keywords = models.JSONField()
    query_results = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(DataHubAccount, on_delete=models.DO_NOTHING, null=True)


    class Meta:
        indexes = [
            models.Index(fields=["account", "query", 'created_at', "query_category", "query_startDate", "query_endDate", "includes_keywords", "query_results"])
        ]


    def __str__(self):
        return str(self.query_category)





class DataHubPositionPoll(models.Model):
    ticker = models.TextField()
    position = models.IntegerField(default=4) # neutral
    account = models.ForeignKey(DataHubAccount, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hash = models.TextField(unique=True)


    class Meta:
        indexes = [
            models.Index(fields=["account", "ticker", 'position', 'created_at'])
        ]


    def __str__(self):
        return str(self.ticker)



class DataHubFeedbackPoll(models.Model):
    ticker = models.TextField()
    position = models.IntegerField(default=4) # neutral
    account = models.ForeignKey(DataHubAccount, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hash = models.TextField(unique=True)
     

    class Meta:
        indexes = [
            models.Index(fields=["account", "ticker", 'position', 'created_at'])
        ]


    def __str__(self):
        return str(self.ticker)



'''
positions:

    1 = Buy and Sell (short-term)
    2 = Buy and Hold (long-term)
    3 = Short Sell
    4 = Neutral


feedbacks:

    1 = Actionabler information
    2 = Insightful information
    3 = Useless information
    4 = Neutral

'''
