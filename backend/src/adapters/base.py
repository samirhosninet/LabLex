from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    """
    Abstract Base Adapter Interface for LabLex evaluation adapters.
    
    IMPORTANT: Adapters must never import or interact with active database models or ORM 
    entities to prevent database coupling (Warning W4). They receive immutable serialized 
    dictionary snapshots (DTOs) of RunSpec and Target data.
    """
    
    @abstractmethod
    def execute(self, runspec_snapshot: dict, target_snapshot: dict) -> dict:
        """
        Executes the evaluation process.
        
        Args:
            runspec_snapshot (dict): The serialized immutable snapshot of the RunSpec.
            target_snapshot (dict): The serialized target manifest containing connection parameters.
            
        Returns:
            dict: A dictionary containing the raw outputs (e.g. sample predictions, metrics, logs).
        """
        pass
