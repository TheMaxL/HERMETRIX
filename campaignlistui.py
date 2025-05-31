import flet as ft
from flet import *
from collections import defaultdict

ads_data = []

class AdsView:
    def __init__(self, page):
        self.page = page

    def on_arrow_click(self, e, ad_title):
        self.page.go(f"/ad/{ad_title}")

    def build(self):
        title = Container(
            content=Text("Ad Campaigns", size=20, text_align="center", weight="bold"),
            padding=padding.only(bottom=10)
        )

        # Group ads by campaign_name
        grouped_ads = defaultdict(list)
        for ad in ads_data:
            campaign = ad.get("campaign_name", "Untitled Campaign")
            grouped_ads[campaign].append(ad)

        campaign_list_controls = []

        if ads_data:
            for campaign_name, ads in grouped_ads.items():
                # Campaign header
                campaign_header = Container(
                    content=Text(campaign_name, size=18, weight="bold", color="#41721E"),
                    padding=padding.only(top=15, bottom=5)
                )
                campaign_list_controls.append(campaign_header)

                # Ads under this campaign
                for ad in ads:
                    ad_tile = Container(
                        content=ListTile(
                            title=Text(ad["title"], size=16, weight="w600"),
                            subtitle=Column([
                                Text(ad["subtitle"], size=12),
                                Text(ad.get("description", ""), size=10, color="gray")
                            ]),
                            trailing=IconButton(
                                Icons.KEYBOARD_ARROW_RIGHT,
                                on_click=lambda e, ad_title=ad["title"]: self.on_arrow_click(e, ad_title),
                                icon_size=30,
                                icon_color="#41721E"
                            ),
                            bgcolor="#FDF8F7"
                        ),
                        bgcolor="#FDF8F7",
                        border_radius=8,
                        padding=1,
                        data=ad["title"]
                    )
                    campaign_list_controls.append(ad_tile)
        else:
            campaign_list_controls.append(
                Container(
                    content=Text(
                        "No ads yet. Tap the + button to create your first ad.",
                        size=14,
                        color="gray",
                        italic=True,
                        text_align="center"
                    ),
                    alignment=alignment.center,
                    padding=padding.only(top=100),
                )
            )

        campaign_list = Column(
            controls=campaign_list_controls,
            scroll="auto",
            horizontal_alignment="center"
        )

        fab = FloatingActionButton(
            icon=Icons.ADD,
            bgcolor="#41721E",
            on_click=lambda e: self.page.go("/create-ad")  # Update this path as needed
        )

        bottom_nav = NavigationBar(
            selected_index=2,
            bgcolor="#F1EDEC",
            indicator_color="#41721E",
            destinations=[
                NavigationDestination(icon=Icons.SHOW_CHART, label="Home"),
                NavigationDestination(icon=Icons.SEARCH, label="Search"),
                NavigationDestination(icon=Icons.ADD_CIRCLE_OUTLINE, bgcolor="#2F4D19", label="Ads"),
                NavigationDestination(icon=Icons.PERSON, label="Profile"),
            ],
            on_change=lambda e: print(f"Nav: {e.control.selected_index}")
            # on_change=lambda e: self.page.go(["/home", "/search", "/ads", "/profile"][e.control.selected_index])

        )

        return View(
            "/ads",
            [
                Column([title, campaign_list], expand=True, scroll="auto", horizontal_alignment="center"),
                fab,
                bottom_nav
            ],
            vertical_alignment="start",
            horizontal_alignment="center"
        )

    
class AdDetailView:
    def __init__(self, page, ad_title):
        self.page = page
        self.ad_title = ad_title
        self.ad = next((ad for ad in ads_data if ad["title"] == self.ad_title), None)

    def on_edit_click(self, e):
        self.page.go(f"/edit-ad/{self.ad_title}")

    def on_delete_click(self, e):
        global ads_data
        ads_data = [ad for ad in ads_data if ad["title"] != self.ad_title]
        self.page.go("/ads")

    def on_back_click(self, e):
        self.page.go("/ads")

    def build(self):
        if self.ad is None:
            return View("/ads", [Text("Ad not found")])

        bottom_nav = NavigationBar(
            selected_index=2,
            bgcolor="#F1EDEC",
            indicator_color="#41721E",
            destinations=[
                NavigationDestination(icon=Icons.SHOW_CHART, label="Home"),
                NavigationDestination(icon=Icons.SEARCH, label="Search"),
                NavigationDestination(icon=Icons.ADD_CIRCLE_OUTLINE, bgcolor="#2F4D19", label="Ads"),
                NavigationDestination(icon=Icons.PERSON, label="Profile"),
            ],
            on_change=lambda e: print(f"Nav: {e.control.selected_index}")
            # on_change=lambda e: self.page.go(["/home", "/search", "/ads", "/profile"][e.control.selected_index])

        )

        return View(
            f"/ad/{self.ad_title}",
            controls=[
                AppBar(
                    title=Text("Ad Details"),
                    leading=IconButton(
                        icon=Icons.ARROW_BACK,
                        icon_size=24,
                        icon_color="#41721E",
                        on_click=self.on_back_click
                    )
                ),
                Container(
                    content=Text(
                        f"Campaign: {self.ad.get('campaign_name', 'Untitled')}",
                        size=16,
                        color="green",
                        italic=True
                    ),
                    padding=padding.only(bottom=5)
                ),
                Container(
                    content=Text(self.ad["title"], size=22, weight="bold"),
                    padding=padding.only(bottom=5)
                ),
                Text(f"Host: {self.ad['subtitle']}", size=16),
                Text(f"Description: {self.ad.get('description', 'No description provided')}", size=14, italic=True),
                Container(
                    content=Column([                        
                        ElevatedButton(
                            "View Data",
                            width=180,
                            height=50,
                            bgcolor="#E8ECE6",
                            color="#214C00",
                            on_click=lambda e: print(f"View Data")                        
                        ),  
                        ElevatedButton(
                            "Edit Info",
                            width=180,
                            height=50,
                            bgcolor="#32620E",
                            color="white",
                            on_click=self.on_edit_click
                        ),
                        ElevatedButton(
                            "Delete Ad",
                            width=180,
                            height=50,
                            bgcolor="#DE3730",
                            color="white",
                            on_click=self.on_delete_click
                        ),
                    ], spacing=10),
                    padding=padding.only(top=20)
                ),
                bottom_nav
            ],
            vertical_alignment="start",
            horizontal_alignment="center",
            scroll="auto"
        )


class CreateAdView(View):
    def __init__(self, page: Page):
        self.page = page
        self.campaign_name = TextField(label="Ad Campaign Name", width=340)
        self.ad_name = TextField(label="Name of ad", width=340)
        self.description = TextField(label="Description", multiline=True, max_lines=4, width=340)
        self.host = TextField(label="Hosting site", width=340)
        self.duration = TextField(label="Duration (in days)", keyboard_type="number", width=340)
        self.type = Dropdown(
            label="Type of ad",
            width=340,
            options=[
                dropdown.Option("Image"),
                dropdown.Option("Video"),
                dropdown.Option("Carousal"),
                dropdown.Option("Story"),
                dropdown.Option("Influencer")
            ]
        )
        self.message = Text("")

        add_button = FloatingActionButton(
            icon=Icons.CHECK,
            bgcolor="#41721E",
            on_click=self.add_ad
        )

        bottom_nav = NavigationBar(
            selected_index=2,
            bgcolor="#F1EDEC",
            indicator_color="#41721E",
            destinations=[
                NavigationDestination(icon=Icons.SHOW_CHART, label="Home"),
                NavigationDestination(icon=Icons.SEARCH, label="Search"),
                NavigationDestination(icon=Icons.ADD_CIRCLE_OUTLINE, bgcolor="#2F4D19", label="Ads"),
                NavigationDestination(icon=Icons.PERSON, label="Profile"),
            ],
            on_change=lambda e: print(f"Nav: {e.control.selected_index}")
            # on_change=lambda e: self.page.go(["/home", "/search", "/ads", "/profile"][e.control.selected_index])

        )

        form_column = Column([
            Container(
                content=Text("Fill out the following details:", weight="bold"),
                alignment=alignment.center_left,
                padding=padding.only(left=15, bottom=10)
            ),
            self.campaign_name,
            self.ad_name,
            self.description,
            self.host,
            self.duration,
            self.type,
            self.message
        ], spacing=10, horizontal_alignment="center")

        super().__init__(
            route="/create-ad",
            controls=[
                AppBar(
                    title=Text("Add Information"),
                    leading=IconButton(Icons.ARROW_BACK, on_click=lambda e: page.go("/ads"))
                ),
                form_column,
                bottom_nav
            ],
            floating_action_button=add_button,
            vertical_alignment="start",
            horizontal_alignment="center"
        )

    def add_ad(self, e):
        if not all([self.ad_name.value, self.description.value, self.host.value, self.duration.value, self.type.value]):
            self.message.value = "Please complete all fields."
            self.message.color = "red"
            self.page.update()
        else:
            ads_data.append({
                "campaign_name": self.campaign_name.value,
                "title": self.ad_name.value,
                "subtitle": f"{self.host.value} • {self.duration.value} mins • {self.type.value}",
                "description": self.description.value
            })
            self.page.go("/ads")

class EditAdView(View):
    def __init__(self, page: Page, ad_title: str):
        self.page = page
        self.ad_title = ad_title
        self.ad = next((ad for ad in ads_data if ad["title"] == ad_title), None)

        if not self.ad:
            super().__init__(route=f"/edit-ad/{ad_title}", controls=[Text("Ad not found.")])
            return

        # Prefill from ad data
        self.ad_name = TextField(label="Name", value=self.ad["title"], width=340)
        self.description = TextField(label="Name of ad", value=self.ad.get("description", ""), width=340)
        
        host_info = self.ad.get("subtitle", "").split(" • ")
        self.host = TextField(label="Hosting site", value=host_info[0] if len(host_info) > 0 else "", width=340)
        self.duration = TextField(label="Duration", value=host_info[1].replace(" mins", "") if len(host_info) > 1 else "", width=340)
        self.ad_type = Dropdown(
            label="Type of ad",
            width=340,
            options=[
                dropdown.Option("Banner"),
                dropdown.Option("Video"),
                dropdown.Option("Popup")
            ],
            value=host_info[2] if len(host_info) > 2 else None
        )

        self.message = Text("")

        save_button = ElevatedButton(
            text="Save",
            bgcolor="#41721E",
            color="white",
            on_click=self.save_changes
        )

        cancel_button = ElevatedButton(
            text="Cancel",
            bgcolor="white",
            color="#41721E",
            on_click=lambda e: self.page.go(f"/ad/{ad_title}")
        )

        bottom_nav = NavigationBar(
            selected_index=2,
            bgcolor="#F1EDEC",
            indicator_color="#41721E",
            destinations=[
                NavigationDestination(icon=Icons.SHOW_CHART, label="Home"),
                NavigationDestination(icon=Icons.SEARCH, label="Search"),
                NavigationDestination(icon=Icons.ADD_CIRCLE_OUTLINE, bgcolor="#2F4D19", label="Ads"),
                NavigationDestination(icon=Icons.PERSON, label="Profile"),
            ],
            on_change=lambda e: print(f"Nav: {e.control.selected_index}")
            # on_change=lambda e: self.page.go(["/home", "/search", "/ads", "/profile"][e.control.selected_index])

        )

        form_column = Column([
            self.ad_name,
            self.description,
            self.host,
            self.duration,
            self.ad_type,
            self.message,
            Row([cancel_button, save_button], alignment="center", spacing=10)
        ], spacing=10, horizontal_alignment="center")

        super().__init__(
            route=f"/edit-ad/{ad_title}",
            controls=[
                AppBar(
                    title=Text("Edit Information"),
                    leading=IconButton(Icons.ARROW_BACK, on_click=lambda e: page.go(f"/ad/{ad_title}"))
                ),
                form_column,
                bottom_nav
            ],
            vertical_alignment="start",
            horizontal_alignment="center"
        )

    def save_changes(self, e):
        if not all([self.ad_name.value, self.description.value, self.host.value, self.duration.value, self.ad_type.value]):
            self.message.value = "Please fill in all fields."
            self.message.color = "red"
            self.page.update()
            return

        # Update ad
        self.ad["title"] = self.ad_name.value
        self.ad["subtitle"] = f"{self.host.value} • {self.duration.value} mins • {self.ad_type.value}"
        self.ad["description"] = self.description.value

        self.page.go(f"/ad/{self.ad['title']}")

def main(page: Page):
    page.window_width = 412
    page.window_height = 917

    def route_change(route):
        page.views.clear()
        if page.route == "/ads":
            page.views.append(AdsView(page).build())
        elif page.route == "/create-ad":
            page.views.append(CreateAdView(page))
        elif page.route.startswith("/ad/"):  
            ad_title = page.route.split("/")[-1] 
            page.views.append(AdDetailView(page, ad_title).build())
        elif page.route.startswith("/edit-ad/"):
            ad_title = page.route.split("/")[-1]
            page.views.append(EditAdView(page, ad_title))
        else:
            page.views.append(AdsView(page).build())
        page.update()

    page.on_route_change = route_change
    page.go(page.route or "/")


if __name__ == "__main__":
    ft.app(target=main)