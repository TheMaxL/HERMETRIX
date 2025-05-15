import flet as ft
from flet import icons as Icons
from flet.plotly_chart import PlotlyChart
from sampledata import get_campaign_data
from chart_all_time import generate_all_time_charts
from chart_this_year import generate_this_year_charts
from chart_this_week import generate_this_week_charts
from chart_today import generate_today_charts
from datetime import datetime, timedelta
import json

class StatsView:
    def __init__(self, show_view_fn, current_view="stats", campaign_index=0, time_filter="Today"):
        self.show_view = show_view_fn
        self.current_view = current_view
        self.campaign_index = campaign_index
        self.time_filter = time_filter
        self.all_data = self._load_data_with_parsed_dates()
        self._load_data()

    def _load_data_with_parsed_dates(self):
        data = get_campaign_data(with_charts=False)
        for campaign in data:
            metrics_dict = campaign.get("metrics", {})
            if isinstance(metrics_dict, dict):
                for key, metric_list in metrics_dict.items():
                    parsed_metrics = []
                    for metric in metric_list:
                        if isinstance(metric, str):
                            try:
                                metric = json.loads(metric)
                            except json.JSONDecodeError:
                                continue
                        if isinstance(metric, dict) and isinstance(metric.get("date"), str):
                            try:
                                metric["date"] = datetime.fromisoformat(metric["date"])
                            except ValueError:
                                continue
                        parsed_metrics.append(metric)
                    metrics_dict[key] = parsed_metrics
                campaign["metrics"] = metrics_dict
        return data

    def _load_data(self):
        self.data = self.all_data[self.campaign_index]
        metrics_by_filter = self.data.get("metrics", {})
        if isinstance(metrics_by_filter, dict):
            self.metrics = metrics_by_filter.get(self._filter_key(), [])
        else:
            self.metrics = self._filter_metrics(metrics_by_filter)
        self.chart_figure = self._get_chart_figure()

    def _filter_key(self):
        return {
            "All time": "all_time",
            "This year": "this_year",
            "This week": "this_week",
            "Today": "today"
        }.get(self.time_filter, "today")

    def _filter_metrics(self, metrics):
        now = datetime.now()
        if self.time_filter == "All time":
            return metrics
        elif self.time_filter == "This year":
            return [m for m in metrics if m.get("date") and m["date"].year == now.year]
        elif self.time_filter == "This week":
            start_of_week = now - timedelta(days=now.weekday())
            return [m for m in metrics if m.get("date") and m["date"] >= start_of_week]
        elif self.time_filter == "Today":
            return [m for m in metrics if m.get("date") and m["date"].date() == now.date()]
        return metrics

    def _get_chart_figure(self):
        if self.time_filter == "All time":
            return generate_all_time_charts()[self.campaign_index]
        elif self.time_filter == "This year":
            return generate_this_year_charts()[self.campaign_index]
        elif self.time_filter == "This week":
            return generate_this_week_charts()[self.campaign_index]
        elif self.time_filter == "Today":
            return generate_today_charts()[self.campaign_index]
        return None

    def get_view(self):
    # Create the scrollable section for charts and details
        scrollable_charts = ft.Container(
        expand=True,
        content=ft.Column(
            controls=[
                self._top_bar(),
                self._filters(),
                self._chart_section(),
                self._metric_summary(),
                self._details(),
            ],
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS,  
        )
    )

        return ft.Column(
        controls=[
            scrollable_charts,
            self._nav_bar(),
        ],
        expand=True,
    )


    def _top_bar(self):
        return ft.Container(
            padding=10,
            content=ft.Stack(
                controls=[
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.Text("Statistics", size=20, weight=ft.FontWeight.BOLD)
                    ),
                    ft.Container(
                        alignment=ft.alignment.center_left,
                        content=ft.IconButton(
                            icon=Icons.ARROW_BACK,
                            on_click=lambda e: self.show_view("dashboard")
                        )
                    ),
                ]
            )
        )

    def _filters(self):
        return ft.Container(
            padding=10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    self._filter_chip("All time"),
                    self._filter_chip("This year"),
                    self._filter_chip("This week"),
                    self._filter_chip("Today"),
                ]
            )
        )

    def _filter_chip(self, label):
        selected = label == self.time_filter
        return ft.Container(
            content=ft.TextButton(
                text=label,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREEN_700 if selected else ft.Colors.WHITE,
                    color=ft.Colors.WHITE if selected else ft.Colors.GREEN_800,
                    side=ft.BorderSide(1, ft.Colors.GREEN_800),
                    shape=ft.RoundedRectangleBorder(radius=20)
                ),
                on_click=lambda e: self._change_filter(label)
            )
        )

    def _change_filter(self, label):
        self.time_filter = label
        self._load_data()
        self.show_view("stats", campaign_index=self.campaign_index, time_filter=label)
        
    def _chart_section(self):
        return ft.Container(
        padding=10,
        bgcolor=ft.Colors.GREY_100,
        border_radius=10,
        margin=ft.margin.symmetric(horizontal=10),
        content=ft.Column(
            controls=[
                ft.Container(
                    height=200,
                    expand=True,
                    content=PlotlyChart(figure=self.chart_figure)
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.Text("Impressions", color=ft.Colors.BLUE, size=12),
                        ft.Text("Click Throughs", color=ft.Colors.RED, size=12),
                        ft.Text("Purchases", color=ft.Colors.GREEN, size=12),
                    ]
                )
            ]
        )
    )

    def _metric_summary(self):
        impressions = sum(m.get("impressions", 0) for m in self.metrics)
        clicks = sum(m.get("clicks", 0) for m in self.metrics)
        purchases = sum(m.get("purchases", 0) for m in self.metrics)

        return ft.Container(
            padding=10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    self._metric_card("Total Impressions", impressions),
                    self._metric_card("Click Throughs", clicks),
                    self._metric_card("Purchases", purchases),
                ]
            )
        )

    def _metric_card(self, label, value):
        return ft.Container(
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text(label, size=12),
                    ft.Text(str(value), size=16, weight=ft.FontWeight.BOLD),
                ],
                spacing=4
            )
        )

    def _details(self):
        d = self.data
        return ft.Container(
            padding=10,
            content=ft.Column(
                controls=[
                    self._info_row("Campaign Name", d.get("campaign", "N/A")),
                    self._info_row("Hosting Site", d.get("host", "N/A")),
                    self._info_row("Type of Ad", d.get("ad_type", "N/A")),
                    self._info_row("Objective", d.get("objective", "N/A")),
                ],
                spacing=10
            )
        )

    def _info_row(self, label, value):
        return ft.Container(
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            content=ft.Column(
                controls=[
                    ft.Text(label, size=12, color=ft.Colors.GREY_600),
                    ft.Text(value, size=14, weight=ft.FontWeight.BOLD),
                ]
            )
        )

    def _nav_bar(self):
        def nav_btn(label, view, icon, selected):
            color = ft.Colors.GREEN_700 if selected else ft.Colors.GREY_500
            return ft.GestureDetector(
                on_tap=lambda e: self.show_view(view),
                content=ft.Column(
                    controls=[
                        ft.Icon(icon, size=20, color=color),
                        ft.Text(label, size=10, color=color, weight=ft.FontWeight.BOLD if selected else ft.FontWeight.NORMAL),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=4
                )
            )

        return ft.Container(
            height=60,
            bgcolor=ft.Colors.GREY_200,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    nav_btn("Home", "dashboard", Icons.HOME, self.current_view == "dashboard"),
                    nav_btn("Search", "search", Icons.SEARCH, self.current_view == "search"),
                    nav_btn("Ads", "ad_campaigns", Icons.CAMPAIGN, self.current_view == "ad_campaigns"),
                    nav_btn("Profile", "user_info", Icons.PERSON, self.current_view == "user_info"),
                ]
            )
        )
