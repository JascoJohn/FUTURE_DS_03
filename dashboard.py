import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Marketing Funnel Dashboard", layout="wide")

# Load data
df = pd.read_csv('data/bank_clean.csv')

st.title("📊 Marketing Funnel & Conversion Dashboard")

# --- Sidebar filters ---
st.sidebar.header("Filters")

def multiselect_filter(label, column):
    options = sorted(df[column].unique().tolist())
    return st.sidebar.multiselect(label, options, default=options)

selected_channel   = multiselect_filter("Channel", 'contact')
selected_month     = multiselect_filter("Month", 'month')
selected_day       = multiselect_filter("Day of Week", 'day_of_week')
selected_job       = multiselect_filter("Job", 'job')
selected_marital   = multiselect_filter("Marital Status", 'marital')
selected_education = multiselect_filter("Education", 'education')
selected_default   = multiselect_filter("Has Credit Default", 'default')
selected_housing   = multiselect_filter("Has Housing Loan", 'housing')
selected_loan      = multiselect_filter("Has Personal Loan", 'loan')
selected_poutcome  = multiselect_filter("Previous Outcome", 'poutcome')

age_min, age_max = int(df['age'].min()), int(df['age'].max())
selected_age = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))

# --- Reset button ---
if st.sidebar.button("Reset All Filters"):
    st.rerun()

# --- Apply filters ---
filtered = df[
    df['contact'].isin(selected_channel) &
    df['month'].isin(selected_month) &
    df['day_of_week'].isin(selected_day) &
    df['job'].isin(selected_job) &
    df['marital'].isin(selected_marital) &
    df['education'].isin(selected_education) &
    df['default'].isin(selected_default) &
    df['housing'].isin(selected_housing) &
    df['loan'].isin(selected_loan) &
    df['poutcome'].isin(selected_poutcome) &
    df['age'].between(selected_age[0], selected_age[1])
]

st.sidebar.markdown(f"**Rows matching filters:** {len(filtered):,} / {len(df):,}")

# --- Handle empty results ---
if filtered.empty:
    st.warning("No data matches the selected filters. Try widening your selection.")
    st.stop()

# --- Recalculate funnel on filtered data ---
stage_1 = filtered['stage_1_contacted'].sum()
stage_2 = filtered['stage_2_engaged'].sum()
stage_3 = filtered['stage_3_converted'].sum()

# --- KPI row ---
col1, col2, col3 = st.columns(3)
col1.metric("Contacted", f"{stage_1:,}")
col2.metric("Engaged", f"{stage_2:,}", f"{stage_2/stage_1*100:.1f}%" if stage_1 else "0%")
col3.metric("Converted", f"{stage_3:,}", f"{stage_3/stage_1*100:.1f}%" if stage_1 else "0%")

# --- Funnel chart ---
fig = go.Figure(go.Funnel(
    y=['Contacted', 'Engaged', 'Converted'],
    x=[stage_1, stage_2, stage_3],
    textinfo='value+percent initial',
    marker={'color': ['#4C72B0', '#55A868', '#C44E52']}
))
fig.update_layout(title="Funnel Breakdown", title_x=0.5)
st.plotly_chart(fig, use_container_width=True)

# --- Channel comparison (now uses filtered data) ---
st.subheader("Conversion Rate by Channel")
if filtered['contact'].nunique() > 0:
    channel_stats = filtered.groupby('contact').agg(
        contacted=('stage_1_contacted', 'sum'),
        converted=('stage_3_converted', 'sum')
    )
    channel_stats['rate_%'] = (channel_stats['converted'] / channel_stats['contacted'] * 100).round(1)
    st.bar_chart(channel_stats['rate_%'])

# --- Monthly trend (now uses filtered data) ---
st.subheader("Monthly Conversion Trend")
month_order = ['mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
month_stats = filtered.groupby('month').agg(
    contacted=('stage_1_contacted', 'sum'),
    converted=('stage_3_converted', 'sum')
).reindex(month_order).dropna()
month_stats['rate_%'] = (month_stats['converted'] / month_stats['contacted'] * 100).round(1)
st.line_chart(month_stats['rate_%'])

# --- Job breakdown (new) ---
st.subheader("Conversion Rate by Job")
job_stats = filtered.groupby('job').agg(
    contacted=('stage_1_contacted', 'sum'),
    converted=('stage_3_converted', 'sum')
)
job_stats['rate_%'] = (job_stats['converted'] / job_stats['contacted'] * 100).round(1)
st.bar_chart(job_stats['rate_%'])

# --- Education breakdown (new) ---
st.subheader("Conversion Rate by Education")
edu_stats = filtered.groupby('education').agg(
    contacted=('stage_1_contacted', 'sum'),
    converted=('stage_3_converted', 'sum')
)
edu_stats['rate_%'] = (edu_stats['converted'] / edu_stats['contacted'] * 100).round(1)
st.bar_chart(edu_stats['rate_%'])

# --- Raw data viewer (new) ---
with st.expander("View Filtered Raw Data"):
    st.dataframe(filtered)
