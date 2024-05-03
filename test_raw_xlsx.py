# Import required libraries
import dash
from dash import html, dcc, dash_table, Dash
from dash.dependencies import Input, Output
import pandas as pd
from filteringSystemColumns import columnDefs

df = pd.read_excel('test_data_3_variable.xlsx')


print(type(df))
print(len(df))
#print(df[0:1])
df_copy = df.copy()


# Initialize the Dash app
app = Dash(__name__)


# Define the layout of the app
app.layout = html.Div([
    html.H1("DASH test app"),
    html.P("press to load data"),
    html.Button("Load Data", id="load-data", n_clicks=0),
    html.Button("save data", id="save-data", n_clicks=0),
    html.Button("Reset", id="reset", n_clicks=0),  # Add the reset button
        dcc.Dropdown(
        id="column-dropdown",
        options=[{'label': i, 'value': i} for i in df_copy.columns],
        multi=True,
        value=df_copy.columns.to_list() #at first all columns are selected
    ),
    dash_table.DataTable(
        id="data-table",
        columns=[{"name": i, "id": i} for i in df_copy.columns],
        data=[],  # Initially, the table data is empty
        filter_action="native",
        page_action="native",
        page_size=150
    ),
    dcc.ConfirmDialog(id="confirm",
                      message="Data is saved as CSV",
    )
])



# callback for table update
@app.callback(
    Output("data-table", "data"), 
    Output("load-data", "disabled"),  # Add an output for the disabled property of the load data button
    [Input("load-data", "n_clicks"), Input("reset", "n_clicks")]  # Add the reset button to the inputs
)
def update_table(n_load_clicks, n_reset_clicks):
    ctx = dash.callback_context

    # Check which button was clicked
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "load-data" and n_load_clicks > n_reset_clicks:
            return df.to_dict("records"), True  # Disable the load data button after loading the data
        elif button_id == "reset" and n_reset_clicks > 0:
            return [], False  # Clear the table and enable the load data button when the reset button is clicked

    # If no button has been clicked, return the current data and the current state of the load data button
    return dash.no_update, dash.no_update

@app.callback(
    Output('data-table', 'columns'),
    [Input('column-dropdown', 'value')]
)
def update_columns(selected_columns):
    return [{"name": i, "id": i} for i in selected_columns]

# callback for saving data
@app.callback(
    [Output("save-data", "n_clicks"), Output("confirm", "displayed")],
    [Input("save-data", "n_clicks"), Input("data-table", "derived_virtual_data"), Input("column-dropdown", "value")] 
)

def save_data(n_clicks, table_data, selected_columns): #TODO: what exactly does storing n_clicks do?
    if n_clicks > 0:
        #creating a dataframe from the table data in the app
        df = pd.DataFrame(table_data)
        #filter for selected columns
        df = df[selected_columns]
        #save to a CSV file
        df.to_csv("table_data.csv", index=False)
        #return resets clicks and second argument is a popup
        return 0, True 
    return 0, False




#run the app
if __name__ == "__main__":
    app.run_server(debug=True)
