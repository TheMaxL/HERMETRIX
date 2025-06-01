import flet as ft
from campaignlistui import AdsView, CreateAdView, AdDetailView, EditAdView
from profileui import ProfileView

def main(page: ft.Page):
    page.window_width = 412
    page.window_height = 917
    page.bgcolor = "#FFFFFF"

    def get_nav_bar(selected_index=0):
        def nav_icon(icon, index):
            return ft.Icon(
                icon,
                color="white" if index == selected_index else "#2F4D19"
            )

        destinations = [
            ft.NavigationDestination(icon=nav_icon(ft.icons.SHOW_CHART, 0), label="Home"),
            ft.NavigationDestination(icon=nav_icon(ft.icons.SEARCH, 1), label="Search"),
            ft.NavigationDestination(icon=nav_icon(ft.icons.ADD_CIRCLE_OUTLINE, 2), label="Ads"),
            ft.NavigationDestination(icon=nav_icon(ft.icons.PERSON, 3), label="Profile"),
        ]

        return ft.NavigationBar(
            selected_index=selected_index,
            bgcolor="#F1EDEC",
            indicator_color="#41721E",
            destinations=destinations,
            on_change=lambda e: page.go(["/", "/search", "/ads", "/profile"][e.control.selected_index]),
        )

    page.views.append(ft.View("/", []))

    def route_change(route):
        index_map = {
            "/": 0,
            "/search": 1,
            "/ads": 2,
            "/profile": 3
        }

        current_index = index_map.get(page.route, 0)

        if page.route == "/":
            content = [ft.Text("Home View"), get_nav_bar(current_index)]

        elif page.route == "/search":
            content = [ft.Text("Search View"), get_nav_bar(current_index)]

        elif page.route == "/ads":
            ads_view = AdsView(page).build()
            ads_view.controls.append(get_nav_bar(current_index))
            content = ads_view.controls

        elif page.route == "/create-ad":
            page.views.append(CreateAdView(page))
            page.update()
            return

        elif page.route.startswith("/ad/"):
            ad_title = page.route.split("/ad/")[1]
            ad_detail = AdDetailView(page, ad_title).build()
            page.views.append(ad_detail)
            page.update()
            return

        elif page.route.startswith("/edit-ad/"):
            ad_title = page.route.split("/edit-ad/")[1]
            page.views.append(EditAdView(page, ad_title))
            page.update()
            return

        elif page.route == "/profile":
            user_data = {"name": "Business", "email": "business@example.com"}
            profile_view = ProfileView(page, user_data).build()
            content = profile_view.controls + [get_nav_bar(current_index)]

        else:
            content = [ft.Text(f"404: {page.route} not found"), get_nav_bar()]


        new_view = ft.View(page.route, content)
        page.views.append(new_view)
        if len(page.views) > 1:
            page.views.pop(0) 
        page.update()

    page.on_route_change = route_change
    page.go(page.route or "/")

ft.app(target=main)
