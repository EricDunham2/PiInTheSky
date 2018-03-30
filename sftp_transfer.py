import paramiko
from threading import Thread

class SFTP(Thread) :
    def __init__(self,_host=None,_port=None,_password=None,_username=None,_localpath=None,_remotepath=None) :
        self.host = _host
        self.port = _port
        self.password = _password
        self.username = _username
        self.localpath = _localpath
        self.remotepath = _remotepath
        Thread.__init__(self)

    def run(self) :
        transport = paramiko.Transport((self.host,self.port))
        transport.connect(username=self.username,password=self.password)
        print 'Transferring...'
        s = paramiko.SFTPClient.from_transport(transport)
        s.put(self.localpath,self.remotepath)
        print 'Transferred...'
        s.close()
        transport.close()
        return
        #super(SFTP,self).join()
