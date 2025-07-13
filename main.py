import yfinance as yf
import pandas as pd
import requests

# Telegram bot ayarları
bot_token = "7820024651:AAE14R_HnsKvcKlnN7OWlZwEr1Ow_Lahk-M"
chat_id = "5106788774"

symbols = ['BTC-USD', 'ETH-USD', 'AAPL']
messages = []

for symbol in symbols:
    print(f"\n{symbol} için analiz yapılıyor...")
    df = yf.download(symbol, period='3mo')
    df = df.dropna()

    # RSI hesapla
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD hesapla
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26

    # Son veriler
    last = df.iloc[-1]
    msg = f"📊 *{symbol}*\nFiyat: {last['Close']:.2f}\nRSI: {last['RSI']:.2f}\nMACD: {last['MACD']:.2f}"
    messages.append(msg)

# Telegram'a gönder
full_message = "\n\n".join(messages)
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {
    "chat_id": chat_id,
    "text": full_message,
    "parse_mode": "Markdown"
}
response = requests.post(url, data=payload)
if response.status_code == 200:
    print("✅ Telegram'a başarıyla gönderildi.")
else:
    print("❌ Gönderim başarısız:", response.text)
