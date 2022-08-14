import sys
from typing import Iterator
sys.path.append("...")
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from os.path import join, dirname
from functools import lru_cache
from fastapi_utils.session import FastAPISessionMaker

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

url = os.environ.get("DATABASE_URL")

engine = create_engine(url , echo= True)

Session = sessionmaker(bind= engine)

def get_db() -> Iterator[Session]:
    """ FastAPI dependency that provides a sqlalchemy session """
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """ This function could be replaced with a global variable if preferred """
    return FastAPISessionMaker(url)
