import pandas as pd
import streamlit as st
import plotly_express as px



st.set_page_config(
    page_title="Cars Report Dashboard",
    page_icon="🚗",
    layout="wide")


st.title("🚗 Car Sales Dashboad 📈")
st.subheader("The Dashboard is fully built on Python 🐍")
st.caption("Desiged with 💟 by Tu Le Anh | Email: leanhtu9598@gmail.com")
st.markdown("---")

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="Car_Sales.xlsx",
        engine="openpyxl",
    )
    return df

df = get_data_from_excel()
df['Date'] = pd.to_datetime(df['Date'])
df['month'] = df['Date'].dt.month
df['year'] = df['Date'].dt.year
df['quarter'] = df['Date'].dt.quarter



# CREATE SIDEBAR

st.sidebar.header("Please Filter Here: ")
region = st.sidebar.multiselect(
    "Select the Region:",
    options=df["Dealer_Region"].unique(),
    default=df["Dealer_Region"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Customer Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

transmission = st.sidebar.multiselect(
    "Select the Transimission:",
    options=df["Transmission"].unique(),
    default=df["Transmission"].unique()
)

year = st.sidebar.multiselect(
    "Select the Year:",
    options=df["year"].unique(),
    default=df["year"].unique()
)



df_selection = df.query(
    "Dealer_Region == @region & Gender == @gender & Transmission == @transmission & year == @year" 
)

# LINE CHART OF CAR MODLE BY MONTH

sales_by_model = df_selection.groupby(by=["month", "year"])[["Price_USD"]].sum().reset_index()
sales_by_model["year"] = sales_by_model["year"].astype(str)
# st.dataframe(sales_by_model)

st.subheader("📊 General Analysis")
model_line_chart = px.line(
    sales_by_model,
    title="Total Sales by Month",
    x='month',
    y='Price_USD',
    color='year',
    markers='star',
    text='Price_USD'
)

(model_line_chart
    .update_layout(
        xaxis_title='Month',
        yaxis_title='Total Sales',
        # template='plotly_white',
        uniformtext_minsize=8, 
        uniformtext_mode='show',
    )
    .update_xaxes(tickfont=dict(size=12))
    .update_traces(texttemplate='%{text:.1s}')
)

# TREE CHART BY DEALER NAME

sales_by_dealer = df_selection.groupby(by=["Dealer_Name"])[["Price_USD"]].sum().reset_index()

dealer_tree_map = px.treemap(
    sales_by_dealer,
    title="Total Sales by Dealer",
    path=["Dealer_Name"],
    values='Price_USD'
)
(dealer_tree_map.update_layout(uniformtext=dict(minsize=10, mode='show')))


left_column, right_column = st.columns(2)
left_column.plotly_chart(dealer_tree_map, use_container_width=True)
right_column.plotly_chart(model_line_chart, use_container_width=True)

st.markdown("---")

# st.dataframe(df_selection)


# TOP KPI
st.subheader("🔎 Detailed Analysis")
total_sales = df_selection["Price_USD"].sum()

#SALE BY BRAND NAME

sales_by_brand = df_selection.groupby(by=["Company"])[["Price_USD"]].sum()
fig_brand_sales = px.bar(
    sales_by_brand,
    x=sales_by_brand.index,
    y="Price_USD",
    text='Price_USD',
    title="<b>Sales by Brand </b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_brand),
    template="plotly_white"
)

fig_brand_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
(fig_brand_sales
    .update_layout(
        xaxis_title='Brand Name',
        yaxis_title='Total Sales',
        # title_x=0.8,
        template='plotly_white',
        uniformtext_minsize=8, 
        uniformtext_mode='show',
        width=900
    )
    .update_xaxes(tickfont=dict(size=12), tickangle=45)
    .update_traces(texttemplate='%{text:.1s}', textposition='outside', width=0.8)
)

# BODY_STYLE PIE CHART
sales_by_body_style = df_selection.groupby(by=["Body_Style"])[["Price_USD"]].sum()
pie_chart = px.pie(
    sales_by_body_style,
    title="Sale by Body Style",
    values="Price_USD",
    names=sales_by_body_style.index
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_brand_sales, use_container_width=True)
right_column.plotly_chart(pie_chart, use_container_width=True)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {margin-top: 0 !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(" <style> div[class^='block-container'] { padding-top: 1rem; } </style> ", unsafe_allow_html=True)
