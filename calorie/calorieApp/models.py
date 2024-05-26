from django.db import models
from django.contrib.auth.models import User
from calorieApp.compute import computation,calorie_computation
from datetime import date
# Create your models here.

class UserDetails(models.Model):
    Gender_choices=(('M','Male'),('F','Female'))
    activity_choices=(('1','Little/No Exercise'),('2','light exercise/sports 1-3 days per week'),('3','moderate exercise/sports 3-5 days per week'),('4','hard exercise/sports 6-7 days per week'),('5','very hard exercise/sports & a physical job'))
    #name=models.ForeignKey(to=User,to_field='username', on_delete=models.CASCADE)
    name=models.OneToOneField(User,on_delete=models.CASCADE)
    age=models.IntegerField()
    height=models.DecimalField(max_digits=10,decimal_places=2)
    weight=models.DecimalField(max_digits=10,decimal_places=2)
    gender=models.CharField(max_length=30,choices=Gender_choices)
    calorie_needed=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    activity_factor=models.CharField(max_length=30,choices=activity_choices)

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        
        self.calorie_needed = calorie_computation(self.gender ,float(self.age),float(self.height),float(self.weight),self.activity_factor)
        print(self.calorie_needed)
        super(UserDetails, self).save(*args, **kwargs)


class AddItems(models.Model):
    meal_choices=(('breakfast','Breakfast'),('lunch','Lunch'),('snack','Snack'),('dinner','Dinner'))
    user=models.ForeignKey(to=User,to_field='username',on_delete=models.CASCADE)
    date=models.DateField(default=date.today)
    food=models.CharField(max_length=70)
    quantity=models.IntegerField()
    calorie=models.DecimalField(max_digits=30,decimal_places=2,blank=True,null=True)
    meal_time=models.CharField(max_length=40,choices=meal_choices)
    def save(self, *args, **kwargs):
        self.calorie = computation(self.food , self.quantity)
        print(self.calorie)
        super(AddItems, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)
