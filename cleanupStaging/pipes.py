class Pipes(object):

    @staticmethod
    def split(str: str, delim = " "):
        return str.split(delim)

    @staticmethod
    def min(obj):
        return min(obj)
    
    @staticmethod
    def max(obj):
        return max(obj)

    @staticmethod
    def length(obj):
        return len(obj)

    @staticmethod
    def to_string(obj):
        return str(obj)