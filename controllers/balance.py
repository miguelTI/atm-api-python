from flask import request
from services.balance import Balance, AccountNotFound


class BalanceController:
    @staticmethod
    def show():
        account_id = str(request.args.get('account_id', ''))
        try:
            balance = Balance.get(account_id)
        except AccountNotFound:
            return "0", 404
        return str(balance)
