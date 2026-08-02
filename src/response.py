class Response:
    def __init__(self, version, status_code, reason_phrase, headers, body):
        self.version = version
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.headers = headers  
        self.body = body
        
