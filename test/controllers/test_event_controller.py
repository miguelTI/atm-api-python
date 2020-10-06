from unittest.mock import MagicMock

import pytest


class TestEventController:
    @pytest.fixture(autouse=True)
    def setUp(self):
        from controllers.event import EventController
        self.testing_class = EventController

    def test_create_cria_o_dto_com_o_json_da_requisicao(self, mocker):
        patched_request = mocker.patch('controllers.event.request', MagicMock())
        patched_request.get_json.return_value = {'test_key': 'test_value'}
        patched_event_dto = mocker.patch('controllers.event.EventDTO', MagicMock())
        mocker.patch('controllers.event.EventFactory', MagicMock())
        self.testing_class.create()
        patched_event_dto.create_from_dict.assert_called_with({'test_key': 'test_value'})

    def test_create_chama_o_event_factory_pasando_o_dto(self, mocker):
        mocker.patch('controllers.event.request', MagicMock())
        patched_event_dto = mocker.patch('controllers.event.EventDTO', MagicMock())
        patched_event_dto.create_from_dict.return_value = "EXPECTED VALUE"
        patched_event_factory = mocker.patch('controllers.event.EventFactory', MagicMock())
        self.testing_class.create()
        patched_event_factory.create_event.assert_called_with("EXPECTED VALUE")

    def test_create_executa_o_evento_criado_pela_factory(self, mocker):
        mocker.patch('controllers.event.request', MagicMock())
        mocker.patch('controllers.event.EventDTO', MagicMock())
        patched_event_factory = mocker.patch('controllers.event.EventFactory', MagicMock())
        mocked_event = patched_event_factory.create_event.return_value = MagicMock()
        self.testing_class.create()
        mocked_event.execute.assert_called()

    def test_create_retorna_0_404_quando_a_conta_nao_existe(self, mocker):
        class ExpectedException(Exception):
            pass

        mocker.patch('controllers.event.request', MagicMock())
        mocker.patch('controllers.event.EventDTO', MagicMock())
        patched_event_factory = mocker.patch('controllers.event.EventFactory', MagicMock())
        mocked_event = patched_event_factory.create_event.return_value = MagicMock()
        mocked_event.execute.side_effect = ExpectedException
        mocker.patch('controllers.event.AccountNotFound', ExpectedException)
        assert self.testing_class.create() == ("0", 404)
