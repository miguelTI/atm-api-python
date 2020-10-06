from repositories.account import AccountRepository, AccountNotFound, Account


class EventDTO:
    def __init__(self):
        self.type = ""
        self.destination = ""
        self.origin = ""
        self.amount = 0

    @staticmethod
    def create_from_dict(event_dict):
        event_dto = EventDTO()
        event_dto.type = event_dict['type']
        event_dto.amount = event_dict['amount']
        event_dto.destination = event_dict['destination'] if 'destination' in event_dict else ""
        event_dto.origin = event_dict['origin'] if 'origin' in event_dict else ""
        return event_dto


class Event:
    def execute(self):
        raise MethodNotImplemented

    def respond(self, origin: Account = None, destination: Account = None):
        response_dict = {}
        if origin:
            response_dict['origin'] = origin.to_dict()
        if destination:
            response_dict['destination'] = destination.to_dict()
        return response_dict, 201


class EventFactory:
    @staticmethod
    def create_event(event_dto) -> Event:
        if event_dto.type == 'transfer':
            return Transfer(event_dto)
        elif event_dto.type == 'withdraw':
            return Withdraw(event_dto)
        elif event_dto.type == 'deposit':
            return Deposit(event_dto)
        raise InvalidEventType


class Deposit(Event):
    def __init__(self, event_dto: EventDTO):
        try:
            self.destination = AccountRepository.find_by_id(event_dto.destination)
        except AccountNotFound:
            self.destination = AccountRepository.create(event_dto.destination)
        self.amount = event_dto.amount

    def execute(self):
        self.destination.balance = self.destination.balance + self.amount
        AccountRepository.save(self.destination)
        return self.respond(destination=self.destination)


class Withdraw(Event):
    def __init__(self, event_dto: EventDTO):
        self.origin = AccountRepository.find_by_id(event_dto.origin)
        self.amount = event_dto.amount

    def execute(self):
        self.origin.balance = self.origin.balance - self.amount
        AccountRepository.save(self.origin)
        return self.respond(origin=self.origin)


class Transfer(Event):
    def __init__(self, event_dto: EventDTO):
        self.origin = AccountRepository.find_by_id(event_dto.origin)
        try:
            self.destination = AccountRepository.find_by_id(event_dto.destination)
        except AccountNotFound:
            self.destination = AccountRepository.create(event_dto.destination)
        self.amount = event_dto.amount

    def execute(self):
        self.origin.balance = self.origin.balance - self.amount
        self.destination.balance = self.destination.balance + self.amount
        AccountRepository.save(self.origin)
        AccountRepository.save(self.destination)
        return self.respond(origin=self.origin, destination=self.destination)


class Reset:
    @staticmethod
    def execute():
        AccountRepository.reset()


class MethodNotImplemented(Exception):
    pass


class InvalidEventType(Exception):
    pass
