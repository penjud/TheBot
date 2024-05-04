import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert

# Establish a connection to the database
engine = create_engine('postgresql://penjud:#18Hoppy70@localhost:5432/thebot')

# Function to parse JSON data and return a DataFrame
def parse_json(json_data):
    # Load JSON data
    data = json.loads(json_data)

    # Extract market definition
    market_def = data['mc'][0]['marketDefinition']

    # Prepare data for DataFrame
    df_data = {
        'market_id': data['mc'][0]['id'],
        'event_type': market_def['eventTypeId'],
        'event_name': market_def['eventName'],
        'event_date': market_def['marketTime'],
        'country_code': market_def['countryCode'],
        'status': market_def['status'],
        'market_type': market_def['marketType'],
        'number_of_runners': market_def['numberOfActiveRunners']
    }
    
    # Create DataFrame
    return pd.DataFrame([df_data])
def upsert(engine, df, table_name, pk_column):
    table = pd.io.sql.get_schema(df, table_name, con=engine).strip('"')
    for row in df.itertuples(index=False):
        row_dict = row._asdict()
        stmt = insert(table).values(row_dict)
        upsert_stmt = stmt.on_conflict_do_update(
            constraint=pk_column,  # ensure this matches your table's primary key constraint name
            set_={c: stmt.excluded[c] for c in row_dict}
        )
        engine.execute(upsert_stmt)

def main(json_data):
    df = parse_json(json_data)
    upsert(engine, df, 'market_data', 'market_id')

# Example JSON data string (use your actual data)
json_data = '{"op":"mcm","clk":"1712242554","pt":1449693988672,"mc":[{"id":"1.117674259","marketDefinition":{"bspMarket":false,"turnInPlayEnabled":false,"persistenceEnabled":true,"marketBaseRate":5.0,"eventId":"27625527","eventTypeId":"7","numberOfWinners":1,"bettingType":"ODDS","marketType":"ANTEPOST_WIN","marketTime":"2016-03-15T15:20:00.000Z","suspendTime":"2016-01-19T12:00:00.000Z","bspReconciled":false,"complete":false,"inPlay":false,"crossMatching":false,"runnersVoidable":false,"numberOfActiveRunners":30,"betDelay":0,"status":"OPEN","runners":[{"status":"ACTIVE","sortPriority":1,"id":6871369,"name":"Faugheen"}],"regulators":["MR_INT"],"countryCode":"GB","discountAllowed":true,"timezone":"Europe/London","openDate":"2016-03-15T13:30:00.000Z","version":1191734098,"name":"Champion Hrd","eventName":"Chelt 15th Mar"},"rc":[],"con":true,"img":false,"tv":140672.29}]}'

# Parse the JSON data
df = parse_json(json_data)

# Insert the data into the PostgreSQL database
df.to_sql('market_data', con=engine, if_exists='append', index=False)
