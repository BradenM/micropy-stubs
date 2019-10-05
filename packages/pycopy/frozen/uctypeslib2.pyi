
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
def pprint(desc: Any, stream: Any=None, cur_ind: Any=0) -> Any:
    #   0: return v&2147483647>>31-VAL_TYPE_BITS
    # ? 0: return v&number>>number-VAL_TYPE_BITS
    def valtype(v: Any) -> Any: ...
        #   0: return v&2147483647>>31-VAL_TYPE_BITS
        # ? 0: return v&number>>number-VAL_TYPE_BITS
