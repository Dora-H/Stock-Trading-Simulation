import numpy as np
import matplotlib.pyplot as mp
import matplotlib.dates as md
import datetime as dt
from matplotlib.font_manager import FontProperties


mp.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
mp.rcParams['axes.unicode_minus'] = False

mp.figure("Trading Simulation 股票草擬策略", facecolor="lightgrey", figsize=(16, 7))
mp.title("Aug/2020-Jan/2021 大成鋼", fontsize=20)

mp.xlabel("Dates 日期", fontsize=14)
mp.ylabel("Profits 利潤率", fontsize=14)


def dmy_to_date(dmy):
    dmy = str(dmy, encoding='utf8')
    date = dt.datetime.strptime(dmy, '%m-%d-%Y').date()
    return date


dates, open_prices, highest_prices, lowest_prices, close_prices \
    = np.loadtxt("./2027_2.twd.csv", delimiter=',', usecols=(1, 3, 4, 5, 6), unpack=True,
                 dtype="M8[D],f4,f4,f4,f4", converters={1: dmy_to_date})


def profit(open_prices, highest_prices, lowest_prices, close_prices):
    buying_prices = open_prices*0.98
    if lowest_prices <= buying_prices <= highest_prices:
        return (close_prices - buying_prices) * 100 / buying_prices
    else:
        return np.nan


profits = np.vectorize(profit)(open_prices, highest_prices, lowest_prices, close_prices)
Nan = np.isnan(profits)
dates, profits = dates[~Nan], profits[~Nan]
gain_dates, gain_profits = dates[profits > 0], profits[profits > 0]
loss_dates, loss_profits = dates[profits < 0], profits[profits < 0]

ax = mp.gca()
ax.xaxis.set_major_locator(md.WeekdayLocator(md.MO))
ax.xaxis.set_major_formatter(md.DateFormatter('%d %b'))
ax.yaxis.set_minor_locator(mp.MultipleLocator())
mp.tick_params(labelsize=10)
mp.xticks(rotation=35)
mp.grid(linestyle=":")
mp.ylim(-4, 5)

if dates.size > 0:
    mp.plot(dates, profits, color="grey", label="(+-)Profits")
    mean = profits.mean()
    mp.axhline(y=mean, linewidth=3, linestyle=":", label="Average Profits : %.2f"%mean)

if gain_dates.size > 0:
    mp.scatter(gain_dates, gain_profits, color="red", label="Gained Profit Points=%d天"%gain_dates.size)
    mean = gain_profits.mean()
    mp.axhline(y=mean, linewidth=3, color="red", linestyle=":", label="Average Gained Profits : %.2f"%mean)

if loss_dates.size > 0:
    mp.scatter(loss_dates, loss_profits, color="green", label="Loss Profit Points=%d天"%loss_dates.size)
    mean = loss_profits.mean()
    mp.axhline(y=mean, linewidth=3, color="green", linestyle=":", label="Average Loss Profits : %.2f" % mean)

mp.text(dates[12], -2.5, s='20210114\nDora practise.', fontsize=20, alpha=0.15)
mp.legend()
mp.show()
