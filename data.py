"""Shared data loading & chart helpers used by all pages."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── Colours ──────────────────────────────────────────────────────────────
SKY     = "#10b981"  # Emerald Green
INDIGO  = "#db2777"  # Deep Pink
PINK    = "#ec4899"  # Vibrant Pink
EMERALD = "#059669"  # Deep Green
ORANGE  = "#10b981"  # Emerald Green
PALETTE = [SKY, INDIGO, PINK, EMERALD, ORANGE, "#6ee7b7", "#fbcfe8", "#34d399"]

LAYOUT = dict(
    paper_bgcolor="rgba(255,255,255,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(color="#334155", family="Inter, Segoe UI, sans-serif", size=13),
    title_font=dict(size=15, color="#0f172a", family="Plus Jakarta Sans, Inter, sans-serif"),
    legend=dict(bgcolor="rgba(255,255,255,0)", font=dict(color="#475569")),
    colorway=PALETTE,
    xaxis=dict(gridcolor="rgba(0,0,0,0.06)", linecolor="rgba(0,0,0,0.1)", zerolinecolor="rgba(0,0,0,0.06)"),
    yaxis=dict(gridcolor="rgba(0,0,0,0.06)", linecolor="rgba(0,0,0,0.1)", zerolinecolor="rgba(0,0,0,0.06)"),
    margin=dict(t=52, b=16, l=16, r=16),
    hoverlabel=dict(bgcolor="#ffffff", bordercolor="#cbd5e1", font_color="#1e293b"),
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
