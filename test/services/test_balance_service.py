from unittest.mock import MagicMock

import pytest


class TestEventController:
    @pytest.fixture(autouse=True)
    def setUp(self):
        from services.balance import Balance
        self.testing_class = Balance

    def test_get_chama_o_account_repository_com_o_id_recebido(self, mocker):
        patched_repository = mocker.patch('services.balance.AccountRepository', MagicMock())
        self.testing_class.get("100")
        patched_repository.find_by_id.assert_called_with("100")

    def test_get_retorna_so_o_balance_da_conta(self, mocker):
        patched_repository = mocker.patch('services.balance.AccountRepository', MagicMock())
        patched_account = patched_repository.find_by_id.return_value = MagicMock()
        patched_account.id = "100"
        patched_account.balance = 200
        assert self.testing_class.get("100") == 200
