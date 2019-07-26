# make_stub_files: Fri 26 Jul 2019 at 02:36:14

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class MsgHandler:
    def __init__(self, receive_callback: Any, connect_helper: Any) -> None: ...
    def setOfflineQueueConfiguration(self, queueSize: Any, dropBehavior: Any) -> None: ...
    def setCredentials(self, srcCAFile: Any, srcKey: Any, srcCert: Any) -> None: ...
    def setEndpoint(self, srcHost: Any, srcPort: Any) -> None: ...
    def setOperationTimeout(self, timeout: Any) -> None: ...
    def setDrainingInterval(self, srcDrainingIntervalSecond: Any) -> None: ...
    def insertShadowCallback(self, callback: Any, payload: Any, status: Any, token: Any) -> None: ...
    def _callShadowCallback(self) -> None: ...
    def createSocketConnection(self) -> bool: ...
    def disconnect(self) -> None: ...
    def isConnected(self) -> Any: ...
        #   0: return connected
        # ? 0: return connected
    def setConnectionState(self, state: Any) -> None: ...
    def _drop_message(self) -> bool: ...
    def push_on_send_queue(self, packet: Any) -> bool: ...
    def priority_send(self, packet: Any) -> Any: ...
        #   0: return msg_sent
        # ? 0: return msg_sent
    def _receive_packet(self) -> Union[Any, bool]: ...
        #   0: return bool
        #   0: return bool
        #   1: return bool
        #   1: return bool
        #   2: return bool
        #   2: return bool
        #   3: return bool
        #   3: return bool
        #   4: return bool
        #   4: return bool
        #   5: return bool
        #   5: return bool
        #   6: return bool
        #   6: return bool
        #   7: return self._recv_callback(msg_type,payload)
        # ? 7: return self._recv_callback(msg_type, payload)
    def _send_pingreq(self) -> Any: ...
        #   0: return self.priority_send(pkt)
        # ? 0: return self.priority_send(pkt)
    def setPingFlag(self, flag: Any) -> None: ...
    def _send_packet(self, packet: Any) -> bool: ...
    def _verify_connection_state(self) -> None: ...
    def _io_thread_func(self) -> None: ...
