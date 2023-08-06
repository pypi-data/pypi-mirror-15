Fynd Alohomora Package
======================

A python package for Fynd Alohomora connector.
Fynd alohomora is the centralized Authentication system for several applications of Fynd.


Usage
=====
**Import the module

from alohomora import check_if_authenticated

** Use it as a decorator

check_if_authenticated(state='some_state', permission='some_permission')
def some_method()
    """
    Your code
    """
    return something