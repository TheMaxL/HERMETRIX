import flet
from flet import Page
from frontendsignlog import HermetrixApp

def main(page: Page):
    HermetrixApp(page)


if __name__ == "__main__":
    flet.app(target=main)
