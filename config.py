# Bybit API 설정
BYBIT_API_KEY = "YOUR_DEMO_API_KEY"
BYBIT_API_SECRET = "YOUR_DEMO_API_SECRET"
TESTNET = True  # 테스트넷 사용 여부

# 거래 설정
TRADE_SETTINGS = {
    'symbols': ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT'],  # 거래 대상 코인
    'trade_amount': 0.001,  # 기본 거래 수량 (BTC 기준)
    'min_spread': 0.1,  # 최소 스프레드 (0.1%)
    'max_spread': 1.0,  # 최대 스프레드 (1%)
    'leverage': 1,  # 레버리지
    'interval': 60,  # 모니터링 간격 (초)
    'stop_loss': 0.5,  # 손절매 기준 (0.5%)
    'take_profit': 0.2,  # 익절매 기준 (0.2%)
}

# 로깅 설정
LOG_SETTINGS = {
    'filename': 'arbitrage.log',
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}
