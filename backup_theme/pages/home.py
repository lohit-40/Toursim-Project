"""Page 1 – Home: Hero banner, key stats, teaser charts."""
import dash
from dash import html, dcc, register_page
import plotly.express as px
import plotly.graph_objects as go
from data import (df, df_inbound, df_gender, df_source,
                  SKY, INDIGO, PINK, EMERALD, ORANGE, LAYOUT, PALETTE)

register_page(__name__, path="/", name="Home", title="Home | India Tourism")

# ── Helper ────────────────────────────────────────────────────────────────
def _stat(icon, value, label, color):
    return html.Div(className="stat-card", children=[
        html.Div(icon,  className="stat-icon"),
        html.Div(value, className="stat-value", style={"color": color}),
        html.Div(label, className="stat-label"),
    ])

# ── Teaser charts ─────────────────────────────────────────────────────────
# 1. Arrivals area sparkline
_fig_arr = px.area(
    df_inbound, x="Year",
    y=["Foreign_Tourist_Arrivals_Million", "NRI_Arrivals_Million",
       "Total_International_Tourist_Arrivals_Million"],
    labels={"value": "Arrivals (Mn)", "variable": ""},
    color_discrete_sequence=[SKY, PINK, EMERALD],
)
_renames = {
    "Foreign_Tourist_Arrivals_Million":             "Foreign Tourists",
    "NRI_Arrivals_Million":                         "NRI",
    "Total_International_Tourist_Arrivals_Million": "Total Intl.",
}
_fig_arr.for_each_trace(lambda t: t.update(name=_renames.get(t.name, t.name)))
_fig_arr.update_traces(opacity=0.75)
_fig_arr.update_layout(**LAYOUT, title="✈️ International Arrivals 2019–2024")

# 2. Top monuments bar
_top5 = df.nlargest(8, "Total 2019")
_fig_mon = px.bar(
    _top5, x="Total 2019", y="Monument",
    orientation="h",
    color="Total 2019", color_continuous_scale="Turbo",
    text="Total 2019",
)
_fig_mon.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
_fig_mon.update_layout(
    **LAYOUT,
    title="🏆 Top 8 Most-Visited Monuments (2019)",
    yaxis_autorange="reversed", coloraxis_showscale=False,
)

# 3. Gender donut
_fig_gen = go.Figure(go.Pie(
    labels=["Male", "Female"],
    values=[56.85, 43.14],
    hole=0.60,
    marker=dict(colors=[SKY, PINK], line=dict(color="#060d1a", width=3)),
    textinfo="label+percent",
    textfont_size=13,
))
_fig_gen.update_layout(
    **LAYOUT,
    title="👤 Tourist Gender Split",
    annotations=[dict(text="56/44", x=0.5, y=0.5, font_size=14, showarrow=False,
                      font_color="#e2e8f0")],
)

# 4. Source countries
_fig_src = px.bar(
    df_source, x="Country", y="Arrivals_2024",
    color="Share_Percent", color_continuous_scale="Blues",
    text="Arrivals_2024",
)
_fig_src.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
_fig_src.update_layout(**LAYOUT, title="🌍 Top Source Countries 2024", coloraxis_showscale=False)


# ── Layout ────────────────────────────────────────────────────────────────
layout = html.Div(className="perspective-container", children=[

    # 3D HERO SECTION
    html.Div(className="hero-3d", children=[
        # Animated background shapes for deep 3D immersion
        html.Div(className="hero-glow-1"),
        html.Div(className="hero-glow-2"),
        html.Div(className="hero-glow-3"),
        
        html.Div(className="hero-content", children=[
            html.Div(className="hero-badge", children=["INTELLIGENCE 2024"]),
            html.H1("India Tourism", className="hero-title-main"),
            html.H1("Reimagined", className="hero-title-sub"),
            html.P(
                "A next-generation immersive exploration of inbound, domestic, "
                "and monument-level tourism data across India. Step into the data.",
                className="hero-subtitle-3d",
            ),
            html.Div(className="hero-cta-wrapper", children=[
                html.A("Enter Monuments", href="/monuments", className="btn-3d-primary"),
                html.A("Global Insights", href="/global", className="btn-3d-secondary"),
            ]),
        ]),
    ]),

    html.Div(className="content-3d-wrapper", children=[
        # STATS STRIP (Floating Cards)
        html.Div(className="stat-grid-3d", children=[
            _stat("✈️",  "20.57 Mn",   "Int'l Arrivals 2024",     SKY),
            _stat("🪪",  "10.62 Mn",   "NRI Arrivals 2024",        INDIGO),
            _stat("🏛️",  "2,948 Mn",   "Domestic Visits 2024",     EMERALD),
            _stat("💰",  "$35 Bn",     "Tourism Receipts 2024",     PINK),
            _stat("🌍",  "USA #1",     "Top Source Country",        ORANGE),
            _stat("📉",  "−72%",       "Drop: 2019 → 2020",         "#f87171"),
            _stat("📈",  "+8.9%",      "India Growth 2024",         EMERALD),
            _stat("🏅",  "178",        "Protected Monuments",       "#a78bfa"),
        ]),

        html.Div(className="divider-3d"),

        # CHARTS SECTION
        html.Div(className="section-header-3d", children=[
            html.Div("DASHBOARD PREVIEW", className="tag-3d"),
            html.H2("Visual Intelligence", className="title-3d"),
        ]),

        # 2-col immersive grid
        html.Div(className="grid-left-heavy-3d", children=[
            html.Div(className="card-3d card-glass", children=[
                html.Div(className="card-glow sky-glow"),
                dcc.Graph(figure=_fig_arr, style={"height": "380px", "background": "transparent"},
                          config={"displayModeBar": False}),
            ]),
            html.Div(className="card-3d card-glass", children=[
                html.Div(className="card-glow indigo-glow"),
                dcc.Graph(figure=_fig_gen, style={"height": "380px", "background": "transparent"},
                          config={"displayModeBar": False}),
            ]),
        ]),

        html.Div(className="grid-right-heavy-3d", children=[
            html.Div(className="card-3d card-glass", children=[
                html.Div(className="card-glow pink-glow"),
                dcc.Graph(figure=_fig_src, style={"height": "380px", "background": "transparent"},
                          config={"displayModeBar": False}),
            ]),
            html.Div(className="card-3d card-glass", children=[
                html.Div(className="card-glow emerald-glow"),
                dcc.Graph(figure=_fig_mon, style={"height": "380px", "background": "transparent"},
                          config={"displayModeBar": False}),
            ]),
        ]),

        html.Div(className="divider-3d"),

        # 3D CTA ROW
        html.Div(className="cta-grid-3d", children=[
            html.A(href="/monuments", className="cta-card-3d link-sky", children=[
                html.Div("🏛️", className="cta-icon"),
                html.H3("Monument Analysis", className="cta-title"),
                html.P("Immersive mapping & protected sites.", className="cta-desc"),
            ]),
            html.A(href="/global", className="cta-card-3d link-indigo", children=[
                html.Div("🌏", className="cta-icon"),
                html.H3("Global Insights", className="cta-title"),
                html.P("Inbound tourism flows & receipts.", className="cta-desc"),
            ]),
            html.A(href="/about", className="cta-card-3d link-pink", children=[
                html.Div("📋", className="cta-icon"),
                html.H3("Data Structure", className="cta-title"),
                html.P("Methodology & source datasets.", className="cta-desc"),
            ]),
        ]),
    ]),
])
