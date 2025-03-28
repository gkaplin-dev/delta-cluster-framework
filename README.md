# delta-cluster-framework

This is a lightweight Python tool that reconstructs delta clusters from Binance trade data — similar to ExoCharts' visualization — for backtesting and signal research.

## Features
- Rebuilds 1-minute candles from raw trade data
- Splits price into customizable cluster sizes (default: 100 ticks / $10)
- Calculates buy/sell volume, delta, and imbalance at each price level
- Highlights potential divergence or extreme orderflow setups
- Easily adjustable logic for testing new strategies

## Example Use
Ideal for strategy backtesting based on:
- CVD divergence
- Footprint imbalances
- Price behavior around extremes
- Market microstructure

## Example Output
- On the left is the terminal output from the script.
- On the right is ExoCharts' delta cluster view for the same candle.
- This confirms that the script correctly reconstructs price clusters, delta, and imbalance levels.

![ExoCharts-comparison](https://github.com/user-attachments/assets/d894c1dd-7ada-49fd-a56f-c8ceef2aea1c)

## Customization
- The current version highlights CVD divergences (delta vs price direction).
- It also detects cluster imbalances (e.g. only buys or only sells at a given level).
- Both features are easy to modify or remove depending on your research or backtest focus.

## Requirements
- Python 3.x
- pandas, numpy
- Trade data from Binance market data

## Note
To run the script use Binance's archived data available here: [Binance Data Portal](https://data.binance.vision/?prefix=data/futures/um/daily/trades/)


## Disclaimer
This is a research and protype tool only. Not financial advice.
