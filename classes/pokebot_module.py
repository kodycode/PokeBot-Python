from bot_logger import logger


class PokeBotModule:
    def post_error_log_msg(self, exc_name: Exception, msg: str, exc: Exception):
        print(f"{msg} See error.log.")
        logger.error(f"{exc_name}: "
                     f"{msg}\n{str(exc)}")
