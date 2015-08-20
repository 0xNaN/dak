from rpc import Ping, Pong, LocalFindNode

class RequestFactory():
     def requestfrombytes(rawRequest, nodeId):
        # XXX: Really Reaaaaallly BAAAD COOODE

        requestLines = rawRequest.split(b'\n')
        reqType, reqHeader, reqParams = [row.decode() for row in requestLines]

        if(reqHeader == ''):
             #LocalRequest has an empty header
            try:
                p = eval("{}()".format(reqType))
            except:
                p = Request()
        else:
            # RemoteRequest has a nodeid as Header
            try:
                s = "{}(\"{}\")".format(reqType, reqHeader)
                p = eval(s)
            except:
                p = Request()

        p.addParamsFromString(reqParams)
        return p


