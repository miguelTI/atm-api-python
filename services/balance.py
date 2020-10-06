from repositories.account import AccountRepository, AccountNotFound


class Balance:
    @staticmethod
    def get(account_id: str):
        account = AccountRepository.find_by_id(account_id)
        return account.balance
