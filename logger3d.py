import logging
import sys
from colorama import Fore, Style


try:
    assert float(sys.version[:3]) >= 3.6
except AssertionError:
    print('Recommend to use python version > 3.6!')
    sys.exit(1)


class ColorLogger(logging.Logger):
    def __init__(self, logger, filename=''):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)
        fmt_s = "[%(asctime)s::%(levelname)s] %(filename)s [line:%(lineno)d]:\n%(message)s"
        # basic stream handler
        s_handler = logging.StreamHandler()
        s_handler.setLevel(logging.DEBUG)
        s_handler.setFormatter(logging.Formatter(fmt_s))
        self.logger.addHandler(s_handler)
        
        if filename:
            f_handler = logging.FileHandler(filename)
            f_handler.setLevel(logging.WARNING)
            f_handler.setFormatter(logging.Formatter(fmt_s))
            self.logger.addHandler(f_handler)

    def debug(self, msg):
        return self.logger.debug(Fore.BLUE + str(msg) + Style.RESET_ALL)

    def info(self, msg):
        return self.logger.info(Fore.GREEN + str(msg) + Style.RESET_ALL)
 
    def warning(self, msg):
        return self.logger.warning(Fore.YELLOW + str(msg) + Style.RESET_ALL)
 
    def error(self, msg):
        return self.logger.error(Fore.RED + str(msg) + Style.RESET_ALL)
 
    def critical(self, msg):
        return self.logger.critical(Fore.RED + str(msg) + Style.RESET_ALL)


L = ColorLogger('automatch', 'automatch.log')
D = L.debug
I = L.info
W = L.warning
E = L.error


if __name__ == '__main__':
    logger = ColorLogger('demo', 'test.log')
    logger.debug('Followings are logger test')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
else:
    logger = ColorLogger('3DLogger', '3d.log')
