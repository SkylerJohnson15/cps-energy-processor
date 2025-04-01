import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from report import generate_report

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Dropdown(
        id='granularity-dropdown',
        options=[
            {'label': 'Daily', 'value': 'daily'},
            {'label': 'Weekly', 'value': 'weekly'},
            {'label': 'Monthly', 'value': 'monthly'}
        ],
        value='monthly',  # Default to monthly for clarity
        clearable=False
    ),
    dcc.Graph(id='usage-chart')
])

# Callback to update the chart
@app.callback(
    Output('usage-chart', 'figure'),
    [Input('granularity-dropdown', 'value')]
)
def update_chart(granularity):
    report = generate_report(granularity)
    fig = px.line(report, x='date', y='total', title=f'CPS Energy {granularity.capitalize()} Usage')
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)