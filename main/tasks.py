from celery import shared_task
import queue
from threading import Thread
from yahoo_fin.stock_info import *
from channels.layers import get_channel_layer
import asyncio
import simplejson as json

@shared_task(bind=True)
def update_stocks(self, stockpicker):
    data = {}
    available_stock = tickers_nifty50()

#this section uses multi threading
    n_thread = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    for i in range(n_thread):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: json.loads(json.dumps(get_quote_table(arg1), ignore_nan = True))}), args = (que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()
    
    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)

    # send data to group
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send("stock_track", {
        "type": "send_stock_update",
        "message": data,
    }))
    return 'DONE'