## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## recipe walkthrough
* walkthrough
  - utter_url
* assert_recipe{"url":"https://www.allrecipes.com/recipe/278144/crab-cheese-fondue/"}
  - slot{"url":"https://www.allrecipes.com/recipe/278144/crab-cheese-fondue/"}
  - action_assert_recipe
  - utter_ask_recipe
* steps
  - utter_next_step

## recipe walkthrough b
* walkthrough
  - utter_url
* assert_recipe{"url":"https://www.allrecipes.com/recipe/278144/crab-cheese-fondue/"}
  - slot{"url":"https://www.allrecipes.com/recipe/278144/crab-cheese-fondue/"}
  - action_assert_recipe
  - utter_ask_recipe

## recipe walkthrough c
* assert_recipe{"url":"https://www.allrecipes.com/recipe/278144/crab-cheese-fondue/"}
  - action_assert_recipe
  - utter_ask_recipe

## ask next step
* next_step
  - action_next_step
  - utter_ask_action
* affirm
  - action_next_step

## ask last step
* last_step
  - action_last_step
  - utter_ask_action
* affirm
  - action_next_step

## ask steps
* steps
 - action_all_steps

## ask ingredients
* ingredients
 - action_ingredients

## request definition
* what_is_a{"object":"peeler"}
  - slot{"object":"peeler"}
  - action_define

## request how-to
* how_do_i{"action":"peel a carrot"}
  - slot{"action":"peel a carrot"}
  - action_how_to

## request first step
* return_to_start
  - action_first_step

## request step
* take_me_to{"numb":"1"}
  - slot{"numb":"1"}
  - action_take_me_to





