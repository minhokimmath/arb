import requests
import hmac
import hashlib
import time
import json
from datetime import datetime
from config import BYBIT_API_KEY, BYBIT_API_SECRET, TESTNET

class BybitAPI:
    def __init__(self):
        self.base_url = "https://api-testnet.bybit.com" if TESTNET else "https://api.bybit.com"
        self.api_key = BYBIT_API_KEY
        self.api_secret = BYBIT_API_SECRET

    def _generate_signature(self, params):
        """API 요청을 위한 서명 생성"""
        timestamp = str(int(time.time() * 1000))
        params['timestamp'] = timestamp
        params['api_key'] = self.api_key
        params['recv_window'] = '5000'
        sorted_params = dict(sorted(params.items()))
        param_str = '&'.join([f"{key}={value}" for key, value in sorted_params.items()])
        signature = hmac.new(
            bytes(self.api_secret, 'utf-8'),
            param_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        params['sign'] = signature
        return params

    def _request(self, method, endpoint, params=None):
        """API 요청 보내기"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = {'Content-Type': 'application/json'}
            if method.upper() == "GET":
                response = requests.get(url, params=self._generate_signature(params), headers=headers)
            else:
                response = requests.post(url, json=self._generate_signature(params), headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Request error: {str(e)}")
            return None

    def get_market_price(self, symbol, category='spot'):
        """현물 또는 선물 가격 조회"""
        endpoint = "/v5/market/tickers"
        params = {'category': category, 'symbol': symbol}
        response = self._request("GET", endpoint, params)
        if response and 'result' in response and 'list' in response['result']:
            return float(response['result']['list'][0]['lastPrice'])
        return None

    def place_order(self, category, symbol, side, order_type, qty):
        """주문 실행"""
        endpoint = "/v5/order/create"
        params = {
            'category': category,
            'symbol': symbol,
            'side': side,
            'orderType': order_type,
            'qty': str(qty)
        }
        return self._request("POST", endpoint, params)
