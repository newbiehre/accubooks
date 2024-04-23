import logging
import os
from datetime import datetime

from src.backend.common.utils import create_dir
from src.backend.global_variables import OUTPUT_PATH

logger_output_dir = create_dir(os.path.join(OUTPUT_PATH, "logs"))
logger_file = os.path.join(logger_output_dir, f"accubooks-{datetime.now().date()}.log")
logging.basicConfig(format='%(asctime)s %(name)s [%(levelname)s] - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO,
                    handlers=[logging.FileHandler(logger_file, mode="a"), logging.StreamHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
