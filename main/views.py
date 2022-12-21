from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async
from yahoo_fin.stock_info import *
import time
import queue
from threading import Thread


# Create your views here.
def stockPicker(request):
    stock_picker = tickers_nifty50()
    #print(stock_picker)
    return render(request, 'main/stockpicker.html', context={'stockpicker':stock_picker})

@login_required
def stockTracker(request):
    #det = get_quote_table('RELIANCE.NS')
    #print(det)
    
    startTime = time.time()
    
    stockpicker = request.GET.getlist('stockpicker')
    print(stockpicker)
    data = {}
    available_stock = tickers_nifty50()

#this section uses multi threading
    n_thread = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    for i in range(n_thread):
        thread = Thread(target= lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args= (que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()
    
    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)

#this section uses no threading but needs better logic    
    # for i in stockpicker:
    #     if i in available_stock:
    #         result = get_quote_table(i)
    #         data[i] = result
    #     else:
    #         return HttpResponse("Error")

    # im = ['RELIANCE.NS','APOLLOHOSP.NS', 'BAJAJFINSV.NS']
    # data={}
    # for i in stockpicker:
    #     details = get_quote_table(i)
    #     data[i] = details
    
    print(data)
    
    endTime = time.time()
    print("completed in : ", endTime-startTime)
    
    return render(request, 'main/stocktracker.html',{'data': data, 'room_name': 'track'})
