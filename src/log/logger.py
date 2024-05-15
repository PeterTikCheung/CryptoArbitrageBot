import logging
import os


class Logger:
    def __init__(self):
        self.log_file_path = self._get_log_file_path()
        self._configure_logging()

    def _get_log_file_path(self):
        # Get the absolute path to the directory containing the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the absolute path to the log file
        return os.path.join(script_dir, 'log.txt')

    def _configure_logging(self):
        # Create the log directory if it doesn't exist
        log_dir = os.path.dirname(self.log_file_path)
        os.makedirs(log_dir, exist_ok=True)

        # Configure the logging module
        logging.basicConfig(filename=self.log_file_path, level=logging.INFO)

    def info(self, message):
        logging.info(message)

    def warning(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)

    def critical(self, message):
        logging.critical(message)
