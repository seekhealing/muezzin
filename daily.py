#!/usr/bin/env python

import logging
import logging.config
import sys
import argparse
 
import muezzin

parser = argparse.ArgumentParser(description='Hear ye, Seekers!')
parser.add_argument('--test', action='store_true', dest='test', default=False,
                    help='Only contact test accounts and enable debug logging.')
parser.add_argument('--dry-run', action='store_true', dest='dry_run', default=False,
                    help='Do everything except actually send anything.')
parser.add_argument('--templates-dir', action='store', dest='templates_dir', default=None,
                    help='Path containing email.j2 and sms.j2 to use.')

args = parser.parse_args()

test_mode = args.test
dry_run = args.dry_run
templates_dir = args.templates_dir

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

muezzin.run(test=test_mode, dry_run=dry_run, templates_dir=templates_dir)
