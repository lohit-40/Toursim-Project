"""Shared data loading & chart helpers used by all pages."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── Colours ──────────────────────────────────────────────────────────────
SKY     = "#38bdf8"
INDIGO  = "#818cf8"
PINK    = "#f472b6"
EMERALD = "#34d399"
ORANGE  = "#fb923c"
PALETTE = [SKY, INDIGO, PINK, EMERALD, ORANGE, "#a78bfa", "#fbbf24", "#f87171"]

LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0", family="Inter, Segoe UI, sans-serif", size=13),
    title_font=dict(size=15, color="#e2e8f0", family="Plus Jakarta Sans, Inter, sans-serif"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0")),
    colorway=PALETTE,
    xaxis=dict(gridcolor="#1e293b", linecolor="#334155", zerolinecolor="#1e293b"),
    yaxis=dict(gridcolor="#1e293b", linecolor="#334155", zerolinecolor="#1e293b"),
    margin=dict(t=52, b=16, l=16, r=16),
    hoverlabel=dict(bgcolor="#1e293b", bordercolor="#334155", font_color="#e2e8f0"),
)

# ─── Monument data (xlsx) ─────────────────────────────────────────────────
df = pd.read_excel("india_tourism_with_location.xlsx")
df.columns = df.columns.str.strip()
if "Location" not in df.columns and "Circle" in df.columns:
    df["Location"] = df["Circle"]

df["Monument"] = (
    df["Name of the Monument"].astype(str)
    .str.replace("'", "", regex=False)
    .str.replace('"', "", regex=False)
    .str.strip()
)
df["Total 2019"]  = df["Domestic-2019-20"] + df["Foreign-2019-20"]
df["Total 2020"]  = df["Domestic-2020-21"] + df["Foreign-2020-21"]
df["YoY Change"]  = df["Total 2020"] - df["Total 2019"]
df["YoY Pct"]     = ((df["YoY Change"] / df["Total 2019"].replace(0, pd.NA)) * 100).round(1)

LOCATIONS = sorted(df["Location"].dropna().unique().tolist())
METRICS   = {
    "Domestic 2019-20": "Domestic-2019-20",
    "Foreign  2019-20": "Foreign-2019-20",
    "Domestic 2020-21": "Domestic-2020-21",
    "Foreign  2020-21": "Foreign-2020-21",
    "Total 2019":       "Total 2019",
    "Total 2020":       "Total 2020",
    "YoY Change":       "YoY Change",
}

# ─── CSV files ────────────────────────────────────────────────────────────
df_inbound  = pd.read_csv("dataset/india_inbound_tourism.csv")
df_source   = pd.read_csv("dataset/india_top_source_countries_2024.csv")
df_gender   = pd.read_csv("dataset/india_tourist_gender_distribution.csv")
df_receipts = pd.read_csv("dataset/tourism_receipts_global_vs_india.csv")
df_world    = pd.read_csv("dataset/world_tourism_arrivals_by_region.csv")
df_world_ex = df_world[df_world["Region"] != "World"].copy()
