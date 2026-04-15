"""Page 4 – About: dataset descriptions, project info."""
from dash import html, register_page
from data import SKY, INDIGO, PINK, EMERALD, ORANGE

register_page(__name__, path="/about", name="About",
              title="About | India Tourism")

DATASETS = [
    {
        "icon": "📊",
        "name": "india_tourism_with_location.xlsx",
        "label": "Main Monument Dataset",
        "desc": "178 ASI-protected monuments with domestic & foreign visitor counts "
                "for FY 2019-20 and 2020-21, grouped by Circle (region).",
        "cols": "Name of the Monument, Circle/Location, Domestic-2019-20, Foreign-2019-20, "
                "Domestic-2020-21, Foreign-2020-21",
        "color": SKY,
    },
    {
        "icon": "✈️",
        "name": "india_inbound_tourism.csv",
        "label": "Inbound Tourism 2019–2024",
        "desc": "Year-wise breakdown of foreign tourist arrivals, NRI arrivals, and "
                "total international tourist arrivals from 2019 to 2024.",
        "cols": "Year, Foreign_Tourist_Arrivals_Million, NRI_Arrivals_Million, Total",
        "color": EMERALD,
    },
    {
        "icon": "🌍",
        "name": "india_top_source_countries_2024.csv",
        "label": "Top Source Countries 2024",
        "desc": "Top 5 countries sending the most tourists to India in 2024 "
                "with their arrival counts and percentage share.",
        "cols": "Rank, Country, Arrivals_2024, Share_Percent",
        "color": INDIGO,
    },
    {
        "icon": "👤",
        "name": "india_tourist_gender_distribution.csv",
        "label": "Gender Distribution",
        "desc": "Male vs female share percentage of foreign tourists visiting India, "
                "based on arrival surveys.",
        "cols": "Category, Share_Percent",
        "color": PINK,
    },
    {
        "icon": "💰",
        "name": "tourism_receipts_global_vs_india.csv",
        "label": "Tourism Receipts 2023–2024",
        "desc": "Comparison of global tourism receipts (USD Billion) vs India's tourism "
                "receipts for 2023 and 2024.",
        "cols": "Year, Global_Tourism_Receipts_USD_Billion, India_Tourism_Receipts_USD_Billion",
        "color": ORANGE,
    },
    {
        "icon": "🌐",
        "name": "world_tourism_arrivals_by_region.csv",
        "label": "World Arrivals by Region 2024",
        "desc": "UNWTO data on international tourist arrivals by world region in 2024, "
                "including market share and year-on-year growth.",
        "cols": "Region, Arrivals_2024_Million, Share_Percent, Growth_2024_vs_2023_Percent",
        "color": "#a78bfa",
    },
    {
        "icon": "🏛️",
        "name": "india_domestic_tourism_highlights.csv",
        "label": "Domestic Tourism Highlights 2024",
        "desc": "High-level domestic tourism indicators for India in 2024: total domestic "
                "visits, top domestic states by tourist volume.",
        "cols": "Indicator, Value_2024",
        "color": EMERALD,
    },
]

TECH_STACK = [
    ("🐍", "Python 3.x",    "Core programming language"),
    ("📊", "Plotly Dash",    "Interactive web dashboard framework"),
    ("📈", "Plotly Express", "Chart generation library"),
    ("🐼", "Pandas",         "Data loading, cleaning, and aggregation"),
    ("📦", "OpenPyXL",       "Reading Excel (.xlsx) files"),
    ("🌐", "Dash Pages",     "Multi-page routing"),
]


def _row(k, v):
    return html.Div(style={
        "display": "flex", "justifyContent": "space-between", "alignItems": "center",
        "padding": "10px 0",
        "borderBottom": "1px solid rgba(255,255,255,0.05)",
    }, children=[
        html.Span(k, style={"color": "#64748b", "fontSize": "13px"}),
        html.Span(v, style={"color": "#e2e8f0", "fontWeight": "600", "fontSize": "13px"}),
    ])


layout = html.Div(className="perspective-container", style={"padding": "32px 40px 60px"}, children=[

    # Hero
    html.Div(style={"textAlign": "center", "marginBottom": "60px", "marginTop": "20px"}, children=[
        html.Div("📋", style={"fontSize": "64px", "marginBottom": "20px", "textShadow": "0 10px 20px rgba(0,0,0,0.5)"}),
        html.Div("Project Information", className="hero-badge",
                 style={"margin": "0 auto 16px", "display": "inline-flex"}),
        html.H1("About This Dashboard", className="hero-title-main"),
        html.P(
            "A final-year project showcasing India's tourism landscape using interactive "
            "data visualization built with Python Dash.",
            className="hero-subtitle-3d", style={"maxWidth": "560px", "margin": "16px auto 0"},
        ),
    ]),

    # Project summary card
    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "24px", "marginBottom": "60px"}, children=[
        html.Div(className="card-3d card-glass", children=[
            html.Div(className="card-glow sky-glow"),
            html.H3("📌 Project Overview", style={
                "color": "#0f172a", "fontWeight": "800", "marginBottom": "20px", "fontSize": "20px"
            }),
            _row("Project Type",  "Final Year Data Analytics Project"),
            _row("Dashboard",     "Multi-Page Plotly Dash Web App"),
            _row("Data Period",   "2019 – 2024"),
            _row("Total Datasets","7 files (1 XLSX + 6 CSV)"),
            _row("Monuments",     "178 ASI-protected sites"),
            _row("Charts",        "12+ interactive visualizations"),
            _row("Pages",         "Home · Monuments · Global · About"),
        ]),
        html.Div(className="card-3d card-glass", children=[
            html.Div(className="card-glow indigo-glow"),
            html.H3("🛠️ Technology Stack", style={
                "color": "#0f172a", "fontWeight": "800", "marginBottom": "20px", "fontSize": "20px"
            }),
            *[html.Div(style={
                "display": "flex", "alignItems": "center", "gap": "16px",
                "padding": "12px 0", "borderBottom": "1px solid rgba(0,0,0,0.05)",
            }, children=[
                html.Span(t[0], style={"fontSize": "28px", "filter": "drop-shadow(0 4px 6px rgba(0,0,0,0.1))"}),
                html.Div([
                    html.Div(t[1], style={"color": "#1e293b", "fontWeight": "700", "fontSize": "15px"}),
                    html.Div(t[2], style={"color": "#475569", "fontSize": "13px"}),
                ]),
            ]) for t in TECH_STACK],
        ]),
    ]),

    # Datasets section
    html.Div(style={"marginBottom": "24px"}, children=[
        html.Div("📂 Data Sources", className="tag-3d"),
        html.H2("Datasets Used", className="title-3d", style={"marginBottom": "12px"}),
        html.P("All data sourced from India's Ministry of Tourism and UNWTO 2024 reports.",
               className="section-desc", style={"marginBottom": "32px"}),
    ]),

    html.Div(className="dataset-grid", style={"marginBottom": "60px", "gap": "24px"}, children=[
        html.Div(className="card-3d card-glass", style={"borderLeftWidth": "4px",
                 "borderLeftColor": d["color"],
                 "borderLeftStyle": "solid", "padding": "24px"}, children=[
            html.Div(style={"display": "flex", "alignItems": "center", "gap": "10px",
                            "marginBottom": "12px"}, children=[
                html.Span(d["icon"], style={"fontSize": "24px"}),
                html.Div([
                    html.Div(d["label"], className="dataset-name", style={"color": d["color"], "fontSize": "15px"}),
                    html.Div(d["name"], style={"fontSize": "12px", "color": "#64748b",
                                               "fontFamily": "monospace", "marginTop": "4px"}),
                ]),
            ]),
            html.P(d["desc"], className="dataset-desc", style={"color": "#94a3b8"}),
            html.Div(style={"marginTop": "14px", "paddingTop": "14px",
                            "borderTop": "1px solid rgba(255,255,255,0.08)"}, children=[
                html.Span("Columns: ", style={"fontSize": "12px", "color": "#64748b",
                                               "fontWeight": "700"}),
                html.Span(d["cols"], style={"fontSize": "12px", "color": "#64748b",
                                             "fontFamily": "monospace"}),
            ]),
        ])
        for d in DATASETS
    ]),

    html.Div(className="divider-3d"),

    # Key findings
    html.Div(style={"marginBottom": "60px"}, children=[
        html.Div("🔍 Key Findings", className="tag-3d"),
        html.H2("What the Data Reveals", className="title-3d",
                style={"marginBottom": "32px"}),
        html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(280px, 1fr))", "gap": "24px"}, children=[
            html.Div(className="card-3d card-glass", style={"borderColor": f"rgba(56,189,248,0.3)"}, children=[
                html.Div("📉", style={"fontSize": "40px", "marginBottom": "16px", "textShadow": "0 10px 20px rgba(0,0,0,0.5)"}),
                html.H4("COVID-19 Impact", style={"color": "#0f172a", "fontWeight": "800", "marginBottom": "12px", "fontSize": "18px"}),
                html.P("International arrivals dropped from 17.91 Mn (2019) to 6.33 Mn (2020) — "
                       "a 64.6% collapse. Monument visits fell sharply across all circles.",
                       style={"color": "#475569", "fontSize": "14px", "lineHeight": "1.7"}),
            ]),
            html.Div(className="card-3d card-glass", style={"borderColor": f"rgba(52,211,153,0.3)"}, children=[
                html.Div("📈", style={"fontSize": "40px", "marginBottom": "16px", "textShadow": "0 10px 20px rgba(0,0,0,0.5)"}),
                html.H4("Strong Recovery", style={"color": "#0f172a", "fontWeight": "800", "marginBottom": "12px", "fontSize": "18px"}),
                html.P("By 2024, international arrivals rebounded to 20.57 Mn — surpassing "
                       "pre-pandemic 2019 levels. Asia-Pacific led with +33.7% growth.",
                       style={"color": "#475569", "fontSize": "14px", "lineHeight": "1.7"}),
            ]),
            html.Div(className="card-3d card-glass", style={"borderColor": f"rgba(244,114,182,0.3)"}, children=[
                html.Div("🇺🇸", style={"fontSize": "40px", "marginBottom": "16px", "textShadow": "0 10px 20px rgba(0,0,0,0.5)"}),
                html.H4("USA Top Source", style={"color": "#0f172a", "fontWeight": "800", "marginBottom": "12px", "fontSize": "18px"}),
                html.P("The United States remained the #1 source of foreign tourists to India in 2024 "
                       "with 1.8 Mn arrivals — an 18.1% share of all inbound tourists.",
                       style={"color": "#475569", "fontSize": "14px", "lineHeight": "1.7"}),
            ]),
        ]),
    ]),

    # Footer
    html.Div(className="card-3d card-glass", style={
        "textAlign": "center",
        "padding": "40px",
    }, children=[
        html.Div("🇮🇳", style={"fontSize": "48px", "marginBottom": "16px", "textShadow": "0 10px 20px rgba(0,0,0,0.5)"}),
        html.P("India Tourism Analytics Dashboard", style={
            "fontWeight": "800", "fontSize": "18px", "color": "#fff", "marginBottom": "8px"
        }),
        html.P("Built with Python & Plotly Dash  •  Data: Ministry of Tourism India, UNWTO 2024, ASI",
               style={"color": "#94a3b8", "fontSize": "14px"}),
    ]),
])
