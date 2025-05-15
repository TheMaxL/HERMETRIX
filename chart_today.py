import plotly.graph_objects as go
from sampledata import get_campaign_data

def generate_today_charts():
    data = get_campaign_data()
    plotly_figures = []

    for entry in data:
        metrics = entry["metrics"]["today"]
        dates = [m["date"].strftime("%H:%M") for m in metrics]  # hourly format
        impressions = [m["impressions"] for m in metrics]
        clicks = [m["clicks"] for m in metrics]
        purchases = [m["purchases"] for m in metrics]

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=dates, y=impressions, mode='lines+markers', name='Impressions', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=dates, y=clicks, mode='lines+markers', name='Clicks', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=dates, y=purchases, mode='lines+markers', name='Purchases', line=dict(color='green')))

        fig.update_layout(
            title=f"{entry['campaign']} - Today (Hourly)",
            xaxis_title="Hour",
            yaxis_title="Count",
            legend_title="Metrics",
            xaxis=dict(tickangle=45),
            margin=dict(l=40, r=20, t=50, b=60),
            height=300,
            width=500,
            autosize=True,
        )

        plotly_figures.append(fig)

    return plotly_figures
