import configparser
from pathlib import Path

class Config:
    def __init__(self, path: str):
        parser = configparser.ConfigParser()
        parser.read(path)

        self.file_path = Path(parser.get("DEFAULT", "linuxpath", fallback="./tests/data/small_sample.txt"))
        self.reread_on_query = parser.getboolean("DEFAULT", "REREAD_ON_QUERY", fallback=False)
        self.use_ssl = parser.getboolean("DEFAULT", "SSL", fallback=False)
        self.port = parser.getint("DEFAULT", "PORT", fallback=44445)
        self.host = parser.get("DEFAULT", "HOST", fallback="0.0.0.0")
