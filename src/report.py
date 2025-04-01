from sqlalchemy import create_engine
import pandas as pd

def generate_report(granularity='daily', db_url="postgresql://postgres:mynewpassword123@localhost:5432/cps_energy"):
    """
    Generate a report of usage totals from the meter_readings table.
    
    Args:
        granularity (str): 'daily', 'weekly', or 'monthly'
        db_url (str): Database connection URL
    
    Returns:
        pandas.DataFrame: Aggregated usage data
    """
    engine = create_engine(db_url)
    
    if granularity == 'daily':
        query = "SELECT DATE(timestamp) as date, SUM(usage_kwh) as total FROM meter_readings GROUP BY DATE(timestamp) ORDER BY DATE(timestamp)"
    elif granularity == 'weekly':
        query = "SELECT DATE_TRUNC('week', timestamp) as date, SUM(usage_kwh) as total FROM meter_readings GROUP BY DATE_TRUNC('week', timestamp) ORDER BY DATE_TRUNC('week', timestamp)"
    elif granularity == 'monthly':
        query = "SELECT DATE_TRUNC('month', timestamp) as date, SUM(usage_kwh) as total FROM meter_readings GROUP BY DATE_TRUNC('month', timestamp) ORDER BY DATE_TRUNC('month', timestamp)"
    else:
        raise ValueError("Invalid granularity. Choose 'daily', 'weekly', or 'monthly'.")
    
    report = pd.read_sql(query, engine)
    return report