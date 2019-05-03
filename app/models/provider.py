# coding: utf-8


class Provider:
    def __init__(self):
        pass

    def get_actions(self, pack=None):
        '''
        return a list of action dict
        '''
        pass

    # TODO: cache ttl
    def get_action(self, ref):
        pass

    def run_action(self, ref, parameters):
        pass

    def authenticate(self, user, password):
        pass


def get_provider(provider):
    from app.models.providers.st2 import ST2Provider

    return {'st2': ST2Provider}[provider]()
