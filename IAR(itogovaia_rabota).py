from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests

# словарь с основными криптовалютами
cripto_currency = {
    "bitcoin": "Bitcoin (Биткоин)",
    "ethereum": "Ethereum (Эфириум)",
    "litecoin": "Litecoin (Лайткоин)",
    "bitcoin-cash": "Bitcoin Cash (Биткоин Кэш)",
    "binancecoin": "Binance Coin (Бинанс Коин)",
    "eos": "EOS (ИОС)",
    "ripple": "Ripple (Рипл, XRP)",
    "stellar": "Stellar (Стеллар, XLM)", 
    "chainlink": "Chainlink (Чейнлинк)",
    "polkadot": "Polkadot (Полкадот)",
    "yearn-finance": "Yearn.finance (Йерн файненс)",
    "solana": "Solana (Солана)"
}

# основные фиатные валюты, ограничивают список (выбраны не все, что бы удобнее было выбирать) - заказчик может выбрать необходимое количество и наименование
currencies = {
    "usd": "Американский доллар",
    "eur": "Евро", 
    "jpy": "Японская йена",
    "gbp": "Британский фунт стерлингов",
    "aud": "Австралийский доллар",
    "cad": "Канадский доллар",
    "chf": "Швейцарский франк",
    "cny": "Китайский юань",
    "rub": "Российский рубль",
    "kzt": "Казахстанский тенге"
}

# ф-я запрашивает через API доступные фиатные валюты для обмена конкретной (выбранной пользователем) криптовалюты (отбираем только те, что есть в списке основных фиатных валют)
def valuti(crypto_id):
    
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
        answer = requests.get(url)# 
        answer.raise_for_status()
        data = answer.json()
        all_currencies = list(data["market_data"]["current_price"].keys())# составляем из json список всех возможных валют для обмена (фиатные, криптовалюта и др.)
        fiats_currencies = [curr for curr in all_currencies if curr in currencies] # оставляем только те, что есть в словаре currencies
        
        return fiats_currencies
    except Exception as e:
        mb.showerror("Ошибка API", f"Ошибка получения данных: {e}. Данная криптовалюта сейчас недоступна для расчета")

def crypto_label(event):# ф-я обновляет метку криптовалюты и список фиатных валют, доступных для обмена
    crypto_id = crypto_combobox.get() # получаем данные выбора криптовалюты
    name = cripto_currency[crypto_id]
    label_1.config(text=name)
    
    fiats_currencies = valuti(crypto_id) # список фиатных валют доступных для обмена полученные по API запросу
    fiats_combobox["values"] = fiats_currencies # обновляем второй комбобокс доступными фиатными валютами
    fiats_combobox.set("")  # сбрасываем выбор
    label_2.config(text="")  # очищаем метку

def fiats_label(event):# ф-я обновляет метку фиатной валюты
    fiat_code = fiats_combobox.get() # получаем данные выбора фиатной валюты
    label_2.config(text=currencies[fiat_code])

def exchange():# ф-я запрашивает данные курса по API
    crypto_id = crypto_combobox.get()
    fiat_code = fiats_combobox.get()
    
    if crypto_id and fiat_code: 
        try:
            #получаем данные по запросу API о курсе определенной криптовалюты к определенной фиатной валюте
            answer = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={fiat_code}")
            answer.raise_for_status()
            data = answer.json()
            
            if crypto_id in data and fiat_code in data[crypto_id]:
                exchange_rate = data[crypto_id][fiat_code]# курс валют из полученных данных
                crypto_name = cripto_currency[crypto_id]
                fiat_name = currencies[fiat_code]
                mb.showinfo("Курс обмена", f"Курс: 1 {crypto_name} = {exchange_rate:.2f} {fiat_name}")
            else:
                mb.showerror("Ошибка", "Данная валютная пара не найдена")
                
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка получения данных: {e}")
    else:
        mb.showwarning("Внимание", "Выберите обе валюты")

root = Tk()
root.title('Курс обмена криптовалюты «КриптоКурс»')
root.geometry("420x350")

Label(text="Криптовалюта:").pack(padx=10, pady=5)
crypto_combobox = ttk.Combobox(values=list(cripto_currency.keys()))
crypto_combobox.pack(padx=10, pady=5)
crypto_combobox.bind("<<ComboboxSelected>>", crypto_label)
label_1 = ttk.Label()
label_1.pack(padx=10, pady=10)

Label(text="Фиатная валюта:").pack(padx=10, pady=5)
fiats_combobox = ttk.Combobox(values=[])
fiats_combobox.pack(padx=10, pady=5)
fiats_combobox.bind("<<ComboboxSelected>>", fiats_label)
label_2 = ttk.Label()
label_2.pack(padx=10, pady=10)

Button(text="Обменный курс", command=exchange).pack(padx=10, pady=10)#запросить обменный курс

root.mainloop()