  
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity
import random

df = pd.read_csv("C:/Users/i310thgeN/Documents/webpage/djangoproject/calorie/calorieApp/Book 4.csv", encoding='cp1252')
df['calories'] = pd.to_numeric(df['calories'], errors='coerce')

vectorizer = CountVectorizer(tokenizer=lambda x: x.split(', '))
item_features = vectorizer.fit_transform(df['ingrediant'])
user_item_matrix = item_features.T

n_factors = 20
random_seed = random.randint(1, 100)

model = NMF(n_components=n_factors, init='random', random_state=random_seed)


def recommend_items(consumed_items, meal_type, n=5):
    cat_allow=[]
    
    top_recommendations = []
    if str(meal_type) =='Breakfast':
        cat_allow=['Breakfast', 'Fruit', ' Side Dish', 'Drink']
        
    elif str(meal_type)=="Lunch":
        cat_allow=['Lunch', 'Side Dish']
    elif str(meal_type)=='Snack':
        cat_allow=['Snack', 'Dessert']
    else:
        cat_allow=['Dinner', 'Side Dish']
    category_recc={cat: [] for cat in cat_allow}
    category_counts = {}
    meal_category_present = False

   

    if not consumed_items:
        top_indices=df.index.to_list()
        random.shuffle(top_indices)
    else:
        W = model.fit_transform(user_item_matrix)
        H = model.components_
        consumed_indices = [df.index[df['FoodItem'] == item].tolist() for item in consumed_items]
        consumed_indices = [index[0] for index in consumed_indices if index]

        if not consumed_indices:
            return []

        user_profile = np.mean(W[consumed_indices], axis=0)

        similarities = cosine_similarity(user_profile.reshape(1, -1), W)

        top_indices = similarities.argsort()[0, ::-1]
        random.shuffle(top_indices) 
    
    
    
    
 
    for index in top_indices:
        if (
            index < len(df)
            
            and any(  
                (meal_type == 'Breakfast' and cat in ['Breakfast', 'Fruit', ' Side Dish', 'Drink'])
                or (meal_type == 'Lunch' and cat in ['Lunch', 'Side Dish'])
                or (meal_type == 'Snack' and cat in ['Snack', 'Dessert'])
                or (meal_type == 'Dinner' and cat in ['Dinner', 'Side Dish'])
                for cat in df.loc[index, 'meal_time'].split(',')
            )
        ):
            
            cat_in=list(df.loc[index,'meal_time'].split(','))
            #print('cat_in',cat_in)
            for i in cat_in:
                if i not in category_counts and (i in cat_allow) and (df.loc[index,'FoodItem'] not in top_recommendations):
                    
                    category_counts[i]=1
                    top_recommendations.append((df.loc[index, 'FoodItem']))
                    
                    category_recc[i].append(df.loc[index, 'FoodItem'])
                elif i  in category_counts and category_counts[i]<3 and (i in cat_allow) and (df.loc[index,'FoodItem'] not in top_recommendations):
                    category_counts[i]+=1
                    top_recommendations.append((df.loc[index, 'FoodItem']))
                    
                    category_recc[i].append(df.loc[index, 'FoodItem'])
                 
        
            
            if meal_type in df.loc[index, 'meal_time'].split(','):
                meal_category_present = True
             

        if len(top_recommendations) == n and meal_category_present:
            break           
    #print(category_recc)
    return category_recc 
def input_recc(items,type):
      
    recommendations = recommend_items(items, type, n=7)
    print(f"Top Recommendations based on Consumed Items ")
    #for item, calories,meal_time in recommendations:
     #   print(f"Item: {item}, Calories: {calories},meal time:{meal_time}")
    
    return recommendations
    
#print(input_recc(['Boiled Rice','Mutton Biryani','Raita','Anda Bhurji', 'Boiled Rice', 'Sandwich'],'Lunch'))
#print(input_recc([],'Breakfast'))  