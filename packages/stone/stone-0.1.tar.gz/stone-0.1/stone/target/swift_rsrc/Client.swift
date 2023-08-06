import Foundation
import Alamofire

public class Box<T> {
	public let unboxed : T
	init (_ v : T) { self.unboxed = v }
}

public class StoneClient {
    var manager : Manager
    var backgroundManager : Manager
    var baseHosts : [String : String]
    
    func additionalHeaders(noauth: Bool) -> [String: String] {
        return [:]
    }
    
    init(manager: Manager, backgroundManager: Manager, baseHosts : [String : String]) {
        self.manager = manager
        self.backgroundManager = backgroundManager
        self.baseHosts = baseHosts
    }
}

public enum CallError<EType> : CustomStringConvertible {
    case InternalServerError(Int, String?, String?)
    case BadInputError(String?, String?)
    case RateLimitError
    case HTTPError(Int?, String?, String?)
    case RouteError(Box<EType>, String?)
    case OSError(ErrorType?)
    
    public var description : String {
        switch self {
        case let .InternalServerError(code, message, requestId):
            var ret = ""
            if let r = requestId {
                ret += "[request-id \(r)] "
            }
            ret += "Internal Server Error \(code)"
            if let m = message {
                ret += ": \(m)"
            }
            return ret
        case let .BadInputError(message, requestId):
            var ret = ""
            if let r = requestId {
                ret += "[request-id \(r)] "
            }
            ret += "Bad Input"
            if let m = message {
                ret += ": \(m)"
            }
            return ret
        case .RateLimitError:
            return "Rate limited"
        case let .HTTPError(code, message, requestId):
            var ret = ""
            if let r = requestId {
                ret += "[request-id \(r)] "
            }
            ret += "HTTP Error"
            if let c = code {
                ret += "\(c)"
            }
            if let m = message {
                ret += ": \(m)"
            }
            return ret
        case let .RouteError(box, requestId):
            var ret = ""
            if let r = requestId {
                ret += "[request-id \(r)] "
            }
            ret += "API route error - \(box.unboxed)"
            return ret
        case let .OSError(err):
            if let e = err {
                return "\(e)"
            }
            return "An unknown system error"
        }
    }
}

func utf8Decode(data: NSData) -> String {
    return NSString(data: data, encoding: NSUTF8StringEncoding)! as String
}

func asciiEscape(s: String) -> String {
    var out : String = ""

    for char in s.unicodeScalars {
        var esc = "\(char)"
        if !char.isASCII() {
            esc = NSString(format:"\\u%04x", char.value) as String
        } else {
            esc = "\(char)"
        }
        out += esc
        
    }
    return out
}


/// Represents a Stone request
///
/// These objects are constructed by the SDK; users of the SDK do not need to create them manually.
///
/// Pass in a closure to the `response` method to handle a response or error.
public class StoneRequest<RType : JSONSerializer, EType : JSONSerializer> {
    let errorSerializer : EType
    let responseSerializer : RType
    let request : Alamofire.Request
    
    init(request: Alamofire.Request,
        responseSerializer: RType,
        errorSerializer: EType)
    {
            self.errorSerializer = errorSerializer
            self.responseSerializer = responseSerializer
            self.request = request
    }
    
    public func cancel() {
        self.request.cancel()
    }
    
    func handleResponseError(response: NSHTTPURLResponse?, data: NSData?, error: ErrorType?) -> CallError<EType.ValueType> {
        let requestId = response?.allHeaderFields["X-Dropbox-Request-Id"] as? String
        if let code = response?.statusCode {
            switch code {
            case 500...599:
                var message = ""
                if let d = data {
                    message = utf8Decode(d)
                }
                return .InternalServerError(code, message, requestId)
            case 400:
                var message = ""
                if let d = data {
                    message = utf8Decode(d)
                }
                return .BadInputError(message, requestId)
            case 429:
                 return .RateLimitError
            case 403, 404, 409:
                let json = parseJSON(data!)
                switch json {
                case .Dictionary(let d):
                    return .RouteError(Box(self.errorSerializer.deserialize(d["error"]!)), requestId)
                default:
                    fatalError("Failed to parse error type")
                }
            case 200:
                return .OSError(error)
            default:
                return .HTTPError(code, "An error occurred.", requestId)
            }
        } else {
            var message = ""
            if let d = data {
                message = utf8Decode(d)
            }
            return .HTTPError(nil, message, requestId)
        }
    }
}

/// An "rpc-style" request
public class StoneRpcRequest<RType : JSONSerializer, EType : JSONSerializer> : StoneRequest<RType, EType> {
    init(client: StoneClient, host: String, route: String, params: JSON, responseSerializer: RType, errorSerializer: EType) {
        let url = "\(client.baseHosts[host]!)\(route)"
        var headers = ["Content-Type": "application/json"]
        let noauth = (host == "notify")
        for (header, val) in client.additionalHeaders(noauth) {
            headers[header] = val
        }
        
        let request = client.backgroundManager.request(.POST, url, parameters: [:], headers: headers,
                                                       encoding: ParameterEncoding.Custom {(convertible, _) in
                let mutableRequest = convertible.URLRequest.copy() as! NSMutableURLRequest
                mutableRequest.HTTPBody = dumpJSON(params)
                return (mutableRequest, nil)
        })
        super.init(request: request,
            responseSerializer: responseSerializer,
            errorSerializer: errorSerializer)
        request.resume()
    }
    
    /// Called when a request completes.
    ///
    /// :param: completionHandler A closure which takes a (response, error) and handles the result of the call appropriately.
    public func response(completionHandler: (RType.ValueType?, CallError<EType.ValueType>?) -> Void) -> Self {
        self.request.validate().response {
            (request, response, dataObj, error) -> Void in
            let data = dataObj!
            if error != nil {
                completionHandler(nil, self.handleResponseError(response, data: data, error: error))
            } else {
                completionHandler(self.responseSerializer.deserialize(parseJSON(data)), nil)
            }
        }
        return self
    }
}

public enum StoneUploadBody {
    case Data(NSData)
    case File(NSURL)
    case Stream(NSInputStream)
}

public class StoneUploadRequest<RType : JSONSerializer, EType : JSONSerializer> : StoneRequest<RType, EType> {

    init(
        client: StoneClient,
        host: String,
        route: String,
        params: JSON, 
        responseSerializer: RType, errorSerializer: EType,
        body: StoneUploadBody) {
            let url = "\(client.baseHosts[host]!)\(route)"
            var headers = [
                "Content-Type": "application/octet-stream",
            ]
            let noauth = (host == "notify")
            for (header, val) in client.additionalHeaders(noauth) {
                headers[header] = val
            }
            
            if let data = dumpJSON(params) {
                let value = asciiEscape(utf8Decode(data))
                headers["Dropbox-Api-Arg"] = value
            }
            
            let request : Alamofire.Request
            
            switch body {
            case let .Data(data):
                request = client.manager.upload(.POST, url, headers: headers, data: data)
            case let .File(file):
                request = client.backgroundManager.upload(.POST, url, headers: headers, file: file)
            case let .Stream(stream):
                request = client.manager.upload(.POST, url, headers: headers, stream: stream)
            }
            super.init(request: request,
                       responseSerializer: responseSerializer,
                       errorSerializer: errorSerializer)
            request.resume()
    }

    
    /// Called as the upload progresses.
    ///
    /// :param: closure
    ///         a callback taking three arguments (`bytesWritten`, `totalBytesWritten`, `totalBytesExpectedToWrite`)
    /// :returns: The request, for chaining purposes
    public func progress(closure: ((Int64, Int64, Int64) -> Void)? = nil) -> Self {
        self.request.progress(closure)
        return self
    }
    
    /// Called when a request completes.
    ///
    /// :param: completionHandler 
    ///         A callback taking two arguments (`response`, `error`) which handles the result of the call appropriately.
    /// :returns: The request, for chaining purposes.
    public func response(completionHandler: (RType.ValueType?, CallError<EType.ValueType>?) -> Void) -> Self {
        self.request.validate().response {
            (request, response, dataObj, error) -> Void in
            let data = dataObj!
            if error != nil {
                completionHandler(nil, self.handleResponseError(response, data: data, error: error))
            } else {
                completionHandler(self.responseSerializer.deserialize(parseJSON(data)), nil)
            }
        }
        return self
    }

}

public class StoneDownloadRequest<RType : JSONSerializer, EType : JSONSerializer> : StoneRequest<RType, EType> {
    var urlPath : NSURL?
    var errorMessage : NSData
    init(client: StoneClient, host: String, route: String, params: JSON, responseSerializer: RType, errorSerializer: EType, destination: (NSURL, NSHTTPURLResponse) -> NSURL, overwrite: Bool = false) {
        let url = "\(client.baseHosts[host]!)\(route)"
        var headers = [String : String]()
        urlPath = nil
        errorMessage = NSData()

        if let data = dumpJSON(params) {
            let value = asciiEscape(utf8Decode(data))
            headers["Dropbox-Api-Arg"] = value
        }
        
        let noauth = (host == "notify")
        for (header, val) in client.additionalHeaders(noauth) {
            headers[header] = val
        }

        weak var _self : StoneDownloadRequest<RType, EType>!
        
        let dest : (NSURL, NSHTTPURLResponse) -> NSURL = { url, resp in
            var finalUrl = destination(url, resp)

            if 200 ... 299 ~= resp.statusCode {
                if NSFileManager.defaultManager().fileExistsAtPath(finalUrl.path!) {
                    if overwrite {
                        do {
                            try NSFileManager.defaultManager().removeItemAtURL(finalUrl)
                        } catch let error as NSError {
                            print("Error: \(error)")
                        }
                    } else {
                        print("Error: File already exists at \(finalUrl.path!)")
                    }
                }
            }
            else {
                _self.errorMessage = NSData(contentsOfURL: url)!
                // Alamofire will "move" the file to the temporary location where it already resides, 
                // and where it will soon be automatically deleted
                finalUrl = url
            }

            _self.urlPath = finalUrl

            return finalUrl
        }
        
        let request = client.backgroundManager.download(.POST, url, headers: headers, destination: dest)

        super.init(request: request, responseSerializer: responseSerializer, errorSerializer: errorSerializer)
        _self = self

        request.resume()
    }
    
    /// Called as the download progresses
    /// 
    /// :param: closure
    ///         a callback taking three arguments (`bytesRead`, `totalBytesRead`, `totalBytesExpectedToRead`)
    /// :returns: The request, for chaining purposes.
    public func progress(closure: ((Int64, Int64, Int64) -> Void)? = nil) -> Self {
        self.request.progress(closure)
        return self
    }
    
    /// Called when a request completes.
    ///
    /// :param: completionHandler
    ///         A callback taking two arguments (`response`, `error`) which handles the result of the call appropriately.
    /// :returns: The request, for chaining purposes.
    public func response(completionHandler: ( (RType.ValueType, NSURL)?, CallError<EType.ValueType>?) -> Void) -> Self {
        self.request.validate()
            .response {
            (request, response, data, error) -> Void in
            if error != nil {
                completionHandler(nil, self.handleResponseError(response, data: self.errorMessage, error: error))
            } else {
                let result = response!.allHeaderFields["Dropbox-Api-Result"] as! String
                let resultData = result.dataUsingEncoding(NSUTF8StringEncoding, allowLossyConversion: false)!
                let resultObject = self.responseSerializer.deserialize(parseJSON(resultData))
                
                completionHandler( (resultObject, self.urlPath!), nil)
            }
        }
        return self
    }
}
