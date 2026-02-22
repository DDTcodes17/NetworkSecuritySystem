import os
import sys
import pandas as pd
from dataclasses import dataclass
from networksecurity.exceptions.exceptions import NetworkSecurityException
from networksecurity.logger.logger import logging

@dataclass
class DataIngestionConfig:
    pass