

from tendril.utils.config import ConfigOption
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)

depends = ['tendril.config.core']


config_elements_tally = [
    ConfigOption(
        "TALLY_HOST",
        "None",
        "Tally hostname"
    ),
    ConfigOption(
        "TALLY_PORT",
        "9002",
        "Tally port"
    ),
    ConfigOption(
        "TALLY_CACHE",
        "os.path.join(SHAREDCACHE_ROOT, 'tally')",
        "Tally cache folder"
    )
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_tally,
                          doc="Tally Connector Configuration")
