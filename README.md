# Intelligent Inventory Optimization & Automated Replenishment System

An end-to-end inventory analytics and automation system that combines historical inventory data, retail transaction behavior, machine-learning demand forecasting, supplier reliability analysis, real-time event simulation, automated replenishment decisions, procurement evaluation, purchase-order generation, and email-based alerts.

The system is designed as a complete data-to-decision pipeline rather than a standalone forecasting model.

---

## 📌 Project Overview

Inventory management requires balancing two competing objectives:

- Maintaining sufficient inventory to satisfy demand.
- Avoiding excessive inventory, holding costs, and unnecessary procurement.

Traditional inventory systems often rely on static reorder thresholds and historical averages. This project develops a data-driven inventory optimization pipeline where demand forecasts, demand variability, supplier reliability, lead-time uncertainty, and current inventory are combined to make automated replenishment decisions.

The system integrates:

1. Multi-source data collection
2. Exploratory Data Analysis
3. Data cleaning and preprocessing
4. Missing-value treatment and validation
5. Feature engineering
6. SQL-based data management
7. Machine-learning demand forecasting
8. Inventory simulation using real retail-event timing
9. Real-time event processing
10. Dynamic reorder-point calculation
11. Supplier evaluation
12. Automated procurement decisions
13. Purchase-order generation
14. Email alerts
15. Business intelligence reporting

The final architecture connects historical analytics with a continuously changing operational inventory environment.

---

# 🏗️ System Architecture

```text
                    DATA SOURCES
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
        ▼                ▼                 ▼
 Dataset A           Dataset B         Dataset C
 Historical          Supply Chain      Procurement
 Inventory           History           KPIs
        │                │                 │
        │                ▼                 ▼
        │          Lead-Time          Supplier
        │          Calibration        Reliability
        │
        ▼
 Demand Forecasting
        │
        ▼
 Feature Engineering
        │
        ▼
 Machine Learning Model
        │
        │
 Dataset D
 Online Retail II
        │
        ▼
 Real Retail Inter-Arrival
 Timing Patterns
        │
        ▼
 Replay Engine
        │
        ▼
 PostgreSQL
        │
        ▼
 Event Listener
        │
        ▼
 Inventory Update
        │
        ▼
 Reorder Engine
        │
        ├───────────────┐
        │               │
     NO_ORDER          ORDER
                        │
                        ▼
              Procurement Engine
                        │
                        ▼
              Supplier Evaluation
                        │
                        ▼
              Purchase Order
                        │
                        ├──────────────► Email Alert
                        │
                        ▼
                Fulfillment Engine
                        │
                        ▼
                  BI Reporting
```
## 📊 Dataset Architecture

A major design decision in this project is that the datasets do not all serve the same purpose.

Each dataset has a clearly defined role.

Dataset A — Historical Inventory

Dataset A is the primary inventory dataset.

It provides the historical relationship between:

Inventory levels
Units sold
Units ordered
Demand
Product
Store
Category
Region
Price
Discount
Promotion
Weather
Seasonality
Competitor pricing
Epidemic conditions
Role

Dataset A is used for:

Historical inventory analysis
Demand analysis
Feature engineering
ML demand forecasting
Establishing inventory behavior
Providing the basis for current inventory and demand profiles

The dataset is represented in PostgreSQL through tables including:

historical_inventory
inventory_ml_features
current_inventory
products
stores
Dataset B — Supply Chain History

Dataset B provides historical supply-chain behavior.

Important variables include:

supplier_lead_time_days
reorder_point
order_quantity
unit_cost
unit_price
promotion_flag
stockout_flag
demand_forecast
inventory_level
units_sold
Role

Dataset B is used primarily for:

Lead-time analysis
Supply-chain behavior analysis
Reorder-point validation
Supplier/warehouse behavior
Lead-time calibration

It is not used as a replacement for Dataset A's demand-forecasting data.

Dataset C — Procurement History / Supplier KPIs

Dataset C contains procurement and supplier-performance information.

Supplier profiles contain:

supplier_id
lead_time_observations
avg_lead_time_days
lead_time_std_days
min_lead_time_days
max_lead_time_days
delivery_rate_pct
defect_rate_pct
compliance_rate_pct
reliability_score
source_procurement_profile
Role

Dataset C is used for:

Supplier reliability calibration
Lead-time behavior
Delivery performance
Defect-rate analysis
Compliance analysis
Supplier scoring
Procurement decisions

Supplier performance therefore influences not only reporting but also the automated procurement stage.

Dataset D — Online Retail II

Dataset D is the Online Retail II dataset.

It is deliberately not used as the demand-forecasting input for Dataset A.

Instead, its primary purpose is to provide realistic retail-event timing behavior.

The transaction timestamps are used to calculate real inter-arrival patterns between retail events.

These timing patterns are then used by the replay engine to generate a realistic stream of inventory events.

Role

Dataset D provides:

Transaction timing
Inter-arrival times
Retail event frequency
Event timing distribution

This allows the system to simulate a continuously operating retail environment instead of simply generating random events at fixed intervals.

## 🔄 Data Processing Pipeline

The project begins with raw datasets and progressively converts them into structured analytical and operational data.
```
Raw Data
   ↓
Data Inspection
   ↓
EDA
   ↓
Cleaning
   ↓
Missing-Value Treatment
   ↓
Validation
   ↓
Feature Engineering
   ↓
Aggregated Tables
   ↓
ML Features
   ↓
PostgreSQL
   ↓
ML + Automation
```
## 🔎 Exploratory Data Analysis

EDA was performed to understand the structure and behavior of the datasets before building the forecasting and automation pipeline.

The analysis focused on:

Inventory
Inventory-level distributions
Units sold
Units ordered
Demand behavior
Product-level variation
Store-level variation
Regional differences
Demand
Daily demand
Demand trends
Demand variability
Seasonal patterns
Weekend effects
Lagged demand behavior
Retail Transactions
Transaction frequency
Quantity distribution
Revenue
Customer behavior
Product-level sales
Country-level activity
Transaction timing
Supply Chain
Lead-time distributions
Supplier variability
Reorder points
Stockout behavior
Order quantities
Procurement
Delivery performance
Defect rates
Compliance
Reliability
Supplier lead times

EDA was used to determine appropriate transformations, aggregation levels, feature-engineering strategies, and modelling inputs.

## 🧹 Data Cleaning & Preprocessing

The raw data was processed before being used for analytics and machine learning.

The cleaning pipeline included:

Data-type validation
Date/time conversion
Duplicate handling
Invalid-value checks
Quantity validation
Price validation
Missing-value identification
Consistency checks
Transaction filtering
Aggregation
Feature validation

The cleaned retail data is stored in:

clean_retail_transactions

Important fields include:

transaction_id
invoice
stock_code
description
quantity
invoice_date
price
customer_id
country
transaction_value
transaction_type

## 🧩 Missing-Value Treatment

Missing values were handled according to the role and meaning of each variable rather than applying one universal imputation method.

Variables were analyzed based on:

Data type
Business meaning
Distribution
Availability of related information
Whether missingness represented a valid business condition

For ML features, missing feature values are also handled before model prediction.

The prediction pipeline ensures that the model receives valid numerical input.

## ⚙️ Feature Engineering

Feature engineering is one of the main components of the forecasting system.

The inventory ML feature table contains:

store_id
product_id
date
demand
units_sold
units_ordered
inventory_level
price
discount
promotion
competitor_pricing
weather_condition
seasonality
epidemic
Lag Features

Historical demand was converted into lagged variables:

lag_1
lag_7
lag_14

These represent previous demand observations and help the model learn temporal relationships.

Rolling Statistics

Rolling demand statistics were created to capture local demand behavior:

rolling_7d_avg
rolling_14d_avg
rolling_30d_avg

rolling_7d_std
rolling_14d_std
rolling_30d_std

These capture:

Short-term demand
Medium-term demand
Long-term demand
Demand variability
Temporal Features

Calendar features include:

day_of_week
day_of_month
month
week_of_year
is_weekend

These allow the model to learn recurring temporal demand patterns.

Trend Features

Demand trend variables include:

demand_trend_7d
demand_trend_30d

These capture whether demand is increasing or decreasing over different time windows.

## 📈 Daily Demand Aggregation

Retail transactions were transformed into daily product-level demand.

The resulting tables include:

product_daily_demand
daily_product_demand
product_daily_calendar

These tables contain aggregated measures such as:

daily quantity
units sold
daily revenue
sales value
transaction count
invoice count
customer count

Daily aggregation provides a stable time-series representation for demand modelling and analysis.

## 🤖 Machine Learning Demand Forecasting

The project uses a LightGBM regression model for demand forecasting.

Model artifact:

lightgbm_inventory_demand_model.pkl

The model uses engineered temporal and demand-history features such as:

lag_1
lag_7
lag_14
rolling_7d_avg
rolling_14d_avg
rolling_30d_avg
rolling_7d_std
rolling_14d_std
rolling_30d_std
demand_trend_7d
demand_trend_30d
day_of_week
day_of_month
month
week_of_year
is_weekend

The model predicts the next demand value used by the replenishment system.

## 🎯 Forecasting Objective

The forecasting component estimates future demand at the store-product level.

Conceptually:
```
Historical Demand
       +
Lag Features
       +
Rolling Statistics
       +
Temporal Features
       +
Demand Trends
       ↓
LightGBM
       ↓
Predicted Demand
```
The prediction is constrained to non-negative values because physical product demand cannot be negative.

## 🗄️ PostgreSQL Database

PostgreSQL acts as the central operational and analytical database.

Database:

inventory_db

The database separates historical analytics from live operational information.

## 📋 Major Database Tables
Historical / Analytical
historical_inventory
inventory_ml_features
product_daily_demand
daily_product_demand
product_daily_calendar
product_ml_features
clean_retail_transactions
Operational
current_inventory
orders
purchase_orders
Product / Store
products
stores
sku_warehouse
Supplier / Procurement
product_supplier_map
supplier_profiles
procurement_orders
supply_chain_history

## 🧠 SQL & Database Layer

SQL is used extensively throughout the system for:

Data extraction
Aggregation
Filtering
Joining
Supplier mapping
Inventory lookup
Feature retrieval
Operational updates
Purchase-order storage
Event processing

Examples of database operations include:

Store → Product → Supplier
Store → Product → Current Inventory
Product → Historical Demand
Supplier → Reliability Profile
Order → Inventory Update
Order → Reorder Decision
Reorder → Purchase Order

The Python application communicates with PostgreSQL using psycopg.

##  🔁 Inventory Replay Engine

The replay engine converts historical retail timing behavior into a simulated real-time event stream.

The engine first analyzes Online Retail II transaction timestamps.

It calculates inter-arrival times between transactions.

Example statistics generated during replay initialization:

Timing pattern loaded: 53627 gaps
95th percentile real gap: 1440 seconds
Median replay gap: 27 seconds

A compression factor is then used to accelerate the historical timing pattern.

This allows a large amount of retail behavior to be replayed within a practical amount of time.

🧪 Why a Replay Engine?

A static dataset does not demonstrate how an inventory system behaves when transactions continuously arrive.

The replay engine creates this operational environment:

Historical Timing
       ↓
Inter-arrival Distribution
       ↓
Compressed Replay
       ↓
Retail Event
       ↓
PostgreSQL
       ↓
Event Listener

This makes it possible to test the entire inventory automation pipeline.

## 📡 Event Listener

The inventory event listener continuously listens for new order notifications through PostgreSQL.

Notification channel:

new_order

The listener waits for newly generated replay events.

When an event arrives, it retrieves the corresponding order and processes it.

Example:

New order notification: 8

PROCESSING ORDER EVENT: 8

Store       : S001
Product     : P0008
Event type  : SALE
Quantity    : 27
Current stock after event: 135

The listener then triggers the reorder engine.

## 📦 Inventory Update

For a sale event:

Current Stock
      -
Sale Quantity
      =
Updated Stock

For example:

Previous stock = 162
Sale quantity  = 27

Updated stock  = 135

The updated inventory state is stored in:

current_inventory

## 🔥 Automated Reorder Engine

The reorder engine combines:

Current inventory
ML demand forecast
Demand variability
Supplier lead time
Supplier lead-time variability
Service-level requirement

to determine whether replenishment is required.

## 📐 Safety Stock

The system uses a 90% service level.

Z = 1.28

Safety stock is calculated using both demand uncertainty and lead-time uncertainty.

The implemented formula is:

SS = Z × √(
        L × demand_std²
        +
        forecast² × lead_time_std²
     )

Where:

SS              = Safety Stock
Z               = Service-level z-score
L               = Supplier lead time
demand_std      = Demand standard deviation
forecast        = Forecast demand
lead_time_std   = Lead-time standard deviation

This allows the replenishment system to account for uncertainty from both sides of the supply chain.

## ⏱️ Lead-Time Demand

Lead-time demand is calculated as:

Lead-Time Demand
=
Forecast Demand × Lead Time

This estimates how much inventory is expected to be consumed while waiting for the replenishment order to arrive.

## 📍 Reorder Point

The reorder point is:
```
Reorder Point
=
Lead-Time Demand
+
Safety Stock
```
Therefore, the reorder point increases when:

Forecast demand increases
Supplier lead time increases
Demand variability increases
Lead-time variability increases
📦 Target Stock & Order Quantity

The replenishment policy uses a seven-day review period.
```
REVIEW_PERIOD_DAYS = 7

Review-period demand:

Review Period Demand
=
Forecast Demand × 7

Target stock:

Target Stock
=
Reorder Point
+
Review Period Demand

If:

Current Stock <= Reorder Point

the system generates:

ORDER

and calculates:

Order Quantity
=
Target Stock - Current Stock

rounded upward to the nearest whole unit.

Otherwise:

NO_ORDER
```
## 🧮 Example Reorder Decision

An actual replay event generated:

Store       : S001
Product     : P0008
Event type  : SALE
Quantity    : 27

After processing:

Current stock after event: 135

The ML and replenishment pipeline calculated:

Forecast demand : 97.33
Reorder point   : 1284.97
Decision        : ORDER
Order quantity  : 1832

Because:

135 <= 1284.97

the system generated a replenishment requirement.

## 🚚 Supplier Selection

Supplier selection is integrated into the replenishment engine.

The system evaluates mapped suppliers using:

Average Lead Time
Reliability Score

A supplier score is calculated as:

Supplier Score
=
Average Lead Time ×
(1 - Reliability Score / 100)

Lower values represent a better balance between speed and reliability.

The supplier with the best score is selected.

## ⭐ Supplier Evaluation

Supplier reliability is classified as:

Reliability >= 85   → EXCELLENT
Reliability >= 75   → GOOD
Reliability >= 65   → FAIR
Otherwise           → POOR

Supplier performance is based on:

reliability_score
delivery_rate_pct
defect_rate_pct
compliance_rate_pct
avg_lead_time_days
lead_time_std_days
## 🛒 Procurement Engine

After the reorder engine determines that an order is required, the procurement engine evaluates the selected supplier.

The procurement engine classifies suppliers using reliability, defect rate, and compliance.

Preferred Supplier

A supplier is classified as:

PREFERRED

when:

Reliability >= 85
AND
Defect Rate <= 5%
AND
Compliance >= 90%
Acceptable Supplier

A supplier is classified as:

ACCEPTABLE

when:

Reliability >= 75
AND
Defect Rate <= 10%
Risky Supplier

All other cases are classified as:

RISKY
## ✅ Procurement Decision

The procurement engine converts the supplier recommendation into an operational decision.
```
PREFERRED / ACCEPTABLE
        ↓
PROCEED

Whereas:

RISKY
   ↓
ORDER_WITH_CAUTION

The procurement result contains:

store_id
product_id
supplier_id
order_quantity
procurement_decision
supplier_rating
recommendation
lead_time_days
delivery_rate_pct
defect_rate_pct
compliance_rate_pct
reliability_score
supplier_source
```
## 📄 Automated Purchase Order Generation

When procurement is approved, the system creates a purchase order in PostgreSQL.

Example:
```
============================================================
              PURCHASE ORDER CREATED
============================================================

po_id               : 1
store_id            : S001
product_id          : P0008
supplier_id         : SUP_9
quantity            : 1832
created_at          : 2026-08-31 15:32:37
expected_arrival    : 2026-09-08 20:06:13
status              : PENDING

The purchase order is stored in:

purchase_orders
```
## 📬 Email Alert System

The system also contains an automated email alert component.

When a reorder is approved, the alert engine can send a notification containing the relevant procurement information.

The email system uses Gmail SMTP authentication with an application-specific password.

Email configuration is stored outside the source code using environment variables.

EMAIL_SENDER
EMAIL_PASSWORD
EMAIL_RECEIVER

The .env file is kept outside version-controlled source files.

## 📦 Fulfillment Engine

Purchase orders are not immediately treated as received inventory.

They initially have:

status = PENDING

The fulfillment engine checks purchase orders against their expected arrival time.
```
Conceptually:

Purchase Order
      ↓
PENDING
      ↓
Expected Arrival Reached
      ↓
FULFILLMENT
      ↓
Inventory Updated
```
This separates procurement from physical receipt and allows supplier lead-time behavior to be represented in the simulation.

## 🔄 Complete Automated Workflow
```
The complete system works as follows:

1. Historical datasets are collected
             ↓
2. Data is cleaned and validated
             ↓
3. EDA identifies demand and inventory patterns
             ↓
4. Daily demand is aggregated
             ↓
5. Lag, rolling, temporal and trend features are created
             ↓
6. ML model learns demand behavior
             ↓
7. LightGBM model predicts demand
             ↓
8. Online Retail II timing patterns are extracted
             ↓
9. Replay engine generates realistic retail events
             ↓
10. Event is inserted into PostgreSQL
             ↓
11. PostgreSQL sends new_order notification
             ↓
12. Listener receives the event
             ↓
13. Current inventory is updated
             ↓
14. Reorder engine calculates forecast
             ↓
15. Demand variability is evaluated
             ↓
16. Safety stock is calculated
             ↓
17. Reorder point is calculated
             ↓
18. ORDER / NO_ORDER is determined
             ↓
19. If ORDER → supplier is evaluated
             ↓
20. Procurement decision is generated
             ↓
21. Purchase order is created
             ↓
22. Email alert is triggered
             ↓
23. Fulfillment engine tracks arrival
             ↓
24. Inventory is updated after fulfillment
             ↓
25. Operational and analytical information
    is available for BI reporting
```
## 🧱 Project Structure
```
inventory_project/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── notebooks/
│   ├── EDA/
│   ├── data_cleaning/
│   ├── feature_engineering/
│   └── model_training/
│
├── models/
│   └── lightgbm_inventory_demand_model.pkl
│
├── sql/
│   ├── schema/
│   ├── transformations/
│   ├── analytical_queries/
│   └── views/
│
├── src/
│   ├── replay_engine.py
│   ├── listener.py
│   ├── reorder_engine.py
│   ├── procurement_engine.py
│   ├── alert_engine.py
│   └── fulfillment_engine.py
│
├── dashboard/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```
## 🛠️ Technology Stack
```
Programming
Python
SQL
Data Processing
Pandas
NumPy
Machine Learning
LightGBM
Joblib
Database
PostgreSQL
psycopg
Analytics
Exploratory Data Analysis
Time-series feature engineering
Statistical demand analysis
Inventory optimization
Automation
PostgreSQL notifications
Event-driven processing
Automated reorder decisions
Automated procurement
Purchase-order generation
Email alerts
Business Intelligence
Power BI
```
## 📌 Key Database Relationships
```
stores
   │
   └──── store_id ──── current_inventory
                           │
                           └──── product_id ──── products
                                                   │
                                                   └── category

products
   │
   └──── product_id ──── product_supplier_map
                                  │
                                  └──── supplier_id
                                           │
                                           ▼
                                  supplier_profiles

Operational flow:

orders
  │
  ├── store_id
  ├── product_id
  └── quantity
        │
        ▼
current_inventory
        │
        ▼
reorder logic
        │
        ▼
purchase_orders
        │
        ▼
fulfillment
```
## 📊 Business Intelligence Dashboard

The BI layer presents the operational and analytical outputs of the inventory system through an interactive reporting interface.

The reporting layer covers:
```
Executive Inventory Overview
Total inventory
Sales
Open purchase orders
Stockout indicators
Inventory health
Demand trends
Inventory Analytics
Current stock
Inventory by store
Inventory by category
Low-stock products
Critical inventory
Inventory trends
Sales & Demand Analytics
Revenue
Units sold
Transaction volume
Customer activity
Product demand
Demand trends
Replenishment Analytics
Current stock
Forecast demand
Reorder point
Safety stock
Target stock
Recommended order quantity
ORDER / NO_ORDER decisions
Supplier Analytics
Supplier reliability
Delivery rate
Defect rate
Compliance
Lead time
Supplier ranking
Supplier classification
Purchase Order Monitoring
Total purchase orders
Pending orders
Fulfilled orders
Order quantities
Expected arrival
Supplier
Store
Product
Purchase-order status
```
The reporting layer is connected to the PostgreSQL operational data so that inventory and procurement activity can be monitored from the same underlying system that powers the automation pipeline.

## 📈 Key Performance Indicators

The system supports monitoring of metrics such as:

Total Inventory
Total Units Sold
Total Revenue
Inventory Value
Average Stock
Low Stock SKUs
Stockout Count
Forecast Demand
Reorder Point
Safety Stock
Order Quantity
Open Purchase Orders
Supplier Reliability
Delivery Rate
Defect Rate
Compliance Rate
Average Lead Time
## 🔐 Configuration & Security

Database credentials and email credentials are not hard-coded into the production workflow.

Sensitive configuration is stored using environment variables.

Example:

DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD

EMAIL_SENDER
EMAIL_PASSWORD
EMAIL_RECEIVER

The .env file should be excluded from Git using:

.env

in .gitignore.

The model file and configuration paths should also be adapted to the environment in which the project is executed.

## ▶️ Running the System

Activate the virtual environment:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Ensure PostgreSQL is running and the database exists:

inventory_db
1. Start the Event Listener
python src/listener.py

Expected output:

```============================================================
              INVENTORY EVENT LISTENER
============================================================

Listening for new orders...
Channel: new_order

✓ Listener connected.
Waiting for replay events...

The listener remains active and waits for new inventory events.
```

2. Start the Replay Engine

In another terminal:

python src/replay_engine.py

The replay engine generates simulated retail events using the timing behavior extracted from Online Retail II.

Example:
```
[replay] event=001 | order=2 | SALE | S004/P0017 | qty=+103
[replay] event=002 | order=3 | SALE | S003/P0003 | qty=+14
```
3. Event Processing

The listener receives the event and automatically triggers the inventory pipeline.

Example:
```
PROCESSING ORDER EVENT: 8

Store       : S001
Product     : P0008
Event type  : SALE
Quantity    : 27
Current stock after event: 135
```
4. Reorder Calculation

The reorder engine calculates:
```
Forecast demand : 97.33
Reorder point   : 1284.97
Decision        : ORDER
Order quantity  : 1832
```
5. Procurement Evaluation

The procurement engine evaluates the supplier.

Example:
```
Supplier        : SUP_9
Supplier rating : EXCELLENT
Recommendation  : PREFERRED
Procurement     : PROCEED
```
6. Purchase Order

The system automatically generates:

po_id
store_id
product_id
supplier_id
quantity
created_at
expected_arrival
status

Example:
```
po_id            : 1
store_id         : S001
product_id       : P0008
supplier_id      : SUP_9
quantity         : 1832
status            : PENDING
```
7. Email Alert

When the procurement condition is satisfied, the alert engine sends the configured notification to the recipient.

8. Fulfillment

The fulfillment engine checks whether pending purchase orders have reached their expected arrival time.
```
Once an order is ready:

PENDING
   ↓
ARRIVED
   ↓
Inventory Updated
```
## 🧪 Example End-to-End Execution

A complete event can follow this path:
```
SALE EVENT

Store: S001
Product: P0008
Quantity: 27
        ↓
Inventory updated
        ↓
Current Stock = 135
        ↓
ML Forecast = 97.33
        ↓
Reorder Point = 1284.97
        ↓
135 <= 1284.97
        ↓
ORDER
        ↓
Order Quantity = 1832
        ↓
Supplier = SUP_9
        ↓
Supplier Rating = EXCELLENT
        ↓
Recommendation = PREFERRED
        ↓
Procurement = PROCEED
        ↓
Purchase Order Created
        ↓
PO Quantity = 1832
        ↓
Email Alert
        ↓
Fulfillment
        ↓
Inventory Replenished
```
This demonstrates the transition from a raw retail event to an automated supply-chain decision.

## 💡 Key Technical Contributions
1. End-to-End Architecture

The project connects data engineering, machine learning, SQL, event processing, inventory optimization, procurement, and BI into one workflow.

2. ML-Driven Replenishment

Demand forecasting is directly integrated into inventory control rather than being treated as an isolated prediction task.

3. Uncertainty-Aware Reorder Point

The reorder point incorporates both:

Demand variability
+
Lead-time variability

through safety-stock calculation.

4. Supplier-Aware Procurement

Supplier reliability and operational performance influence procurement decisions.

5. Realistic Event Simulation

Online Retail II transaction timing is used to reproduce realistic retail event-arrival behavior.

6. Event-Driven Automation

New transactions automatically trigger downstream inventory processing through PostgreSQL notifications.

7. Automated Purchase Orders

The system converts replenishment decisions into actual purchase-order records.

8. Automated Alerts

Approved procurement actions can trigger email notifications.

## 🎯 Business Impact

The system is designed to help organizations:

Reduce stockout risk
Improve inventory availability
Reduce excessive inventory
Incorporate demand uncertainty
Account for supplier lead-time uncertainty
Identify unreliable suppliers
Automate repetitive replenishment decisions
Improve procurement visibility
Reduce manual intervention
Monitor inventory continuously

## 🚀 Project Outcome

The completed system demonstrates how a traditional inventory workflow can be transformed into a data-driven automated decision system.

Instead of:
```
Sale
 ↓
Manual inventory check
 ↓
Manual reorder decision
 ↓
Manual supplier selection
 ↓
Manual purchase order

the system implements:

Sale
 ↓
Automatic inventory update
 ↓
ML demand forecast
 ↓
Dynamic reorder-point calculation
 ↓
Supplier evaluation
 ↓
Automated procurement decision
 ↓
Purchase-order generation
 ↓
Email notification
 ↓
Fulfillment
 ↓
Inventory update
 ↓
BI monitoring
```
The project therefore combines data analytics, machine learning, SQL, supply-chain concepts, event-driven architecture, and business intelligence into a single operational inventory optimization system.
