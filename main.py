import yfinance as yf
import pandas as pd
import ta
import pyttsx3
from colorama import Fore, init
from datetime import datetime
import traceback

# =====================
# START
# =====================

init(autoreset=True)

engine = pyttsx3.init()

print("\n🚀 MARKET SNIPER AI STARTED\n")

# =====================
# SETTINGS
# =====================

SYMBOLS = [
    "BTC-USD",
    "ETH-USD",
    "GC=F"
]

TIMEFRAME = "15m"
PERIOD = "5d"

# =====================
# VOICE
# =====================

def voice(text):

    try:
        engine.say(text)
        engine.runAndWait()

    except:
        pass

# =====================
# SESSION
# =====================

def get_session():

    hour = datetime.now().hour

    if 0 <= hour < 8:
        return "ASIA"

    elif 8 <= hour < 16:
        return "LONDON"

    else:
        return "NEW YORK"

# =====================
# MAIN
# =====================

try:

    for symbol in SYMBOLS:

        print(Fore.CYAN + f"\n📊 SCANNING : {symbol}")

        # DOWNLOAD DATA
        df = yf.download(
            tickers=symbol,
            interval=TIMEFRAME,
            period=PERIOD,
            progress=False,
            auto_adjust=True
        )

        # CHECK
        if df.empty:

            print(Fore.RED + "❌ NO DATA")
            continue

        # FIX COLUMNS
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # INDICATORS
        df['EMA9'] = ta.trend.ema_indicator(df['Close'], window=9)
        df['EMA20'] = ta.trend.ema_indicator(df['Close'], window=20)
        df['RSI'] = ta.momentum.rsi(df['Close'], window=14)

        latest = df.iloc[-1]

        price = float(latest['Close'])
        ema9 = float(latest['EMA9'])
        ema20 = float(latest['EMA20'])
        rsi = float(latest['RSI'])

        # SIGNAL
        signal = "WAIT"

        if ema9 > ema20 and rsi > 55:
            signal = "BUY"

        elif ema9 < ema20 and rsi < 45:
            signal = "SELL"

        # SL TP
        if signal == "BUY":

            sl = round(price * 0.995, 2)
            tp = round(price * 1.015, 2)

        elif signal == "SELL":

            sl = round(price * 1.005, 2)
            tp = round(price * 0.985, 2)

        else:

            sl = 0
            tp = 0

        # RR
        if signal != "WAIT":

            rr = round(
                abs(tp - price) /
                abs(price - sl),
                2
            )

        else:
            rr = 0

        # OUTPUT
        print(Fore.YELLOW + "=" * 50)

        print(Fore.GREEN + f"💰 PRICE      : {price}")
        print(Fore.CYAN + f"⚡ SIGNAL     : {signal}")
        print(Fore.RED + f"🛑 STOP LOSS : {sl}")
        print(Fore.GREEN + f"✅ TAKE PROFIT: {tp}")
        print(Fore.MAGENTA + f"📈 RR         : 1:{rr}")
        print(Fore.BLUE + f"📉 RSI        : {round(rsi,2)}")
        print(Fore.WHITE + f"🌍 SESSION    : {get_session()}")

        print(Fore.YELLOW + "=" * 50)

        # VOICE
        if signal != "WAIT":
            voice(f"{signal} signal detected")

except Exception as e:

    print("\n❌ ERROR AAYA:\n")

    traceback.print_exc()

# =====================
# SCREEN HOLD
# =====================

input("\n⏸️ SCREEN BAND NAHI HOGI — ENTER DABAO EXIT KE LIYE...")