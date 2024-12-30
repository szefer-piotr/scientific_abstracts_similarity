import logging
import sys

def setup_logging() -> None:
    """Setup logging configuration."""
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    sys_stdout_handler = logging.StreamHandler(sys.stdout)
    sys_stdout_handler.setLevel(logging.DEBUG)
    root.addHandler(sys_stdout_handler)

def setup_logging_with_formatters() -> None:
    """Setup logging configuration with formatters."""
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    sys_stdout_handler = logging.StreamHandler(sys.stdout)
    sys_stdout_handler.setLevel(logging.DEBUG)
    sys_stdout_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    sys_stdout_handler.setFormatter(sys_stdout_formatter)
    root.addHandler(sys_stdout_handler)