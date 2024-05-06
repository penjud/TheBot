from db_connection import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

# Example of a detailed table class for 'Market'
class Market(Base):
    __tablename__ = 'markets'
    market_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    status = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    market = relationship("Market", back_populates="events")

Market.events = relationship("Event", order_by=Event.event_id, back_populates="market")

# Function to create all tables
def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created successfully.")

if __name__ == '__main__':
    create_tables()
# The code snippet above defines a Market table with columns for market_id, name, status, is_active, and created_at. It also defines an Event table with columns for event_id, name, start_time, and market_id. The tables are related such that each market can have multiple events.