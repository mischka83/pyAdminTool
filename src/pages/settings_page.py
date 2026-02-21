# -----------------------------
# pages/settings_page.py
# -----------------------------
import flet as ft
from utils.config import load_config, save_config

def settings_page(page: ft.Page):
    config = load_config()

    ldaps_field = ft.TextField(label="LDAPS Pfad", value=config.get("ldaps_url", ""))
    user_field = ft.TextField(label="Benutzername", value=config.get("username", ""))
    password_field = ft.TextField(label="Passwort", value=config.get("password", ""), password=True)
    basedn_field = ft.TextField(label="Base DN", value=config.get("base_dn", ""))
    feld5_field = ft.TextField(label="Feld 5", value=config.get("feld5", ""))

    status_text = ft.Text("")

    def save_settings(e):
        new_config = {
            "ldaps_url": ldaps_field.value,
            "username": user_field.value,
            "password": password_field.value,
            "base_dn": basedn_field.value,
            "feld5": feld5_field.value
        }
        save_config(new_config)
        status_text.value = "✅ Einstellungen gespeichert!"
        status_text.update()

    return ft.Column(
        [
            ft.Text("Einstellungen", size=24),
            ldaps_field,
            user_field,
            password_field,
            basedn_field,
            feld5_field,
            ft.ElevatedButton("Speichern", on_click=save_settings),
            status_text
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )