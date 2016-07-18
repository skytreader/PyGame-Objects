#! usr/bin/env python

class InstanceException(Exception):
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

class VectorDirectionException(Exception):
    pass
