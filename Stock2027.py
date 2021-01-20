import numpy as np
import matplotlib.pyplot as mp
import matplotlib.dates as md
import datetime as dt
from matplotlib.font_manager import FontProperties

# 使圖片說明呈現中文
mp.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
mp.rcParams['axes.unicode_minus'] = False

# 資料圖片標題
mp.figure("Trading Simulation 股票草擬策略", facecolor="lightgrey", figsize=(16, 7))
mp.title("Aug/2020-Jan/2021 大成鋼", fontsize=20)

# 資料x、y軸
mp.xlabel("Dates 日期", fontsize=14)
mp.ylabel("Profits 利潤率", fontsize=14)


# 函數轉換日期類型
def dmy_to_date(dmy):
    dmy = str(dmy, encoding='utf8')
    date = dt.datetime.strptime(dmy, '%m-%d-%Y').date()
    return date


# 依據 開盤、高價、低價、收盤價資料傳入
dates, open_prices, highest_prices, lowest_prices, close_prices \
    = np.loadtxt("./2027_2.twd.csv", delimiter=',', usecols=(1, 3, 4, 5, 6), unpack=True,
                 dtype="M8[D],f4,f4,f4,f4", converters={1: dmy_to_date})



# 擬定購買價格策略函數
def profit(open_prices, highest_prices, lowest_prices, close_prices):
    # 只要價格低於開盤價*0.98元便買進
    buying_prices = open_prices*0.98
    if lowest_prices <= buying_prices <= highest_prices:
        return (close_prices - buying_prices) * 100 / buying_prices
    # 但因策略發生價格未達到下限，表示持續上漲，策略失效買不到
    else:
        return np.nan  # 返回無效數值


# 使用向量化將數組轉成標量化運算
profits = np.vectorize(profit)(open_prices, highest_prices, lowest_prices, close_prices)
# 過濾因策略無效產生的無效值(未產生交易)
Nan = np.isnan(profits)                      # 返回過濾出來的無效交易值
# 將過濾出來的無效交易值放入日期、利潤源中
dates, profits = dates[~Nan], profits[~Nan]  # 返回剩下的策略成功數值(盈虧參雜)
# 再細分出營利日(利潤大於0
gain_dates, gain_profits = dates[profits > 0], profits[profits > 0]
# 再細分出虧損日(利潤小於0
loss_dates, loss_profits = dates[profits < 0], profits[profits < 0]


# 設定格線繪製
ax = mp.gca()
# 設定x軸主要刻度(依據每周周一，不含周末)
ax.xaxis.set_major_locator(md.WeekdayLocator(md.MO))
# 設定X軸主刻度顯示方式(日期/月份英文縮寫)
ax.xaxis.set_major_formatter(md.DateFormatter('%d %b'))
# 設定Y軸主要次刻度(依據多點定位器，默認參數為1)
ax.yaxis.set_minor_locator(mp.MultipleLocator())
# 設定所有標籤字體大小為10
mp.tick_params(labelsize=10)
mp.xticks(rotation=35)
mp.grid(linestyle=":")
mp.ylim(-4, 5)

# 繪製圖前，須考量，並非交易日都會成功，萬一此策略全失策，即交易日就為空，故當日期>0，才有交易成功
if dates.size > 0:
    mp.plot(dates, profits, color="grey", label="(+-)Profits")
    # 繪製綜合平均營利水平線
    mean = profits.mean()
    mp.axhline(y=mean, linewidth=3, linestyle=":", label="Average Profits : %.2f"%mean)
# 繪製營利日
if gain_dates.size > 0:
    mp.scatter(gain_dates, gain_profits, color="red", label="Gained Profit Points=%d天"%gain_dates.size)
    mean = gain_profits.mean()
    # 繪製單純平均營利水平線
    mp.axhline(y=mean, linewidth=3, color="red", linestyle=":", label="Average Gained Profits : %.2f"%mean)
# 繪製虧損日
if loss_dates.size > 0:
    mp.scatter(loss_dates, loss_profits, color="green", label="Loss Profit Points=%d天"%loss_dates.size)
    mean = loss_profits.mean()
    # 繪製單純平均虧損水平線
    mp.axhline(y=mean, linewidth=3, color="green", linestyle=":", label="Average Loss Profits : %.2f" % mean)

mp.text(dates[12], -2.5, s='20210114\nDora practise.', fontsize=20, alpha=0.15)
mp.legend()
mp.show()
