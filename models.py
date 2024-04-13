from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Strategy(db.Model):
    __tablename__ = 'strategies'
    strategy_id = Column(Integer, primary_key=True)
    strategy_name = Column(String, unique=True, nullable=False)
    strategy_settings = Column(String)
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Sport(db.Model):
    __tablename__ = 'sports'
    sport_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    events = relationship("Event", back_populates="sport")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Event(db.Model):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    sport_id = Column(Integer, ForeignKey('sports.sport_id'))
    name = Column(String, nullable=False)
    start_time = Column(DateTime)
    venue = Column(String, nullable=True)
    sport = relationship("Sport", back_populates="events")
    markets = relationship("Market", back_populates="event")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Market(db.Model):
    __tablename__ = 'markets'
    market_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    market_name = Column(String, nullable=False)
    market_type = Column(String, nullable=False)
    market_time = Column(DateTime)
    market_status = Column(String, nullable=True)
    event = relationship("Event", back_populates="markets")
    runners = relationship("Runner", back_populates="market")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Runner(db.Model):
    __tablename__ = 'runners'
    runner_id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    runner_name = Column(String, nullable=False)
    market = relationship("Market", back_populates="runners")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    bets = db.relationship("Bet", back_populates="user")
    api_usages = db.relationship("BetfairAPIUsage", back_populates="user")
    whitelists = db.relationship("UserIPWhitelist", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserIPWhitelist(db.Model):
    __tablename__ = 'user_ip_whitelist'
    whitelist_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ip_address = Column(String, nullable=False)
    user = relationship("User", back_populates="whitelists")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Bet(db.Model):
    __tablename__ = 'bets'
    bet_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    runner_id = Column(Integer, ForeignKey('runners.runner_id'))
    user = relationship("User", back_populates="bets")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class BetfairAPIUsage(db.Model):
    __tablename__ = 'betfair_api_usage'
    usage_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="api_usages")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class MarketChange(db.Model):
    __tablename__ = 'market_changes'
    change_id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    market = relationship("Market")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class PriceVolumeData(db.Model):
    __tablename__ = 'price_volume_data'
    data_id = Column(Integer, primary_key=True)
    runner_id = Column(Integer, ForeignKey('runners.runner_id'))
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    runner = relationship("Runner")
    market = relationship("Market")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class HistoricalData(db.Model):
    __tablename__ = 'historical_data'
    historical_id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    event_id = Column(Integer, ForeignKey('events.event_id'))
    market = relationship("Market")
    event = relationship("Event")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class AdditionalData(db.Model):
    __tablename__ = 'additional_data'
    additional_data_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    event = relationship("Event")
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

if __name__ == '__main__':
    from server import app, db
    
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    app.run(host='0.0.0.0', port=5000)