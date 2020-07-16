import os
import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
    dbuser = os.environ['USERS_DB_USER'],
    dbpassword = os.environ['USERS_DB_PASSWORD'],
    dbhost = os.environ['USERS_DB_HOST'],
    dbport = os.environ.get('USERS_DB_PORT', 5432),
    dbname = os.environ['USERS_DB_NAME']
    yield open_session(dbhost, dbport, dbname, dbuser, dbpassword)

@contextlib.contextmanager
def open_login_session():
    dbuser = os.environ['LOGIN_DB_USER'],
    dbpassword = os.environ['LOGIN_DB_PASSWORD'],
    dbhost = os.environ['LOGIN_DB_HOST'],
    dbport = os.environ.get('LOGIN_DB_PORT', 5432),
    dbname = os.environ['LOGIN_DB_NAME']
    yield open_session(dbhost, dbport, dbname, dbuser, dbpassword)
