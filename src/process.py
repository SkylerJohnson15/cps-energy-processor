from sqlalchemy import create_engine, inspect
import pandas as pd

def process_and_store(df, db_url, granularity='daily'):
    """
    Process the DataFrame and store it in PostgreSQL with time-based categorization.
    
    Args:
        df (pandas.DataFrame): The DataFrame containing meter data.
        db_url (str): The PostgreSQL connection URL.
        granularity (str): The time granularity for categorization ('daily', 'weekly', 'monthly').
    
    Returns:
        int: Number of records stored.
    """
    # Clean and format the data
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['usage_kwh'] = pd.to_numeric(df['usage'], errors='coerce')
    df = df.dropna(subset=['usage_kwh'])

    # Add a time_period column based on granularity
    if granularity == 'daily':
        df['time_period'] = df['timestamp'].dt.date
    elif granularity == 'weekly':
        df['time_period'] = df['timestamp'].dt.to_period('W').apply(lambda r: r.start_time.date())
    elif granularity == 'monthly':
        df['time_period'] = df['timestamp'].dt.to_period('M').apply(lambda r: r.start_time.date())
    else:
        raise ValueError("Invalid granularity. Choose 'daily', 'weekly', or 'monthly'.")

    # Connect to the database
    engine = create_engine(db_url)
    
    # Check if the table exists and has the correct schema
    inspector = inspect(engine)
    if 'meter_readings' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('meter_readings')]
        if 'time_period' not in columns:
            with engine.connect() as conn:
                conn.execute("ALTER TABLE meter_readings ADD COLUMN time_period DATE;")
                # Optionally populate time_period for existing data
                conn.execute("UPDATE meter_readings SET time_period = DATE(timestamp) WHERE time_period IS NULL;")

    # Store in PostgreSQL
    df.to_sql('meter_readings', engine, if_exists='append', index=False)
    return len(df)