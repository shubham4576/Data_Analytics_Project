import dash
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import pandas as pd
import webbrowser

app = dash.Dash()
colors = {
  'text':'#000000'
  }


def load_data():
    global df
    df = pd.read_csv('global_terror.csv')
    month = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

    global month_list
    month_list = [{'label': key, 'value': value} for key, value in month.items()]

    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
    # print(country_list)

    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()

    global city_list
    city_list = df.groupby("provstate")["city"].unique().apply(list).to_dict()

    global attack_list
    attack_list = [{'label': str(i), 'value': str(i)} for i in sorted((df['attacktype1_txt'].unique().tolist()))]

    global region_list
    region_list = [{'label': str(i), 'value': str(i)} for i in sorted((df['region_txt'].unique().tolist()))]

    global year_list
    year_list = sorted(df['iyear'].unique().tolist())

    global year_dict
    year_dict = {str(year): str(year) for year in year_list}

    global chart_dropdown_values
    chart_dropdown_values = {"Terrorist Organisation": 'gname',
                             "Target Nationality": 'natlty1_txt',
                             "Target Type": 'targtype1_txt',
                             "Type of Attack": 'attacktype1_txt',
                             "Weapon Type": 'weaptype1_txt',
                             "Region": 'region_txt',
                             "Country Attacked": 'country_txt'
                             }
    chart_dropdown_values = [{'label': i, 'value': k} for i, k in chart_dropdown_values.items()]

def create_app_ui():
    main_layout = html.Div([
        html.H1(children="Terrorism Analysis with Insights", id='main_title', style={"textAlign":"center", "color":colors}),
        html.Br(),
        html.Br(),
        dcc.Tabs(id="Tabs", value="Map", children=[
            dcc.Tab(label="Map Tool", id="Maptool", value="Map", children=[
                dcc.Tabs(id="subtabs1", value="Map", children=[
                    dcc.Tab(label="World Map Tool", id="WorldMap", value="WorldMap"),
                    dcc.Tab(label="India Map Tool", id="IndiaMap", value="IndiaMap")
                ]),
                dcc.Dropdown(
                    id='dropdown_month',
                    options=month_list,
                    placeholder='Select Month',
                    multi=True
                ),
                dcc.Dropdown(
                    id='dropdown_date',
                    options=[{'lable': 'All', 'value': 'All'}],
                    placeholder='Select Day',
                    multi=True
                ),
                dcc.Dropdown(
                    id='dropdown_region',
                    options=region_list,
                    placeholder='Select Region',
                    multi=True
                ),
                dcc.Dropdown(
                    id='dropdown_country',
                    options=[{'lable': 'All', 'value': 'All'}],
                    placeholder='Select Country',
                    multi=True
                ),
                dcc.Dropdown(
                    id='dropdown_state',
                    options=[{'label': 'All', 'value': 'All'}],
                    placeholder='Select State or Province',
                    multi=True
                ),
                dcc.Dropdown(
                    id='dropdown_city',
                    options=[{'label': 'All', 'value': 'All'}],
                    placeholder='Select City',
                    multi=True
                ),
                dcc.Dropdown(
                    id='dropdown_attack',
                    options=attack_list,
                    placeholder='Select Attack Type',
                    multi=True
                ),
                html.H5(children="Select Year", id="year_title"),
                dcc.RangeSlider(
                    id="year_slider",
                    min=min(year_list),
                    max=max(year_list),
                    marks=year_dict,
                    value=[min(year_list),max(year_list)],
                    step=None
                ),
                html.Br()
            ]),
            dcc.Tab(label="Chart Tool", id="Charttool", value="Chart", children=[
                dcc.Tabs(id="subtabs2", value="Chart", children=[
                    dcc.Tab(label="World Chart Tool", id="WorldChart", value="WorldChart"),
                    dcc.Tab(label="India Chart Tool", id="IndiaChart", value="IndiaChart")
                ]),
                dcc.Dropdown(
                    id="dropdown_chart",
                    options=chart_dropdown_values,
                    placeholder="Select Options",
                    value="region_txt"
                ),
                html.Br(),
                html.Br(),
                html.Hr(),
                dcc.Input(
                    id="search",
                    placeholder="Select Filter"
                ),
                html.Hr(),
                html.Br(),
                dcc.RangeSlider(
                    id="chart_year_slider",
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                ),
                html.Br()
            ])
        ]),
        html.Br(),
        html.Div(id="graph_obj", children="Graph will be shown here", style={"textAlign":"center"})
    ])
    return main_layout

# Callback of Our Page
@app.callback(Output("graph_obj", "children"),
              [
                  Input("Tabs", "value"),
                  Input("subtabs2", "value"),
                  Input("dropdown_month", "value"),
                  Input("dropdown_date", "value"),
                  Input("dropdown_region", "value"),
                  Input("dropdown_country", "value"),
                  Input("dropdown_state", "value"),
                  Input("dropdown_city", "value"),
                  Input("dropdown_attack", "value"),
                  Input("year_slider", "value"),
                  Input("dropdown_chart", "value"),
                  Input("search", "value"),
                  Input("chart_year_slider", "value"),

              ])

def update_app_ui(Tabs, subtabs2, month_value, date_value, region_value, country_value, state_value,
                  city_value, attack_value, year_value, chart_dp_value, search, chart_year_value,):
    fig = None
    if (Tabs == "Map"):
        print("Data Type of month value = ", str(type(month_value)))
        print("Data of month value = ", month_value)

        print("Data Type of Day value = ", str(type(date_value)))
        print("Data of Day value = ", date_value)

        print("Data Type of region value = ", str(type(region_value)))
        print("Data of region value = ", region_value)

        print("Data Type of country value = ", str(type(country_value)))
        print("Data of country value = ", country_value)

        print("Data Type of state value = ", str(type(state_value)))
        print("Data of state value = ", state_value)

        print("Data Type of city value = ", str(type(city_value)))
        print("Data of city value = ", city_value)

        print("Data Type of Attack value = ", str(type(attack_value)))
        print("Data of Attack value = ", attack_value)

        print("Data Type of year value = ", str(type(year_value)))
        print("Data of year value = ", year_value)
        # year_filter
        year_range = range(year_value[0], year_value[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
        # month_filter
        if month_value == [] or month_value is None:
            pass
        else:
            if date_value == [] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value)
                                & (new_df["iday"].isin(date_value))]
        # region, country, state, city filter
        if region_value == [] or region_value is None:
            pass
        else:
            if country_value == [] or country_value is None:
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                        (new_df["country_txt"].isin(country_value)) &
                                        (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                        (new_df["country_txt"].isin(country_value)) &
                                        (new_df["provstate"].isin(state_value)) &
                                        (new_df["city"].isin(city_value))]

        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)]

        if new_df.shape[0]:
            pass
        else:
            new_df = pd.DataFrame(columns=['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
                                           'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])

            new_df.loc[0] = [0, 0, 0, None, None, None, None, None, None, None, None]

        mapFigure = px.scatter_mapbox(new_df,
                                      lat="latitude",
                                      lon="longitude",
                                      color="attacktype1_txt",
                                      hover_name="city",
                                      hover_data=["region_txt", "country_txt", "provstate", "city", "attacktype1_txt",
                                                  "nkill", "iyear", "imonth", "iday"],
                                      zoom=1
                                      )
        mapFigure.update_layout(mapbox_style="stamen-toner",
                                autosize=True,
                                margin=dict(l=0, r=0, t=25, b=20),
                                )

        fig = mapFigure

    elif (Tabs == "Chart"):
        fig = None
        chart_df = None
        year_range_chart = range(chart_year_value[0], chart_year_value[1] + 1)
        chart_df = df[df["iyear"].isin(year_range_chart)]

        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"] == "South Asia") &
                                (chart_df["country_txt"] == "India")]

        if chart_dp_value is not None:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case = False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        else:
            raise PreventUpdate

        if chart_df.shape[0]:
            pass
        else:
            chart_df = pd.DataFrame(columns=['iyear', 'count', chart_dp_value])
            chart_df.loc[0] = [0, 0, "No data"]

        fig = px.area(
            chart_df,
            x= "iyear",
            y ="count",
            color = chart_dp_value
        )

    return dcc.Graph(figure=fig)

@app.callback(
    Output("dropdown_date", "options"),
    [
        Input("dropdown_month", "value")
    ]
)

def update_date(month):
    date_list = [x for x in range(1,32)]
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback([
    Output("dropdown_region", "value"),
    Output("dropdown_region", "disabled"),
    Output("dropdown_country", "value"),
    Output("dropdown_country", "disabled"),
],
    [
        Input("subtabs1", "value")
    ])

def update_r(Tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if Tab == "WorldMap":
        pass
    elif Tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c

@app.callback(
    Output('dropdown_country', 'options'),
    [
         Input('dropdown_region', 'value')
    ]
)
def set_country_options(region_value):
    option = []
    # Making the country Dropdown data
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output("dropdown_state", "options"),
    [
        Input("dropdown_country", "value")
    ]
)

def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]

@app.callback(
    Output('dropdown_city', 'options'),
    [
        Input('dropdown_state', 'value')
    ]
)

def set_city_options(state_value):
  # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]


def open_browser():
    webbrowser.open_new('http://127.0.0.1:4050/')


# main function
def main():
    print('Starting the Project...')
    # calling functions
    load_data()
    open_browser()
    global app
    app.layout = create_app_ui()
    app.title = "Terrorism Analysis With Insights"
    # running the web application
    app.run_server(port=4050)

    print('Ending the Project....')
    # Deallocating the memory
    df = None
    app = None
    month = None
    attack_list = None
    region_list = None
    year_list = None
    year_dict = None


if __name__ == '__main__':
    main()