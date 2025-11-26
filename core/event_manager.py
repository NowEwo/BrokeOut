from objects.prototype import Entity


class EventManager:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, object: Entity, event: str):
        if not event in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(object)

    def send_event(self, event: str):
        if not event in self.listeners:
            return
        for entity in self.listeners[event]:
            getattr(entity, event)()

    def reset(self):
        self.listeners = {}