import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData

load_dotenv()
# SQLAlchemy
engine = create_engine(os.getenv('DATABASE_URL'))
metadata = MetaData()


