import pandas as pd
from sqlalchemy import create_engine

# MySQL connection details
username = 'root'
password = 'your_password'
host = 'localhost' 
port = '3306'  
database = 'michael'

# Create the SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Push DataFrame to MySQL, replacing the table if it exists
df.to_sql('crypto', con=engine, if_exists='replace', index=False)

print("DataFrame has been successfully written to the MySQL table.")
