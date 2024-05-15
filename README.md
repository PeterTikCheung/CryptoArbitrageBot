<h3 align="center">Crypto Lantency Trading Bot</h3>

---

## 🧐 About <a name = "About"></a>

The Trading Bot is an automated tool designed to execute trading strategies based on predefined rules. It connects to a cryptocurrency exchange (Binance and Bybit) via API and performs trades on your behalf.


## 🎈 Prerequisites <a name="prerequisites"></a>

To use the Trading Bot, you need the following prerequisites:
<ul>
  <li>Python 3.7 or above</li>
  <li>API credentials from a supported cryptocurrency exchange</li>
  <li>Provides logging ("log.txt" file in log directory) and error handling for troubleshooting</li>
</ul>

## 🏁 Getting Started <a name = "getting_started"></a>
1. install module

```
pip install -r requirement.txt
```
2. run the main file
```
python3 src/main.py
```


## 🔧 Features <a name = "features"></a>

<ul>
  <li>Fetches all real-time market data from the exchange</li>
  <li>Compare the symbols in Bybit with same symbols in Binance</li>
  <li>Executes future trades based on price difference in different exchanges</li>
  <li>Provides logging ("log.txt" file in log directory) and error handling for troubleshooting</li>
  <li>Config file for setting up your own setting</li>
  <li>Place order of specific symbol with stop loss and take profit</li>
</ul>




## ✍️ Authors <a name = "authors"></a>

- [@PeterMtCheung](https://github.com/PeterMtCheung) - Idea & Initial work
