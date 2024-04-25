import os
import sys
import time
import paramiko


class SFTPClient:
    def __init__(self, common):
        self.c = common

        self.parseConfig()

        self.processes = [
            self.c.createProcessNoArgs(self.getIPFromMAC),
            self.c.createProcessNoArgs(self.sendFile)
        ]
    
    def parseConfig(self):
        self.remote_path = self.c.config["sftp"]["client"]["remote_path"]

        self.mac_address = self.c.config["sftp"]["client"]["mac_address"]
        self.port = self.c.config["sftp"]["client"]["port"]
        self.username = self.c.config["sftp"]["client"]["username"]
        self.password = self.c.config["sftp"]["client"]["password"]

    def clearARPTable(self):
        self.executeShellCommand(f"sudo ip -s -s neigh flush all")

    def formatMACAddress(self, mac_address):
        return mac_address.lower().replace("-", ":")
    
    def getIPFromMAC(self):
        formatted_mac_address = self.formatMACAddress(self.mac_address)
        ip_address = self.c.executeShellCommandReturn(f"arp -a | grep '{formatted_mac_address}' | awk '{{print $2}}'")
        
        self.c.q_ip_address.put(ip_address.replace("(", "").replace(")", ""))
    
    def connect(self):
        self.host = self.c.q_ip_address.get()
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.ssh.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)
            self.sftp = self.ssh.open_sftp()
            print(f"SFTP Client connected to {self.username}@{self.host}")
        except Exception as e:
            print(f"An error occurred during {sys._getframe().f_code.co_name} : {e}")
        
        
    
    def close(self):
        if self.sftp:
            self.sftp.close()
        self.ssh.close()


    def sendFile(self):
        self.connect()
        local_file_name = self.c.q_local_zip_file_path.get()
        remote_file_path = f"{self.remote_path}\\{os.path.basename(local_file_name)}"

        try:
            self.sftp.put(local_file_name, remote_file_path)
            print(f"File {local_file_name} uploaded successfully to {self.host}:{remote_file_path}")

        except Exception as e:
            print(f"An error occurred during {sys._getframe().f_code.co_name} : {e}")

        finally:
            self.close()
        
    def start(self):
        for p in self.processes:
            p.start()