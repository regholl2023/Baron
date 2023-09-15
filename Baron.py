# Baron
# A Heuristic-based Rule System model that predicts CALL or PUT options based on pre-trained data
# Created by Pavon Dunbar

import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import datetime
import warnings  # Comment Out To Show Warnings Globally
import mplcursors
warnings.filterwarnings("ignore")  # Comment Out To Show Warnings Globally
from ta import add_all_ta_features
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.momentum import StochasticOscillator
from ta.volatility import AverageTrueRange


def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period="1y")
    return stock_data


def get_stock_data(ticker, period='1y'):
    stock_data = yf.download(ticker, period=period)
    stock_data = add_all_ta_features(stock_data, open="Open", high="High", low="Low", close="Close", volume="Volume",
                                     fillna=True)
    return stock_data


def technical_analysis(stock_data):
    reasons = []

    # RSI Analysis
    rsi = stock_data['momentum_rsi'][-1]
    if rsi < 30:
        reasons.append(f"RSI indicates oversold conditions at {rsi:.2f}.")
    elif rsi > 70:
        reasons.append(f"RSI indicates overbought conditions at {rsi:.2f}.")

    # MACD Analysis using columns from `add_all_ta_features`
    macd_line = stock_data['trend_macd'][-1]
    macd_signal = stock_data['trend_macd_signal'][-1]
    if macd_line > macd_signal:
        reasons.append("MACD line is above the signal line indicating bullish momentum.")
    elif macd_line < macd_signal:
        reasons.append("MACD line is below the signal line indicating bearish momentum.")

    # Bollinger Bands Analysis
    bollinger = BollingerBands(close=stock_data['Close'], window=20, window_dev=2)
    stock_data['bollinger_hband'] = bollinger.bollinger_hband()
    stock_data['bollinger_lband'] = bollinger.bollinger_lband()
    if stock_data['Close'][-1] > stock_data['bollinger_hband'][-1]:
        reasons.append("Price is above the upper Bollinger Band, indicating it might be overbought.")
    elif stock_data['Close'][-1] < stock_data['bollinger_lband'][-1]:
        reasons.append("Price is below the lower Bollinger Band, indicating it might be oversold.")

    # Stochastic Oscillator Analysis
    stochastic_oscillator = StochasticOscillator(high=stock_data['High'], low=stock_data['Low'],
                                                 close=stock_data['Close'], window=14, smooth_window=3)
    stock_data['stoch_osc'] = stochastic_oscillator.stoch()
    stock_data['stoch_signal'] = stochastic_oscillator.stoch_signal()
    if stock_data['stoch_osc'][-1] > 80 and stock_data['stoch_signal'][-1] > 80:
        reasons.append("Stochastic Oscillator indicates overbought conditions.")
    elif stock_data['stoch_osc'][-1] < 20 and stock_data['stoch_signal'][-1] < 20:
        reasons.append("Stochastic Oscillator indicates oversold conditions.")

    # Moving Averages Crossover Analysis
    short_window = 50
    long_window = 200
    short_mavg = stock_data['Close'].rolling(window=short_window).mean()
    long_mavg = stock_data['Close'].rolling(window=long_window).mean()
    if short_mavg[-1] > long_mavg[-1] and short_mavg[-2] <= long_mavg[-2]:
        reasons.append("Golden cross: Short-term moving average crossed above long-term moving average, indicating potential bullish momentum.")
    elif short_mavg[-1] < long_mavg[-1] and short_mavg[-2] >= long_mavg[-2]:
        reasons.append("Death cross: Short-term moving average crossed below long-term moving average, indicating potential bearish momentum.")

    # Average True Range (ATR) Analysis
    # ATR Calculation
    atr_period = 14  # You can adjust the ATR period as needed
    atr = AverageTrueRange(stock_data['High'], stock_data['Low'], stock_data['Close'], atr_period)
    stock_data['atr'] = atr.average_true_range()
    atr_value = stock_data['atr'][-1]
    if atr_value > 0.05:  # You can adjust the threshold
        reasons.append(f"The Average True Range (ATR) is high ({atr_value:.2f}), indicating increased volatility.")

    # Relative Strength Analysis
    market_index_ticker = '^GSPC'  # Replace with the relevant market index ticker
    market_data = yf.download(market_index_ticker, period="1y")
    stock_returns = stock_data['Close'].pct_change().dropna()
    market_returns = market_data['Close'].pct_change().dropna()
    stock_relative_strength = (stock_returns.mean() - market_returns.mean()) / stock_returns.std()
    if stock_relative_strength > 0:
        reasons.append(f"The stock shows relative strength compared to the market index.")

    # Price Patterns Analysis (Example: Head and Shoulders)
    if stock_data['Close'][-3] > stock_data['Close'][-2] < stock_data['Close'][-1]:
        reasons.append("Possible head and shoulders pattern detected, which may indicate a trend reversal.")

    return reasons


def volume_analysis(stock_data):
    reasons = []

    latest_volume = stock_data['Volume'][-1]
    average_volume = stock_data['Volume'].mean()

    if latest_volume > (1.5 * average_volume):
        reasons.append(f"Trading volume is significantly higher than average, indicating strong market interest.")
    elif latest_volume < (0.5 * average_volume):
        reasons.append(f"Trading volume is much lower than average, indicating potential disinterest or consolidation.")

    return reasons


def historical_volatility(stock_data):
    log_returns = np.log(stock_data['Close'] / stock_data['Close'].shift(1))
    volatility = log_returns.std() * np.sqrt(252)  # Annualizing daily volatility
    return volatility


def fundamental_analysis(ticker):
    reasons = []
    fundamentals = yf.Ticker(ticker).info

    if "dividendYield" in fundamentals and fundamentals["dividendYield"] > 0.03:
        reasons.append(f"The stock has a good dividend yield of {fundamentals['dividendYield'] * 100}%.")

    if "forwardPE" in fundamentals and fundamentals["forwardPE"] < 20:
        reasons.append(f"The stock has a forward P/E ratio of {fundamentals['forwardPE']}, indicating it might be undervalued.")

    return reasons


def basic_analysis(stock_data, ticker):
    reasons = []

    # Moving Average Analysis
    short_window = 40
    long_window = 100

    signals = stock_data.copy()
    signals['short_mavg'] = stock_data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = stock_data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    if signals['short_mavg'][-1] > signals['long_mavg'][-1] and signals['short_mavg'][-2] <= signals['long_mavg'][-2]:
        reasons.append("Short-term moving average crossed above long-term moving average, indicating potential bullish momentum.")

    # Incorporate Technical Analysis
    reasons.extend(technical_analysis(stock_data))

    # Incorporate Volume Analysis
    reasons.extend(volume_analysis(stock_data))

    # Incorporate Fundamental Analysis
    reasons.extend(fundamental_analysis(ticker))

    volatility = historical_volatility(stock_data)
    if volatility > 0.3:  # a basic threshold
        reasons.append(f"The stock has high historical volatility of {volatility:.2f}, indicating potential risks.")

    if reasons:
        return "uptrend", reasons
    else:
        return "downtrend", ["Recent trends do not support a strong bullish signal."]


def volatility_analysis(data):
    reasons = []

    # Use standard deviation as a measure of volatility.
    # The larger the standard deviation, the more volatile the stock.
    volatility = data['Close'].std()

    if volatility > 1.5:  # This threshold can be adjusted based on your requirements.
        reasons.append(f"The stock has high historical volatility of {volatility:.2f}, indicating potential risks.")

    return reasons


def decision(ticker, days_out=30):
    stock_data = fetch_data(ticker)
    stock_data = add_all_ta_features(
        stock_data,
        open="Open",
        high="High",
        low="Low",
        close="Close",
        volume="Volume"
    )

    reasons = []

    fundamental_reasons = fundamental_analysis(ticker)
    technical_reasons = technical_analysis(stock_data)
    volume_reasons = volume_analysis(stock_data)
    volatility_reasons = volatility_analysis(stock_data)

    reasons.extend(fundamental_reasons)
    reasons.extend(technical_reasons)
    reasons.extend(volume_reasons)
    reasons.extend(volatility_reasons)

    # Decision based on reasons count
    total_score = len(fundamental_reasons) + len(technical_reasons) - len(volume_reasons) - len(volatility_reasons)

    current_price = stock_data['Close'].iloc[-1]
    price_adjustment = current_price * 0.05

    if total_score > 3:
        action = "BUY a CALL option"
        strike_price_otm = current_price + price_adjustment
        strike_price_itm = current_price - price_adjustment
    elif total_score > 0:
        action = "SELL a PUT option"
        strike_price_otm = current_price - price_adjustment
        strike_price_itm = current_price + price_adjustment
    elif total_score > -3:
        action = "SELL a CALL option"
        strike_price_otm = current_price - price_adjustment
        strike_price_itm = current_price + price_adjustment
    else:
        action = "BUY a PUT option"
        strike_price_otm = current_price + price_adjustment
        strike_price_itm = current_price - price_adjustment

    # Plot the stock's closing prices
    plt.figure(figsize=(12, 6))
    line, = plt.plot(stock_data.index, stock_data['Close'], label='Closing Price', color='blue')

    plt.title(f'{ticker} Stock Price Chart')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    # Add cursor tooltips to display the closing price and option Greeks
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f"Date: {stock_data.index[int(sel.target.index)].strftime('%Y-%m-%d')}\n"
        f"Closing Price: ${line.get_ydata()[int(sel.target.index)]:.2f}\n"
    ))    

    # Save the chart to a file or display it
    chart_filename = f'{ticker}_chart.png'
    plt.savefig(chart_filename)
    plt.show()

    return {
        "decision": action,
        "strike_price_otm": strike_price_otm,
        "strike_price_itm": strike_price_itm,
        "expiration_date": (datetime.datetime.now() + datetime.timedelta(days=days_out)).strftime('%Y-%m-%d'),
        "reasons": reasons,
        "chart_filename": chart_filename  # Include the chart filename in the result
    }


if __name__ == "__main__":
    print("--- Hello there! I'm Baron, your personal stock option trading and investing assistant. Let's make you SOME MONEY!! ---\n")
    ticker = input("Enter a stock ticker: ").upper()
    days_out = int(input("Enter the number of days out for the option's expiration: "))

    result = decision(ticker, days_out)

    print("\nDecision:", result['decision'])
    print(f"Strike Price (OTM): ${result['strike_price_otm']:.2f}")
    print(f"Strike Price (ITM): ${result['strike_price_itm']:.2f}")
    print("Expiration Date:", result['expiration_date'])
    print("\nReasons:")
    for reason in result['reasons']:
        print(f"- {reason}")

    # Display the chart filename
    print("\nChart:")
    print(result['chart_filename'])

    # Disclaimer
    print("\n--- Disclaimer: Potential for Losses in Options Investing ---\n")
    print("Options investing carries the potential for significant financial losses. Due to factors like market volatility, leverage, time decay, and incomplete information, options trading can result in substantial losses. It's important to note that the information provided here is not financial advice. Investors should seek guidance from a qualified financial advisor and exercise caution when considering options trading to manage these risks effectively. By using this tool, you agree to hold Baron, its creator Pavon Dunbar, and any affiliates and representatives harmless form any financial losses that may result from errors and misuse.")
