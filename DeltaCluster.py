import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "DayTrades", "BTCUSDT-trades-2025-03-23.csv")

TICK_SIZE = 0.1
CLUSTER_TICKS = 100  # $10
CLUSTER_SIZE = TICK_SIZE * CLUSTER_TICKS
MAX_CANDLES = 1440

# Load CSV
print("Loading data...")
df = pd.read_csv(CSV_PATH)

# Convert timestamp to datetime
df['time'] = pd.to_datetime(df['time'], unit='ms')
df['side'] = df['is_buyer_maker'].apply(lambda x: 'sell' if x else 'buy')

# Floor timestamps to minute
df['minute'] = df['time'].dt.floor('min')
unique_minutes = df['minute'].unique()[:MAX_CANDLES]

for minute in unique_minutes:
    trades = df[df['minute'] == minute]
    if trades.empty:
        continue

    low = trades['price'].min()
    high = trades['price'].max()
    clusters = defaultdict(lambda: {'buy': 0.0, 'sell': 0.0})

    # Cluster volume accumulation
    for _, row in trades.iterrows():
        cluster_key = round(((row['price'] + 5) // CLUSTER_SIZE) * CLUSTER_SIZE, 1)
        clusters[cluster_key][row['side']] += row['qty']

    # Get open and close price
    open_price = trades.iloc[0]['price']
    close_price = trades.iloc[-1]['price']

    # Total delta calculation
    total_buy = trades[trades['side'] == 'buy']['qty'].sum()
    total_sell = trades[trades['side'] == 'sell']['qty'].sum()
    total_delta = total_buy - total_sell

    # CVD divergence detection
    if total_delta > 0 and close_price < open_price:
        cvd_div = "CVD Divergence"
    elif total_delta < 0 and close_price > open_price:
        cvd_div = "CVD Divergence"
    else:
        cvd_div = "No Divergence"

    print(f"\nCandle: {minute.strftime('%Y-%m-%d %H:%M')}, High: {high}, Low: {low}, Trades: {len(trades)}")
    for level in sorted(clusters.keys(), reverse=True):
        buy_vol = clusters[level]['buy']
        sell_vol = clusters[level]['sell']
        delta = buy_vol - sell_vol
        imbalance = buy_vol == 0 or sell_vol == 0

        display_level = level + 5  # Shift visual level by $5
        line = f"Cluster ${display_level:.0f} - ${display_level + CLUSTER_SIZE:.0f} | Sell: {sell_vol:.4f}  ||  Buy: {buy_vol:.4f}  ||  Δ: {delta:.4f}"
        if imbalance:
            line += " | Imbalance: YES"
        print(line)

    print(f"\nTotal Delta: {total_delta:.4f} ({cvd_div})")
