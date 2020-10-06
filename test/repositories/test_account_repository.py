from unittest.mock import MagicMock

import pytest


class TestAccountRepository:
    @pytest.fixture(autouse=True)
    def setUp(self):
        from repositories.account import AccountRepository
        self.testing_class = AccountRepository
        self.testing_class.existing_accounts = {}

    def test_find_by_id_retorna_a_conta_se_existe_dentro_do_dicionario(self):
        expected_account = MagicMock()
        mocked_accounts = {
            "100": expected_account
        }
        self.testing_class.existing_accounts = mocked_accounts
        assert self.testing_class.find_by_id("100") == expected_account

    def test_find_by_id_lanca_account_not_found_se_a_conta_nao_existe_no_dicionario(self, mocker):
        class MockedException(Exception):
            pass

        mocked_accounts = {
            "100": MagicMock()
        }
        self.testing_class.existing_accounts = mocked_accounts
        mocker.patch('repositories.account.AccountNotFound', MockedException)
        with pytest.raises(MockedException):
            self.testing_class.find_by_id("200")

    def test_create_retorna_uma_nova_conta_com_o_id_indicado(self, mocker):
        mocker.patch('repositories.account.Account', MagicMock())
        assert self.testing_class.create("100").id == "100"

    def test_create_lanca_duplicated_account_id_se_o_id_informado_ja_existe_no_dicionario(self, mocker):
        class MockedException(Exception):
            pass

        mocked_accounts = {
            "100": MagicMock()
        }
        self.testing_class.existing_accounts = mocked_accounts
        mocker.patch('repositories.account.DuplicatedAccountId', MockedException)
        with pytest.raises(MockedException):
            self.testing_class.create("100")

    def test_save_acrescenta_a_conta_no_dicionario_usando_o_id_como_chave(self):
        mocked_accounts = {}
        self.testing_class.existing_accounts = mocked_accounts
        mocked_account = MagicMock()
        mocked_account.id = "100"
        self.testing_class.save(mocked_account)
        assert "100" in self.testing_class.existing_accounts

    def test_save_atualiza_a_conta_no_dicionario(self):
        mocked_accounts = {
            "100": MagicMock()
        }
        self.testing_class.existing_accounts = mocked_accounts
        mocked_account = MagicMock()
        mocked_account.id = "100"
        self.testing_class.save(mocked_account)
        assert self.testing_class.existing_accounts["100"] == mocked_account

    def test_reset_apaga_todas_as_contas_existentes_no_dicionario(self):
        mocked_accounts = {
            "100": MagicMock(),
            "200": MagicMock(),
            "300": MagicMock()
        }
        self.testing_class.existing_accounts = mocked_accounts
        self.testing_class.reset()
        assert not self.testing_class.existing_accounts
