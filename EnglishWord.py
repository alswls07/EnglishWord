file=open(r'C:\Users\sky70\OneDrive\바탕 화면\김민진\코딩\EnglishWord\EnglishWordList.txt', 'r')

english_list={}

for string in file:
    s=string.split()
    key=s.pop(0)
    value=''.join(str(x) for x in s)
    english_list[key]=value

print(english_list)

file.close()