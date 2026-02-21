import flet as ft

def toggle_theme(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
    page.update()
