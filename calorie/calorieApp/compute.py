import pandas as pd
import numpy as np



#data=pd.read_csv(r'C:\Users\i310thgeN\Documents\webpage\djangoproject\calorie\calorieApp\calories.csv')
data=pd.read_csv(r'C:/Users/i310thgeN/Documents/webpage/djangoproject/calorie/calorieApp/Book 4.csv'  , encoding='cp1252',skipinitialspace = True)

#print(data.columns)

item=data["FoodItem"].tolist()
calorie=data['calories'].tolist()
data.set_index('unit', inplace=True)

combined=data.values.tolist()
#print(combined)
def return_unit(item):
    item=str(item)
    unit=data.index[data['FoodItem'] == item.title()][0]
    if str(unit)=='gm': 
        unit_str='\t\t\t\t\t\t\tEnter Quantity Consumed in grams!!'
    else:
         unit_str=f'\t\t\t\t\t\t\t\t\Enter Number of {unit} consumed'
    return unit_str
def computation(item,quantity):
    
    for i in combined:
        if i[0]==item.title():
            calorie=int(i[1])/int(i[2])
            #print("calorie",calorie)
            #print(quantity)
            result=calorie*quantity
            break
        else:
            result='item not found'
    return result
def foods():
    return item


def calorie_computation(gender,age,height,weight,activity):
    if gender == 'F':
            BMR= 447.593 + (9.247 * weight) + (3.098 *height) - (4.330 * age)
    else:
            BMR= 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    if activity == '1':
         BMR*=1.2
    elif activity == '2':
         BMR*=1.375
    elif activity == '3':
         BMR*=1.55
    elif activity == '4':
         BMR*=1.725
    else:
         BMR*=1.9
    return BMR
    
#print(computation('idli',2))

def return_recepie(item):
    item=item.title()
    recepie= (data[data.FoodItem==item]['recepie']).values
    
    recepie_str= str(recepie[0])
    
    recepie_list=[i.strip() for i in recepie_str.split(';')]
    recepie_list.append('<br><br>')
    recepie_list.insert(0,'<h1 style="font-style: italic;color: darkgoldenrod;">Recipe</h1>')
    recepie_li='<br><br>'.join(recepie_list)
    return recepie_li

def return_ingrediant(item):
     ing=(data[data.FoodItem == item]['ingrediant']).values
     ing_str=str(",".join(ing))
     
     return ing_str

#print(return_recepie('poha'))
#print(return_ingrediant('Burger'))