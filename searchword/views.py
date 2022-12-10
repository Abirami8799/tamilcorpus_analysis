
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files import File
from tamil.utf8 import get_letters, get_letters_length, get_words
from .models import Demo
from .basics import word_startswith, word_endswith, contains, grantha, position
from django.views import View
from django.utils.http import urlquote


def home(request):
    return render(request,'base.html')


def FirstSearch(val1, val2, val3):
        
    if (bool(val1) and bool(val2) and bool(val3)) and (len(val3) <=20):
        l = get_letters(val1)
        m = get_letters(val2)
        data = Demo.objects.filter(start_letter__icontains =val1[0],end_letter__icontains= val2[-1]).filter(words__startswith=val1,words__endswith=val2,length__iexact=val3).values('words')
        s= word_startswith(l,data)   
        data1 = word_endswith(m, s)
        filename = 'Starts_'+val1+'_Ends_'+val2+'_Length_'+val3
        
    elif (bool(val1) and bool(val2)):
        l = get_letters(val1)
        m = get_letters(val2)
        data = Demo.objects.filter(start_letter__icontains = val1[0],end_letter_icontains = val2[-1]).filter(words__startswith=val1,words__endswith=val2, length__lte = 20).values('words')
        s= word_startswith(l,data)   
        data1 = word_endswith(m, s)
        filename = 'Starts_'+val1+'_Ends_'+val2
    
    elif (bool(val2) and bool(val3)) and (int(val3)<=20):
        l = get_letters(val2)
        data = Demo.objects.filter(end_letter__icontains = val2[-1]).filter(words__endswith=val2,length__iexact=val3).values('words')
        data1 = word_endswith(l,data)
        filename = 'Ends_'+val2+'_Length_'+val3


    elif (bool(val1) and bool(val3))and (int(val3)<=20):
        l = get_letters(val1)
        data = Demo.objects.filter(start_letter__icontains = val1[0]).filter(words__startswith=val1,length__iexact=val3).values('words')
        data1 = word_startswith(l,data)
        filename = 'Starts_'+val1+'_Length_'+val3


    elif bool(val1):
        l = get_letters(val1)
        value = Demo.objects.filter(start_letter__icontains = val1[0]).filter(words__startswith=val1, length__lte = 20).values('words')
        data1 = word_startswith(l,value)
        filename = 'Starts_'+val1                    
        

    elif bool(val2):
        l = get_letters(val2)
        value = Demo.objects.filter(end_letter__icontains = val2[-1]).filter(words__endswith=val2, length__lte = 20).values('words')
        data1 = word_endswith(l,value)
        filename = 'Ends_'+val2 
    

    elif bool(val3) and (int(val3) <=20):
        data1 = Demo.objects.filter(length__iexact = val3).values('words')
        filename = 'Length_'+val3
    
    return data1,filename

def SecondSearch(val4):
    
    l = get_letters(val4)
    s = Demo.objects.filter(words__icontains=val4,length__lte = 20).values('words')  
    data1 = contains(l, s)
    filename = 'Contains_'+val4	
    return data1,filename



class GetTamilWord(View):
        
    def post(self, request):            
        val1=request.POST['start']      
        val2=request.POST['end']        
        val3= request.POST['length']
        val4 =request.POST['contains']
        val5 = request.POST['words']
        val6 = request.POST['position']
        

        if val1 or val2 or val3:
            data1,filename =  FirstSearch(val1, val2, val3)
            n_word, g_word = grantha(data1)
            request.session['g_name'] = g_word  
            request.session['n_name'] = n_word
            request.session['filename'] = filename
            if len(n_word) > 0 or len(g_word) > 0:
                return render(request,'grantha.html',{'data': n_word, 'data1': 'res1',
                'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-lg btn-success','status_g':'btn btn-lg btn-secondary'})
            else:
                return render(request,'base.html')

        elif bool(val4) and request.POST.get('ck1'):
            data1,filename = SecondSearch(val4)
            n_word, g_word = grantha(data1)
            request.session['g_name'] = g_word  
            request.session['n_name'] = n_word
            request.session['filename'] = filename
            if len(n_word) > 0 or len(g_word) > 0:          
               return render(request,'grantha.html',{'data': n_word, 'data1': 'res1',
            'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-lg btn-success','status_g':'btn btn-lg btn-secondary'})
            else:
                return render(request,'base.html')
        elif val5 and val6 and request.POST.get('ck1'):
            s = Demo.objects.filter(words__icontains=val5, length__range = (val6,20)).values('words') 
            data1 = position(val5, val6, s)
            n_word, g_word = grantha(data1)
            request.session['g_name'] = g_word  
            request.session['n_name'] = n_word
            request.session['filename'] = 'Letter_'+val5+'_position_'+val6
            if len(n_word) > 0 or len(g_word) > 0:           
               return render(request,'grantha.html',{'data': n_word, 'data1': 'res1', 
            'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-lg btn-success','status_g':'btn btn-lg btn-secondary'})
            else:
                return render(request,'base.html')
        else:
            return render(request, 'base.html')

     
         

class GetGranthaWord(View):

    def post(self, request):
        g_word = request.session['g_name']
        n_word = request.session['n_name']  
        if request.POST.get('res3'):              
            if len(g_word) > 0:                
                return render(request,'grantha.html',{'data':g_word, 'data1': 'res3',
                'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-lg btn-secondary','status_g':'btn btn-lg btn-success'})
            else:
                return render(request,'grantha.html',
                {'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-lg btn-secondary','status_g':'btn btn-lg btn-success'})
        elif request.POST.get('res4'):            
            if len(n_word) > 0:                
                return render(request,'grantha.html',{'data':n_word, 'data1': 'res4',
                'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-lg btn-success','status_g':'btn btn-lg btn-secondary'})
            else:
                return render(request,'grantha.html',
                {'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-lg btn-success','status_g':'btn btn-lg btn-secondary'})

        else:
            return render(request, 'base.html')

def download(request): 
    
    if request.POST.get('res1') or request.POST.get('res4'):
        filename = request.session['filename']        
        response = HttpResponse(content_type = 'text\plain')
        response['Content-Disposition'] =  "attachment; filename={}".format(urlquote(filename+'.txt'))
        n_word = request.session['n_name']   
        lines=[]
        for i in n_word:
            word = i.get('words')
            lines.append(f'{word}\n')

        response.writelines(lines)
        return response
    elif request.POST.get('res3'):
        filename = request.session['filename'] 
        response = HttpResponse(content_type = 'text\plain')
        response['Content-Disposition'] =  'attachment; filename={}'.format(urlquote(filename+'.txt'))
        g_word = request.session['g_name']   
        lines=[]
        for i in g_word:
            word = i.get('words')
            lines.append(f'{word}\n')

        response.writelines(lines)
        return response
    else:
        response = HttpResponse(content_type = 'text\plain')
        response['Content-Disposition'] =  'attachment; filename= empty.txt' 
        lines=[]
        response.writelines(lines)
        return response
        

