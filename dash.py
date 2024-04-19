import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div(html.H1('Average Temperatures Cordoba (ESP), Hanoi (VN) & San Francisco (US)'))
if __name__ == '__main__':
     app.run_server(port=8080)
app =dash.Dash()

app.layout = html.Div([html.H1('Average Temperatures Cordoba (ESP), Hanoi (VN) & San Francisco (US)', style={'textAlign': 'center', 'color': 'green'}), 
                       # adding the main title
                       html.H2('Welcome', style ={'paddingLeft': '30px', 'color' : 'white'}),
                       html.H3('These are the Graphs', style ={'color' : 'purple'})
                      ])

if __name__ == '__main__':
     app.run_server(port=8080)

#let's check our df:
avg_temp = pd.read_csv('avg_temp_per_month.csv')
#avg_temp
avg_temp.dropna(inplace=True)
from dash import dash_table
app =dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

d_table = dash_table.DataTable(avg_temp.to_dict('records'),
                                  [{"name": i, "id": i} for i in avg_temp.columns]) 

# set app layout

app.layout = html.Div([html.H1('Average Temperatures in Cordoba , San Francisco & Hanoi', style={'textAlign': 'center', 'color': 'green'}), 
                       # adding the main title
                       html.H2('Temperatures (Cº)', style ={'textAlign': 'center','paddingLeft': '30px', 'color' : 'black'}),
                       html.Div(d_table),
])

if __name__ == '__main__':
     app.run_server(port=8080)

d_table = dash_table.DataTable(avg_temp.to_dict('records'),
                                  [{"name": i, "id": i} for i in avg_temp.columns],
                               style_data={'color': 'white','backgroundColor': 'black'},
                               style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'
    })

app =dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([html.H1('Average Temperatures in Cordoba , San Francisco & Hanoi', style={'textAlign': 'center', 'color': 'black'}), 
                       # adding the main title
                       html.H2('Temperatures (Cº)', style ={'textAlign': 'center','paddingLeft': '30px', 'color' : 'black'}),
                       html.Div(d_table),
], style={'backgroundColor': 'pink', 'padding': '20px'})  # Set background color to pink, why not?

if __name__ == '__main__':
     app.run_server(port=808)

fig1 = px.line(data_frame=avg_temp, 
              x='month', 
              y='average_temp', 
              height=500, 
              title="Average Temperature (Cº) in Cordoba, Hanoi and San Francisco", 
              markers=True,
              color='city'
             )
fig1.update_yaxes(title_text='Average Temperature (°C)')
fig1.update_xaxes(title_text='Month', tickmode='linear', dtick=1)
#fig1.show()

#max temperature per city:
max_temp = pd.read_csv('max_temp_table.csv')
#max_temp
#table has lots of duplicates, let's fix it:
max_temp = max_temp.drop_duplicates()
#max_temp
fig2 = px.bar(max_temp, y='max_temp', x='city', text_auto='.2s', color='city',
            title="Max Temperature (Cº) in Cordoba, San Francisco & Hanoi")
fig2.update_traces(textfont_size=15, textangle=0, textposition="outside", cliponaxis=False)
fig2.update_yaxes(title_text='Max Temperature (°C)')
fig2.update_xaxes(tickfont=dict(size=20))
#fig2.show()

#for the map, let's check our df:
sunny_days = pd.read_csv('total_sunny_days.csv')

# Dictionary mapping cities to countries
city_to_country = {
    'Cordoba': 'Spain',
    'San Francisco': 'United States',
    'Hanoi': 'Vietnam'
}

country_to_iso = {
    'Spain': 'ESP',
    'United States': 'US',
    'Vietnam': 'VN'}

# Map cities to countries
sunny_days['country'] = sunny_days['city'].map(city_to_country)
#sunny_days

# Map countries to ISO codes
sunny_days['iso_code'] = sunny_days['country'].map(country_to_iso)
#sunny_days
fig3 = px.choropleth(data_frame= sunny_days, 
                    locations=['Spain', 'United States', 'Vietnam'], 
                    projection='orthographic', 
                    scope='world',
                    color='sunny_days', 
                    locationmode='country names',
                    title='Max Temperature (Cº) per Country'
                   )

fig3.update_layout(width=900,  # Adjust width 
                  height=700),  # Adjust height
    
fig3.write_html('map.html')
#fig3.show()
#changing plots background:
fig1 = fig1.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
#fig1
fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
#fig2
fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="black"
    )
#fig3
app.layout = html.Div([
    html.Div([
        html.H1('Average Temperatures in Cordoba , San Francisco & Hanoi', style={'textAlign': 'center', 'color': 'black', 'marginBottom': '0'}),
        html.H2('Temperatures (Cº)', style={'textAlign': 'center', 'paddingLeft': '30px', 'color': 'black'})
    ], style={'backgroundColor': 'pink', 'padding': '20px'}), 
    d_table, 
    dcc.Graph(figure=fig1),  
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3)
])

if __name__ == '__main__':
    app.run_server(port=8080)