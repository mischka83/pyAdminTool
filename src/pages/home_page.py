import flet as ft

def home_page():
    return ft.Column([
        ft.Text("Willkommen auf der Startseite!", size=24),
        ft.Text("Dies ist ein Beispielinhalt."),
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)