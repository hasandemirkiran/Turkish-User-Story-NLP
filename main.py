import os
import string
import zeyrek
import nltk

nltk.download('punkt')
analyzer = zeyrek.MorphAnalyzer()

sentence_list = []
stopwords = []

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

        action_object = " ".join(words_sw[role_index + 1: action_index])
        print(action_object)
        if "böylece" in words_sw:
            benefit_action = analyzer.lemmatize(words_sw[-1])[0][1][-1]

            boylece_index = words_sw.index("böylece") + 1
            benefit_action_object = " ".join(words_sw[boylece_index:-1])
