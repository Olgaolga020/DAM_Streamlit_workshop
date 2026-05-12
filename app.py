import pandas as pd
import plotly.express as px

# =========================================================
# Page setup
# =========================================================

DATA_PATH = "ncr_ride_bookings.csv"


# =========================================================
# Load and prepare data
# =========================================================
#region Przygotowanie danych
rides = pd.read_csv(DATA_PATH)

rides["Date"] = pd.to_datetime(rides["Date"])

rides["Is Completed"] = rides["Booking Status"] == "Completed"
rides["Is Cancelled"] = rides["Booking Status"].str.contains("Cancelled", na=False)
rides["Is Incomplete"] = rides["Booking Status"].str.contains("Incomplete", na=False)
rides["Is No Driver Found"] = rides["Booking Status"].str.contains("No Driver", na=False)
rides["Is Not Completed"] = ~rides["Is Completed"]
#endregion

# =========================================================
# Header
# =========================================================


# =========================================================
# Sidebar filters
# =========================================================

completed_rides = rides[rides["Is Completed"]]
not_completed_rides = rides[rides["Is Not Completed"]]

# =========================================================
# Tabs
# =========================================================



# =========================================================
# Tab 1: Overview
# =========================================================
#region Przygotowanie danych do zakładki
total_bookings = round(len(rides),0)
success_rate = round(rides["Is Completed"].mean() * 100,2)
cancellation_rate = round(rides["Is Cancelled"].mean() * 100,2)
total_revenue = round(completed_rides["Booking Value"].sum()/1000,0)
avg_distance = round(completed_rides["Ride Distance"].mean(),2)

daily_bookings = rides.groupby("Date").size().reset_index(name="Bookings")

status_overview = rides["Booking Status"].value_counts().reset_index()
status_overview.columns = ["Status", "Bookings"]

revenue_by_vehicle = (
    completed_rides
    .groupby("Vehicle Type")["Booking Value"]
    .sum()
    .reset_index()
    .sort_values("Booking Value", ascending=False)
)

revenue_by_payment = (
    completed_rides
    .groupby("Payment Method")["Booking Value"]
    .sum()
    .reset_index()
    .sort_values("Booking Value", ascending=False)
)
#endregion

print("OVERVIEW")

# -------------
# KPI 
# -------------
print("Bookings", total_bookings)
print("Success rate", str(success_rate) + "%")
print("Cancellation rate", str(cancellation_rate) + "%")
print("Revenue", "₹" + str(total_revenue) + "tys")
print("Avg distance", str(round(avg_distance,2)) + "km")

# -------------
# Wykres liniowy liczby bookingów
# -------------
fig = px.line(daily_bookings, x="Date", y="Bookings")
#fig.show()

# -------------
# Wykres kołowy statusów 
# -------------
fig = px.pie(status_overview, names="Status", values="Bookings", hole=0.35)
#fig.show()

# -------------
# Wykres słupkowy typu pojazdu
# -------------
fig = px.bar(revenue_by_vehicle, x="Vehicle Type", y="Booking Value")
#fig.show()

# -------------
# Wykres słupkowy metody płatności
# -------------
fig = px.bar(revenue_by_payment, x="Payment Method", y="Booking Value")
#fig.show()

# -------------
# Wykres rozrzutu distans vs wartość
# -------------
fig = px.scatter(
    completed_rides,
    x="Ride Distance",
    y="Booking Value",
    hover_data=["Payment Method", "Pickup Location", "Drop Location"],
)
#fig.show()

# =========================================================
# Tab 2: Cancellations & issues
# =========================================================
#region Przygotowanie danych do zakładki
cancellation_rate = round(rides["Is Cancelled"].mean() * 100,2)
incomplete_rate = round(rides["Is Incomplete"].mean() * 100,2)
no_driver_rate = round(rides["Is No Driver Found"].mean() * 100,2)

cancelled_count = rides["Is Cancelled"].sum()
incomplete_count = rides["Is Incomplete"].sum()
no_driver_count = rides["Is No Driver Found"].sum()

issue_status = not_completed_rides["Booking Status"].value_counts().reset_index()
issue_status.columns = ["Booking Status", "Bookings"]
#endregion

print("CANCELLATIONS & ISSUES")

# -------------
# KPI 
# -------------
print("Cancellation rate", str(cancellation_rate) + "%")
print("Incomplete rate", str(incomplete_rate) + "%")
print("No driver rate", str(no_driver_rate) + "%")

# -------------
# Wykres słupkowy booking status
# -------------
fig = px.bar(issue_status, x="Bookings", y="Booking Status", orientation="h")
fig.update_layout(yaxis={"categoryorder": "total ascending"})
#fig.show()

# -------------
# Wykres kołowy powód rezygnacji klienta
# -------------
data = rides["Reason for cancelling by Customer"].dropna().value_counts().reset_index()
data.columns = ["Reason", "Count"]
fig = px.pie(data, names="Reason", values="Count", hole=0.35)
#fig.show()

# -------------
# Wykres kołowy powód rezygnacji kierowcy
# -------------
data = rides["Driver Cancellation Reason"].dropna().value_counts().reset_index()
data.columns = ["Reason", "Count"]
fig = px.pie(data, names="Reason", values="Count", hole=0.35)
#fig.show()

# -------------
# Wykres kołowy powód niewykonania przejazdu
# -------------
data = rides["Incomplete Rides Reason"].dropna().value_counts().reset_index()
data.columns = ["Reason", "Count"]
fig = px.pie(data, names="Reason", values="Count", hole=0.35)
#fig.show()

# -------------
# Wykres kołowy status
# -------------
data = pd.DataFrame({
    "Issue type": ["Cancelled", "Incomplete", "No driver found"],
    "Count": [cancelled_count, incomplete_count, no_driver_count]
})
fig = px.pie(data, names="Issue type", values="Count", hole=0.35)
#fig.show()


# =========================================================
# Tab 3: Ratings & time
# =========================================================
#region Przygotowanie danych do zakładki
avg_customer_rating = round(completed_rides["Customer Rating"].mean(),2)
avg_driver_rating = round(completed_rides["Driver Ratings"].mean(),2)
avg_vtat = round(rides["Avg VTAT"].mean(),2)
avg_ctat = round(completed_rides["Avg CTAT"].mean(),2)

rating_pairs = completed_rides.groupby(["Driver Ratings", "Customer Rating"]).size().reset_index(name="Number of rides")
#endregion

print("RATINGS & TIME")

# -------------
# KPI 
# -------------
print("Avg customer rating", avg_customer_rating)
print("Avg driver rating", avg_driver_rating)
print("Avg VTAT", str(avg_vtat) + " min")
print("Avg CTAT", str(avg_ctat) + " min")

# -------------
# Histogram ocen klientów
# -------------
fig = px.histogram(completed_rides, x="Customer Rating", nbins=20)
fig.update_xaxes(range=[2.8, 5.2])
#fig.show()

# -------------
# Histogram ocen kierowców
# -------------
fig = px.histogram(completed_rides, x="Driver Ratings", nbins=20)
fig.update_xaxes(range=[2.8, 5.2])
#fig.show()

# -------------
# WYkres rozrzutu ocen kierowców i klientów
# -------------
fig = px.scatter(
    rating_pairs,
    x="Driver Ratings",
    y="Customer Rating",
    size="Number of rides",
    hover_data=["Number of rides"],
)
fig.update_xaxes(range=[2.8, 5.2])
fig.update_yaxes(range=[2.8, 5.2])
#fig.show()

# -------------
# Wykres pudełkowy ocena a VTAT
# -------------
fig = px.box(completed_rides, x="Customer Rating", y="Avg VTAT")
fig.update_xaxes(range=[2.8, 5.2])
#fig.show()

# -------------
# Wykres pudełkowy ocena a CTAT
# -------------
fig = px.box(completed_rides, x="Customer Rating", y="Avg CTAT")
fig.update_xaxes(range=[2.8, 5.2])
#fig.show()