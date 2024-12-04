
from abc import ABC, abstractmethod

import logging

logger = logging.getLogger(__name__)


class Queryable(ABC):

    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError("Queryable classes should not be instantiated directly")

    # Representation as part of a query
    def __str__(self) -> str:
        return self._get_query_string()
    
    @abstractmethod
    def _get_query_string(self):
        raise NotImplementedError("Queryable classes should implement _get_query_string method")
    



   
    


 