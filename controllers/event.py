from flask import request
from services.events import EventFactory, EventDTO, AccountNotFound


class EventController:
    @staticmethod
    def create():
        event_dict = request.get_json()
        event_dto = EventDTO.create_from_dict(event_dict)
        try:
            event = EventFactory.create_event(event_dto)
            return event.execute()
        except AccountNotFound:
            return "0", 404
