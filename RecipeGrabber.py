from bs4 import BeautifulSoup
from RecipeX import Recipe
import html
import requests
import re

#Takes a AllRecipes.com Url, returns a recipe object
def GrabFromRemote(url):
    get = requests.get(url)
    soup = BeautifulSoup(get.text,'html.parser')
    
    ingredients = soup.find(id="lst_ingredients_1").get_text() + soup.find(id="lst_ingredients_2").get_text()
    ingredients = re.sub("[\n]+","\n",ingredients)
    ingredients = re.sub("(^[\n]|[\n]$|\nAdd all ingredients to list)","",ingredients)
    ingredients = ingredients.split("\n")
    #ingredients = [get_ingredient(ingredient) for ingredient in ingredients]
    
    title = soup.find(id="recipe-main-content").get_text()

    steps = soup.find(class_="directions--section__steps").get_text()
    steps = re.sub("[\n]{2,}","@",steps)
    steps = re.sub("[\s]{2,}","",steps)
    steps = steps[1:-1].split("@")
    time = steps[0:3]
    steps = steps[3:]

    i = 0
    while i < len(steps):
        steps[i] = re.split("(?:\. |; |! )",steps[i])
        steps[i][-1].replace(".","")
        i+=1
    
    newsteps = []
    for step in steps:
        if isinstance(step,str):
            newsteps.append(step)
        elif isinstance(step,list):
            newsteps.extend(step)
    steps = newsteps


    notesAndNutr = ""
    
    for x in soup.find_all(class_="recipe-footnotes"):
        notesAndNutr += x.get_text()
    notesAndNutr = re.sub("[\n]{2,}","@",notesAndNutr)
    notesAndNutr = re.sub("[\s]{2,}","",notesAndNutr)

    notes = ""
    if "@Foot" in notesAndNutr:
        notes \
            = notesAndNutr[notesAndNutr.index("@Foot"):notesAndNutr.index("@Nutr")]
        notes = re.sub("^@F.*\n","",notes)

    nutr = notesAndNutr[notesAndNutr.index("ing:")+4:notesAndNutr.index(".\nFull")].split(";\n")
    recipe = Recipe(title,ingredients,steps,notes,nutr,time)
    #print(recipe.title,recipe.ingredients,recipe.directions,recipe.notes,recipe.nutrition,recipe.timing)

    return recipe

def grab_steps(steps):

    return []

#rec = GrabFromRemote("https://www.allrecipes.com/recipe/262174")

#print([str(ingredient) for ingredient in rec.ingredients])
#rec.change_servings(2)
#print([str(ingredient) for ingredient in rec.ingredients])
#rec.change_servings(1/8)
#print([str(ingredient) for ingredient in rec.ingredients])




# print(rec.ingredients)
# rec.change_servings(2)
# print(rec.directions)
# print([str(ingredient) for ingredient in rec.ingredients])
# print(rec.notes)
# print(rec.nutrition)
# print(rec.timing)
# print(rec.title)
