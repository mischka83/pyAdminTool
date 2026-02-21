# pages/ad_person_search_page.py
import flet as ft
import threading
from functools import partial
from utils.ad_person import search_persons, get_person_details, export_person_details

debounce_timer = None

def ad_person_search_page(page: ft.Page):
    search_field = ft.TextField(label="Person suchen", width=300, on_change=lambda e: debounce_search(e.control.value))
    suggestions_list = ft.ListView(spacing=0, height=150)
    suggestions_container = ft.Container(content=suggestions_list, bgcolor=ft.Colors.WHITE, width=300, padding=5,
                                         border_radius=5, shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_300),
                                         visible=False)
    status_text = ft.Text("")
    details_column = ft.Column(scroll=ft.ScrollMode.AUTO, height=500)

    # --- Debounce für Personensuche ---
    def debounce_search(query):
        global debounce_timer
        if debounce_timer:
            debounce_timer.cancel()
        debounce_timer = threading.Timer(0.3, lambda: show_person_suggestions(query))
        debounce_timer.start()

    # --- Vorschläge anzeigen ---
    def show_person_suggestions(query):
        suggestions_list.controls.clear()
        if len(query) < 3:
            suggestions_container.visible = False
            page.update()
            return
        try:
            persons = search_persons(query)
            if persons:
                for person_name in persons:
                    btn = ft.TextButton(content=ft.Row([ft.Text(person_name)], alignment=ft.MainAxisAlignment.START),
                                        style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_GREY_50}),
                                        on_click=partial(select_person, person_name))
                    suggestions_list.controls.append(btn)
                suggestions_container.visible = True
            else:
                suggestions_container.visible = False
        except Exception as ex:
            suggestions_list.controls.append(ft.Text(f"Fehler: {ex}"))
            suggestions_container.visible = True
        page.update()

    # --- Details anzeigen ---
    def select_person(person_name, e):
        suggestions_container.visible = False
        details_column.controls.clear()
        status_text.value = f"Details für {person_name}:"
        status_text.update()
        try:
            details = get_person_details(person_name)
            if details:
                # Card für Basisdaten
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(details["DisplayName"], size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Name: {details['Name']}"),
                            ft.Text(f"Vorname: {details['Vorname']}"),
                            ft.Text(f"Nachname: {details['Nachname']}"),
                            ft.Text(f"E-Mail: {details['E-Mail']}"),
                            ft.Text(f"Abteilung: {details['Abteilung']}"),
                            ft.Text(f"Titel: {details['Titel']}"),
                            ft.Text(f"Telefon: {details['Telefon']}"),
                        ]),
                        padding=10
                    )
                )
                details_column.controls.append(card)

                # Accordion für Gruppen
                if details["Gruppen"]:
                    accordion = ft.ExpansionTile(title=ft.Text("Gruppenmitgliedschaften"), controls=[
                        ft.Column([ft.Text(f"- {group}") for group in details["Gruppen"]])
                    ])
                    details_column.controls.append(accordion)

                # Export-Button
                export_btn = ft.ElevatedButton("Export als CSV", icon=ft.Icons.DOWNLOAD, on_click=lambda _: export_details(details))
                details_column.controls.append(export_btn)
            else:
                details_column.controls.append(ft.Text("Keine Details gefunden"))
        except Exception as ex:
            details_column.controls.append(ft.Text(f"Fehler: {ex}"))
        page.update()

    # --- Export ---
    def export_details(details):
        try:
            file_path = export_person_details(details)
            status_text.value = f"✅ Export erfolgreich: {file_path}"
        except Exception as ex:
            status_text.value = f"❌ Fehler beim Export: {ex}"
        page.update()

    return ft.Column([
        ft.Text("AD Personensuche", size=24, weight=ft.FontWeight.BOLD),
        search_field,
        suggestions_container,
        status_text,
        details_column
    ])