import flet as ft
from components.app_header import app_header
from components.app_footer import app_footer
from pages.home_page import home_page
from pages.settings_page import settings_page
from utils.pfx_converter import convert_pfx_file
from utils.navigation import create_navigation_drawer

def main(page: ft.Page):
    page.title = "Admin Tools"
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- Shared state ---
    selected_file = ft.Text("")
    password_input = ft.TextField(label="Passwort", password=True)
    status_text = ft.Text("")

    # --- FilePicker ---
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            selected_file.value = e.files[0].path
            status_text.value = f"Ausgewählte Datei: {selected_file.value}"
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    def pick_file(e):
        file_picker.pick_files()

    # --- PFX Konvertierung ---
    def convert_pfx(e):
        if not selected_file.value or not password_input.value:
            status_text.value = "Bitte Datei und Passwort angeben."
            page.update()
            return

        convert_pfx_file(
            file_path=selected_file.value,
            password=password_input.value,
            output_status=status_text
        )
        page.update()

    # --- Content Area ---
    content_area = ft.Column(expand=True)

    # --- Drawer ---
    page.drawer = create_navigation_drawer(
        page=page,
        content_area=content_area,
        selected_file=selected_file,
        password_field=password_input,
        output_status=status_text,
        pick_file=pick_file,
        convert_pfx=convert_pfx
    )

    # --- Header & Layout ---
    page.appbar = app_header(page, "Startseite")
    main_column = ft.Column(controls=[content_area, app_footer()], expand=True, spacing=0)
    page.add(main_column)

    # --- Initial Page ---
    content_area.controls.append(home_page())
    page.update()


ft.app(target=main)
#ft.app(target=main, view=ft.AppView.WEB_BROWSER)
