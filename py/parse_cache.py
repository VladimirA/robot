
f = open("cache")
fout = open("cache_out",'w')
finalString=""
for line in f.readlines():
    if (line.startswith("000")):
        subLine = line[59:]
        finalString += subLine.replace('\n','')

import string
valid_characters = string.ascii_letters + string.digits + '$'

chars = list(finalString)
for index in range(1, len(chars)-1):
    if (chars[index]=='.' and chars[index-1] not in valid_characters):
        chars[index]= '\n'


finalString = ''.join(chars)

#finalString = finalString.replace('..','\n\n')
#finalString = finalString.replace('. ','\n ')
#finalString = finalString.replace('.<','\n<')
#finalString = finalString.replace('.}','\n}')
#finalString = finalString.replace('.function','\nfunction')
print >> fout, finalString

