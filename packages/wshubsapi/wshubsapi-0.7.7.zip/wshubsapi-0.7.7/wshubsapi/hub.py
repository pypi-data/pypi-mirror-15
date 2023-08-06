from wshubsapi import utils
from wshubsapi.connected_clients_group import ConnectedClientsGroup
from wshubsapi.connected_clients_holder import ConnectedClientsHolder

__author__ = 'Jorge'


class UnsuccessfulReplay:
    def __init__(self, reply):
        self.reply = reply


class Hub(object):
    def __init__(self):
        hub_name = self.__class__.__dict__.get("__HubName__", self.__class__.__name__)
        setattr(self.__class__, "__HubName__", hub_name)

        self._client_functions = dict()
        self._define_client_functions()
        self._clients_holder = ConnectedClientsHolder(self)

    def subscribe_to_hub(self, _sender):
        if _sender.api_get_real_connected_client() in self._clients_holder.hub_subscribers:
            return False
        self._clients_holder.hub_subscribers.append(_sender.api_get_real_connected_client())
        return True

    def unsubscribe_from_hub(self, _sender):
        """
        :type _sender: ClientInHub
        """
        real_connected_client = _sender.api_get_real_connected_client()
        if real_connected_client in self._clients_holder.hub_subscribers:
            self._clients_holder.hub_subscribers.remove(real_connected_client)
            return True
        return False

    def get_subscribed_clients_ids(self):
        return [c.ID for c in self._clients_holder.get_subscribed_clients()]

    @property
    def clients(self):
        return self._clients_holder

    @property
    def client_functions(self):
        return self._client_functions

    @client_functions.setter
    def client_functions(self, client_functions):
        assert isinstance(client_functions, dict)
        for function_name, function in client_functions.items():
            assert isinstance(function_name, utils.string_class)
            assert hasattr(function, '__call__')
        self._client_functions = client_functions

    @staticmethod
    def _construct_unsuccessful_replay(reply):
        return UnsuccessfulReplay(reply)

    def _define_client_functions(self):
        pass
