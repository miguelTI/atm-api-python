from entities.account import Account


class AccountRepository:
    existing_accounts = {}

    @staticmethod
    def find_by_id(id: str) -> Account:
        if id not in AccountRepository.existing_accounts:
            raise AccountNotFound
        return AccountRepository.existing_accounts[id]

    @staticmethod
    def create(id: str) -> Account:
        if id in AccountRepository.existing_accounts:
            raise DuplicatedAccountId
        new_account = Account()
        new_account.id = id
        return new_account

    @staticmethod
    def save(account: Account):
        AccountRepository.existing_accounts[account.id] = account

    @staticmethod
    def reset():
        AccountRepository.existing_accounts = {}


class AccountNotFound(Exception):
    pass


class DuplicatedAccountId(Exception):
    pass
