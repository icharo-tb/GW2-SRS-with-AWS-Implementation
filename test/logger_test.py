import logging
import logging.config


logging.config.fileConfig("")

logger = logging.getLogger('gw2Logger')

logger.debug('WW')
logger.info('II')