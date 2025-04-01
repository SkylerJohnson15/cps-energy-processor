from sqlalchemy import create_engine
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

    # Store in PostgreSQL
    engine = create_engine(db_url)
    df.to_sql('meter_readings', engine, if_exists='append', index=False)
    return len(df)