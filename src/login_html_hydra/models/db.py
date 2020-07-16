import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from login_html_hydra.config import UserEnv, LoginEnv

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
    dbuser = UserEnv.DB_USER,
    dbpassword = UserEnv.DB_PASSWORD,
    dbhost = UserEnv.DB_HOST
    dbport = UserEnv.DB_PORT
    dbname = UserEnv.DB_NAME
    yield open_session(dbhost, dbport, dbname, dbuser, dbpassword)

@contextlib.contextmanager
def open_login_session():
    dbuser = LoginEnv.DB_USER,
    dbpassword = LoginEnv.DB_PASSWORD,
    dbhost = LoginEnv.DB_HOST
    dbport = LoginEnv.DB_PORT
    dbname = LoginEnv.DB_NAME
    yield open_session(dbhost, dbport, dbname, dbuser, dbpassword)
