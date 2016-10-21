#! usr/bin/env python

class VectorDirectionException(Exception):
    """
    Used by methods taking in a vector with the assumption that the vector
    describes a particular direction movement.
    """
    pass

class InvalidConfigStateException(ValueError):
    """
    Used to signal invalid configuration values.
    """
    pass

class MalformedDialogException(Exception):
    """
    Raised when the dialog file is in improper form. The message should specify
    exactly how/why the dialog file is invalid.
    """
