class PostgresConnectionModel():
    def __init__(self, host, user, password, database):
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        
    @property
    def host(self):
        return self._host
    
    @property
    def user(self):
        return self._user
    
    @property
    def password(self):
        return self._password

    @property
    def database(self):
        return self._database

class APIConnectionModel():
    def __init__(self, url):
        self._url = url
        
    @property
    def url(self):
        return self._url