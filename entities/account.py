class Account:
    def __init__(self):
        self.id: int = 0
        self.balance: int = 0

    def to_dict(self):
        return {
            'id': self.id,
            'balance': self.balance
        }
