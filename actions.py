# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from RecipeGrabber import GrabFromRemote
from RecipeX import Recipe
import re
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

recipe = None
stepindex = 0

class ActionAssertRecipe(Action):

    def name(self):
        return "action_assert_recipe"

    def run(self,dispatcher,tracker,domain):
        global recipe
        global stepindex
        url = tracker.get_slot("url")

        try:
            recipe = GrabFromRemote(url)
            dispatcher.utter_message(text="Alright, I got that. Let's go over " + recipe.title)
        except:
            dispatcher.utter_message(text="Something went wrong with your URL. Please try again, and make sure it's spelled correctly." + url)

class ActionLastStep(Action):

    def name(self):
        return "action_last_step"

    def run(self,dispatcher,tracker,domain):
        global stepindex
        global recipe
        if recipe == None:
            dispatcher.utter_message(text="You haven't given me a recipe yet!")
        elif stepindex == 0:
            dispatcher.utter_message(text="There was no step before this.")
        else:
            stepindex-=1
            last_step = recipe.directions[stepindex]
            dispatcher.utter_message(text="The last step was:" + last_step)

        return []

class ActionNextStep(Action):
    global recipe
    global stepindex

    def name(self):
        return "action_next_step"

    def run(self,dispatcher,tracker,domain):
        global stepindex
        global recipe
        if recipe == None:
            dispatcher.utter_message(text="You haven't given me a recipe yet!")
        elif stepindex >= len(recipe.directions) - 1:
            dispatcher.utter_message(text="There was no step after this.")
        else:
            stepindex+=1
            next_step = recipe.directions[stepindex]
            dispatcher.utter_message(text="The next step is: " + next_step)

        return []

class ActionFirstStep(Action):
    def name(self):
        return "action_first_step"

    def run(self,dispatcher,tracker,domain):
        global recipe
        global stepindex
        stepindex = 0
        if recipe == None or recipe.directions == []:
            dispatcher.utter_message("There are no steps available. Have you given me a URL yet?")
            return []
        
        relp = "The first step is: "
        relp+=recipe.directions[0]
        dispatcher.utter_message(relp)

        return []

class ActionTakeMeTo(Action):
    def name(self):
        return "action_take_me_to"
    
    def run(self,dispatcher,tracker,domain):
        global recipe
        global stepindex

        if recipe == None or recipe.directions == []:
            dispatcher.utter_message("There are no steps available. Have you given me a URL yet?")
            return []
        
        baselista = ["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth","eleventh","twelveth","thirteenth","fourteenth"]

        numb = tracker.get_slot("numb")
        if numb.lower() in baselista:
            numb = baselista.index(numb)
        else:
            re.sub("[A-Za-z,.]","", numb)
            try:
                numb = int(numb) - 1
            except:
                dispatcher.utter_message("I didn't recognize that step number.")

        if numb >= 0 and numb < len(recipe.directions):
            stepindex = numb
            dispatcher.utter_message("Step " + str(numb) + " is: " + recipe.directions[stepindex])
        else:
            dispatcher.utter_message("I didn't recognize what step you mean.")

        return []

class ActionIngredients(Action):
    def name(self):
        return "action_ingredients"

    def run(self,dispatcher,tracker,domain):
        global recipe

        if recipe == None or recipe.ingredients == []:
            dispatcher.utter_message("I can't find any ingredients. Did you give me a recipe?")
            return []
        
        ingredients = "The ingredients for " + recipe.title + " are:\n"
        for x in recipe.ingredients:
            ingredients += x + "\n"

        dispatcher.utter_message(ingredients)

        return []
        


class ActionAllSteps(Action):
    def name(self):
        return "action_all_steps"

    def run(self,dispatcher,tracker,domain):
        global recipe

        if recipe == None or recipe.steps == []:
            dispatcher.utter_message("I can't find any steps. Did you give me a recipe?")
            return []
        
        steps = "The steps for " + recipe.title + " are:\n"
        for x in recipe.directions:
            steps += x + "\n"

        dispatcher.utter_message(steps)

        return []

class ActionDefine(Action):
    def name(self):
        return "action_define"

    def run(self,dispatcher,tracker,domain):
        define = tracker.get_slot("object")

        dispatcher.utter_message("Try this to find the definition of " + define + ": https://www.merriam-webster.com/dictionary/" + define)

        return []

class ActionHowTo(Action):
    def name(self):
        return "action_how_to"
    
    def run(self,dispatcher,tracker,domain):
        how_to = tracker.get_slot("action")
        how_to = how_to.replace(" ","+")

        dispatcher.utter_message("This search might help you: https://www.youtube.com/results?search_query=how+to+",how_to)

        return []


