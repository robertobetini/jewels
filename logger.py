from constants import Log, LogLevel
from datetime import datetime
from typing import Any

LOG_LABEL_TEMPLATE = "{0} - [{1}] {2:}"
LOG_LABEL_MAP = {
	LogLevel.ERROR: "ERROR",
	LogLevel.WARN: "WARN",
	LogLevel.INFO: "INFO",
	LogLevel.DEBUG: "DEBUG"
}

def check_log_level(func):
	def wrapper(self, *args, **kwargs):
		log_level = args[1]
		if log_level > Log.LOG_LEVEL:
			return

		func(self, *args)

	return wrapper

class Logger:
	def __init__(self, name: str):
		self.name = name

	def _format(self, text: str, level: LogLevel) -> str:
		now = datetime.now().isoformat(timespec="seconds")
		return LOG_LABEL_TEMPLATE.format(now, LOG_LABEL_MAP[level], text)

	def log(self, text: str, level: LogLevel) -> None:
		raise NotImplementedError()

	def debug(self, obj: Any) -> None:
		self.log(obj, LogLevel.DEBUG)

	def info(self, obj: Any) -> None:
		self.log(obj, LogLevel.INFO)

	def warn(self, obj: Any) -> None:
		self.log(obj, LogLevel.WARN)

	def error(self, obj: Any) -> None:
		self.log(obj, LogLevel.ERROR)

class ConsoleLogger(Logger):
	NAME = "console_logger"

	def __init__(self):
		super().__init__(ConsoleLogger.NAME)

	@check_log_level
	def log(self, text: str, level: LogLevel) -> None:
		print(self._format(text, level))

class FileLogger(Logger):
	NAME = "file_logger"

	def __init__(self, file_path: str):
		try:
			with open(file_path, "x") as file:
				pass
		except:
			pass

		with open(file_path, "a") as file:
			pass

		self.file_path = file_path
		super().__init__(FileLogger.NAME)

	def log(self, text: str, level: LogLevel) -> None:
		with open(self.file_path, "a") as file:
			file.write(self._format(text, level) + "\n")

class AggregateLogger(Logger):
	NAME = "aggregate_logger"

	def __init__(self, loggers: list[Logger]):
		super().__init__(AggregateLogger.NAME)
		self.loggers = loggers

	def log(self, text: str, level: LogLevel) -> None:
		for logger in self.loggers:
			logger.log(text, level)
