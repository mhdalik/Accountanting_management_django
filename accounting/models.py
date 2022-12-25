from django.db import models

# Create your models here.

class Entities(models.Model):
    entity_name = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(default=True)
    debit = models.IntegerField(blank=True,null=True)
    credit = models.IntegerField(blank=True,null=True)
    balance = models.IntegerField(blank=True,null=True)
    
    def __str__(self) -> str:
        return str(self.entity_name) 


class Account_names(models.Model):
    ac_name=models.CharField(max_length=30, null=True)
    is_loan_ac=models.BooleanField(default=False)
    entity=models.ForeignKey(Entities, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return str(self.ac_name) 
    

class Journal(models.Model):
    date = models.DateField()
    r_v_number = models.IntegerField(blank=True,null=True)
    item = models.CharField(max_length=20,blank=True,null=True,default='Not Given')
    account = models.ForeignKey(Account_names,on_delete=models.CASCADE)
    debit = models.IntegerField(null=True,blank=True)
    credit = models.IntegerField(null=True, blank=True)
    entity=models.ForeignKey(Entities, null=True, on_delete=models.SET_NULL)
    
    