# Import required libraries
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import pandas as pd

# Sample data to display, mimicking data fetched from an API
data = {
    "ID": [1, 2, 3, 4, 5],
    "Name": ["Alice", "Bob", "Charlie", "Dana", "Elliot"],
    "Age": [28, 34, 29, 32, 35],
    "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Simple Dash App"),
    html.Button("Load Data", id="load-data", n_clicks=0),
    dash_table.DataTable(
        id="data-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=[],  # Initially, the table data is empty
    ),
])

# Define callback to update the table's data
@app.callback(
    Output("data-table", "data"),
    [Input("load-data", "n_clicks")]
)
def update_table(n_clicks):
    if n_clicks > 0:
        return df.to_dict("records")  # Convert DataFrame to dictionary
    return []  # Return empty list if button has not been clicked

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
