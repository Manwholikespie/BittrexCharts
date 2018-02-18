from account import *
# import time
from pprint import pprint
import plotly.offline as py
import plotly.graph_objs as go

class BCharts(object):
    def __init__(self, coinList, BTC_PRICE):
        self.coins = coinList
        self.BTC_PRICE = BTC_PRICE
    
    def plot_pie(self):
        TOTAL_SUM = sum([c.usd_value for c in myCoins])
        labels = [c.ticker for c in myCoins]
        values = [c.btc_value for c in myCoins]
        usdlabels = [('$%.2f' % c.usd_value) for c in myCoins]

        trace = go.Pie(labels=labels,
                values=values,
                text=usdlabels,
                hoverinfo='text+value+percent',
                textinfo='label',
                textfont=dict(size=20))

        data = [trace]

        layout = go.Layout(
            title = "Total bal: $%.2f" % (TOTAL_SUM)
        )

        fig = go.Figure(data=data, layout=layout)

        py.plot(fig, filename='pie.html')
        print('Plot saved in pie.html')

if __name__ == '__main__':
    myCoins = get_bal()
    myCharts = BCharts(myCoins, BTC_PRICE)
    myCharts.plot_pie()