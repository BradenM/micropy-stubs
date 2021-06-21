
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class MicroWebTemplate:
    def __init__(self, code: Any, escapeStrFunc: Any=None, filepath: Any='') -> None: ...
    def Validate(self) -> Optional[str(ex)]: ...
    def Execute(self) -> Any: ...
        #   0: return self._rendered
        # ? 0: return self._rendered
    def _parseCode(self, execute: Any) -> None: ...
    def _parseBloc(self, execute: Any) -> Optional[Any]: ...
        #   0: return newTokenToProcess
        # ? 0: return newTokenToProcess
        #   1: return None
        #   1: return None
    def _processToken(self, tokenContent: Any, execute: Any) -> Any: ...
        #   0: return newTokenToProcess
        # ? 0: return newTokenToProcess
    def _processInstructionPYTHON(self, instructionBody: Any, execute: Any) -> None: ...
    def _processInstructionIF(self, instructionBody: Any, execute: Any) -> None: ...
    def _processInstructionELIF(self, instructionBody: Any, execute: Any) -> Any: ...
        #   0: return MicroWebTemplate.INSTRUCTION_ELIF
        # ? 0: return MicroWebTemplate.INSTRUCTION_ELIF
    def _processInstructionELSE(self, instructionBody: Any, execute: Any) -> Any: ...
        #   0: return MicroWebTemplate.INSTRUCTION_ELSE
        # ? 0: return MicroWebTemplate.INSTRUCTION_ELSE
    def _processInstructionFOR(self, instructionBody: Any, execute: Any) -> None: ...
    def _processInstructionEND(self, instructionBody: Any, execute: Any) -> Any: ...
        #   0: return MicroWebTemplate.INSTRUCTION_END
        # ? 0: return MicroWebTemplate.INSTRUCTION_END
    def _processInstructionINCLUDE(self, instructionBody: Any, execute: Any) -> None: ...
