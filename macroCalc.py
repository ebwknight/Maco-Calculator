# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 14:17:14 2021

Whadup poopoo-head. Here's a macro calculator. Exports to excel for your financial ass

@author: evanbwknight
"""

import pandas as pd
import openpyxl
import numpy as np
from bs4 import BeautifulSoup as soup
import requests
import re
from nutritionix import Nutritionix

nix = Nutritionix(app_id="628fcca6", api_key="c3cd31c6207e1ce3b00a35615cba1295")

print("Instructions:\nPlease enter your ingredients one at a time followed by the ammount in grams when prompted.\nWhen finished, enter nothing for ingredient and grams and simply press enter twice")
ingredients = []
meal = []
try:
    grub = input("First Ingredient: ")
    ammount = input("Ammount (in grams): ")
    while grub:
        ingredients.append(tuple([str(grub), int(ammount)]))
        grub = input("Next ingredient: ")
        ammount = input("Ammount (in grams): ")
             
    
    for ingredient in ingredients:
        
        food = nix.search(ingredient[0], results="0:1")
        foodID = food.json()['hits'][0]['_id']
        data = nix.item(id=foodID).json()
        #print(data)
        
        if data['nf_serving_weight_grams'] != None:
            calories = ((data['nf_calories'] / data['nf_serving_weight_grams']) * ingredient[1])
            fat = ((data['nf_total_fat'] / data['nf_serving_weight_grams']) * ingredient[1])
            carbs = ((data['nf_total_carbohydrate'] / data['nf_serving_weight_grams']) * ingredient[1])
            protein = ((data['nf_protein'] / data['nf_serving_weight_grams']) * ingredient[1])
            sugar = ((data['nf_sugars'] / data['nf_serving_weight_grams']) * ingredient[1])
            meal.append([ingredient[0], round(calories,0), round(fat,0), round(carbs,0), round(protein,0), round(sugar,0)])
        else:
            print("No grams per serving data available for " + data['item_name'])
            print("Ingredient not appended to sheet")
                  
        
    totalCals = 0
    totalFats = 0
    totalCarbs = 0
    totalProtein = 0
    totalSugar = 0
    
    for item in meal:
        totalCals += item[1]
        totalFats += item[2]
        totalCarbs += item[3]
        totalProtein += item[4]
        totalSugar += item[5]
    
    meal.append(['Totals', totalCals, totalFats, totalCarbs, totalProtein, totalSugar])
    
    mealDF = pd.DataFrame(meal, columns = ['Ingredient', 'Calories', 'Fats', 'Carbs', 'Protein', 'Sugars'])
    filename = input("Please enter a filename. Do not include a filetype (Example: lasagna, not lasagna.txt): ")
    mealDF.to_excel('{}.xlsx'.format(filename), index = False)  

except Exception as e:
    print(e)
    
    