# class Config:
#     DEBUG = True
#     SECRET_KEY = "your_secret_key"


# class Config:
#     DEBUG = True
#     SECRET_KEY = "your_secret_key"
    
#     # MySQL Configuration
#     MYSQL_HOST = 'localhost'
#     MYSQL_PORT = 3306
#     MYSQL_USER = 'root'
#     MYSQL_PASSWORD = 'Rahi1807@'
#     MYSQL_DB = 'RTSMA'



import os

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")

    # MySQL Configuration from environment
   MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-xyz.render.com")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER",'root')
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD",'Rahi1807@')
    MYSQL_DB = os.getenv("MYSQL_DB",'RTSMA')
