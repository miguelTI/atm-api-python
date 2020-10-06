from unittest.mock import MagicMock

import pytest


class TestBalanceController:
    @pytest.fixture(autouse=True)
    def setUp(self):
        from controllers.balance import BalanceController
        self.testing_class = BalanceController

    def test_show_passa_o_query_param_account_id_ao_servico_de_balance(self, mocker):
        patched_request = mocker.patch('controllers.balance.request', MagicMock())
        patched_request.args.get.return_value = "100"
        patched_balance = mocker.patch('controllers.balance.Balance', MagicMock())
        self.testing_class.show()
        patched_balance.get.assert_called_with("100")

    def test_show_retorna_0_e_404_quando_a_conta_nao_existe(self, mocker):
        class ExpectedException(Exception):
            pass
        patched_request = mocker.patch('controllers.balance.request', MagicMock())
        patched_request.args.get.return_value = "123"
        patched_balance = mocker.patch('controllers.balance.Balance', MagicMock())
        patched_balance.get.side_effect = ExpectedException
        mocker.patch('controllers.balance.AccountNotFound', ExpectedException)
        assert self.testing_class.show() == ("0", 404)

    def test_show_retorna_o_balance_como_string(self, mocker):
        patched_request = mocker.patch('controllers.balance.request', MagicMock())
        patched_request.args.get.return_value = "100"
        patched_balance = mocker.patch('controllers.balance.Balance', MagicMock())
        patched_balance.get.return_value = 200
        assert isinstance(self.testing_class.show(), str)
