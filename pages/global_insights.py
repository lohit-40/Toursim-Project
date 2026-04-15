"""Page 3 – Global Insights: India's position in world tourism."""
from dash import html, dcc, register_page
import plotly.express as px
import plotly.graph_objects as go
from data import (df_inbound, df_source, df_gender, df_receipts, df_world_ex,
                  SKY, INDIGO, PINK, EMERALD, ORANGE, LAYOUT, PALETTE)

register_page(__name__, path="/global", name="Global Insights",
              title="Global | India Tourism")

# ── Charts ────────────────────────────────────────────────────────────────

# 1. Arrivals area
fig_arr = px.area(
    df_inbound, x="Year",
    y=["Foreign_Tourist_Arrivals_Million",
       "NRI_Arrivals_Million",
       "Total_International_Tourist_Arrivals_Million"],
    labels={"value": "Arrivals (Million)", "variable": "Type"},
    color_discrete_sequence=[SKY, PINK, EMERALD],
    title="✈️ India International Tourism Trend (2019–2024)",
)
_renames = {
    "Foreign_Tourist_Arrivals_Million": "Foreign Tourists",
    "NRI_Arrivals_Million": "NRI",
    "Total_International_Tourist_Arrivals_Million": "Total",
}
fig_arr.for_each_trace(lambda t: t.update(name=_renames.get(t.name, t.name)))
fig_arr.update_traces(opacity=0.72)
fig_arr.update_layout(**LAYOUT)

# 2. Source countries horizontal bar (ranked)
fig_src = px.bar(
    df_source.sort_values("Arrivals_2024"),
    x="Arrivals_2024", y="Country", orientation="h",
    color="Share_Percent", color_continuous_scale="Teal",
    text="Arrivals_2024",
    title="🌍 Top 5 Source Countries (2024 Arrivals)",
)
fig_src.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
fig_src.update_layout(**LAYOUT, coloraxis_showscale=False)

# 3. Gender donut
fig_gen = go.Figure(go.Pie(
    labels=["Male", "Female"],
    values=[56.85, 43.14],
    hole=0.62,
    marker=dict(colors=[INDIGO, PINK], line=dict(color="#060d1a", width=3)),
    textinfo="label+percent",
    textfont_size=14,
    pull=[0.04, 0],
))
fig_gen.update_layout(
    **LAYOUT,
    title="👤 Foreign Tourist Gender Distribution",
    annotations=[dict(text="Gender", x=0.5, y=0.5, font_size=14,
                      showarrow=False, font_color="#0f172a")],
)

# 4. Receipts grouped bar
fig_rec = go.Figure([
    go.Bar(name="Global (USD Bn)",
           x=df_receipts["Year"].astype(str),
           y=df_receipts["Global_Tourism_Receipts_USD_Billion"],
           marker_color=INDIGO,
           text=df_receipts["Global_Tourism_Receipts_USD_Billion"].map("{:.0f}B".format)),
    go.Bar(name="India (USD Bn)",
           x=df_receipts["Year"].astype(str),
           y=df_receipts["India_Tourism_Receipts_USD_Billion"],
           marker_color=EMERALD,
           text=df_receipts["India_Tourism_Receipts_USD_Billion"].map("{:.2f}B".format)),
])
fig_rec.update_traces(textposition="outside")
fig_rec.update_layout(**LAYOUT, barmode="group",
                       title="💰 Tourism Receipts: Global vs India (USD Billion)")

# 5. World arrivals donut
fig_world = px.pie(
    df_world_ex, names="Region", values="Arrivals_2024_Million",
    color_discrete_sequence=PALETTE,
    hole=0.45,
    title="🌐 World Tourist Arrivals by Region (2024, Million)",
)
fig_world.update_traces(textinfo="label+percent", pull=[0.04,0,0,0,0])
fig_world.update_layout(**LAYOUT)

# 6. Regional growth horizontal bar
fig_growth = px.bar(
    df_world_ex.sort_values("Growth_2024_vs_2023_Percent"),
    x="Growth_2024_vs_2023_Percent", y="Region",
    orientation="h",
    color="Growth_2024_vs_2023_Percent",
    color_continuous_scale="Teal",
    text="Growth_2024_vs_2023_Percent",
    title="🚀 Tourism Growth by Region: 2024 vs 2023 (%)",
)
fig_growth.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig_growth.update_layout(**LAYOUT, coloraxis_showscale=False)

# 7. Regional share bar
fig_share = px.bar(
    df_world_ex.sort_values("Share_Percent", ascending=False),
    x="Region", y="Share_Percent",
    color="Share_Percent", color_continuous_scale="Pinkyl",
    text="Share_Percent",
    title="📊 Regional Market Share of World Tourism 2024 (%)",
)
fig_share.update_traces(texttemplate="%{text:.1f}%", textposition="outside", cliponaxis=False)
fig_share.update_layout(**LAYOUT, coloraxis_showscale=False)
fig_share.update_yaxes(range=[0, 62])


# ── Layout ────────────────────────────────────────────────────────────────
def _kpi(icon, val, label, cls):
    return html.Div(className=f"kpi {cls}", children=[
        html.Div(icon, className="kpi-icon"),
        html.Div(val,  className=f"kpi-value {cls}-text"),
        html.Div(label, className="kpi-label"),
    ])

layout = html.Div(className="perspective-container", style={"padding": "32px 40px 60px"}, children=[

    # Header
    html.Div(style={"marginBottom": "28px"}, children=[
        html.Div("🌏 International Tourism Data", className="tag-3d"),
        html.H1("Global & National Tourism Insights", className="title-3d"),
        html.P("India's position in global tourism: arrivals, receipts, source markets, "
               "gender breakdown, and regional comparisons.",
               className="section-desc", style={"maxWidth": "640px"}),
    ]),

    # KPI strip
    html.Div(className="kpi-grid", style={"marginBottom": "28px"}, children=[
        _kpi("🌍", "1,465 Mn",   "World Arrivals 2024",     "sky"),
        _kpi("📈", "+12.2%",     "Global Growth 2024",      "emerald"),
        _kpi("🇮🇳",  "20.57 Mn",  "India Arrivals 2024",     "indigo"),
        _kpi("💰", "$1,731 Bn",  "Global Receipts 2024",    "orange"),
        _kpi("💵", "$35 Bn",     "India Receipts 2024",     "pink"),
    ]),

    html.Div(className="divider-3d"),

    # Row A: Arrivals trend (wide) + Source countries
    html.Div(style={"marginBottom": "24px"}, children=[
        html.Div("📈 India Arrivals & Source Markets", className="tag-3d",
                 style={"marginBottom": "16px", "marginTop": "20px"}),
        html.Div(className="grid-left-heavy-3d", children=[
            html.Div(className="card-3d card-glass", children=[
                html.Div(className="card-glow sky-glow"),
                dcc.Graph(figure=fig_arr, style={"height": "380px", "background": "transparent"},
                          config={"displayModeBar": False}),
            ]),
            html.Div(className="card-3d card-glass", children=[
                html.Div(className="card-glow indigo-glow"),
                dcc.Graph(figure=fig_src, style={"height": "380px", "background": "transparent"},
                          config={"displayModeBar": False}),
            ]),
        ]),
    ]),

    # Row B: Gender + Receipts
    html.Div(style={"marginBottom": "24px"}, children=[
        html.Div("💰 Receipts & Demographics", className="tag-3d",
                 style={"marginBottom": "16px", "marginTop": "20px"}),
        html.Div(className="grid-right-heavy-3d", children=[
            html.Div(className="card-3d card-glass", children=[
                html.Div(className="card-glow pink-glow"),
                dcc.Graph(figure=fig_gen, style={"height": "360px", "background": "transparent"},
                          config={"displayModeBar": False}),
            ]),
            html.Div(className="card-3d card-glass", children=[
                html.Div(className="card-glow emerald-glow"),
                dcc.Graph(figure=fig_rec, style={"height": "360px", "background": "transparent"},
                          config={"displayModeBar": False}),
            ]),
        ]),
    ]),

    # Row C: World arrivals + Growth
    html.Div(style={"marginBottom": "24px"}, children=[
        html.Div("🌐 World Tourism Landscape 2024", className="tag-3d",
                 style={"marginBottom": "16px", "marginTop": "20px"}),
        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "24px"}, children=[
            html.Div(className="card-3d card-glass", children=[
                html.Div(className="card-glow indigo-glow"),
                dcc.Graph(figure=fig_world, style={"height": "370px", "background": "transparent"},
                          config={"displayModeBar": False}),
            ]),
            html.Div(className="card-3d card-glass", children=[
                html.Div(className="card-glow emerald-glow"),
                dcc.Graph(figure=fig_growth, style={"height": "370px", "background": "transparent"},
                          config={"displayModeBar": False}),
            ]),
        ]),
    ]),

    # Row D: Share bar (full-width)
    html.Div(className="card-3d card-glass", children=[
        html.Div(className="card-glow sky-glow", style={"left": "50%"}),
        dcc.Graph(figure=fig_share, style={"height": "340px", "background": "transparent"},
                  config={"displayModeBar": False}),
    ]),

    html.Div(className="divider-3d"),

    # Summary callout
    html.Div(className="card-3d card-glass", style={
        "textAlign": "center",
        "padding": "40px",
    }, children=[
        html.Div("ℹ️", style={"fontSize": "48px", "marginBottom": "20px", "textShadow": "0 10px 20px rgba(0,0,0,0.5)"}),
        html.H3("India's Share in World Tourism", style={
            "color": "#0f172a", "fontWeight": "800", "marginBottom": "12px", "fontSize": "24px"
        }),
        html.P(
            "India represents 1.4% of all world tourist arrivals (20.57 Mn of 1,465 Mn in 2024). "
            "Asia-Pacific as a whole grew the fastest at +33.7%, led by post-COVID recovery. "
            "India's own tourism receipts grew to $35 Bn, reflecting strong domestic and inbound demand.",
            style={"color": "#475569", "lineHeight": "1.8", "maxWidth": "700px", "margin": "0 auto", "fontSize": "15px"},
        ),
    ]),
])
