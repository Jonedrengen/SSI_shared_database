# Import required libraries
import dash
from dash import html, dcc, dash_table, Dash
from dash.dependencies import Input, Output, State
import pandas as pd
import requests
from filteringSystemColumns import columnDefs
from Pydantic_models import PatientUpdate

response_Patient_table = requests.get("http://0.0.0.0:8888/Patient")
print(type(response_Patient_table))
if response_Patient_table.status_code == 200: #if resonse is "ok"
    data = pd.json_normalize(response_Patient_table.json())
    print(f"data is: {type(data)}")
else:
    print(f"Request failed with status code {response_Patient_table.status_code}")

# some useless changing of data

data_copy = data.copy()


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
        options=[{'label': i, 'value': i} for i in data_copy.columns],
        multi=True,
        value=data_copy.columns.to_list(), #at first all columns are selected
        style={'display': 'none'}
    ),
    html.Button('Update patient info', id='show-button', n_clicks=0),
    html.Div(id='Patient-update', style={'display': 'none'}, children=[
        dcc.Input(id='input-identifier', type='text', placeholder='patient identifier'),
        dcc.Input(id='input-name', type='text', placeholder='name'),
        dcc.Input(id='input-gender', type='text', placeholder='gender'),
        dcc.Input(id='input-deceased', type='text', placeholder='deceased state'),
        dcc.Input(id='input-birthDate', type='text', placeholder='birthDate (xxxx-xx-xx)'),
        dcc.Input(id='input-address', type='text', placeholder='address'),
        html.Button('update patient', id='submit-button')
    ]),
    dash_table.DataTable(
        id="data-table",
        columns=[{"name": i, "id": i} for i in data_copy.columns],
        data=[],  # Initially, the table data is empty
        filter_action="native",
        page_action="native",
        page_size=50
    ),
    dcc.ConfirmDialog(id="confirm",
                      message="Data is saved as CSV",
    )
])


# callback for table update
@app.callback(
    Output("data-table", "data"), 
    Output("load-data", "disabled"),  # Add an output for the disabled property of the load data button
    [Input("load-data", "n_clicks"), Input("reset", "n_clicks")]  # add the reset button to the inputs
)
def update_table(n_load_clicks, n_reset_clicks):
    ctx = dash.callback_context

    # check which button was clicked
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "load-data" and n_load_clicks > n_reset_clicks:
            return data_copy.to_dict("records"), True  #disable the load data button after loading the data
        elif button_id == "reset" and n_reset_clicks > 0:
            return [], False  # clear the table and enable the load data button when the reset button is clicked

    # If no button has been clicked, return the current data and the current state of the load data button
    return dash.no_update, dash.no_update

@app.callback(
    Output('data-table', 'columns'),
    [Input('column-dropdown', 'value')]
)
def update_columns(selected_columns):
    return [{"name": i, "id": i} for i in selected_columns]

#callback to hide or shown the dropdown menu
@app.callback(
    Output('Patient-update', 'style'),
    [Input('show-button', 'n_clicks')]
)
def toggle_form(n_clicks):
    if n_clicks is not None and n_clicks % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

# callback for saving data
@app.callback(
    [Output("save-data", "n_clicks"), Output("confirm", "displayed")],
    [Input("save-data", "n_clicks"), Input("data-table", "derived_virtual_data"), Input("column-dropdown", "value")] 
)

def save_data(n_clicks, table_data, selected_columns): #TODO: what exactly does storing n_clicks do?
    if n_clicks > 0:
        #creating a dataframe from the table data in the app
        data_copy = pd.DataFrame(table_data)
        #filter for selected columns
        data_copy = data_copy[selected_columns]
        #save to a CSV file
        data_copy.to_csv("table_data.csv", index=False)
        #return resets clicks and second argument is a popup
        return 0, True 
    return 0, False

# callback for performing PUT request

@app.callback(
    Output('Patient-update', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-identifier', 'value'),
     State('input-name', 'value'),
     State('input-gender', 'value'),
     State('input-deceased', 'value'),
     State('input-birthDate', 'value'),
     State('input-address', 'value')]
)
def update_patient(n_clicks, identifier, name, gender, deceased, birthDate, address):
    if n_clicks is None or n_clicks == 0:
        return dash.no_update
    patient_update = PatientUpdate(identifier=identifier, 
                                   name=name, 
                                   gender=gender, 
                                   deceased=deceased, 
                                   birthDate=birthDate, 
                                   address=address)
    data = patient_update.model_dump()
    response = requests.put(f"http://0.0.0.0:8888/Patient/{identifier}", json=data)
    if response.status_code == 200:
        return "Patient updated successfully"
    else:
        return f"Request failed with status code {response.status_code}"


#run the app
if __name__ == "__main__":
    app.run_server(debug=True)
