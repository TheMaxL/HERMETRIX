import flet as ft

def main(page: ft.Page):
    page.window_width = 412
    page.window_height = 917

    # sample data
    ad_campaigns = [
    {"name": "Summer Collection", "type": "image"},
    {"name": "Product Demo", "type": "video"},
    {"name": "New Arrivals", "type": "carousel"},
    {"name": "Celebrity Endorsement", "type": "influencer"},
    {"name": "24-Hour Flash Sale", "type": "story"},
    {"name": "Brand Awareness", "type": "image"},
    {"name": "How-To Tutorial", "type": "video"},
    {"name": "Product Variations", "type": "carousel"},
    {"name": "Micro-Influencer Series", "type": "influencer"},
    {"name": "Behind the Scenes", "type": "story"},
    {"name": "Seasonal Promotion", "type": "image"},
    {"name": "Customer Testimonials", "type": "video"},
    {"name": "Color Options", "type": "carousel"},
    {"name": "Industry Expert Takeover", "type": "influencer"},
    {"name": "Limited Time Offer", "type": "story"},
    {"name": "High-Res Product Shots", "type": "image"},
    {"name": "360° View", "type": "video"},
    {"name": "Before/After", "type": "carousel"},
    {"name": "User-Generated Content", "type": "influencer"},
    {"name": "Countdown Deal", "type": "story"},
    {"name": "Lifestyle Imagery", "type": "image"},
    {"name": "Unboxing Video", "type": "video"},
    {"name": "Feature Highlights", "type": "carousel"},
    {"name": "Brand Ambassador", "type": "influencer"},
    {"name": "Poll/Vote", "type": "story"}
]

    ad_types = ["image", "video", "carousel", "influencer", "story"]

    result_search = ft.Container(
        visible=False,
        content=ft.Column([
            ft.Text("Results", weight="bold"),
            ft.Column()
        ])
    )


    # ad type filter
    type_filter = ft.Dropdown(
        options=[ft.dropdown.Option(typ) for typ in ad_types],
        hint_text="Ad type",
        width=150,
        border_radius=10,
        visible=False,
        on_change=lambda e: filter_results(),
    )

    # filter visibility
    def toggle_filter(e):
        type_filter.visible = not type_filter.visible
        filter_button.icon = ft.icons.FILTER_ALT if type_filter.visible else ft.icons.FILTER_ALT_OFF

        if not type_filter.visible:
            result_search.visible = False
        
        page.update()

    filter_button = ft.IconButton(
        icon=ft.icons.FILTER_ALT_OFF,
        on_click=toggle_filter,
        tooltip="Show/Hide Filter",
        icon_color="#FFFFFF",
        bgcolor="#41721E",
    )

    def filter_results():
        search_term = search_field.value.lower() if search_field.value else ""
        selected_type = type_filter.value if type_filter.visible else None

        if search_term or (type_filter.visible and selected_type):
            matching_ads = [
                ad for ad in ad_campaigns
                if (search_term in ad["name"].lower())
                and (selected_type is None or ad["type"] == selected_type)
            ]
            
            display_results(matching_ads)
        else:
            result_search.visible = False
            page.update()

    def display_results(results):
        result_search.content.controls[1].controls.clear()

        if results:
            result_search.visible = True
            for ad in results:
                result_search.content.controls[1].controls.append(
                    ft.ListTile(
                        title=ft.Text(ad["name"], size=16),
                        subtitle=ft.Text(f"Type: {ad['type']}") if type_filter.visible else None,
                        on_click=lambda e, ad=ad: print(ad)
                    )
                )
            result_search.content.controls[1].spacing = 0
            result_search.content.controls[1].tight = False
        else:
            result_search.visible = False
        page.update()


    def change_ad(e):
        if e.control.value:
            filter_results()
        else:
            result_search.visible=False
            page.update()


    def clear_search(e):
        search_field.value = ""
        if type_filter.visible:
            type_filter.value = None
        result_search.visible=False
        page.update()

    # clear button
    close_button = ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.CLOSE,
            on_click=clear_search,
            icon_color="#534341",
            icon_size=22,
        ),
        padding=ft.padding.only(top=20),  # Adjust this value as needed
)

    search_button = ft.IconButton(
        icon=ft.Icons.SEARCH,
        # on_click=lambda e: print("Search clicked"),
        icon_color="#534341",
    )

    search_field = ft.TextField(
        hint_text="Search here...",
        prefix_icon=search_button,
        suffix=close_button,
        on_change=change_ad,
        on_submit=lambda e: print("Search submitted:", e.control.value),
        cursor_color="#41721E",
        cursor_width=2,
        cursor_height=20,
        cursor_radius=4,
        bgcolor="#ebe7e6", 
        border_radius=50, 
        border_color="#ebe7e6",
        text_style=ft.TextStyle(color="#534341"),
        height=45,
        width=300,
        content_padding=ft.padding.only(bottom=50)
        
    )

    # layout of filter
    filter_row = ft.Row(
        [filter_button, type_filter],
        spacing=10,
        visible=True,
    )

    page.add(
        ft.Column([
            ft.Row([search_field]),
            filter_row,
            result_search
        ],
        spacing=20,
        )
    )

    filter_results()

ft.app(main)