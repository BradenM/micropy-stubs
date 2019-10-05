
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
    def __init__(self, names: Any, dest: Any, action: Any, nargs: Any, const: Any, default: Any, help: Any) -> None: ...
    def parse(self, optname: Any, args: Any) -> Any: ...
        #   0: return args.pop(0)
        # ? 0: return args.pop(number)
        #   1: return args.pop(0)
        # ? 1: return args.pop(number)
        #   2: return self.default
        # ? 2: return self.default
        #   3: return ret
        # ? 3: return ret
        #   4: return self.const
        # ? 4: return self.const
def _dest_from_optnames(opt_names: Any) -> Any: ...
    #   0: return dest.lstrip('-').replace('-','_')
    # ? 0: return dest.lstrip(str).replace(str, str)
class ArgumentParser:
    def __init__(self) -> None: ...
    def add_argument(self, *args, **kwargs) -> None: ...
    def usage(self, full: Any) -> Optional[str]:
        def render_arg(arg: Any) -> str: ...
    def parse_args(self, args: Any=None) -> Any: ...
        #   0: return self._parse_args_impl(args,bool)
        # ? 0: return self._parse_args_impl(args, bool)
    def parse_known_args(self, args: Any=None) -> Any: ...
        #   0: return self._parse_args_impl(args,bool)
        # ? 0: return self._parse_args_impl(args, bool)
    def _parse_args_impl(self, args: Any, return_unknown: Any) -> Any: ...
        #   0: return self._parse_args(args,return_unknown)
        # ? 0: return self._parse_args(args, return_unknown)
    def _parse_args(self, args: Any, return_unknown: Any) -> Union[Any, Tuple[Any, Any]]:
        def consume_unknown() -> None: ...
