import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Streamlit app title
st.title('Commodity Prices Over Time')

# Use Streamlit's file uploader to select the data file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Parse and load data into a Pandas DataFrame
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(data.head())

    # Convert 'Date' to datetime if not already
    data['Date'] = pd.to_datetime(data['Date'])

    # Get the unique symbols (commodities)
    symbols = data['Symbol'].unique()

    # Create a Streamlit selectbox to choose the commodity
    selected_symbol = st.selectbox('Choose a commodity to display', symbols)

    # Extract the data for this symbol
    symbol_data = data[data['Symbol'] == selected_symbol]

    # Create a figure
    fig = go.Figure()

    # Add scatter plot
    fig.add_trace(go.Scatter(x=symbol_data['Date'],
                             y=symbol_data['Close'],
                             mode='markers',
                             name=selected_symbol))

    # Get the years in the data for this symbol
    years = symbol_data['Date'].dt.year.unique()

    # Update x-axis and y-axis labels
    fig.update_xaxes(title_text="Date",
                     tickvals=[f"{year}-01-01" for year in years],
                     ticktext=[str(year) for year in years])
    fig.update_yaxes(title_text="Close Price")

    # Update layout
    fig.update_layout(title=f'{selected_symbol} Prices Over Time',
                      showlegend=False,
                      margin=dict(t=50, b=50, l=50, r=50),
                      title_font=dict(size=14),
                      height=400,  # Height of each individual plot
                      width=900)  # Width of each individual plot

    # Use Streamlit to display the Plotly plot
    st.plotly_chart(fig)
