from datetime import datetime, timedelta
import random

def generate_metrics_over_time(start_date, periods, interval):
    data = []
    for i in range(periods):
        date = start_date + i * interval
        impressions = random.randint(8000, 20000)
        clicks = int(impressions * random.uniform(0.05, 0.15))
        purchases = int(clicks * random.uniform(0.10, 0.25))

        data.append({
            "date": date,
            "impressions": impressions,
            "clicks": clicks,
            "purchases": purchases
        })
    return data


def get_campaign_data(with_charts=False):
    campaigns = [
        {
            "campaign": "Hermetrix LED Launch",
            "host": "YouTube",
            "ad_type": "Video",
            "objective": "Brand awareness"
        },
        {
            "campaign": "Holiday Console Push",
            "host": "Facebook",
            "ad_type": "Carousel",
            "objective": "Sales"
        },
        {
            "campaign": "XD Performance Promo",
            "host": "Instagram",
            "ad_type": "Image",
            "objective": "Website visits"
        }
    ]

    today = datetime.now()
    start_of_year = datetime(today.year, 1, 1)
    start_of_week = today - timedelta(days=today.weekday())
    start_of_day = datetime(today.year, today.month, today.day)

    for campaign in campaigns:
        # All time (2024 + 2025, per month)
        metrics_all_time = generate_metrics_over_time(datetime(2024, 1, 1), 24, timedelta(days=30))

        # This year (monthly until now)
        months_elapsed = today.month
        metrics_this_year = generate_metrics_over_time(start_of_year, months_elapsed, timedelta(days=30))

        # This week (daily starting Monday)
        metrics_this_week = generate_metrics_over_time(start_of_week, 7, timedelta(days=1))

        # Today (hourly)
        metrics_today = generate_metrics_over_time(start_of_day, 24, timedelta(hours=1))

        campaign["metrics"] = {
            "all_time": metrics_all_time,
            "this_year": metrics_this_year,
            "this_week": metrics_this_week,
            "today": metrics_today
        }

    if with_charts:
        from charts.charts import generate_charts
        chart_paths = generate_charts()
        for i, path_set in enumerate(chart_paths):
            campaigns[i]["charts"] = path_set

    return campaigns
