import os
import shutil
import zipfile

from datetime import datetime


class SFTPServer:
    def __init__(self, common):
        self.c = common

        self.parseConfig()

        self.processes = [
            self.c.createProcessNoArgs(self.run)
        ]
    
    def parseConfig(self):
        self.checkpoint_dir = self.c.config["sftp"]["server"]["checkpoint_dir"]
        self.source_dir = self.c.config["sftp"]["server"]["source_dir"]
        self.unnecessary_files = self.c.config["sftp"]["server"]["unnecessary_files"]
        self.file_basename = self.c.config["sftp"]["server"]["file_basename"]
    
    def deleteUnnecessaryFiles(self):
        for i in self.unnecessary_files:
            self.c.executeShellCommand(f"sudo rm -f {i}")
    
    def initializeCheckpoint(self):
        self.c.executeShellCommand(f"sudo rm -rf {self.checkpoint_dir}")
    
    def copyCurrentFiles(self):
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M")

        checkpoint_file = f"{self.file_basename}_{timestamp}"
        self.zip_file = f"{checkpoint_file}.zip"

        os.makedirs(self.checkpoint_dir, exist_ok=True)

        self.checkpoint_path = os.path.join(self.checkpoint_dir, checkpoint_file)

        shutil.copytree(self.source_dir, self.checkpoint_path)
    
    def zipCurrentFiles(self):
        local_zip_file_path = os.path.join(self.checkpoint_dir, self.zip_file)
        with zipfile.ZipFile(local_zip_file_path, 'w') as zipf:
            for root, dirs, files in os.walk(self.checkpoint_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, self.checkpoint_path))
        
        self.c.q_local_zip_file_path.put(local_zip_file_path)
    
    def run(self):
        self.deleteUnnecessaryFiles()
        self.initializeCheckpoint()
        self.copyCurrentFiles()
        self.zipCurrentFiles()
    
    def start(self):
        for p in self.processes:
            p.start()
    
