import dash_ag_grid as dag
from dash import Dash, html
import pandas as pd

app = Dash(__name__)

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/ag-grid/olympic-winners.csv"
)

columnDefs = [
    {
        "field": "athlete",
        "filter": "agTextColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
        },
    },
    {
        "field": "age",
        "maxWidth": 100,
        "filter": "agNumberColumnFilter",
        "filterParams": {
            "buttons": ["apply", "reset"],
            "closeOnApply": True,
        },
    },
    {
        "field": "country",
        "filter": "agTextColumnFilter",
        "filterParams": {
            "buttons": ["clear", "apply"],
        },
    },
    {
        "field": "year",
        "filter": "agNumberColumnFilter",
        "filterParams": {
            "buttons": ["apply", "cancel"],
            "closeOnApply": True,
        },
        "maxWidth": 100,
    },
    {"field": "sport"},
]

app.layout = html.Div(
    [
        dag.AgGrid(
            id="applying-filters",
            rowData=df.to_dict("records"),
            columnDefs=columnDefs,
            defaultColDef={"flex": 1, "filter": True},
            dashGridOptions={"animateRows": False}
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
