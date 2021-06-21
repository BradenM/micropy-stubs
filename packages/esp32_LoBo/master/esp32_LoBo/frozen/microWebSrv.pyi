
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class MicroWebSrvRoute:
    def __init__(self, route: Any, method: Any, func: Any, routeArgNames: Any, routeRegex: Any) -> None: ...
class MicroWebSrv:
    def route(cls: Any, url: Any, method: Any='GET') -> Any:
        #   0: return func
        # ? 0: return func
        #   1: return route_decorator
        # ? 1: return route_decorator
        def route_decorator(func: Any) -> Any: ...
            #   0: return func
            # ? 0: return func
    def HTMLEscape(s: str) -> str: ...
    def _tryAllocByteArray(size: Any) -> Optional[Any]: ...
        #   0: return bytearray(size)
        # ? 0: return bytearray(size)
        #   1: return None
        #   1: return None
    def _tryStartThread(func: Any, args: Any=(), stacksize: Any=8192) -> Union[Any, bool]: ...
        #   0: return th
        # ? 0: return th
        #   1: return bool
        #   1: return bool
    def _unquote(s: str) -> str: ...
    def _unquote_plus(s: str) -> Any: ...
        #   0: return MicroWebSrv._unquote(s.replace('+',' '))
        # ? 0: return MicroWebSrv._unquote(str.replace(str, str))
    def _fileExists(path: Any) -> bool: ...
    def _isPyHTMLFile(filename: str) -> Any: ...
        #   0: return filename.lower().endswith(MicroWebSrv._pyhtmlPagesExt)
        # ? 0: return str.lower().endswith(MicroWebSrv._pyhtmlPagesExt)
    def __init__(self, routeHandlers: Any=[], port: Any=80, bindIP: Any='0.0.0.0', webPath: Any='/flash/www') -> None: ...
    def _serverProcess(self) -> None: ...
    def Start(self, threaded: Any=bool, stackSize: Any=8192) -> None: ...
    def Stop(self) -> None: ...
    def IsStarted(self) -> Any: ...
        #   0: return self._started
        # ? 0: return self._started
    def threadID(self) -> Any: ...
        #   0: return self.thID
        # ? 0: return self.thID
    def State(self) -> Any: ...
        #   0: return self._state
        # ? 0: return self._state
    def SetNotFoundPageUrl(self, url: Any=None) -> None: ...
    def GetMimeTypeFromFilename(self, filename: str) -> Optional[Any]: ...
        #   0: return self._mimeTypes[ext]
        # ? 0: return self._mimeTypes[ext]
        #   1: return None
        #   1: return None
    def GetRouteHandler(self, resUrl: Any, method: Any) -> Union[Tuple[Any, Any], Tuple[Any, None], Tuple[None, None]]: ...
    def _physPathFromURLPath(self, urlPath: Any) -> Optional[Any]: ...
        #   0: return physPath
        # ? 0: return physPath
        #   1: return physPath
        # ? 1: return physPath
        #   2: return None
        #   2: return None
        def __init__(self, microWebSrv: Any, socket: Any, addr: Any) -> None: ...
        def _processRequest(self) -> None: ...
        def _parseFirstLine(self, response: Any) -> bool: ...
        def _parseHeader(self, response: Any) -> bool: ...
        def _getConnUpgrade(self) -> Optional[Any]: ...
            #   0: return self._headers.get('Upgrade','').lower()
            # ? 0: return self._headers.get(str, str).lower()
            #   1: return None
            #   1: return None
        def GetServer(self) -> Any: ...
            #   0: return self._microWebSrv
            # ? 0: return self._microWebSrv
        def GetAddr(self) -> Any: ...
            #   0: return self._addr
            # ? 0: return self._addr
        def GetIPAddr(self) -> Any: ...
            #   0: return self._addr[0]
            # ? 0: return self._addr[number]
        def GetPort(self) -> Any: ...
            #   0: return self._addr[1]
            # ? 0: return self._addr[number]
        def GetRequestMethod(self) -> Any: ...
            #   0: return self._method
            # ? 0: return self._method
        def GetRequestTotalPath(self) -> Any: ...
            #   0: return self._path
            # ? 0: return self._path
        def GetRequestPath(self) -> Any: ...
            #   0: return self._resPath
            # ? 0: return self._resPath
        def GetRequestQueryString(self) -> Any: ...
            #   0: return self._queryString
            # ? 0: return self._queryString
        def GetRequestQueryParams(self) -> Any: ...
            #   0: return self._queryParams
            # ? 0: return self._queryParams
        def GetRequestHeaders(self) -> Any: ...
            #   0: return self._headers
            # ? 0: return self._headers
        def GetRequestContentType(self) -> Any: ...
            #   0: return self._contentType
            # ? 0: return self._contentType
        def GetRequestContentLength(self) -> Any: ...
            #   0: return self._contentLength
            # ? 0: return self._contentLength
        def ReadRequestContent(self, size: Any=None) -> Union[Any, bytes]: ...
        def ReadRequestPostedFormData(self) -> Any: ...
            #   0: return res
            # ? 0: return res
        def ReadRequestContentAsJSON(self) -> Optional[Any]: ...
            #   0: return loads(self.ReadRequestContent())
            # ? 0: return loads(self.ReadRequestContent())
            #   1: return None
            #   1: return None
        def __init__(self, client: Any) -> None: ...
        def _write(self, data: Any) -> Any: ...
            #   0: return self._client._socket.write(data)
            # ? 0: return self._client._socket.write(data)
        def _writeFirstLine(self, code: Any) -> None: ...
        def _writeHeader(self, name: str, value: Any) -> None: ...
        def _writeContentTypeHeader(self, contentType: Any, charset: Any=None) -> None: ...
        def _writeServerHeader(self) -> None: ...
        def _writeEndHeader(self) -> None: ...
        def _writeBeforeContent(self, code: Any, headers: Any, contentType: Any, contentCharset: Any, contentLength: Any) -> None: ...
        def WriteSwitchProto(self, upgrade: Any, headers: Any=None) -> None: ...
        def WriteResponse(self, code: Any, headers: Any, contentType: Any, contentCharset: Any, content: Any) -> bool: ...
        def WriteResponsePyHTMLFile(self, filepath: Any, headers: Any=None) -> Any: ...
            #   0: return self.WriteResponse(200,headers,'text/html','UTF-8',tmplResult)
            # ? 0: return self.WriteResponse(number, headers, str, str, tmplResult)
            #   1: return self.WriteResponse(500,None,'text/html','UTF-8',self._execErrCtnTmpl%{'module':'PyHTML', 'message':str(ex)})
            # ? 1: return self.WriteResponse(number, None, str, str, self._execErrCtnTmpl%Dict[{str:str, str:str(ex)}])
            #   2: return self.WriteResponseNotImplemented()
            # ? 2: return self.WriteResponseNotImplemented()
        def WriteResponseFile(self, filepath: Any, contentType: Any=None, headers: Any=None) -> bool: ...
        def WriteResponseFileAttachment(self, filepath: Any, attachmentName: Any, headers: Any=None) -> Any: ...
            #   0: return self.WriteResponseFile(filepath,None,headers)
            # ? 0: return self.WriteResponseFile(filepath, None, headers)
        def WriteResponseOk(self, headers: Any=None, contentType: Any=None, contentCharset: Any=None, content: Any=None) -> Any: ...
            #   0: return self.WriteResponse(200,headers,contentType,contentCharset,content)
            # ? 0: return self.WriteResponse(number, headers, contentType, contentCharset, content)
        def WriteResponseJSONOk(self, obj: Any=None, headers: Any=None) -> Any: ...
            #   0: return self.WriteResponse(200,headers,'application/json','UTF-8',dumps(obj))
            # ? 0: return self.WriteResponse(number, headers, str, str, dumps(obj))
        def WriteResponseRedirect(self, location: Any) -> Any: ...
            #   0: return self.WriteResponse(302,headers,None,None,None)
            # ? 0: return self.WriteResponse(number, headers, None, None, None)
        def WriteResponseError(self, code: Any) -> Any: ...
            #   0: return self.WriteResponse(code,None,'text/html','UTF-8',self._errCtnTmpl%{'code':code, 'reason':responseCode[0], 'message':responseCode[1]})
            # ? 0: return self.WriteResponse(code, None, str, str, self._errCtnTmpl%Dict[{str:code, str:responseCode[number], str:responseCode[number]}])
        def WriteResponseJSONError(self, code: Any, obj: Any=None) -> Any: ...
            #   0: return self.WriteResponse(code,None,'application/json','UTF-8',dumps(obj if obj else {} ))
            # ? 0: return self.WriteResponse(code, None, str, str, dumps(Union[Any, Dict[{}]]))
        def WriteResponseBadRequest(self) -> Any: ...
            #   0: return self.WriteResponseError(400)
            # ? 0: return self.WriteResponseError(number)
        def WriteResponseForbidden(self) -> Any: ...
            #   0: return self.WriteResponseError(403)
            # ? 0: return self.WriteResponseError(number)
        def WriteResponseNotFound(self) -> Any: ...
            #   0: return self.WriteResponseError(404)
            # ? 0: return self.WriteResponseError(number)
        def WriteResponseMethodNotAllowed(self) -> Any: ...
            #   0: return self.WriteResponseError(405)
            # ? 0: return self.WriteResponseError(number)
        def WriteResponseInternalServerError(self) -> Any: ...
            #   0: return self.WriteResponseError(500)
            # ? 0: return self.WriteResponseError(number)
        def WriteResponseNotImplemented(self) -> Any: ...
            #   0: return self.WriteResponseError(501)
            # ? 0: return self.WriteResponseError(number)
