"""Page 2 – Monument Analysis: fully interactive explorer."""
from dash import html, dcc, register_page, callback, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from data import (df, LOCATIONS, METRICS,
                  SKY, INDIGO, PINK, EMERALD, ORANGE, LAYOUT, PALETTE)

register_page(__name__, path="/monuments", name="Monuments",
              title="Monuments | India Tourism")

# ── KPI helper ────────────────────────────────────────────────────────────
def _kpi(icon, value, label, cls):
    return html.Div(className=f"kpi {cls}", children=[
        html.Div(icon,  className="kpi-icon"),
        html.Div(value, className=f"kpi-value {cls}-text"),
        html.Div(label, className="kpi-label"),
    ])

# ── Metric dropdown options ────────────────────────────────────────────────
METRIC_OPTIONS = [{"label": f"{'🏠' if 'Dom' in k else '🌐' if 'For' in k else '🔢' if 'Total' in k else '📉'} {k}", "value": v}
                  for k, v in METRICS.items()]

CHART_OPTIONS = [
    {"label": "🏆 Bar – Top 15 Monuments",     "value": "bar"},
    {"label": "📊 Histogram – Distribution",   "value": "hist"},
    {"label": "🧩 Sunburst – Region Tree",      "value": "sunburst"},
    {"label": "🌌 3D Scatter",                  "value": "3d"},
    {"label": "🧮 Correlation Heatmap",         "value": "corr"},
    {"label": "💡 Foreign vs Domestic",         "value": "scatter"},
    {"label": "📉 YoY Change Bar",              "value": "yoy"},
]

# ── Layout ────────────────────────────────────────────────────────────────
layout = html.Div(className="perspective-container", style={"padding": "32px 40px 60px"}, children=[

    # Header
    html.Div(style={"marginBottom": "28px"}, children=[
        html.Div("🏛️ ASI Protected Monuments", className="tag-3d"),
        html.H1("Monument-Level Visitor Analysis", className="title-3d"),
        html.P("Explore visitor data across 178 protected monuments across India. "
               "Use filters to drill down by location, year, and visitor type.",
               className="section-desc", style={"maxWidth": "620px"}),
    ]),

    # Filter bar - FIXED Z-INDEX BUG HERE
    html.Div(className="card-glass", style={
        "display": "flex", "gap": "20px", "alignItems": "flex-end",
        "marginBottom": "30px", "padding": "24px", "borderRadius": "18px",
        "position": "relative", "zIndex": 50  # Forces dropdown to overlay everything below
    }, children=[
        html.Div(style={"flex": "1"}, children=[
            html.Label("Chart Type", className="filter-label"),
            dcc.Dropdown(id="m-chart", options=CHART_OPTIONS, value="bar", clearable=False),
        ]),
        html.Div(style={"flex": "1"}, children=[
            html.Label("Primary Metric", className="filter-label"),
            dcc.Dropdown(id="m-metric", options=METRIC_OPTIONS, value="Total 2019", clearable=False),
        ]),
        html.Div(style={"flex": "2"}, children=[
            html.Label("Filter Locations (multi-select)", className="filter-label"),
            dcc.Dropdown(id="m-loc", options=[{"label": l, "value": l} for l in LOCATIONS],
                         value=LOCATIONS, multi=True, placeholder="All locations…"),
        ]),
    ]),

    # Dynamic KPI row
    html.Div(id="m-kpis", className="kpi-grid", style={"marginBottom": "24px", "position": "relative", "zIndex": 10}),

    # Main chart
    html.Div(className="card-3d card-glass", style={"marginBottom": "24px"}, children=[
        html.Div(className="card-glow sky-glow"),
        dcc.Graph(id="m-chart-graph", style={"height": "55vh", "background": "transparent"},
                  config={"displayModeBar": True, "modeBarButtonsToRemove":
                          ["select2d", "lasso2d", "toImage"]}),
    ]),

    # Comparison cards
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "24px", "marginBottom": "24px"}, children=[
        html.Div(className="card-3d card-glass", children=[
            html.Div(className="card-glow indigo-glow"),
            dcc.Graph(id="m-secondary-1", style={"height": "320px", "background": "transparent"},
                      config={"displayModeBar": False}),
        ]),
        html.Div(className="card-3d card-glass", children=[
            html.Div(className="card-glow pink-glow"),
            dcc.Graph(id="m-secondary-2", style={"height": "320px", "background": "transparent"},
                      config={"displayModeBar": False}),
        ]),
    ]),

    # Data Table
    html.Details(children=[
        html.Summary("📋 Raw Data Table  (click to expand)", style={
            "cursor": "pointer",
            "fontWeight": "700",
            "color": SKY,
            "fontSize": "14px",
            "padding": "4px 0",
            "userSelect": "none",
        }),
        html.Div(style={"marginTop": "14px"}, children=[
            dash_table.DataTable(
                id="m-table",
                page_size=12,
                sort_action="native",
                filter_action="native",
                style_table={"overflowX": "auto"},
                style_header={
                    "backgroundColor": "rgba(12, 74, 110, 0.6)",
                    "color": "white",
                    "fontWeight": "700",
                    "border": "1px solid rgba(255,255,255,0.05)",
                    "fontSize": "12px",
                    "textTransform": "uppercase",
                    "letterSpacing": "0.3px",
                },
                style_cell={
                    "backgroundColor": "rgba(15, 23, 42, 0.4)",
                    "color": "#e2e8f0",
                    "border": "1px solid rgba(255,255,255,0.05)",
                    "textAlign": "center",
                    "fontSize": "13px",
                    "padding": "10px 12px",
                    "maxWidth": "220px",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                },
                style_data_conditional=[{
                    "if": {"row_index": "odd"},
                    "backgroundColor": "rgba(13, 27, 46, 0.5)",
                }],
            ),
        ]),
    ], className="card-3d card-glass", style={"marginBottom": "20px"}),
])


# ── Callback ──────────────────────────────────────────────────────────────
@callback(
    [
        Output("m-chart-graph",  "figure"),
        Output("m-secondary-1",  "figure"),
        Output("m-secondary-2",  "figure"),
        Output("m-table",        "data"),
        Output("m-table",        "columns"),
        Output("m-kpis",         "children"),
    ],
    [
        Input("m-chart",  "value"),
        Input("m-metric", "value"),
        Input("m-loc",    "value"),
    ],
)
def update_monuments(chart_type, metric, sel_locs):
    sl  = sel_locs if sel_locs else LOCATIONS
    dff = df[df["Location"].isin(sl)].copy()

    # ── KPIs ─────────────────────────────────────────────────────────────
    total_2019 = int(dff["Total 2019"].sum())
    total_2020 = int(dff["Total 2020"].sum())
    pct = ((total_2020 - total_2019) / total_2019 * 100) if total_2019 else 0
    top_mon = dff.loc[dff[metric].idxmax(), "Name of the Monument"] \
              if not dff.empty and metric in dff.columns else "N/A"

    kpis = [
        _kpi("🏛️", f"{total_2019:,}",     "Visitors 2019",       "sky"),
        _kpi("📉",  f"{total_2020:,}",     "Visitors 2020",       "indigo"),
        _kpi("📊",  f"{pct:+.1f}%",        "2019 → 2020 Change",  "emerald" if pct >= 0 else "pink"),
        _kpi("🔢",  f"{len(dff)}",          "Monuments Shown",     "orange"),
        _kpi("🏆",  str(top_mon)[:20] + "…" if len(str(top_mon)) > 20 else str(top_mon),
             "Top Monument",  "pink"),
    ]

    # ── Main chart ────────────────────────────────────────────────────────
    L = dict(**LAYOUT)

    if chart_type == "bar":
        top = dff.nlargest(15, metric)
        fig = px.bar(top, x=metric, y="Monument", orientation="h",
                     color=metric, color_continuous_scale="Pinkyl",
                     hover_data={"Location": True, metric: ":,"},
                     title=f"🏆 Top 15 Monuments by {metric}",
                     text=metric)
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(**L, yaxis_autorange="reversed", coloraxis_showscale=False)

    elif chart_type == "hist":
        fig = px.histogram(dff, x=metric, color="Location",
                           marginal="box", nbins=30,
                           title=f"📊 Distribution of {metric}")
        fig.update_layout(**L)

    elif chart_type == "sunburst":
        dfs = dff[dff[metric] > 0].copy()
        fig = px.sunburst(dfs, path=["Location", "Monument"],
                          values=metric,
                          color=metric, color_continuous_scale="Teal",
                          title="🧩 Composition by Region → Monument")
        fig.update_layout(**L, coloraxis_showscale=False)

    elif chart_type == "3d":
        fig = px.scatter_3d(
            dff, x="Domestic-2019-20", y="Foreign-2019-20", z="Domestic-2020-21",
            color="Location", hover_name="Name of the Monument", opacity=0.8,
            title="🌌 3D: Domestic-2019 × Foreign-2019 × Domestic-2020")
        fig.update_layout(**L)

    elif chart_type == "corr":
        cols = ["Domestic-2019-20","Foreign-2019-20","Domestic-2020-21","Foreign-2020-21"]
        corr = dff[cols].corr()
        fig  = px.imshow(corr, text_auto=".2f",
                         color_continuous_scale="Teal",
                         title="🧮 Correlation Heatmap")
        fig.update_layout(**L)

    elif chart_type == "scatter":
        fig = px.scatter(dff, x="Domestic-2019-20", y="Foreign-2019-20",
                         color="Location", hover_name="Name of the Monument",
                         title="💡 Foreign vs Domestic Visitors (2019-20)")
        fig.update_layout(**L)

    else:  # yoy
        fig = px.bar(dff.sort_values("YoY Change"), x="YoY Change", y="Monument",
                     orientation="h", color="YoY Change",
                     color_continuous_scale="Pinkyl",
                     title="📉 Year-on-Year Visitor Change (2020 vs 2019)")
        fig.update_layout(**L, yaxis_autorange="reversed", coloraxis_showscale=False)

    # ── Secondary charts ──────────────────────────────────────────────────
    # A: location comparison bar
    loc_grp = dff.groupby("Location")[["Total 2019","Total 2020"]].sum().reset_index()
    fig2 = go.Figure([
        go.Bar(name="2019", x=loc_grp["Location"], y=loc_grp["Total 2019"],
               marker_color=SKY),
        go.Bar(name="2020", x=loc_grp["Location"], y=loc_grp["Total 2020"],
               marker_color=INDIGO),
    ])
    fig2.update_layout(**L, barmode="group", title="📍 Visitors by Circle (2019 vs 2020)")

    # B: foreign share donut
    dom = int(dff[["Domestic-2019-20","Domestic-2020-21"]].sum().sum())
    frn = int(dff[["Foreign-2019-20","Foreign-2020-21"]].sum().sum())
    fig3 = go.Figure(go.Pie(
        labels=["Domestic", "Foreign"],
        values=[dom, frn],
        hole=0.58,
        marker=dict(colors=[EMERALD, PINK], line=dict(color="#060d1a", width=3)),
        textinfo="label+percent",
    ))
    fig3.update_layout(**L, title="🌐 Domestic vs Foreign Share (All years)",
                       annotations=[dict(text=f"{frn/(dom+frn)*100:.1f}%\nForeign",
                                         x=0.5, y=0.5, showarrow=False,
                                         font_color="#0f172a", font_size=13)])

    # ── Table ─────────────────────────────────────────────────────────────
    show = ["Name of the Monument","Location",
            "Domestic-2019-20","Foreign-2019-20",
            "Domestic-2020-21","Foreign-2020-21",
            "Total 2019","Total 2020","YoY Change"]
    show = [c for c in show if c in dff.columns]
    tbl_cols = [{"name": c,"id": c,"type": "numeric","format":{"specifier":","}}
                if c not in ["Name of the Monument","Location"] else {"name": c,"id": c}
                for c in show]

    return fig, fig2, fig3, dff[show].to_dict("records"), tbl_cols, kpis
