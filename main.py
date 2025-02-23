from strategy.arbitrage import ArbitrageStrategy
import time
from config import TRADE_SETTINGS

def main():
    strategy = ArbitrageStrategy()
    while True:
        opportunity = strategy.find_arbitrage_opportunity()
        if opportunity:
            symbol, spot_price, futures_price, spread = opportunity
            print(f"Arbitrage opportunity found for {symbol}: Spread = {spread:.2f}%")
            trade_result = strategy.execute_trade(symbol, spot_price, futures_price, spread)
            if trade_result:
                print(f"Trade executed: {trade_result}")
            else:
                print("Trade execution failed.")
        time.sleep(TRADE_SETTINGS['interval'])

if __name__ == "__main__":
    main()
