import subprocess

import multiprocessing as mp

from config import Config

class Common(Config):
    def __init__(self, config_path):
        super().__init__(config_path)

        self.initializeQueues()
    
    def initializeQueues(self):
        self.q_ip_address = self.createQueue()
        self.q_local_zip_file_path = self.createQueue()
    
    def executeShellCommand(self, command):
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"{command} executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing {command}: {e}")
    
    def executeShellCommandReturn(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
            print(f"{command} executed successfully.")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error executing {command}: {e}")
    
    def createProcessNoArgs(self, f):
        return mp.Process(target=f)
    
    def createQueue(self):
        return mp.Queue()