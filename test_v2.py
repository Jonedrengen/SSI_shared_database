# Import required libraries
import dash
from dash import html, dcc, dash_table, Dash
from dash.dependencies import Input, Output
import pandas as pd
import requests
from filteringSystemColumns import columnDefs

response = requests.get("http://0.0.0.0:8888/Patient")
print(type(response))
if response.status_code == 200:
    data_raw = pd.json_normalize(response.json())
    data_opened = pd.json_normalize(data_raw['patients'].explode())
    print(type(data_opened))
else:
    print(f"Request failed with status code {response.status_code}")

# Convert to a DataFrame
df = pd.DataFrame(data_opened)
print(type(df))
print(df[0:4])
df_copy = df.copy()


# Initialize the Dash app
app = Dash(__name__)


# Define the layout of the app
app.layout = html.Div([
    html.H1("DASH app"),
    html.Button("Load Data", id="load-data", n_clicks=0),
    html.Button("Clear Table", id="clear-table", n_clicks=0),  # Add the clear table button
    dash_table.DataTable(
        id="data-table",
        columns=[{"name": i, "id": i} for i in df_copy.columns],
        data=[],  # Initially, the table data is empty
        filter_action="native"
    ),
])


# callback for table update
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
