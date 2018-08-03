def get_db_config(env):
    return {
        'host': env.get('DB_HOST'),
        'port': env.get('DB_PORT'),
        'user': env.get('DB_USER'),
        'password': env.get('DB_PASSWORD'),
        'dbname': env.get('DB_NAME'),
    }


def get_logging_config(env):
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'google-style': {
                'format': '[%(asctime)s] %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S %z'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'google-style',
                'stream': 'ext://sys.stdout'
            }
        },
        'loggers': {
            '': {
                'level': 'INFO',
                'handlers': ['console'],
            },
        },
    }
