
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files import File
from tamil.utf8 import get_letters, get_letters_length, get_words
from .models import Demo
from .basics import word_startswith, word_endswith, contains, grantha, position
from django.views import View
from django.utils.http import urlquote
from django.db.models import Q
import pandas as pd
from django.shortcuts import redirect
import json
import time
import dask.dataframe as dd


def home(request):
    return render(request,'index.html')



def FirstSearch(val1, val2, val3, val4):
        
    filters = Q()
    if val1:
        filters &= Q(words__startswith=val1)
    if val2:
        filters &= Q(words__endswith=val2)

    if val3 and val3.isdigit() and int(val3) <= 20:
        filters &= Q(length=int(val3))
    else:
        filters &= Q(length__lte=20)  
    
    if val4:
        filters &= Q(words__icontains=val4)
        

    # Query execution
    data = Demo.objects.filter(filters).values('words')

    # Processing based on conditions
    if val1 and val2 and val3 and val4:
        data = word_startswith(get_letters(val1), data)
        data = word_endswith(get_letters(val2), data)
        data = contains(get_letters(val4), data)
        filename = f'Starts_{val1}_Ends_{val2}_Length_{val3}_Contains_{val4}'
    
    elif val1 and val2 and val3:
        data = word_startswith(get_letters(val1), data)
        data = word_endswith(get_letters(val2), data)
        filename = f'Starts_{val1}_Ends_{val2}_Length_{val3}'
    
    elif val1 and val2 and val4:
        data = word_startswith(get_letters(val1), data)
        data = word_endswith(get_letters(val2), data)
        data = contains(get_letters(val4), data)
        filename = f'Starts_{val1}_Ends_{val2}_Contains_{val4}'

    elif val1 and val3 and val4:
        data = word_startswith(get_letters(val1), data)
        data = contains(get_letters(val4), data)
        filename = f'Starts_{val1}_Contains_{val4}_Length_{val3}'

    elif val2 and val3 and val4:
        data = word_endswith(get_letters(val2), data)
        data = contains(get_letters(val4), data)
        filename = f'Ends_{val2}_Contains_{val4}_Length_{val3}'

    elif val1 and val2:
        data = word_startswith(get_letters(val1), data)
        data = word_endswith(get_letters(val2), data)
        filename = f'Starts_{val1}_Ends_{val2}'

    elif val1 and val3:
        data = word_startswith(get_letters(val1), data)
        filename = f'Starts_{val1}_Length_{val3}'

    elif val1 and val4:
        data = word_startswith(get_letters(val1), data)
        data = contains(get_letters(val4), data)
        filename = f'Starts_{val1}_Contains_{val4}'

    elif val2 and val3:
        data = word_endswith(get_letters(val2), data)
        filename = f'Ends_{val2}_Length_{val3}'

    elif val2 and val4:
        data = word_endswith(get_letters(val2), data)
        data = contains(get_letters(val4), data)
        filename = f'Ends_{val2}_Contains_{val4}'

    elif val3 and val4:
        data = contains(get_letters(val4), data)
        filename = f'Length_{val3}_Contains_{val4}'

    elif val1:
        data = word_startswith(get_letters(val1), data)
        filename = f'Starts_{val1}'
    
    elif val2:
        data = word_endswith(get_letters(val2), data)
        filename = f'Ends_{val2}'
    
    elif val3:
        filename = f'Length_{val3}'

    elif val4:
        data = contains(get_letters(val4), data)
        filename = f'Contains_{val4}'    
    return data,filename


class GetTamilWord(View):
        
    def post(self, request):  

        if request.POST.get("search"):
            val1=request.POST['start']      
            val2=request.POST['end']        
            val3= request.POST['length']
            val4 =request.POST['contains']

            if val1 or val2 or val3 or val4:
                data1,filename =  FirstSearch(val1, val2, val3, val4)
                n_word, g_word = grantha(data1)
                request.session['g_name'] = g_word  
                request.session['n_name'] = n_word
                request.session['start'] = val1
                request.session['end'] = val2
                request.session['length'] = val3
                request.session['contains'] = val4
                request.session['filename'] = filename
                request.session['data1'] = 'res4'
                if len(n_word) > 0 or len(g_word) > 0:
                    return render(request,'names.html',{'data': n_word, 'start': val1,'end':val2, 'length':val3,'contains':val4,
                    'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-sm btn-cl1','status_g':'btn btn-lg btn-secondary'})
                else:
                    return render(request, 'index.html',{'start': val1,'end':val2, 'length':val3,'contains':val4,"msg":"கொடுக்கப்பட்ட உள்ளீட்டிற்கு ஏற்ப எந்தவொரு வெளியீடும் கிடைக்கவில்லை."})
            else:
                return render(request, 'index.html',{"msg":"தயவு செய்து உள்ளீட்டை அளிக்கவும்."})
                    

        if request.POST.get("search2"):
            words_dict = {key: value for key, value in request.POST.items() if key.startswith("words[")}
            if bool(len(words_dict)) and (int(len(words_dict)) <=20) and (not all(value == '' for value in words_dict.values())):
                data1 = Demo.objects.filter(length = len(words_dict)).values('words')
                df = pd.DataFrame(list(data1))
                df = dd.from_pandas(df, npartitions=4)
                filtered_dict = {int(k.strip('words[]'))-1: v for k, v in words_dict.items() if v != ''}

                df['letters'] = df['words'].map(get_letters, meta=('x', 'object'))

                for i in range(7):
                    df[f'col_{i}'] = df['letters'].map(lambda x, idx=i: x[idx] if len(x) > idx else '', meta=('x', 'object'))

                for i, val in filtered_dict.items():
                    df = df[df[f'col_{i}'] == val]

                data2 = []
                for part in df[['words']].partitions:
                    data2.extend(part.compute().to_dict(orient='records'))

                n_word, g_word = grantha(data2)
                filename = f'Length_{len(words_dict)}_{'_'.join(f"{k}_{v}" for k, v in words_dict.items() if v != '')}'
                request.session['g_name'] = g_word  
                request.session['n_name'] = n_word
                request.session['filename'] = filename
                request.session['words_dict'] = words_dict
                request.session['bx_val'] = len(words_dict)
                request.session['data1'] = 'res4'
                if len(n_word) > 0 or len(g_word) > 0:
                    return render(request,'names.html',{'data': n_word, 'data1': 'res1', 'words_dict': words_dict,'bx_val': len(words_dict),
                    'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-sm btn-cl1','status_g':'btn btn-lg btn-secondary'})
                else:
                    return render(request, 'index.html',{'words_dict': words_dict,'bx_val': len(words_dict),"msg":"கொடுக்கப்பட்ட உள்ளீட்டிற்கு ஏற்ப எந்தவொரு வெளியீடும் கிடைக்கவில்லை."})

            else:
                return render(request, 'index.html',{"msg":"தயவு செய்து உள்ளீட்டை அளிக்கவும்."})
            
        if request.POST.get('res3') or request.POST.get('res4'):  
            g_word = request.session['g_name']
            n_word = request.session['n_name'] 
            val1 = request.session['start']
            val2 = request.session['end']
            val3 = request.session['length']
            val4 = request.session['contains'] 
            words_dict= request.session['words_dict']
            bx_val = request.session['bx_val']

            if request.POST.get('res3'):
                request.session['data1'] ='res3'
                if len(g_word) > 0:                
                    return render(request,'names.html',{'data':g_word, 'start': val1,'end':val2, 'length':val3,'contains':val4,  'words_dict': words_dict,'bx_val': bx_val,
                    'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-lg btn-secondary','status_g':'btn btn-sm btn-cl1'})
                else:
                    return render(request,'names.html', {'start': val1,'end':val2, 'length':val3,'contains':val4, 'words_dict': words_dict,'bx_val': bx_val,
                    'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-lg btn-secondary','status_g':'btn btn-sm btn-cl1'})
            
            elif request.POST.get('res4'):
                request.session['data1'] = 'res4'       
                if len(n_word) > 0:                
                    return render(request,'names.html',{'data':n_word, 'start': val1,'end':val2, 'length':val3,'contains':val4, 'words_dict': words_dict,'bx_val': bx_val,
                    'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-sm btn-cl1','status_g':'btn btn-lg btn-secondary'})
                else:
                    return render(request,'names.html', {'start': val1,'end':val2, 'length':val3,'contains':val4, 'words_dict': words_dict,'bx_val': bx_val,
                    'count_n':len(n_word),'count_g':len(g_word),'status_n':'btn btn-sm btn-cl1','status_g':'btn btn-lg btn-secondary'})
     

        elif request.POST.get('download'):
            g_word = request.session.get('g_name')
            n_word = request.session.get('n_name')
            data1 = request.session.get('data1')
            filename = request.session.get('filename', 'download')
            response = HttpResponse(content_type="text/plain")
            response['Content-Disposition'] = f'attachment; filename={urlquote(filename)}.txt'

            lines = []
            word_list = g_word if data1 == 'res3' else n_word
            for i in word_list:
                word = i.get('words')
                lines.append(f'{word}\n')
            response.writelines(lines)
            return response

        else:
            return redirect('home')         

