import pandas as pd
import plotly.express as px
import streamlit as st

# Page setup
st.set_page_config(
    page_title="Uber Ride Analytics Dashboard",
    layout="wide"
)
DATA_PATH = "ncr_ride_bookings.csv"

# Helper functions
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    numeric_columns = [
        "Avg VTAT",
        "Avg CTAT",
        "Booking Value",
        "Ride Distance",
        "Driver Ratings",
        "Customer Rating",
    ]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def format_number(value):
    return f"{value:,.0f}"

def format_money(value):
    return f"₹{value:,.0f}"


def format_percent(value):
    return f"{value:.1f}%"


# -----------------------------
# Load data
# -----------------------------
rides = load_data(DATA_PATH)

# -----------------------------
# Header
# -----------------------------
st.title("🚗 Uber Ride Analytics Dashboard")
st.caption(
    "An interactive dashboard for exploring ride bookings, revenue, cancellations and ratings."
)

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

min_date = rides["Date"].min()
max_date = rides["Date"].max()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

vehicle_options = sorted(rides["Vehicle Type"].dropna().unique())
selected_vehicles = st.sidebar.multiselect(
    "Vehicle type",
    options=vehicle_options,
    default=vehicle_options,
)

status_options = sorted(rides["Booking Status"].dropna().unique())
selected_statuses = st.sidebar.multiselect(
    "Booking status",
    options=status_options,
    default=status_options,
)

payment_options = sorted(rides["Payment Method"].dropna().unique())
selected_payments = st.sidebar.multiselect(
    "Payment method",
    options=payment_options,
    default=payment_options,
)

# -----------------------------
# Apply filters
# -----------------------------
filtered_rides = rides.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_rides = filtered_rides[
        (filtered_rides["Date"] >= pd.to_datetime(start_date))
        & (filtered_rides["Date"] <= pd.to_datetime(end_date))
    ]

filtered_rides = filtered_rides[
    filtered_rides["Vehicle Type"].isin(selected_vehicles)
    & filtered_rides["Booking Status"].isin(selected_statuses)
    & filtered_rides["Payment Method"].isin(selected_payments)
]

# -----------------------------
# KPIs
# -----------------------------
total_bookings = len(filtered_rides)

completed_rides = filtered_rides[
    filtered_rides["Booking Status"].str.contains("Completed", case=False, na=False)
]

cancelled_rides = filtered_rides[
    filtered_rides["Booking Status"].str.contains("Cancelled", case=False, na=False)
]

completed_count = len(completed_rides)
cancelled_count = len(cancelled_rides)

success_rate = (completed_count / total_bookings * 100) if total_bookings > 0 else 0
cancellation_rate = (cancelled_count / total_bookings * 100) if total_bookings > 0 else 0

total_revenue = completed_rides["Booking Value"].sum()
avg_distance = completed_rides["Ride Distance"].mean()
avg_customer_rating = completed_rides["Customer Rating"].mean()

st.subheader("Key Metrics")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total bookings", format_number(total_bookings))
col2.metric("Completed rides", format_number(completed_count))
col3.metric("Success rate", format_percent(success_rate))
col4.metric("Cancellation rate", format_percent(cancellation_rate))
col5.metric("Revenue", format_money(total_revenue))
col6.metric("Avg distance", f"{avg_distance:.1f} km" if pd.notna(avg_distance) else "N/A")

st.divider()

# -----------------------------
# Charts row 1
# -----------------------------
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Bookings over time")

    bookings_by_date = (
        filtered_rides
        .groupby("Date")
        .size()
        .reset_index(name="Bookings")
        .sort_values("Date")
    )

    fig_bookings_time = px.line(
        bookings_by_date,
        x="Date",
        y="Bookings",
        markers=True,
        title="Daily number of bookings"
    )

    st.plotly_chart(fig_bookings_time, use_container_width=True)

with right_col:
    st.subheader("Bookings by vehicle type")

    bookings_by_vehicle = (
        filtered_rides
        .groupby("Vehicle Type")
        .size()
        .reset_index(name="Bookings")
        .sort_values("Bookings", ascending=False)
    )

    fig_vehicle_bookings = px.bar(
        bookings_by_vehicle,
        x="Vehicle Type",
        y="Bookings",
        title="Number of bookings by vehicle type"
    )

    st.plotly_chart(fig_vehicle_bookings, use_container_width=True)

# -----------------------------
# Charts row 2
# -----------------------------
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Revenue by vehicle type")

    revenue_by_vehicle = (
        completed_rides
        .groupby("Vehicle Type")["Booking Value"]
        .sum()
        .reset_index()
        .sort_values("Booking Value", ascending=False)
    )

    fig_revenue_vehicle = px.bar(
        revenue_by_vehicle,
        x="Vehicle Type",
        y="Booking Value",
        title="Revenue generated by completed rides"
    )

    st.plotly_chart(fig_revenue_vehicle, use_container_width=True)

with right_col:
    st.subheader("Revenue by payment method")

    revenue_by_payment = (
        completed_rides
        .groupby("Payment Method")["Booking Value"]
        .sum()
        .reset_index()
        .sort_values("Booking Value", ascending=False)
    )

    fig_payment = px.pie(
        revenue_by_payment,
        names="Payment Method",
        values="Booking Value",
        title="Revenue distribution by payment method"
    )

    st.plotly_chart(fig_payment, use_container_width=True)

st.divider()

# -----------------------------
# Cancellations
# -----------------------------
st.subheader("Cancellation Analysis")

cancel_col1, cancel_col2 = st.columns(2)

with cancel_col1:
    customer_reasons = (
        filtered_rides["Reason for cancelling by Customer"]
        .dropna()
        .value_counts()
        .reset_index()
    )
    customer_reasons.columns = ["Reason", "Count"]

    fig_customer_cancel = px.bar(
        customer_reasons,
        x="Count",
        y="Reason",
        orientation="h",
        title="Customer cancellation reasons"
    )

    st.plotly_chart(fig_customer_cancel, use_container_width=True)

with cancel_col2:
    driver_reasons = (
        filtered_rides["Driver Cancellation Reason"]
        .dropna()
        .value_counts()
        .reset_index()
    )
    driver_reasons.columns = ["Reason", "Count"]

    fig_driver_cancel = px.bar(
        driver_reasons,
        x="Count",
        y="Reason",
        orientation="h",
        title="Driver cancellation reasons"
    )

    st.plotly_chart(fig_driver_cancel, use_container_width=True)

st.divider()

# -----------------------------
# Ratings
# -----------------------------
st.subheader("Ratings by Vehicle Type")

ratings_by_vehicle = (
    completed_rides
    .groupby("Vehicle Type")[["Driver Ratings", "Customer Rating"]]
    .mean()
    .reset_index()
)

ratings_long = ratings_by_vehicle.melt(
    id_vars="Vehicle Type",
    value_vars=["Driver Ratings", "Customer Rating"],
    var_name="Rating Type",
    value_name="Average Rating"
)

fig_ratings = px.bar(
    ratings_long,
    x="Vehicle Type",
    y="Average Rating",
    color="Rating Type",
    barmode="group",
    title="Average driver and customer ratings by vehicle type"
)

fig_ratings.update_yaxes(range=[0, 5])

st.plotly_chart(fig_ratings, use_container_width=True)

# -----------------------------
# Data preview
# -----------------------------
with st.expander("Show filtered data"):
    st.write(f"Showing {len(filtered_rides):,} rows after applying filters.")
    st.dataframe(filtered_rides, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.caption("Built with Streamlit, pandas and Plotly.")
