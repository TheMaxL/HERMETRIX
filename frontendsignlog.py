import flet
from flet import Page, View, Column, Text, TextField, ElevatedButton, icons, Image, Container, alignment, GestureDetector

import backendsignlog


def main(page: Page):
    page.title = "HERMETRIX"
    page.window_width = 412
    page.window_height = 917
    page.bgcolor = "#FFFFFF"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.padding = 20
    page.spacing = 20

    message_text = Text("", color="#B69548", size=14)

    def create_welcome_view():
        logo = Container(
            content=Image(
                src="assets/HERMETRIXLOGOFIN.png",
                width=200,
                height=200,
                fit="contain",
            ),
            alignment=alignment.center,
            width=page.window_width,
            height=220,
        )

        btn_signup = ElevatedButton("Sign Up", width=180, height=50, bgcolor="#32620E", color="#FFFFFF", on_click=lambda e: page.go("/signup"))
        btn_login = ElevatedButton("Log In", width=180, height=50, bgcolor="#203D0A", color="#FFFFFF", on_click=lambda e: page.go("/login"))

        col = Column([logo, btn_signup, btn_login], alignment="center", horizontal_alignment="center", spacing=30, expand=True)
        return View("/", [col])

    def create_signup_view():
        heading = Text("Sign Up", size=30, weight="bold", color="#32620E", text_align="center")

        input_firstname = TextField(label="First Name", width=300, height=45)
        input_lastname = TextField(label="Last Name", width=300, height=45)
        input_username = TextField(label="Username", width=300, height=45)
        input_email = TextField(label="Email", width=300, height=45)
        input_password = TextField(label="Password", password=True, can_reveal_password=True, width=300, height=45)
        input_confirm = TextField(label="Confirm Password", password=True, can_reveal_password=True, width=300, height=45)

        def on_register_click(e):
            message_text.value = ""
            firstname = input_firstname.value.strip()
            lastname = input_lastname.value.strip()
            username = input_username.value.strip()
            email = input_email.value.strip()
            password = input_password.value
            confirm = input_confirm.value

            if not all([firstname, lastname, username, email, password, confirm]):
                message_text.value = "Please fill in all fields."
                message_text.color = "red"
            elif password != confirm:
                message_text.value = "Passwords do not match."
                message_text.color = "red"
            else:
                success = backendsignlog.sign_up(firstname, lastname, username, email, password, confirm)
                message_text.value = "Sign up successful!" if success else "Sign up failed. Try again."
                message_text.color = "#B69548" if success else "red"
            page.update()

        btn_register = ElevatedButton("Register", width=180, height=50, bgcolor="#32620E", color="#FFF2D2", on_click=on_register_click)
        btn_back = ElevatedButton("Back", icon=icons.ARROW_BACK, bgcolor="#203D0A", color="#FFF2D2", on_click=lambda e: page.go("/"))

        login_text_link = GestureDetector(
            content=Text("Already have an account? Log In", size=14, color="#203D0A", weight="bold"),
            on_tap=lambda e: page.go("/login")
        )

        col = Column([
            heading,
            input_firstname,
            input_lastname,
            input_username,
            input_email,
            input_password,
            input_confirm,
            btn_register,
            message_text,
            login_text_link,
            btn_back
        ], alignment="center", horizontal_alignment="center", spacing=12)

        container = Container(content=col, alignment=alignment.center, width=page.window_width, height=page.window_height)
        return View("/signup", [container])

    def create_login_view():
        heading = Text("Log In", size=30, weight="bold", color="#32620E", text_align="center")

        input_email = TextField(label="Email", width=300, height=45)
        input_password = TextField(label="Password", password=True, can_reveal_password=True, width=300, height=45)

        def on_login_click(e):
            message_text.value = ""
            email = input_email.value.strip()
            password = input_password.value

            if not email or not password:
                message_text.value = "Please fill in all fields."
                message_text.color = "red"
            else:
                success = backendsignlog.log_in(email, password)
                message_text.value = "Login successful!" if success else "Invalid email or password."
                message_text.color = "#B69548" if success else "red"
            page.update()

        btn_login = ElevatedButton("Log In", width=180, height=50, bgcolor="#32620E", color="#FFFFFF", on_click=on_login_click)
        btn_back = ElevatedButton("Back", icon=icons.ARROW_BACK, bgcolor="#203D0A", color="#FFFFFF", on_click=lambda e: page.go("/"))

        signup_text_link = GestureDetector(
            content=Text("Don't have an account? Sign Up", size=14, color="#203D0A", weight="bold"),
            on_tap=lambda e: page.go("/signup")
        )

        col = Column([
            heading,
            input_email,
            input_password,
            btn_login,
            message_text,
            signup_text_link,
            btn_back
        ], alignment="center", horizontal_alignment="center", spacing=12)

        container = Container(content=col, alignment=alignment.center, width=page.window_width, height=page.window_height)
        return View("/login", [container])

    page.views.append(create_welcome_view())
    page.views.append(create_signup_view())
    page.views.append(create_login_view())

    def route_change(route):
        if page.route == "/":
            page.views.clear()
            page.views.append(create_welcome_view())
        elif page.route == "/signup":
            page.views.clear()
            page.views.append(create_signup_view())
        elif page.route == "/login":
            page.views.clear()
            page.views.append(create_login_view())
        else:
            page.views.clear()
            page.views.append(create_welcome_view())
        page.update()

    page.on_route_change = route_change
    page.go(page.route or "/")


if __name__ == "__main__":
    flet.app(target=main)
    
