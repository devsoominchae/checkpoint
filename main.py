from checkpoint.common import Common
from checkpoint.sftp_client import SFTPClient
from checkpoint.sftp_server import SFTPServer

class Main:
    def __init__(self):
        self.config_path = "/home/globalbridge/gbai_center/re-identification/checkpoint/checkpoint_config.json"
        self.common = Common(self.config_path)
        self.sftp_server = SFTPServer(self.common)
        self.sftp_client = SFTPClient(self.common)
    
    def run(self):
        self.common.executeShellCommand("sudo -v")
        self.sftp_client.start()
        self.sftp_server.start()

if __name__ == "__main__":
    main = Main()
    main.run()

