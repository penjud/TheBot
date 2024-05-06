#models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Strategy(Base):
    __tablename__ = 'strategies'
    strategy_id = Column(Integer, primary_key=True)
    strategy_name = Column(String, unique=True, nullable=False)
    strategy_settings = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Sport(Base):
    __tablename__ = 'sports'
    sport_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    events = relationship("Event", back_populates="sport")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    sport_id = Column(Integer, ForeignKey('sports.sport_id'))
    name = Column(String, nullable=False)
    start_time = Column(DateTime)
    venue = Column(String, nullable=True)
    sport = relationship("Sport", back_populates="events")
    markets = relationship("Market", back_populates="event")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Market(Base):
    __tablename__ = 'markets'
    market_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    market_name = Column(String, nullable=False)
    market_type = Column(String, nullable=False)
    market_time = Column(DateTime)
    market_status = Column(String, nullable=True)
    event = relationship("Event", back_populates="markets")
    runners = relationship("Runner", back_populates="market")
    predictions = relationship("ModelPrediction", back_populates="market")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Runner(Base):
    __tablename__ = 'runners'
    runner_id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    runner_name = Column(String, nullable=False)
    market = relationship("Market", back_populates="runners")
    predictions = relationship("ModelPrediction", back_populates="runner")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    bets = relationship("Bet", back_populates="user")
    api_usages = relationship("BetfairAPIUsage", back_populates="user")
    whitelists = relationship("UserIPWhitelist", back_populates="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ModelPrediction(Base):
    __tablename__ = 'model_predictions'
    prediction_id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    runner_id = Column(Integer, ForeignKey('runners.runner_id'))
    predicted_odds = Column(Float, nullable=False)
    model_accuracy = Column(Float)
    prediction_time = Column(DateTime)
    market = relationship("Market", back_populates="predictions")
    runner = relationship("Runner", back_populates="predictions")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserIPWhitelist(Base):
    __tablename__ = 'user_ip_whitelist'
    whitelist_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ip_address = Column(String, nullable=False)
    user = relationship("User", back_populates="whitelists")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Bet(Base):
    __tablename__ = 'bets'
    bet_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    runner_id = Column(Integer, ForeignKey('runners.runner_id'))
    user = relationship("User", back_populates="bets")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BetfairAPIUsage(Base):
    __tablename__ = 'betfair_api_usage'
    usage_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="api_usages")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MarketChange(Base):
    __tablename__ = 'market_changes'
    change_id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    market = relationship("Market")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PriceVolumeData(Base):
    __tablename__ = 'price_volume_data'
    data_id = Column(Integer, primary_key=True)
    runner_id = Column(Integer, ForeignKey('runners.runner_id'))
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    runner = relationship("Runner")
    market = relationship("Market")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HistoricalData(Base):
    __tablename__ = 'historical_data'
    historical_id = Column(Integer, primary_key=True)
    market_id = Column(Integer, ForeignKey('markets.market_id'))
    event_id = Column(Integer, ForeignKey('events.event_id'))
    market = relationship("Market")
    event = relationship("Event")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AdditionalData(Base):
    __tablename__ = 'additional_data'
    additional_data_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    event = relationship("Event")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)