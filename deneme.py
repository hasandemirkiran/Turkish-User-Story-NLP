import re
import zeyrek
import json
analyzer = zeyrek.MorphAnalyzer()

txt = "e posta"


for x in txt.split():
    deneme = analyzer.lemmatize(x)[0][1][-1]
    print(deneme)
