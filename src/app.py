import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import base64
import io
import pandas as pd
from process import process_and_store
from sqlalchemy import create_engine

# Initialize Dash app with Bootstrap for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Database URL (update with your password)
db_url = "postgresql://postgres:mynewpassword123@localhost:5432/cps_energy"

# Define layout with tabs
app.layout = html.Div([
    html.H1("CPS Energy Meter Data Processor", className="text-center mt-4"),
    html.P("Upload meter data and manage it with ease.", className="text-center"),
    dcc.Tabs([
        dcc.Tab(label='Import Data', children=[
            html.Div([
                dcc.Dropdown(
                    id='granularity-dropdown',
                    options=[
                        {'label': 'Daily', 'value': 'daily'},
                        {'label': 'Weekly', 'value': 'weekly'},
                        {'label': 'Monthly', 'value': 'monthly'}
                    ],
                    value='daily',
                    clearable=False,
                    className="mt-3",
                    style={'width': '200px'}
                ),
                dcc.Upload(
                    id='upload-data',
                    children=dbc.Button('Upload CSV', color="primary"),
                    multiple=False,
                    className="mt-3"
                ),
                html.P("Expected CSV format: columns 'meter_id', 'timestamp', 'usage'", className="text-muted mt-2"),
                dcc.Loading(
                    id="loading-upload",
                    type="default",
                    children=html.Div(id='output-data-upload', className="mt-3")
                ),
                # Add a download button
                dbc.Button("Download All Data", id="download-button", color="secondary", className="mt-3"),
                dcc.Download(id="download-data")
            ], className="d-flex flex-column align-items-center")
        ]),
        dcc.Tab(label='Visualize Data', children=[
            html.P("Visualization coming soon...", className="mt-3 text-center")
        ])
    ])
])

# Callback for uploading data
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('granularity-dropdown', 'value')]
)
def update_output(contents, filename, granularity):
    if contents is not None:
        try:
            # Decode uploaded file
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            # Process and store using your function with granularity
            processed = process_and_store(df, db_url, granularity)
            return dbc.Alert(f"Successfully imported {filename}. Stored {processed} records with {granularity} categorization.", color="success")
        except Exception as e:
            return dbc.Alert(f"Error importing {filename}: {str(e)}", color="danger")
    return "No file uploaded."

# Callback for downloading data
@app.callback(
    Output("download-data", "data"),
    [Input("download-button", "n_clicks")],
    prevent_initial_call=True
)
def download_data(n_clicks):
    # Query all data from the meter_readings table
    engine = create_engine(db_url)
    query = "SELECT timestamp, usage_kwh, time_period FROM meter_readings"
    df = pd.read_sql(query, engine)
    
    # Convert DataFrame to CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_string = csv_buffer.getvalue()
    
    # Return the CSV file for download
    return dict(content=csv_string, filename="meter_readings_data.csv")

if __name__ == '__main__':
    app.run(debug=True)