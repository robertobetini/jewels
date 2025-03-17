from constants import Log
from abstract import Scene
from logger import Logger, FileLogger, ConsoleLogger, AggregateLogger

_loggers: list[Logger] = [ ConsoleLogger(), FileLogger(Log.LOG_FILE_PATH) ]

class Global:
	current_scene: Scene | None = None
	logger: Logger = AggregateLogger(_loggers)
