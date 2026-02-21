# -----------------------------
# components/app_header.py
# -----------------------------
import flet as ft

def toggle_drawer(page: ft.Page):
    page.drawer.open = not page.drawer.open
    page.update()


def toggle_theme(page: ft.Page):
    page.theme_mode = (
        ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
    )
    page.update()


def app_header(page: ft.Page, title: str):
    return ft.AppBar(
        leading=ft.IconButton(icon=ft.Icons.MENU, on_click=lambda _: toggle_drawer(page)),
        title=ft.Text(title),
        center_title=False,
        actions=[
            ft.IconButton(
                icon=ft.Icons.DARK_MODE,
                on_click=lambda _: toggle_theme(page)
            )
        ],
    )