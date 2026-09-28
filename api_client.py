import datetime
import requests
import json
def get(url):
    try:
        r=requests.get(url,timeout=15)
        if r.status_code == 200:
            return r
        else:
            return (f'Ощибка {r.status_code}')
    except requests.exceptions.MissingSchema:
        return ('Ошибка: вы забыли указать http:// или https:// в начале URL!')
    except requests.exceptions.ConnectionError:
        return('Не удолось подключиться к серверу')
    except  requests.exceptions.Timeout:
        return('Превышеное ожидание')
        
def json_conect(respons):
    return respons.json()
    
def generate_items(respons,key):
    day = respons[key]
    return (x for x in day)
    
def filter_price(items,min_price,max_price):
    for x in items:
        if max_price >= float(x['price']) >= min_price:
            yield x

def Filter_category(price,category_items):
    for x in price:
        if x['category'] == category_items:
            yield x

def filter_quantity_min(price,quantity_users,users_quantity):
    for x in price:
        if x['users_quantity'] <= quantity_users:
             yield x    
def filter_quantity_max(price,quantity_users,users_quantity):
    for x in price:
        if x['users_quantity'] >= quantity_users:
             yield x    

def filter_quantity_range(price,users_quantity,quantity_users_min,quantity_users_max):
    for x in price:
        if quantity_users_min <= x[users_quantity]<=quantity_users_max:
            yield x


def statuc(Filter_category):
    dt_now = datetime.datetime.now()
    dt_now = dt_now.strftime('%B %d %Y %H:%M')
    try:
        first = next(Filter_category)
    except StopIteration:
        return('Нет товаров, соответствующих фильтрам')
    max_price = float(first['price'])
    min_price = float(first['price'])
    sum_price = float(first['price'])
    name_max=first['title']
    name_min=first['title']
    count = 1
    quantity = int(first['stock'])
    for x in Filter_category:
        price = x['price']
        quantity +=int(x['stock'])
        if float(min_price) >=float(price):
            min_price=float(price)
            name_min = x['title']
        if float(max_price) <= float(price):
            max_price=float(price)
            name_max = x['title']
        count+=1
        sum_price+=float(price)
    avg_price= round((sum_price/count),2)
    return f'''Максимальная цена:{max_price}\nТовар:{name_max}\nМинимальная цена:{min_price}\nТовар:{name_min}\nКоличество всех позиций:{count}\nКоличество товаров на складу{quantity}\nCредняя цена:{avg_price}\nВремя создание файла:{dt_now}'''

def save_file(name_file,statuc):
    name_file = name_file+".json"
    with open(name_file,'w',encoding="utf-8") as file:
        json.dump(statuc,file,indent=4,ensure_ascii=False)
        return name_file
        
def load_file(name_file):
    try:
        with open(name_file,'r',encoding='utf-8') as r_file:
            data = json.load(r_file)
        
    except FileNotFoundError:
        return f'Файл не существует {name_file}'
        
    except json.JSONDecodeError:
        return"Файл существует, но внутри невалидный JSON"
        
    return data
        
            
    
    
    
         
         
