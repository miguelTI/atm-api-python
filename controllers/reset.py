from services.events import Reset


class ResetController:
    @staticmethod
    def create():
        Reset.execute()
        return 'OK'
