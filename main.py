import os
import string
import zeyrek
import nltk
import re

nltk.download('punkt')
analyzer = zeyrek.MorphAnalyzer()

stopwords = []

# $sentence: [$role, $action, $action_object, $action_place, $action_tool, $benefit_action, $benefit_object, $benefit_place, $benefit_tool]
# if not exist => 'null'
sentence_dictionary = {}

with open("stopwords.txt", 'r', encoding='utf-8') as file:
    stopwords = file.read().splitlines()

with open("492data.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()

    for words in lines:
        words = words.split()

        for i in range(len(words)):
            if not ("\'" or "-") in words[i]:
                table = words[i].maketrans(string.punctuation, (len(string.punctuation)) * " ")
                words[i] = words[i].translate(table).lower().strip()

        words_sw = [word for word in words if not word in stopwords]
        role_index = words_sw.index("olarak")
        role = " ".join(words_sw[1:role_index])

        action_index = words_sw.index("istiyorum") - 1
        action = words_sw[action_index]

        
        # item of action may include - object, place, tool
        action_item = words_sw[role_index + 1: action_index]
        # print(action_item)

        flag_action_object = False
        flag_action_place = False
        flag_action_tool = False
        last_item = ''

        action_object_list = []
        action_place_list = []
        action_tool_list = []

        action_tool_found = False

        for item in reversed(action_item):

            index_of_item = action_item.index(item)

            x = re.search("[i, ı, u , ü]$", item)
            y = re.search("de$|da$|te$|ta$|e$|a$|dan$|den$", item)
            z = re.search("le$|la$|ile$", item)


            # check if the type is new for this item
            is_new_type = False

            lemmatized = analyzer.lemmatize(item)[0][1][-1]
            
            if(lemmatized.lower() != item.lower()):
                if x and not flag_action_object and not action_tool_found:
                    last_item = 'action_object'
                    flag_action_object= True
                    action_object_list.append(item)
                    is_new_type = True

                elif y and not flag_action_place and not action_tool_found:
                    place_check = re.search("ğında$|ğinde$|ğunda$|ğünde$", item)
                    if(place_check):
                        pass
                    else:
                        last_item = 'action_place'
                        flag_action_place= True
                        action_place_list.append(item)
                        is_new_type = True
                
                elif z and not flag_action_tool :
                    last_item = 'action_tool'
                    flag_action_tool= True   
                    action_tool_list.append(item)
                    is_new_type = True
                    action_tool_found = not action_tool_found

            elif(index_of_item == len(action_item)-1):
                last_item = 'action_object'
                flag_action_object= True
                action_object_list.append(item)
                is_new_type = True

            if not is_new_type:
                if last_item == 'action_object':
                    action_object_list.append(item)
                elif last_item == 'action_place':
                    action_place_list.append(item)
                elif last_item == 'action_tool':
                    action_tool_list.append(item)

        print("--------------------------")
        print("Action Object: ", action_object_list)
        print("Action Place: ", action_place_list)
        print("Action Tool: ", action_tool_list)
        print("--------------------------")


            

        if "böylece" in words_sw:
            benefit_action = analyzer.lemmatize(words_sw[-1])[0][1][-1]

            boylece_index = words_sw.index("böylece") + 1
            benefit_action_object = " ".join(words_sw[boylece_index:-1])
