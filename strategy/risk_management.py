class RiskManagement:
    def __init__(self, max_loss_percentage=0.5, max_position_size=0.01):
        """
        리스크 관리 클래스
        :param max_loss_percentage: 최대 손실 허용 비율 (예: 0.5%)
        :param max_position_size: 최대 포지션 크기 (예: 총 자산의 1%)
        """
        self.max_loss_percentage = max_loss_percentage
        self.max_position_size = max_position_size

    def calculate_position_size(self, total_balance, current_price):
        """
        포지션 크기 계산
        :param total_balance: 총 자산
        :param current_price: 현재 가격
        :return: 포지션 크기 (거래 수량)
        """
        max_position_value = total_balance * self.max_position_size
        return max_position_value / current_price

    def check_stop_loss(self, entry_price, current_price):
        """
        손절매 조건 확인
        :param entry_price: 진입 가격
        :param current_price: 현재 가격
        :return: 손절매 필요 여부 (True/False)
        """
        loss_percentage = abs((current_price - entry_price) / entry_price) * 100
        return loss_percentage >= self.max_loss_percentage

    def check_take_profit(self, entry_price, current_price, take_profit_percentage):
        """
        익절매 조건 확인
        :param entry_price: 진입 가격
        :param current_price: 현재 가격
        :param take_profit_percentage: 익절매 기준 비율 (예: 0.2%)
        :return: 익절매 필요 여부 (True/False)
        """
        profit_percentage = abs((current_price - entry_price) / entry_price) * 100
        return profit_percentage >= take_profit_percentage
