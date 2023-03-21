from sqlmodel import create_engine
from os import environ


# case with postgresql, mysql, sqlite
engine = {
    environ.get('DATABASE_URL').startswith("postgres"): create_engine(environ.get('DATABASE_URL')),
    environ.get('DATABASE_URL').startswith("mysql"): create_engine(environ.get('DATABASE_URL')),
    environ.get('DATABASE_URL').startswith("sqlite"): create_engine(
        environ.get('DATABASE_URL'), connect_args={"check_same_thread": False}
    ),
}[True]
