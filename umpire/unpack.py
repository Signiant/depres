"""unpack.py"""

HELPTEXT = """
     ----- Unpack Module -----

The unpack module unpacks a tar gz or zip file.

Usage: Currently N/A

"""

import sys, os, subprocess
from maestro.core import module
from tqdm import tqdm
import logging, tarfile, zipfile

HELP_KEYS = ["h", "help"]

class UnpackError(Exception):
    pass

class UnpackModule(module.AsyncModule):
    # Required ID of this module
    id = "unpack"
    file_path = None
    destination_path = None
    delete_archive = False
    log_level = None

    def help(self):
        print(self.help_text)
        exit(0)

    def untar_gzip(self):
        with tarfile.open(name=self.file_path) as tar:
            for member in tqdm(iterable=tar.getmembers(), desc=f'Extracting {self.file_path}', total=len(tar.getmembers())):
                tar.extract(member=member, path=self.destination_path)

    def unzip(self):
        with zipfile.ZipFile(self.file_path) as zf:
            for member in tqdm(zf.infolist(), desc=f'Extracting {self.file_path}'):
                try:
                    zf.extract(member, self.destination_path)
                except zipfile.error as e:
                    pass

    def run(self,kwargs):
        logger = logging
        FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
        logger.basicConfig(format=FORMAT, stream=sys.stdout, level=self.log_level)
        logger.debug("Running Unpack")
        if self.file_path.endswith("tar.gz") or self.file_path.endswith("tgz"):
            self.untar_gzip()
        elif self.file_path.endswith(".zip"):
            logger.debug("Untar")
            self.unzip()
        else:
            raise UnpackError("Unable to unpack this type of file: " + os.path.split(self.file_path)[1])

        if self.delete_archive is True:
            os.remove(self.file_path)
