import flet as ft
from flet.plotly_chart import PlotlyChart
from chart_today import generate_today_charts
from stats import StatsView
from flet import Page

class ViewSwitcher:
    def __init__(self, page: ft.Page):
        self.page = page

    def show_view(self, view_name: str, current_view=None, campaign_index=0, time_filter="Today"):
        print(f"Switching to view: {view_name}")  # DEBUG
        # Clear current views
        self.page.views.clear()

        # Determine which view to show based on the view_name
        if view_name == "dashboard":
            view = self.create_dashboard_view()
        elif view_name == "stats":
            view = self.create_stats_view(campaign_index, time_filter)
        else:
            # For unknown views, show a placeholder message
            view = self.create_placeholder_view(view_name)

        # Add the new view
        self.page.views.append(ft.View(route=view_name, controls=[view]))
        self.page.go(view_name)

    def create_dashboard_view(self):
        return DashboardView(
        lambda vn, **kwargs: self.show_view(vn, **kwargs),
        "dashboard",  
        self.page
    ).get_view()

    def create_stats_view(self, campaign_index, time_filter):
        """Create and return the stats view."""
        return StatsView(
            lambda vn, **kwargs: self.show_view(vn, **kwargs),
            current_view="stats",
            campaign_index=campaign_index,
            time_filter=time_filter
        ).get_view()

    def create_placeholder_view(self, view_name):
        """Create a placeholder view for unknown pages."""
        return ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Text(f"{view_name.capitalize()} Page (Coming soon)", size=20, weight=ft.FontWeight.BOLD)
        )

class DashboardView:
    def __init__(self, show_view_fn, current_view, page: Page):
        self.show_view = show_view_fn
        self.current_view = current_view
        self.page = page
        
        self.page.title = "Hermetrix Dashboard"
        self.page.theme_mode = ft.ThemeMode.LIGHT

        self.page.window.width = 412
        self.page.window.height = 917
        self.page.window.resizable = False

    def get_view(self):
        title = ft.Container(
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=10),
            content=ft.Text(
                "Dashboard",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.GREY_800,
            )
        )

        # Use Plotly charts directly
        charts = generate_today_charts()
        chart_widgets = []

        for i, fig in enumerate(charts):
            chart_widgets.append(
                ft.GestureDetector(
                    on_tap=self._make_tap_handler(i),
                    content=ft.Container(
                        content=PlotlyChart(fig, expand=True),
                        bgcolor=ft.Colors.WHITE,
                        padding=12,
                        margin=ft.margin.only(bottom=10),
                        border_radius=12,
                        shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.BLACK12),
                        height=300,
                    )
                )
            )

        scrollable_charts = ft.Container(
            expand=True,
            content=ft.Column(
                controls=[title] + chart_widgets,
                spacing=20,
                scroll=ft.ScrollMode.ALWAYS,
            )
        )

        nav_bar = ft.Container(
            content=ft.Row(
                controls=[
                    self._nav_button("Home", "dashboard", self.current_view == "dashboard", ft.Icons.SHOW_CHART),
                    self._nav_button("Search", "search", self.current_view == "search", ft.Icons.SEARCH),
                    self._nav_button("Ads", "ad_campaigns", self.current_view == "ad_campaigns", ft.Icons.CAMPAIGN),
                    self._nav_button("Profile", "user_info", self.current_view == "user_info", ft.Icons.PERSON),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            height=60,
            bgcolor=ft.Colors.GREY_200,
            padding=ft.padding.symmetric(horizontal=10),
        )

        return ft.Column(
            controls=[
                scrollable_charts,
                nav_bar,
            ],
            expand=True,
        )

    def _nav_button(self, label, target, selected, icon):
        color = ft.Colors.GREEN_700 if selected else ft.Colors.GREY_500
        weight = ft.FontWeight.BOLD if selected else ft.FontWeight.NORMAL
        return ft.GestureDetector(
            on_tap=lambda e: self.show_view(target),
            content=ft.Column(
                controls=[
                    ft.Icon(icon, size=24, color=color),
                    ft.Text(label, size=10, color=color, weight=weight),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=4,
            )
        )

    def _make_tap_handler(self, index):
        return lambda e: self.show_view("stats", campaign_index=index)


def main(page: Page):
    view_switcher = ViewSwitcher(page)
    view_switcher.show_view("dashboard")
    
ft.app(target=main)
