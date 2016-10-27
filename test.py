class Sealtiel(object):

    def outer(self, bar):
        self.__outer(bar)

    def __outer(self, bar):
        lineno = 0
    
        def inner():
            print lineno
            print bar[lineno]
    
        inner()

sealtiel = Sealtiel()
sealtiel.outer("abcd")
