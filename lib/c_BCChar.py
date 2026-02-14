all = ['BCChar']

from .g_attr import\
    ATTR_NORMAL as _ATTR_NORMAL

class BCChar:
    """
    Represents a text character
    """

    #region init

    def __init__(self, ord:int, attr:int = _ATTR_NORMAL):
        """
        Initializer for BBChar
        
        :param ord:
            Ordinal code
        :param attr:
            Text attribute
        """
        self.__ord = ord
        self.__attr = attr

    #endregion

    #region operators

    def __repr__(self):
        return f"BCChar({self.__ord}, attr = {self.__attr})"
    
    def __str__(self):
        return chr(self.__ord)
    
    def __eq__(self, value: object):
        return self.__eq(value)
    
    def __ne__(self, value: object):
        return not self.__eq(value)
    
    def __gt__(self, value: object):
        r = self.__cmp(value)
        if r is None: return NotImplemented
        return r > 0
    
    def __ge__(self, value: object):
        r = self.__cmp(value)
        if r is None: return NotImplemented
        return r >= 0
    
    def __lt__(self, value: object):
        r = self.__cmp(value)
        if r is None: return NotImplemented
        return r < 0
    
    def __le__(self, value: object):
        r = self.__cmp(value)
        if r is None: return NotImplemented
        return r <= 0
    
    def __hash__(self):
        return self.__ord

    #endregion

    #region properties

    @property
    def ord(self):
        """
        Ordinal code
        """
        return self.__ord
    
    @property
    def attr(self):
        """
        Text attribute
        """
        return self.__attr

    #endregion

    #region helper methods

    def __eq(self, other: object):
        if isinstance(other, BCChar):
            return self.__ord == other.__ord and self.__attr == other.__attr
        if isinstance(other, str):
            return len(other) == 1 and self.__ord == ord(other)
        return False

    def __cmp(self, other: object) -> None|int:
        if isinstance(other, BCChar):
            if self.__ord != other.__ord: return self.__ord - other.__ord
            return self.__attr - other.__attr
        if isinstance(other, str):
            if len(other) != 1: return None
            return self.__ord - ord(other)
        return None
    
    #endregion