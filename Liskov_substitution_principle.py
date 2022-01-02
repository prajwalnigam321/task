class FTPClient:
  def __init__(self, host, port):
    ...

  def upload(self, file:bytes):
    ...

  def download(self, target:str) -> bytes:
    ...

class FTPSClient(FTPClient):
    def __init__(self, host, port, username, password):
        self._client = FTPSDriver(host, port, user=username, password=password)
