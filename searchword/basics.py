import tamil
from tamil.utf8 import get_letters, get_letters_length, get_words

def word_startswith(l, value):
    s=[]
    for each in value:
        try:
            m = get_letters(each.get('words'))
            x = m[0:0+len(l)]        
            if x == l:
               s.append(each)
        except:
           continue
    return s

def word_endswith(l, value):
    s=[]
    for each in value:
        try:
            m = get_letters(each.get('words'))
            x = m[-len(l):]        
            if x == l:
               s.append(each)
        except:
            continue
    return s

def word__length(l, value):
    s=[]
    for each in value:
        try:
            m = each.get('length')  
            if m == l :
               s.append(each)
        except:
            continue
    return s

def contains(l, value):
    s=[]      
    for each in value:
        try:
            m = get_letters(each.get('words'))

            y = m.index(l[0])
            x = m[y:y+len(l)]
            if x == l:
               s.append(each) 
        except:
            continue
    return s 


def position(l, v, value):
    s=[]
    for each in value:
        try:
            m = get_letters(each.get('words'))
            record_position = int(v) -1
            if l == m[record_position]:
                s.append(each)
        except:
            continue
    return s

def grantha(value):
    s = ['ஶ்', 'ஶ', 'ஶா', 'ஶி', 'ஶீ', 'ஶு', 'ஶூ', 'ஶெ', 'ஶே', 'ஶை', 'ஶொ', 'ஶோ', 'ஶௌ', 'ஜ்', 'ஜ', 'ஜா', 'ஜி', 'ஜீ', 'ஜு', 'ஜூ', 'ஜெ', 'ஜே', 'ஜை', 'ஜொ', 'ஜோ', 'ஜௌ', 'ஷ்', 'ஷ', 'ஷா', 'ஷி', 'ஷீ', 'ஷு', 'ஷூ', 'ஷெ', 'ஷே', 'ஷை', 'ஷொ', 'ஷோ', 'ஷௌ', 'ஸ்', 'ஸ', 'ஸா', 'ஸி', 'ஸீ', 'ஸு', 'ஸூ', 'ஸெ', 'ஸே', 'ஸை', 'ஸொ', 'ஸோ', 'ஸௌ', 'ஹ்', 'ஹ', 'ஹா', 'ஹி', 'ஹீ', 'ஹு', 'ஹூ', 'ஹெ', 'ஹே', 'ஹை', 'ஹொ', 'ஹோ', 'ஹௌ', 'க்ஷ்', 'க்ஷ', 'க்ஷா', 'க்ஷி', 'க்ஷீ', 'க்ஷு', 'க்ஷூ', 'க்ஷெ', 'க்ஷே', 'க்ஷை', 'க்ஷொ', 'க்ஷோ', 'க்ஷௌ']
    g=[]
    n=[]
    for each in value:
        try:
            m = get_letters(each.get('words'))
            y = [m for i in m if i in s]
            if len(y) > 0 : 
                g.append(each)
            else:
                n.append(each)
        except:
            continue
    return n,g


