class Coin(object):
    def __init__(self, ticker, amount, price, BTC_PRICE=None):
        self.ticker = ticker
        self.amount = amount
        self.btc_price = price
        self.btc_value = amount*price

        if BTC_PRICE:
            self.usd_value = self.btc_value * BTC_PRICE
        else:
            self.usd_value = None
    
    def printInfo(self):
        print('%s \t %.8f \t %.2f' % (self.ticker,
                                      self.btc_value,
                                      self.usd_value))