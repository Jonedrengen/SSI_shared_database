# Import required libraries
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import pandas as pd

data = pd.read_csv("Patient_test_data.csv")

# Convert to a DataFrame
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Simple Dash App"),
    html.Button("Load Data", id="load-data", n_clicks=0),
    html.Button("Clear Table", id="clear-table", n_clicks=0),  # Add the clear table button
    dash_table.DataTable(
        id="data-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=[],  # Initially, the table data is empty
    ),
])

# defining callback to update table data
@app.callback(
    Output("data-table", "data"),
    [Input("load-data", "n_clicks"), Input("clear-table", "n_clicks")]
)

def update_table(n_load_clicks, n_clear_clicks):
    ctx = dash.callback_context

    # Check which button was clicked
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "load-data" and n_load_clicks > 0:
            return df.to_dict("records")  # Convert DataFrame to dictionary
        elif button_id == "clear-table" and n_clear_clicks > 0:
            return []  # Return empty list to clear the table

    # If no button has been clicked, return the current data
    return dash.no_update

# defining callback to disable the load data button after data is loaded
@app.callback(
    Output("load-data", "disabled"),
    [Input("load-data", "n_clicks"), Input("clear-table", "n_clicks")]
)

def disable_button(n_load_clicks, n_clear_clicks):
    return n_load_clicks > n_clear_clicks


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
