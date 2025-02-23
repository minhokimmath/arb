from api.bybit_api import BybitAPI
import time
from datetime import datetime

class DataCollector:
    def __init__(self):
        self.api = BybitAPI()

    def collect_market_data(self, symbol, category='spot'):
        """
        시장 데이터 수집 (가격, 거래량 등)
        :param symbol: 거래 대상 코인 (예: BTCUSDT)
        :param category: 시장 종류 (spot 또는 linear)
        :return: 가격, 거래량 데이터
        """
        endpoint = "/v5/market/tickers"
        params = {'category': category, 'symbol': symbol}
        response = self.api._request("GET", endpoint, params)
        if response and 'result' in response and 'list' in response['result']:
            ticker = response['result']['list'][0]
            return {
                'price': float(ticker['lastPrice']),
                'volume': float(ticker['volume24h']),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        return None

    def collect_historical_data(self, symbol, category='spot', interval='1', limit=100):
        """
        과거 데이터 수집 (캔들 데이터)
        :param symbol: 거래 대상 코인 (예: BTCUSDT)
        :param category: 시장 종류 (spot 또는 linear)
        :param interval: 데이터 간격 (1분, 5분 등)
        :param limit: 데이터 개수
        :return: 캔들 데이터 리스트
        """
        endpoint = "/v5/market/kline"
        params = {
            'category': category,
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        response = self.api._request("GET", endpoint, params)
        if response and 'result' in response and 'list' in response['result']:
            return response['result']['list']
        return None
