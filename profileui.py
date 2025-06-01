import flet as ft
from flet import *

class ProfileView(ft.UserControl):
    def __init__(self, page, user_data):
        super().__init__()
        self.page = page
        self.user_data = user_data
        self.avatar = None
        self.name_text = None

    def _close_dialog(self):
        self.page.dialog.open = False
        self.page.update()

    def build(self):

        # Avatar with initial
        self.avatar = CircleAvatar(
            content=Text(self.user_data['name'][0].upper(), color="white", size=30),
            bgcolor="#2F4D19",
            radius=40,
        )

        self.name_text = Text(self.user_data['name'], size=22, weight=FontWeight.BOLD)

        def open_edit_profile_dialog(e):
            # Dialog for editing name and changing photo
            def save_profile(e):
                new_name = name_field.value.strip()
                if new_name:
                    self.user_data['name'] = new_name
                    self.name_text.value = new_name
                    self.avatar.content.value = new_name[0].upper()
                    self.avatar.content.update()
                    self.name_text.value = new_name
                    self.name_text.update()
                    self.page.dialog.open = False
                    self.page.update()

            def change_photo(e):
                self.page.update()
                # Placeholder for photo change logic

            name_field = TextField(label="Name", value=self.user_data['name'], max_lines=1, height=60)
            change_photo_btn = ElevatedButton("Change Photo", on_click=change_photo)
            save_btn = ElevatedButton("Save", on_click=save_profile, bgcolor="#2F4D19", color="white")
            cancel_btn = OutlinedButton("Cancel", on_click=lambda e: self._close_dialog())

            content_container = ft.Container(
                content=ft.Column(
                    [
                        self.avatar,
                        change_photo_btn,
                        name_field,
                    ],
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                height=180,        
                width=250,
                alignment=ft.alignment.center,
            )

            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Edit Profile"),
                content=content_container, 
                actions=[cancel_btn, save_btn],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            self.page.dialog.open = True
            self.page.update()

        def open_edit_email_dialog(e):
            def save_email(e):
                new_email = email_field.value.strip()
                if new_email and "@" in new_email:
                    self.user_data['email'] = new_email
                    email_tile.subtitle.value = new_email
                    self.page.dialog.open = False
                    self.page.update()

            email_field = TextField(label="Email", value=self.user_data['email'])
            save_btn = ElevatedButton("Save", on_click=save_email, bgcolor="#2F4D19", color="white")
            cancel_btn = OutlinedButton("Cancel", on_click=lambda e: self._close_dialog())

            self.page.dialog = AlertDialog(
                title=Text("Edit Email"),
                content=email_field,
                actions=[cancel_btn, save_btn],
                actions_alignment=MainAxisAlignment.END,
            )
            self.page.dialog.open = True
            self.page.update()

        def open_change_password_dialog(e):
            def save_password(e):
                if (new_pass_field.value.strip() and
                    new_pass_field.value == confirm_pass_field.value):
                    self.page.dialog.open = False
                    self.page.snack_bar = SnackBar(Text("Password changed"))
                    self.page.snack_bar.open = True
                    self.page.update()
                else:
                    error_text.value = "Passwords do not match or are empty"
                    self.page.update()

            new_pass_field = TextField(label="New password", password=True, can_reveal_password=True)
            confirm_pass_field = TextField(label="Confirm password", password=True, can_reveal_password=True)
            error_text = Text("", color=colors.RED)

            save_btn = ElevatedButton("Change", on_click=save_password, bgcolor="#2F4D19", color="white")
            cancel_btn = OutlinedButton("Cancel", on_click=lambda e: self._close_dialog())

            content_container = ft.Container(
                content=ft.Column(
                    [
                        new_pass_field,
                        confirm_pass_field,
                        error_text,
                    ],
                    spacing=10,
                ),
                height=125, 
                width=250,
            )

            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Change Password"),
                content=content_container,
                actions=[cancel_btn, save_btn],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.dialog.open = True
            self.page.update()

        def confirm_account_deletion(e):
            def delete_account(ev):
                self.page.dialog.open = False
                self.page.snack_bar = SnackBar(Text("Account deleted"))
                self.page.snack_bar.open = True
                self.page.update()
                # actual deletion logic/back to login page

            cancel_btn = OutlinedButton("Cancel", on_click=lambda e: self._close_dialog())
            delete_btn = ElevatedButton("Delete", bgcolor="#DE3730", on_click=delete_account, color="white")

            self.page.dialog = AlertDialog(
                title=Text("Confirm Delete Account"),
                content=Text("Are you sure you want to permanently delete your account?"),
                actions=[cancel_btn, delete_btn],
                actions_alignment=MainAxisAlignment.END,
            )
            self.page.dialog.open = True
            self.page.update()

        def confirm_logout(e):
            def logout(ev):
                self.page.dialog.open = False
                self.page.snack_bar = SnackBar(Text("Logged out"))
                self.page.snack_bar.open = True
                self.page.update()
                # actual logout logic / back to login page

            cancel_btn = OutlinedButton("Cancel", on_click=lambda e: self._close_dialog())
            logout_btn = ElevatedButton("Log out", on_click=logout, bgcolor="#DE3730", color="white")

            self.page.dialog = AlertDialog(
                title=Text("Confirm Logout"),
                content=Text("Are you sure you want to log out?"),
                actions=[cancel_btn, logout_btn],
                actions_alignment=MainAxisAlignment.END,
            )
            self.page.dialog.open = True
            self.page.update()

        email_tile = ListTile(
            title=Text("Email"),
            subtitle=Text(self.user_data['email']),
            trailing=Icon(icons.KEYBOARD_ARROW_RIGHT),
            on_click=open_edit_email_dialog,
        )
        password_tile = ListTile(
            title=Text("Change password"),
            trailing=Icon(icons.KEYBOARD_ARROW_RIGHT),
            on_click=open_change_password_dialog,
        )
        delete_account_tile = ListTile(
            title=Text("Delete account permanently", color=colors.RED),
            trailing=Icon(icons.KEYBOARD_ARROW_RIGHT, color=colors.RED),
            on_click=confirm_account_deletion,
        )
        logout_tile = ListTile(
            title=Text("Log out account"),
            trailing=Icon(icons.KEYBOARD_ARROW_RIGHT),
            on_click=confirm_logout,
        )

        account_section = Column(
            controls=[
                Text("Account", weight=FontWeight.BOLD, size=12, color=colors.GREY),
                email_tile,
                password_tile,
                delete_account_tile,
            ],
            spacing=2,
        )
        # Uncomment the following section if you want to add support and about options
        # support_section = Column(
        #     controls=[
        #         Text("Support & about", weight=FontWeight.BOLD, size=12, color=colors.GREY),
        #         ListTile(
        #             title=Text("Report a problem"),
        #             trailing=Icon(icons.KEYBOARD_ARROW_RIGHT),
        #             on_click=lambda e: print("Report a problem clicked"),
        #         ),
        #         ListTile(
        #             title=Text("Support"),
        #             trailing=Icon(icons.KEYBOARD_ARROW_RIGHT),
        #             on_click=lambda e: print("Support clicked"),
        #         ),
        #         ListTile(
        #             title=Text("Policies"),
        #             trailing=Icon(icons.KEYBOARD_ARROW_RIGHT),
        #             on_click=lambda e: print("Policies clicked"),
        #         ),
        #     ],
        #     spacing=2,
        # )

        login_section = Column(
            controls=[
                Text("Login", weight=FontWeight.BOLD, size=12, color=colors.GREY),
                logout_tile,
            ],
            spacing=2,
        )

        header_row = Row(
            controls=[
                Text("Profile", size=20),
                IconButton(icons.EDIT, on_click=open_edit_profile_dialog, icon_color="#2F4D19"),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )

        body = Column(
            controls=[
                header_row,
                Row(
                    controls=[
                        Column(
                            controls=[self.avatar, self.name_text],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                Divider(),
                account_section,
                # Divider(),
                # support_section,
                Divider(),
                login_section,
            ],
            scroll=ScrollMode.AUTO,
            expand=True,
            spacing=10,
        )

        return View(
            "/profile",
            controls=[body],
            vertical_alignment=CrossAxisAlignment.START,
        )


def main(page: ft.Page):
    page.window_width = 412
    page.window_height = 917
    page.title = "Profile Page"
    page.bgcolor = ft.colors.WHITE

    user_data = {
        "name": "Business",
        "email": "business@example.com",
    }

    def route_change(route):
        page.views.clear()

        if page.route == "/profile":
            page.views.append(ProfileView(page, user_data).build())
        else:
            page.views.append(
                ft.View("/", controls=[Text(f"Unknown route: {page.route}")])
            )

        page.update()

    page.on_route_change = route_change
    page.go("/profile")

if __name__ == "__main__":
    ft.app(target=main)
