
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class ContextDecorator(object):
    def _recreate_cm(self) -> Any: ...
        #   0: return self
        # ? 0: return self
    def __call__(self, func: Any) -> Any:
        #   0: return func(*args,None=kwds)
        # ? 0: return func(*args, None=kwds)
        #   1: return inner
        # ? 1: return inner
        def inner(*args, **kwds) -> Any: ...
            #   0: return func(*args,None=kwds)
            # ? 0: return func(*args, None=kwds)
    def __init__(self, func: Any, *args, **kwds) -> None: ...
    def _recreate_cm(self) -> Any: ...
        #   0: return self.__class__(self.func,*self.args,None=self.kwds)
        # ? 0: return self.__class__(self.func, *self.args, None=self.kwds)
    def __enter__(self) -> Any: ...
        #   0: return next(self.gen)
        # ? 0: return next(self.gen)
    def __exit__(self, type: Any, value: Any, traceback: Any) -> Optional[bool]: ...
def contextmanager(func: Any) -> Any:
    #   0: return _GeneratorContextManager(func,*args,None=kwds)
    # ? 0: return _GeneratorContextManager(func, *args, None=kwds)
    #   1: return helper
    # ? 1: return helper
    def helper(*args, **kwds) -> Any: ...
        #   0: return _GeneratorContextManager(func,*args,None=kwds)
        # ? 0: return _GeneratorContextManager(func, *args, None=kwds)
