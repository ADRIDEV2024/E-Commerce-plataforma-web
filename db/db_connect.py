from sqlalchemy import create_engine, MetaData


engine = create_engine("mysql+pymysql://adridev:456631@localhost:3300/db-costumers")

conn = engine.connect()
metadata = MetaData()
