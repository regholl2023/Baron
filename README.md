# Baron

Baron is a Python program for stock option trading decisions based on technical, fundamental, and volatility analysis. It is designed to assist traders in making decisions about buying or selling call and put options for a given stock. 

Baron uses various technical indicators, fundamental metrics, and historical volatility to generate trading recommendations. It also displays reasons for the trading decision.

# Synopsis 

Baron begins by importing necessary libraries, including yFinance for fetching stock data, TA-Lib for technical analysis, and matplotlib for chart plotting.

Several functions are defined to perform various tasks:

**fetch_data(ticker)** fetches historical stock data for the specified ticker.

**get_stock_data(ticker, period)** downloads stock data for a given period and adds technical indicators using TA-Lib.

**technical_analysis(stock_data)** analyzes technical indicators such as RSI, MACD, Bollinger Bands, Stochastic Oscillator, moving averages, ATR, and relative strength.

**volume_analysis(stock_data)** assesses trading volume.

**historical_volatility(stock_data)** calculates historical volatility.

**fundamental_analysis(ticker)** examines fundamental metrics like dividend yield and forward P/E ratio.

**basic_analysis(stock_data, ticker)** combines technical, volume, and fundamental analysis to provide a basic trading recommendation.

**volatility_analysis(data)** assesses volatility based on standard deviation.

**The decision(ticker, days_out)** function combines various analyses to make a trading decision. It calculates a total score based on the analyses and recommends buying or selling call or put options with strike prices. It also generates a price chart for visualization.

In the main part of Baron's code:

1. Users are prompted to enter a stock ticker and the number of days until option expiration.
2. The decision function is called to generate a trading decision and associated information.
3. The trading decision, strike prices, expiration date, reasons, and a chart of the stock's closing prices are displayed.
4. A disclaimer is provided, warning users of the potential risks and losses associated with options trading.

In conclusion, Baron is a comprehensive tool for traders to make informed decisions about options trading based on a combination of technical, fundamental, and volatility analyses. It provides transparency by explaining the reasoning behind each recommendation. Users are also reminded of the risks involved in options trading.

# Requirements

A terminal window (for now until I get a frontend developed).

Python3.  You can check to see if Python3 is on your system by running the command below:

```
python3 --version
```

If a version number prints out, you are good to go.

# Clone This Repository

Run this command below to clone this repo and begin using it.

```
git clone https://github.com/pavondunbar/Baron && cd Baron
```


# Create a Python Virtual Environment

It is recommended to create a Python virtual environment to run Baron.  Running a virtual environment will prevent library conflicts with other Python projects or applications you may have on your system.

Create a virtual environment named BaronEnv (or whatever you want to call it) by running the following command:

```
python3 -m venv BaronEnv
```

If your virtual environment isn't created, you can use this command to create it:

```
virtualenv BaronEnv
```

Next, type this into the terminal

```
ls
```

You should see BaronEnv (or whatever name you gave your virtual environment) and Baron.py

If you see both of those items, your virtual environment has been set up.

# Activate the Virtual Environment

After you've created your Python virtual environment, activate it by running the command below:

```
source BaronEnv/bin/activate
```

**NOTE:** You can turn off your virtual environment by typing this in the terminal

```
deactivate
```

# Install Required Libraries Using PIP

Run the following command to install the libraries you need to run and train Roxy:

```
pip install yfinance matplotlib numpy ta mplcursors datetime
```

# Initialize Baron

Now the fun begins!  Run the following command to Initialize Baron:

```
python3 Baron.py
```

Baron will initialize and ask you to submit a stock ticker symbol for a company as well as a number of days out for the option's expiration.

After you submit the stock ticker symbol and number days out for the expiration, Baron will do a quick iteration over the dataset to make a determination.

Once Baron is complete with its iteration, it will output a decision for you to either BUY or SELL a CALL or PUT OPTION, the strike prices ITM (in the money) and OTM (out the money), and the reasons for its decision.

# Closing Notes

1. Baron uses the Yahoo Finance (yfinance) dataset to make its determination.
2. Baron uses the following technical indicators: Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD), Bollinger Bands, Stochastic Oscillators, Moving Averages (Golden Cross and Death Cross), Average True Range (ATR), Relative Strength (Compared to a Market Index), and Price Patterns (e.g., Head and Shoulders).
3. As of this time, Baron **does not use the Option Greeks (Delta, Gamma, Vega, Theta, and Rho)** to make its determination.
4. Baron is **not an AI model**

# Disclaimer

If you enjoy using Baron to hopefully make you more money and be better informed to make an investment decision regarding stock options, that is awesome and I appreciate it.  But please...**do not use Baron as a "final decision maker" when analyzing a certain stock.** 

As a human, you should still do your research and due diligence before you make any investment decisions to buy or sell call or put option contracts.

By using Baron, you agree to hold Baron, its creator Pavon Dunbar, or any affiliates or representatives of Baron harmless from any financial damages, errors, etc that may result from its use or misuse.

Baron is a **work in progress** and will be consistently updated.

# Let's Get Social!

Feel free to connect with me.  My Linktree is https://linktr.ee/pavondunbar
