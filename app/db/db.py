import sys
sys.path.append("...")
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

url = os.environ.get("DATABASE_URL")

engine = create_engine(url , echo= True)

Session = sessionmaker(bind= engine)