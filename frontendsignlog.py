from flet import Page, View, Column, Text, TextField, ElevatedButton, icons, Image, Container, alignment, GestureDetector

import backendsignlog 

class HermetrixApp:
    def __init__(self, page: Page):
        self.page = page
        self.page.title = "HERMETRIX"
        self.page.window_width = 412
        self.page.window_height = 917
        self.page.bgcolor = "#FFFFFF"
        self.page.vertical_alignment = "center"
        self.page.horizontal_alignment = "center"
        self.page.padding = 20
        self.page.spacing = 20

        self.message_text = Text("", color="#B69548", size=14)

        self.page.on_route_change = self.route_change
        self.page.views.append(self.create_welcome_view())
        self.page.go(self.page.route or "/")

    def create_welcome_view(self):
        logo = Container(
            content=Image(
                src="assets/HERMETRIXLOGOFIN.png",
                width=200,
                height=200,
                fit="contain",
            ),
            alignment=alignment.center,
            width=self.page.window_width,
            height=220,
        )

        btn_signup = ElevatedButton("Sign Up", width=180, height=50, bgcolor="#32620E", color="#FFFFFF", on_click=lambda e: self.page.go("/signup"))
        btn_login = ElevatedButton("Log In", width=180, height=50, bgcolor="#203D0A", color="#FFFFFF", on_click=lambda e: self.page.go("/login"))

        col = Column([logo, btn_signup, btn_login], alignment="center", horizontal_alignment="center", spacing=30, expand=True)
        return View("/", [col])

    def create_signup_view(self):
        heading = Text("Sign Up", size=30, weight="bold", color="#32620E", text_align="center")

        input_firstname = TextField(label="First Name", width=300, height=45)
        input_lastname = TextField(label="Last Name", width=300, height=45)
        input_username = TextField(label="Username", width=300, height=45)
        input_email = TextField(label="Email", width=300, height=45)
        input_password = TextField(label="Password", password=True, can_reveal_password=True, width=300, height=45)
        input_confirm = TextField(label="Confirm Password", password=True, can_reveal_password=True, width=300, height=45)

        def on_register_click(e):
            self.message_text.value = ""
            firstname = input_firstname.value.strip()
            lastname = input_lastname.value.strip()
            username = input_username.value.strip()
            email = input_email.value.strip()
            password = input_password.value
            confirm = input_confirm.value

            if not all([firstname, lastname, username, email, password, confirm]):
                self.message_text.value = "Please fill in all fields."
                self.message_text.color = "red"
            elif password != confirm:
                self.message_text.value = "Passwords do not match."
                self.message_text.color = "red"
            else:
                success = backendsignlog.sign_up(firstname, lastname, username, email, password, confirm)
                self.message_text.value = "Sign up successful!" if success else "Sign up failed. Try again."
                self.message_text.color = "#B69548" if success else "red"
            self.page.update()

        btn_register = ElevatedButton("Register", width=180, height=50, bgcolor="#32620E", color="#FFF2D2", on_click=on_register_click)
        btn_back = ElevatedButton("Back", icon=icons.ARROW_BACK, bgcolor="#203D0A", color="#FFF2D2", on_click=lambda e: self.page.go("/"))

        login_text_link = GestureDetector(
            content=Text("Already have an account? Log In", size=14, color="#203D0A", weight="bold"),
            on_tap=lambda e: self.page.go("/login")
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
            self.message_text,
            login_text_link,
            btn_back
        ], alignment="center", horizontal_alignment="center", spacing=12)

        container = Container(content=col, alignment=alignment.center, width=self.page.window_width, height=self.page.window_height)
        return View("/signup", [container])

    def create_login_view(self):
        heading = Text("Log In", size=30, weight="bold", color="#32620E", text_align="center")

        input_email = TextField(label="Email", width=300, height=45)
        input_password = TextField(label="Password", password=True, can_reveal_password=True, width=300, height=45)

        def on_login_click(e):
            self.message_text.value = ""
            email = input_email.value.strip()
            password = input_password.value

            if not email or not password:
                self.message_text.value = "Please fill in all fields."
                self.message_text.color = "red"
                self.page.update()
            else:
                success = backendsignlog.log_in(email, password, self.page)
                if success:
                    self.message_text.value = "Login successful!"
                    self.message_text.color = "#B69548"
                    
                    from dashboardui import ViewSwitcher
                    view_switcher = ViewSwitcher(self.page)
                    view_switcher.show_view("dashboard")
                    return
                    
                else:
                    self.message_text.value = "Invalid email or password."
                    self.message_text.color = "red"
                    self.page.update()

        btn_login = ElevatedButton("Log In", width=180, height=50, bgcolor="#32620E", color="#FFFFFF", on_click=on_login_click)
        btn_back = ElevatedButton("Back", icon=icons.ARROW_BACK, bgcolor="#203D0A", color="#FFFFFF", on_click=lambda e: self.page.go("/"))

        signup_text_link = GestureDetector(
            content=Text("Don't have an account? Sign Up", size=14, color="#203D0A", weight="bold"),
            on_tap=lambda e: self.page.go("/signup")
        )

        col = Column([
            heading,
            input_email,
            input_password,
            btn_login,
            self.message_text,
            signup_text_link,
            btn_back
        ], alignment="center", horizontal_alignment="center", spacing=12)

        container = Container(content=col, alignment=alignment.center, width=self.page.window_width, height=self.page.window_height)
        return View("/login", [container])
    
   
     
    def route_change(self, route):
        self.page.views.clear()

        # Initialize view to None to avoid accessing it before assignment
        view = None

        if self.page.route == "/":
            view = self.create_welcome_view()
        elif self.page.route == "/signup":
            view = self.create_signup_view()
        elif self.page.route == "/login":
            view = self.create_login_view()
        else:
            view = self.create_welcome_view()

        if view is not None:
            self.page.views.append(view)
        else:
            print("Error: view is None")

        self.page.update()
