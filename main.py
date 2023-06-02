from flet import *
from core import SortAlg

def main(page:Page):
    page.title = "Sorting Algorithms"
    page.theme_mode = "dark"
    page.window_height = 500
    page.window_width = 676
    page.vertical_alignment = "CENTER"
    page.window_resizable = False
    page.window_maximizable = False
    page.window_center()

    app = SortAlg(page)
    page.add(app)
    page.update()

if __name__ == "__main__":
    app(target=main)