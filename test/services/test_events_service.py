from unittest.mock import MagicMock, call

import pytest


class TestEventDTO:
    @pytest.fixture(autouse=True)
    def setUp(self):
        from services.events import EventDTO
        self.testing_class = EventDTO

    def test_create_from_dict_retorna_uma_instancia_da_classe(self):
        example_dict = {
            'type': 'test',
            'amount': 100,
            'destination': '200',
            'origin': '300'
        }
        assert isinstance(self.testing_class.create_from_dict(example_dict), self.testing_class)

    def test_create_from_dict_usa_o_valor_type_do_dicionario(self):
        example_dict = {
            'type': 'test',
            'amount': 100,
            'destination': '200',
            'origin': '300'
        }
        assert self.testing_class.create_from_dict(example_dict).type == 'test'

    def test_create_from_dict_usa_o_valor_amount_do_dicionario(self):
        example_dict = {
            'type': 'test',
            'amount': 100,
            'destination': '200',
            'origin': '300'
        }
        assert self.testing_class.create_from_dict(example_dict).amount == 100

    def test_create_from_dict_usa_o_valor_destination_do_dicionario(self):
        example_dict = {
            'type': 'test',
            'amount': 100,
            'destination': '200',
            'origin': '300'
        }
        assert self.testing_class.create_from_dict(example_dict).destination == '200'

    def test_create_from_dict_usa_o_valor_origin_do_dicionario(self):
        example_dict = {
            'type': 'test',
            'amount': 100,
            'destination': '200',
            'origin': '300'
        }
        assert self.testing_class.create_from_dict(example_dict).origin == '300'

    def test_create_from_dict_deixa_a_propriedade_destination_vazia_se_o_valor_nao_existe_no_dicionario(self):
        example_dict = {
            'type': 'test',
            'amount': 100,
            'origin': '300'
        }
        assert not self.testing_class.create_from_dict(example_dict).destination

    def test_create_from_dict_deixa_a_propriedade_origin_vazia_se_o_valor_nao_existe_no_dicionario(self):
        example_dict = {
            'type': 'test',
            'amount': 100,
            'destination': '200'
        }
        assert self.testing_class.create_from_dict(example_dict).origin == ''


class TestEvent:
    @pytest.fixture(autouse=True)
    def setUp(self):
        from services.events import Event
        self.testing_instance = Event()

    def test_execute_lanca_method_not_implemented_por_defeito(self):
        from services.events import MethodNotImplemented
        with pytest.raises(MethodNotImplemented):
            self.testing_instance.execute()

    def test_respond_retorna_um_dicionario_e_o_status_code_201(self):
        origin_account = MagicMock()
        destination_account = MagicMock()
        resposta, status = self.testing_instance.respond(origin=origin_account, destination=destination_account)
        assert isinstance(resposta, dict) and status == 201

    def test_respond_retorna_as_contas_como_dicionario(self):
        origin_account = MagicMock()
        origin_account.to_dict.return_value = {'id': '100'}
        destination_account = MagicMock()
        destination_account.to_dict.return_value = {'id': '200'}
        resposta, status = self.testing_instance.respond(origin=origin_account, destination=destination_account)
        assert 'origin' in resposta and resposta['origin'] == {'id': '100'} and 'destination' in resposta and resposta['destination'] == {'id': '200'}


class TestEventFactory:
    @pytest.fixture(autouse=True)
    def setUp(self):
        from services.events import EventFactory
        self.testing_class = EventFactory

    def test_create_event_retorna_um_objeto_transfer_quando_o_tipo_da_dto_e_transfer(self, mocker):
        class CustomTransfer:
            def __init__(self, pedido_dto):
                pass

        mocker.patch('services.events.Transfer', CustomTransfer)
        mocked_dto = MagicMock()
        mocked_dto.type = 'transfer'
        assert isinstance(self.testing_class.create_event(mocked_dto), CustomTransfer)

    def test_create_event_retorna_um_objeto_withdraw_quando_o_tipo_da_dto_e_withdraw(self, mocker):
        class CustomWithdraw:
            def __init__(self, pedido_dto):
                pass

        mocker.patch('services.events.Withdraw', CustomWithdraw)
        mocked_dto = MagicMock()
        mocked_dto.type = 'withdraw'
        assert isinstance(self.testing_class.create_event(mocked_dto), CustomWithdraw)

    def test_create_event_retorna_um_objeto_deposit_quando_o_tipo_da_dto_e_deposit(self, mocker):
        class CustomDeposit:
            def __init__(self, pedido_dto):
                pass

        mocker.patch('services.events.Deposit', CustomDeposit)
        mocked_dto = MagicMock()
        mocked_dto.type = 'deposit'
        assert isinstance(self.testing_class.create_event(mocked_dto), CustomDeposit)

    def test_create_event_lanca_invalid_event_type_quando_o_tipo_da_dto_e_invalido(self, mocker):
        class MockedException(Exception):
            pass

        mocker.patch('services.events.InvalidEventType', MockedException)
        mocked_dto = MagicMock()
        mocked_dto.type = 'invalid'
        with pytest.raises(MockedException):
            self.testing_class.create_event(mocked_dto)


class TestDeposit:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        from services.events import Deposit
        mocker.patch('services.events.AccountRepository', MagicMock())
        self.testing_class = Deposit
        mocked_dto = MagicMock()
        self.testing_instance = Deposit(mocked_dto)

    def test_ao_criar_a_instancia_busca_a_conta_destino_usando_o_account_repository(self, mocker):
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        mocked_dto = MagicMock()
        mocked_dto.destination = "100"
        self.testing_class(mocked_dto)
        mocked_repository.find_by_id.assert_called_once_with("100")

    def test_ao_criar_a_instancia_se_a_conta_nao_existe_cria_uma_nova_conta_usando_o_account_repository(self, mocker):
        class MockedException(Exception):
            pass

        mocker.patch('services.events.AccountNotFound', MockedException)
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        mocked_repository.find_by_id.side_effect = MockedException
        mocked_dto = MagicMock()
        mocked_dto.destination = "300"
        self.testing_class(mocked_dto)
        mocked_repository.create.assert_called_once_with("300")

    def test_ao_criar_a_instancia_define_o_amount_usando_o_dto(self):
        mocked_dto = MagicMock()
        mocked_dto.amount = 20
        created_instance = self.testing_class(mocked_dto)
        assert created_instance.amount == 20

    def test_execute_acrescenta_a_amount_ao_balance_da_conta_destino(self):
        self.testing_instance.destination.balance = 10
        self.testing_instance.amount = 20
        self.testing_instance.execute()
        assert self.testing_instance.destination.balance == 30

    def test_execute_persiste_a_alteracao_usando_o_account_repository(self, mocker):
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        self.testing_instance.execute()
        mocked_repository.save.assert_called_once_with(self.testing_instance.destination)

    def test_execute_chama_o_metodo_respond_com_a_conta_destino(self, mocker):
        mocked_method = mocker.patch.object(self.testing_instance, 'respond', MagicMock())
        self.testing_instance.execute()
        mocked_method.assert_called_once_with(destination=self.testing_instance.destination)


class TestWithdraw:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        from services.events import Withdraw
        mocker.patch('services.events.AccountRepository', MagicMock())
        self.testing_class = Withdraw
        mocked_dto = MagicMock()
        self.testing_instance = Withdraw(mocked_dto)

    def test_ao_criar_a_instancia_busca_a_conta_origem_usando_o_account_repository(self, mocker):
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        mocked_dto = MagicMock()
        mocked_dto.origin = "100"
        self.testing_class(mocked_dto)
        mocked_repository.find_by_id.assert_called_once_with("100")

    def test_ao_criar_a_instancia_lanca_exception_se_o_repositorio_lanca_exception(self, mocker):
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        mocked_repository.find_by_id.side_effect = Exception
        mocked_dto = MagicMock()
        mocked_dto.origin = "100"
        with pytest.raises(Exception):
            self.testing_class(mocked_dto)

    def test_ao_criar_a_instancia_define_o_amount_usando_o_dto(self):
        mocked_dto = MagicMock()
        mocked_dto.amount = 20
        created_instance = self.testing_class(mocked_dto)
        assert created_instance.amount == 20

    def test_execute_subtrai_a_amount_ao_balance_da_conta_origem(self):
        self.testing_instance.origin.balance = 20
        self.testing_instance.amount = 5
        self.testing_instance.execute()
        assert self.testing_instance.origin.balance == 15

    def test_execute_persiste_a_alteracao_usando_o_account_repository(self, mocker):
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        self.testing_instance.execute()
        mocked_repository.save.assert_called_once_with(self.testing_instance.origin)

    def test_execute_chama_o_metodo_respond_com_a_conta_origem(self, mocker):
        mocked_method = mocker.patch.object(self.testing_instance, 'respond', MagicMock())
        self.testing_instance.execute()
        mocked_method.assert_called_once_with(origin=self.testing_instance.origin)


class TestTransfer:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        from services.events import Transfer
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        mocked_repository.find_by_id.side_effect = MagicMock(), MagicMock()
        self.testing_class = Transfer
        mocked_dto = MagicMock()
        self.testing_instance = Transfer(mocked_dto)

    def test_ao_criar_a_instancia_busca_a_conta_destino_usando_o_account_repository(self, mocker):
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        mocked_dto = MagicMock()
        mocked_dto.destination = "100"
        self.testing_class(mocked_dto)
        mocked_repository.find_by_id.assert_called_with("100")

    def test_ao_criar_a_instancia_se_a_conta_destino_nao_existe_cria_uma_nova_conta_usando_o_account_repository(self, mocker):
        class MockedException(Exception):
            pass

        mocker.patch('services.events.AccountNotFound', MockedException)
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        mocked_repository.find_by_id.side_effect = MagicMock(), MockedException
        mocked_dto = MagicMock()
        mocked_dto.destination = "300"
        self.testing_class(mocked_dto)
        mocked_repository.create.assert_called_once_with("300")

    def test_ao_criar_a_instancia_define_o_amount_usando_o_dto(self, mocker):
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        mocked_repository.find_by_id.side_effect = MagicMock(), MagicMock()
        mocked_dto = MagicMock()
        mocked_dto.amount = 20
        created_instance = self.testing_class(mocked_dto)
        assert created_instance.amount == 20

    def test_execute_subtrai_a_amount_ao_balance_da_conta_origem(self):
        self.testing_instance.origin.balance = 20
        self.testing_instance.amount = 5
        self.testing_instance.execute()
        assert self.testing_instance.origin.balance == 15

    def test_execute_acrescenta_a_amount_ao_balance_da_conta_destino(self):
        self.testing_instance.destination.balance = 10
        self.testing_instance.amount = 20
        self.testing_instance.execute()
        assert self.testing_instance.destination.balance == 30

    def test_execute_persiste_a_alteracao_usando_o_account_repository(self, mocker):
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        self.testing_instance.execute()
        mocked_repository.save.assert_has_calls(calls=[call(self.testing_instance.origin), call(self.testing_instance.destination)])

    def test_execute_chama_o_metodo_respond_com_as_duas_contas(self, mocker):
        mocked_method = mocker.patch.object(self.testing_instance, 'respond', MagicMock())
        self.testing_instance.execute()
        mocked_method.assert_called_once_with(origin=self.testing_instance.origin, destination=self.testing_instance.destination,)


class TestReset:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        from services.events import Reset
        mocker.patch('services.events.AccountRepository', MagicMock())
        self.testing_class = Reset

    def test_execute_chama_o_account_repository(self, mocker):
        mocked_repository = mocker.patch('services.events.AccountRepository', MagicMock())
        self.testing_class.execute()
        mocked_repository.reset.assert_called_once()
