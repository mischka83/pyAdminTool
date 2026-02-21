# pages/pfx_converter_page.py
import flet as ft

def pfx_converter_page(
    selected_file: ft.Text,
    password_field: ft.TextField,
    output_status: ft.Text,
    pick_file,
    convert_pfx
) -> ft.Column:
    """
    PFX Converter Page Layout.

    Args:
        selected_file: ft.Text control für die ausgewählte Datei
        password_field: ft.TextField für Passwort
        output_status: ft.Text für Statusmeldungen
        pick_file: Funktion zum Auswählen der Datei
        convert_pfx: Funktion zum Konvertieren der Datei
    Returns:
        ft.Column: Page Layout
    """
    return ft.Column(
        spacing=20,
        controls=[
            ft.Text("PFX Konverter", style="headlineMedium"),
            ft.Row(
                controls=[
                    ft.ElevatedButton("Datei auswählen", on_click=pick_file),
                    selected_file,
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
            ),
            password_field,
            ft.ElevatedButton("Konvertieren", on_click=convert_pfx),
            output_status,
        ],
        expand=True
    )
