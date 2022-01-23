from abc import ABC, abstractmethod

class Communication:
    def create_communication(self):
        pass

    def delete_communication(self):
        pass

    def edit_communication(self):
        pass


class TrainCommunication(Communication):
    def create_communication(self):
        pass


class PlaneCommunication(Communication):
    def create_communication(self):
        pass


class BusCommunication(Communication):
    def create_communication(self):
        pass


class MeanOfTransport(ABC):
    def __init__(self, name, site_link):
        self.name = name
        self.site_link = site_link

    @abstractmethod
    def add_address(self):
        pass


class Airport(MeanOfTransport):
    def __init__(self, name, site_link=None):
        super().__init__(name=name, site_link=site_link)

    def add_transport(self):
        pass

    def add_address(self):
        pass


class TrainStation(MeanOfTransport):
    def __init__(self, name, site_link=None):
        super().__init__(name=name, site_link=site_link)

    def add_transport(self):
        pass

    def add_address(self):
        pass


class BusStation(MeanOfTransport):
    def __init__(self, name, site_link=None):
        super().__init__(name=name, site_link=site_link)

    def add_transport(self):
        pass

    def add_address(self):
        pass
