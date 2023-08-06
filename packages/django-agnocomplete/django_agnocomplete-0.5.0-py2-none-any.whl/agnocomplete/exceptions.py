"""
Agnocomplete exception classes
"""


class UnregisteredAgnocompleteException(Exception):
    """
    Occurs when trying to instanciate an unregistered Agnocompletion class
    """
    pass


class AuthenticationRequiredAgnocompleteException(Exception):
    """
    Occurs when trying to instanciate an unregistered Agnocompletion class
    """
    pass


class ImproperlyConfiguredView(Exception):
    """
    Occurs if you want to misuse an AgnocompleteGenericView
    """
    pass
