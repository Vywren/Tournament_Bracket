from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Step 1: Create a database engine (for SQLite)
engine = create_engine('sqlite:///:memory:')  # Or use a file-based SQLite with 'sqlite:///example.db'

# Step 2: Define the base class
Base = declarative_base()

# Step 3: Define your model class
class User(Base):
    __tablename__ = 'users'
    
    # Primary key with auto-increment (SQLite automatically increments INTEGER PRIMARY KEY)
    id = Column(Integer, primary_key=True)
    
    # Other columns
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

# Step 4: Create the table in the database
Base.metadata.create_all(engine)

# Step 5: Set up session
Session = sessionmaker(bind=engine)
session = Session()

# Step 6: Create and add a new User object
new_user = User(name="John Doe", email="john@example.com")
session.add(new_user)

# Step 7: Commit the session to persist the object in the database
session.commit()

# The auto-incremented id can now be accessed
print(f"New user id: {new_user.id}")