import redis
import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from login_html_hydra.config import UserEnv, LoginEnv, RedisEnv

@contextlib.contextmanager
def open_session(dbhost, dbport, dbname, dbuser, dbpassword, echo=True,):
    engine = create_engine(f'postgresql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}', echo=echo)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    session = Session()
    try:
        yield session
    finally:
        #session.close()
        engine.dispose()


@contextlib.contextmanager
def open_users_session():
    dbuser = UserEnv.DB_USER
    dbpassword = UserEnv.DB_PASSWORD
    dbhost = UserEnv.DB_HOST
    dbport = UserEnv.DB_PORT
    dbname = UserEnv.DB_NAME
    with open_session(dbhost, dbport, dbname, dbuser, dbpassword) as session:
        yield session

@contextlib.contextmanager
def open_login_session():
    dbuser = LoginEnv.DB_USER
    dbpassword = LoginEnv.DB_PASSWORD
    dbhost = LoginEnv.DB_HOST
    dbport = LoginEnv.DB_PORT
    dbname = LoginEnv.DB_NAME
    with open_session(dbhost, dbport, dbname, dbuser, dbpassword) as session:
        yield session


@contextlib.contextmanager
def open_redis_session():
    REDIS_HOST = RedisEnv.HOST
    REDIS_PORT = RedisEnv.PORT
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=None, socket_timeout=None)
    try:
        yield r
    finally:
        r.close()