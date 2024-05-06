from sqlalchemy.orm import sessionmaker
from database.db_setup import engine, Base
from database.models import HistoricalData, MarketConditions, AdditionalData, SimulatedMarketData, UpcomingEvents, Runners, Markets, StrategyAssessmentResults
import logging

logging.basicConfig(level=logging.DEBUG)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

def get_historical_data_for_runner(runner_id):
    session = Session()
    historical_data = session.query(HistoricalData).filter(HistoricalData.runner_id == runner_id).all()
    session.close()
    return historical_data

def get_market_conditions(market_id):
    session = Session()
    market_conditions = session.query(MarketConditions).filter(MarketConditions.market_id == market_id).first()
    session.close()
    return market_conditions

def get_additional_data_for_runner(runner_id):
    session = Session()
    additional_data = session.query(AdditionalData).filter(AdditionalData.runner_id == runner_id).first()
    session.close()
    return additional_data

def get_historical_data():
    session = Session()
    historical_data = session.query(HistoricalData).all()
    session.close()
    return historical_data

def get_simulated_market_data():
    session = Session()
    simulated_market_data = session.query(SimulatedMarketData).all()
    session.close()
    return simulated_market_data

def get_upcoming_events():
    session = Session()
    upcoming_events = session.query(UpcomingEvents).all()
    session.close()
    return upcoming_events

def get_runners_by_market(market_id):
    session = Session()
    runners = session.query(Runners).filter(Runners.market_id == market_id).all()
    session.close()
    return runners

def get_markets_by_event(event_id):
    session = Session()
    markets = session.query(Markets).filter(Markets.event_id == event_id).all()
    session.close()
    return markets

def get_historical_data_for_strategy_assessment():
    session = Session()
    historical_data = session.query(Markets, Runners, HistoricalData, MarketConditions, AdditionalData).join(Runners, Markets.market_id == Runners.market_id).join(HistoricalData, Markets.market_id == HistoricalData.market_id).join(MarketConditions, Markets.market_id == MarketConditions.market_id).join(AdditionalData, HistoricalData.market_id == AdditionalData.market_id).all()
    session.close()
    return historical_data

def store_strategy_assessment_results(market_id, selection_id, strategy_score):
    session = Session()
    new_result = StrategyAssessmentResults(market_id=market_id, selection_id=selection_id, strategy_score=strategy_score)
    session.add(new_result)
    session.commit()
    session.close()
    return True