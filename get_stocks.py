import pyotp
import robin_stocks.robinhood as r

import time


from decouple import config

totp = pyotp.TOTP(config('robin_mfa')).now()
login = r.login(config('robin_username'),config('robin_password'),mfa_code=totp)
stocks = r.build_holdings()

for i in range(10):

    result_list = []

    for stock,value in stocks.items():
        list = {
            "code":stock,
            'invested':float(value["average_buy_price"]), 
            'quantity':float(value["quantity"]), 
            'current_price': float(value["price"]),
            'price_point':float(value["average_buy_price"]) * float(value["quantity"])
            }
        result_list.append(list)

    cryptos = r.get_crypto_positions()

    for d_ in cryptos:
            quantity = float(d_["quantity"])
            code = d_["currency"]["code"]
            cost = float(d_["cost_bases"][0]["direct_cost_basis"])
            price_point = cost/quantity
            _ = r.get_crypto_quote(code)
            current_price = round(float(_["ask_price"]),4)
            list = {
                'code':code, 
                'invested': cost, 
                'quanitity':quantity, 
                'price_point':price_point,
                'current_price': current_price,
                }
            result_list.append(list)

    for vs in result_list:
        print(vs["code"] + " is " + str(vs["current_price"]))
    print("************")
    time.sleep(10)