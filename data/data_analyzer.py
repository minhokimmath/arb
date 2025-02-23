import numpy as np

class DataAnalyzer:
    def __init__(self):
        pass

    def calculate_volatility(self, price_data):
        """
        변동성 계산
        :param price_data: 가격 데이터 리스트
        :return: 변동성 (표준편차)
        """
        returns = np.diff(price_data) / price_data[:-1]
        return np.std(returns) * 100  # 변동성을 %로 반환

    def calculate_trend(self, price_data):
        """
        추세 계산 (단순 이동평균 기반)
        :param price_data: 가격 데이터 리스트
        :return: 추세 (상승/하락/중립)
        """
        if len(price_data) < 2:
            return "neutral"
        ma_short = np.mean(price_data[-5:])  # 5기간 이동평균
        ma_long = np.mean(price_data[-10:])  # 10기간 이동평균
        if ma_short > ma_long:
            return "up"
        elif ma_short < ma_long:
            return "down"
        else:
            return "neutral"

    def calculate_volume_trend(self, volume_data):
        """
        거래량 추세 계산
        :param volume_data: 거래량 데이터 리스트
        :return: 거래량 추세 (증가/감소/중립)
        """
        if len(volume_data) < 2:
            return "neutral"
        if volume_data[-1] > volume_data[-2]:
            return "increasing"
        elif volume_data[-1] < volume_data[-2]:
            return "decreasing"
        else:
            return "neutral"
