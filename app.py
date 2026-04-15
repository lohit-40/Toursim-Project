"""
India Tourism Analytics – Multi-Page Dash App
Entry point: registers all pages and renders the shared navbar.
"""
from dash import Dash, html, dcc, page_container, page_registry, Input, Output, callback
import dash

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap"
    ],
    suppress_callback_exceptions=True,
)
app.title = "India Tourism Analytics 🇮🇳"

# ─── Custom index string (meta tags + dark scrollbar) ────────────────────
app.index_string = """<!DOCTYPE html>
<html lang="en">
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <meta name="description" content="India Tourism Intelligence Dashboard – Interactive Analytics 2019-2024">
    <meta name="theme-color" content="#060d1a">
</head>
<body>
    {%app_entry%}
    <footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>"""

# ─── Navbar ───────────────────────────────────────────────────────────────
NAV_ITEMS = [
    {"href": "/",        "label": "🏠 Home"},
    {"href": "/monuments","label": "🏛️ Monuments"},
    {"href": "/global",  "label": "🌏 Global"},
    {"href": "/about",   "label": "📋 About"},
]

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),

    # Navbar
    html.Nav(className="navbar", children=[
        html.A(["🇮🇳 ", html.Span("Tourism Analytics")],
               href="/", className="navbar-brand"),

        html.Div(className="nav-links", children=[
            html.A(item["label"], href=item["href"],
                   className="nav-link", id=f"nav-{i}")
            for i, item in enumerate(NAV_ITEMS)
        ]),
    ]),

    # Page content
    html.Div(page_container, className="page-wrapper"),

], className="app-main-wrapper")


# ─── Active-link highlighter ──────────────────────────────────────────────
@callback(
    [Output(f"nav-{i}", "className") for i in range(len(NAV_ITEMS))],
    Input("url", "pathname"),
)
def set_active(pathname):
    classes = []
    for item in NAV_ITEMS:
        if pathname == item["href"]:
            classes.append("nav-link active")
        else:
            classes.append("nav-link")
    return classes


if __name__ == "__main__":
    app.run(port=8060, debug=True)