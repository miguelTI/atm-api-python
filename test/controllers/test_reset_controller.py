from unittest.mock import MagicMock

import pytest


class TestResetController:
    @pytest.fixture(autouse=True)
    def setUp(self):
        from controllers.reset import ResetController
        self.testing_class = ResetController

    def test_create_chama_o_servico_de_reset(self, mocker):
        patched_reset = mocker.patch('controllers.reset.Reset', MagicMock())
        self.testing_class.create()
        patched_reset.execute.assert_called()

    def test_create_retorna_ok(self, mocker):
        mocker.patch('controllers.reset.Reset', MagicMock())
        assert self.testing_class.create() == 'OK'
