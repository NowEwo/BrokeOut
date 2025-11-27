from objects.prototype import Entity
from systems.logging import Logger
import pygame

class EventManager:
    def __init__(self):
        self.listeners = {}
        self.logger = Logger("core.event_manager")

        self.logger.success("Event manager loaded")

    def subscribe(self, object: Entity, event: str):
        if not event in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(object)
        self.logger.log(f"New subscription from {object} to event {event}")
        self.logger.log(self.listeners, "verbose")

    def send_event(self, event: str):
        if not event in self.listeners:
            return
        for entity in self.listeners[event]:
            getattr(entity, event)()
            self.logger.log(f"Sent event {event} to object {entity}")

    def handle_events(self):
        for event in pygame.event.get():
            event_name = pygame.event.event_name(event.type)
            self.logger.log(event_name, "event_name")
            if event_name in self.listeners.keys():
                for i in self.listeners[event_name]:
                    self.logger.log(f"Sent event {event} to object {i}")
                    getattr(i, event_name)(event)
        return True

    def reset(self):
        self.listeners = {}