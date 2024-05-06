# bot_automation.py
from data_extraction import extract_data
from data_insertion import insert_data
from database.db_table_creation import create_tables
from error_handling import log_error

def main():
    try:
        # Call the functions to create tables
        create_tables()
        
        # Extract and clean data
        data = extract_data('home/tim/vscode_projects/place/TheBot/Data/historical_data/historical_data.bz2')
        
        # Insert data into the database
        insert_data('market', data)
    except Exception as e:
        log_error(str(e))

if __name__ == '__main__':
    main()
