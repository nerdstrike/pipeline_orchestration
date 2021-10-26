import configparser


class Config:
    DEBUG = False
    PORT = 5000
    __parser = configparser.ConfigParser()

    with open('db.ini', 'r') as file:
        __parser.read_file(file)

    DB_URL = f'{__parser.get("orchestration_db","engine")}:///{__parser.get("orchestration_db","db")}'
    # Set to False when not using sqlite
    SAME_THREAD = True


class DevConfig(Config):
    DEBUG = True
