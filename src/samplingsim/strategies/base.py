from abc import ABC, abstractmethod
from ..models import Results

class SamplingStrategy(ABC):
    
    @abstractmethod
    def run_strategy(self) -> Results:
        raise NotImplementedError

