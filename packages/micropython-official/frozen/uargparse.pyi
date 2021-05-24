
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
    def __init__(self, names: Any, dest: Any, action: Any, nargs: Any, const: Any, default: Any, help: Any) -> None: ...
    def parse(self, optname: Any, args: Any) -> Any: ...
        #   0: return args.pop()
        # ? 0: return args.pop()
        #   1: return args.pop()
        # ? 1: return args.pop()
        #   2: return self.default
        # ? 2: return self.default
        #   3: return ret
        # ? 3: return ret
        #   4: return self.const
        # ? 4: return self.const
def _dest_from_optnames(opt_names: Any) -> Any: ...
    #   0: return dest.lstrip().replace()
    # ? 0: return dest.lstrip().replace()
class ArgumentParser:
    def __init__(self) -> None: ...
    def add_argument(self, *args, **kwargs) -> None: ...
    def usage(self, full: Any) -> Optional[Any]:
        #   0: return %arg.dest
        # ? 0: return %arg.dest
        #   1: return %(arg.dest, arg.nargs)
        # ? 1: return %Tuple[arg.dest, arg.nargs]
        #   2: return %(arg.dest, arg.nargs)
        # ? 2: return %Tuple[arg.dest, arg.nargs]
        #   3: return
        #   3: return 
        #   4: return
        #   4: return
        def render_arg(arg: Any) -> Optional[Any]: ...
            #   0: return %arg.dest
            # ? 0: return %arg.dest
            #   1: return %(arg.dest, arg.nargs)
            # ? 1: return %Tuple[arg.dest, arg.nargs]
            #   2: return %(arg.dest, arg.nargs)
            # ? 2: return %Tuple[arg.dest, arg.nargs]
            #   3: return
            #   3: return
    def parse_args(self, args: Any=) -> Any: ...
        #   0: return self._parse_args_impl(args)
        # ? 0: return self._parse_args_impl(args)
    def parse_known_args(self, args: Any=) -> Any: ...
        #   0: return self._parse_args_impl(args)
        # ? 0: return self._parse_args_impl(args)
    def _parse_args_impl(self, args: Any, return_unknown: Any) -> Any: ...
        #   0: return self._parse_args(args,return_unknown)
        # ? 0: return self._parse_args(args, return_unknown)
    def _parse_args(self, args: Any, return_unknown: Any) -> Union[Any, Tuple[Any, Any]]:
        def consume_unknown() -> None: ...
