import flet as ft
from pages.home_page import home_page
from pages.pfx_converter_page import pfx_converter_page
from pages.settings_page import settings_page
from pages.decode_page import decode_page
from pages.ad_group_search_page import ad_group_search_page
from pages.ad_person_search_page import ad_person_search_page
from pages.ad_laps_page import ad_laps_page

def create_navigation_drawer(page: ft.Page, content_area: ft.Column,
                             selected_file, password_field, output_status,
                             pick_file, convert_pfx):
    """
    Erstellt einen Navigation Drawer mit Seitenwechsel-Logik.
    """
    # --- PFX Converter Seite ---
    pfx_page = pfx_converter_page(
        selected_file=selected_file,
        password_field=password_field,
        output_status=output_status,
        pick_file=pick_file,
        convert_pfx=convert_pfx
    )

    # --- Helper Funktion für Seitenwechsel ---
    def switch_page(page_name: str, index: int):
        page.drawer.selected_index = index
        content_area.controls.clear()

        if page_name == "home":
            content_area.controls.append(home_page())
            page.appbar.title = ft.Text("Startseite")
        elif page_name == "ad_person_search":
            content_area.controls.append(ad_person_search_page(page))
            page.appbar.title = ft.Text("AD Personen Suche")
        elif page_name == "ad_group_search":
            content_area.controls.append(ad_group_search_page(page))
            page.appbar.title = ft.Text("AD Gruppen Suche")
        elif page_name == "ad_laps":
            content_area.controls.append(ad_laps_page(page))
            page.appbar.title = ft.Text("AD LAPS Mitglieder")
        elif page_name == "pfx_converter":
            content_area.controls.append(pfx_page)
            page.appbar.title = ft.Text("PFX Konverter")
        elif page_name == "decode":
            from pages.decode_page import decode_page
            content_area.controls.append(decode_page(page))
            page.appbar.title = ft.Text("Dekode Zertifikat")
        elif page_name == "settings":
            content_area.controls.append(settings_page(page))
            page.appbar.title = ft.Text("Einstellungen")

        page.drawer.open = False
        page.update()


    # --- Drawer Definition ---
    drawer = ft.NavigationDrawer(
        selected_index=0,
        controls=[
            ft.ListTile(
                leading=ft.Icon(ft.Icons.HOME),
                title=ft.Text("Home"),
                on_click=lambda e: switch_page("home", 0)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.PERSON),
                title=ft.Text("AD Person Suche"),
                on_click=lambda e: switch_page("ad_person_search", 1)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.GROUP),
                title=ft.Text("AD Gruppen Suche"),
                on_click=lambda e: switch_page("ad_group_search", 2)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.SECURITY),
                title=ft.Text("AD LAPS Mitglieder"),
                on_click=lambda e: switch_page("ad_laps", 3)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.KEY),
                title=ft.Text("PFX Konverter"),
                on_click=lambda e: switch_page("pfx_converter", 4)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.KEY),
                title=ft.Text("Decode"),
                on_click=lambda e: switch_page("decode", 5)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.SETTINGS),
                title=ft.Text("Settings"),
                on_click=lambda e: switch_page("settings", 6)
            ),
        ]
    )

    return drawer
