from ..api.bybit_api import BybitAPI
from config import TRADE_SETTINGS
import time

class ArbitrageStrategy:
    def __init__(self):
        self.api = BybitAPI()
        self.symbols = TRADE_SETTINGS['symbols']
        self.min_spread = TRADE_SETTINGS['min_spread']
        self.max_spread = TRADE_SETTINGS['max_spread']

    def calculate_spread(self, spot_price, futures_price):
        """스프레드 계산"""
        if spot_price and futures_price:
            return ((futures_price - spot_price) / spot_price) * 100
        return None

    def find_arbitrage_opportunity(self):
        """차익거래 기회 찾기"""
        for symbol in self.symbols:
            spot_price = self.api.get_market_price(symbol, 'spot')
            futures_price = self.api.get_market_price(symbol, 'linear')
            spread = self.calculate_spread(spot_price, futures_price)
            if spread and self.min_spread <= abs(spread) <= self.max_spread:
                return symbol, spot_price, futures_price, spread
        return None

    def execute_trade(self, symbol, spot_price, futures_price, spread):
        """거래 실행"""
        if spread > 0:
            # 선물이 더 비쌈 -> 현물 매수, 선물 매도
            spot_side = "Buy"
            futures_side = "Sell"
        else:
            # 현물이 더 비쌈 -> 현물 매도, 선물 매수
            spot_side = "Sell"
            futures_side = "Buy"

        # 주문 실행
        spot_order = self.api.place_order('spot', symbol, spot_side, 'Market', TRADE_SETTINGS['trade_amount'])
        futures_order = self.api.place_order('linear', symbol, futures_side, 'Market', TRADE_SETTINGS['trade_amount'])

        if spot_order and futures_order:
            return {
                'symbol': symbol,
                'spot_price': spot_price,
                'futures_price': futures_price,
                'spread': spread,
                'spot_order': spot_order,
                'futures_order': futures_order
            }
        return None
