#!/usr/bin/env python

import logging
import logging.config
import sys
 
import muezzin

args = sys.argv[1:]
test_mode = '--test' in args
dry_run = '--dry-run' in args

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'level': 'DEBUG' if test_mode else 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': { 
        'muezzin': { 
            'handlers': ['default'],
            'level': 'DEBUG',
        },
    } 
}
logging.config.dictConfig(logging_config)

muezzin.run(test=test_mode, dry_run=dry_run)
