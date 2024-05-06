# test_models.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from database.models import Base, User  # Ensure Base is imported if it's required for defining models

# Setup in-memory SQLite engine
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)  # Create tables
Session = sessionmaker(bind=engine)

def test_user_creation():
    # Create a new session for the test
    session = Session()
    try:
        # Perform test operations
        new_user = User(username="testuser", email="test@example.com")
        session.add(new_user)
        session.commit()

        # Retrieve and assert
        retrieved_user = session.query(User).filter_by(username="testuser").first()
        assert retrieved_user.email == "test@example.com"
    finally:
        # Ensure the session is closed after the test
        session.close()

