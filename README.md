# Uber Ride Analytics Dashboard — Streamlit Workshop
An interactive dashboard built with Streamlit and Plotly during the Data Analytics Meeting student conference at Gdańsk University of Technology.
The goal of this workshop is to introduce beginners to building interactive data applications in Python using Streamlit.

---

## What will you build?
During the workshop, we will create an interactive analytics dashboard for Uber ride bookings.

The dashboard includes:
- KPI metrics,
- interactive filters,
- tabs and layout sections,
- Plotly charts,
- booking and revenue analysis,
- cancellations and ratings overview.

By the end of the workshop, you will have your own working Streamlit dashboard.

---

## Workshop goals

This workshop is designed for beginners.

You will learn:
- how Streamlit works,
- how to structure a dashboard application,
- how to build layouts using columns, tabs and sidebars,
- how to turn Python scripts into web apps.

No frontend experience is required.

---

## Repository structure

```text
.
├── app.py                      # Starter workshop version
├── app_final.py                # Final dashboard version
├── ncr_ride_bookings.csv       # Dataset
├── requirements.txt            # Python dependencies
├── README.md                   # Workshop instructions
└── streamlit_cheatsheet.pdf    # Streamlit cheat sheet
```

---

## Recommended setup (GitHub Codespaces)

To avoid installation problems during the workshop, we recommend using GitHub Codespaces.

### Step 1 — Open the repository

Open the workshop repository on GitHub.

### Step 2 — Open Codespaces

Click:

```text
Code → Codespaces → Create codespace on main
```

Wait until the environment starts.

### Step 3 — Install dependencies

Open the terminal and run:

```bash
pip install -r requirements.txt
```

### Step 4 — Run the app

```bash
streamlit run app.py
```

Streamlit will automatically open the application in the browser.

---

## Dataset

The dataset contains Uber ride booking information, including:
- booking status,
- ride distance,
- booking value,
- vehicle type,
- payment method,
- customer and driver ratings,
- cancellation reasons,
- ride timing metrics.

Dataset file:

```text
ncr_ride_bookings.csv
https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard?select=ncr_ride_bookings.csv
```

---

## Workshop flow

We will start from the starter version:

```text
app.py
```

and gradually build the dashboard step by step.

If you fall behind or want to compare your solution, you can check:

```text
app_final.py
```

---

## Technologies used

- Python
- Streamlit
- pandas
- Plotly

---

## Requirements

Dependencies are listed in:

```text
requirements.txt
```

Current requirements:

```txt
streamlit
pandas
plotly
```

Recommended Python version:

```text
Python 3.10 or newer

---

## Final result

At the end of the workshop, you should have:
- a working interactive dashboard,
- a basic understanding of Streamlit,
- a reusable project template for future dashboard projects.

---

## Credits

Workshop prepared for:

**Data Analytics Meeting 2026**  
Gdańsk University of Technology

Created by Julia Sowińska.
