from strategy.arbitrage import ArbitrageStrategy
from strategy.risk_management import RiskManagement
from data.data_collector import DataCollector
from data.data_analyzer import DataAnalyzer
import time
from config import TRADE_SETTINGS

def main():
    strategy = ArbitrageStrategy()
    risk_manager = RiskManagement(max_loss_percentage=0.5, max_position_size=0.01)
    data_collector = DataCollector()
    data_analyzer = DataAnalyzer()

    while True:
        # 차익거래 기회 탐색
        opportunity = strategy.find_arbitrage_opportunity()
        if opportunity:
            symbol, spot_price, futures_price, spread = opportunity
            print(f"Arbitrage opportunity found for {symbol}: Spread = {spread:.2f}%")

            # 리스크 관리: 포지션 크기 계산
            total_balance = 10000  # 예시: 총 자산 10,000 USDT
            position_size = risk_manager.calculate_position_size(total_balance, spot_price)
            print(f"Calculated position size: {position_size:.6f} {symbol}")

            # 거래 실행
            trade_result = strategy.execute_trade(symbol, spot_price, futures_price, spread)
            if trade_result:
                print(f"Trade executed: {trade_result}")

                # 리스크 관리: 손절매 및 익절매 확인
                entry_price = spot_price
                current_price = data_collector.collect_market_data(symbol, 'spot')['price']
                if risk_manager.check_stop_loss(entry_price, current_price):
                    print("Stop loss triggered!")
                if risk_manager.check_take_profit(entry_price, current_price, 0.2):
                    print("Take profit triggered!")
            else:
                print("Trade execution failed.")

        # 데이터 수집 및 분석
        historical_data = data_collector.collect_historical_data(symbol, 'spot', interval='1', limit=100)
        if historical_data:
            price_data = [float(data[4]) for data in historical_data]  # 종가 데이터 추출
            volatility = data_analyzer.calculate_volatility(price_data)
            trend = data_analyzer.calculate_trend(price_data)
            print(f"Market Analysis - Volatility: {volatility:.2f}%, Trend: {trend}")

        time.sleep(TRADE_SETTINGS['interval'])

if __name__ == "__main__":
    main()
