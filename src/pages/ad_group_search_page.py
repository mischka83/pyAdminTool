# pages/ad_group_search_page.py
import flet as ft
import threading
from functools import partial
from utils.ad_group import search_groups, get_group_members, export_members_to_csv

debounce_timer = None

def ad_group_search_page(page: ft.Page):
    # UI-Elemente
    search_field = ft.TextField(label="Gruppenname", width=300, on_change=lambda e: debounce_search(e.control.value))
    suggestions_list = ft.ListView(spacing=0, height=150)
    suggestions_container = ft.Container(content=suggestions_list, bgcolor=ft.Colors.WHITE, width=300, padding=5,
                                         border_radius=5, shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_300),
                                         visible=False)
    status_text = ft.Text("")
    members_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("Name")), ft.DataColumn(ft.Text("Display Name"))],
                                 rows=[], heading_row_color=ft.Colors.BLUE_GREY_100,
                                 data_row_color={ft.ControlState.HOVERED: ft.Colors.BLUE_GREY_50}, column_spacing=20)
    members_container = ft.Column(controls=[members_table], scroll=ft.ScrollMode.AUTO, height=500)

    # Neues Suchfeld für Mitglieder
    member_search_field = ft.TextField(label="Mitglieder durchsuchen", width=300, on_change=lambda e: filter_members(e.control.value))

    # Originaldaten für Filter
    all_members = []

    # --- Debounce für Gruppensuche ---
    def debounce_search(query):
        global debounce_timer
        if debounce_timer:
            debounce_timer.cancel()
        debounce_timer = threading.Timer(0.3, lambda: show_group_suggestions(query))
        debounce_timer.start()

    # --- Gruppenvorschläge anzeigen ---
    def show_group_suggestions(query):
        suggestions_list.controls.clear()
        if len(query) < 4:
            suggestions_container.visible = False
            page.update()
            return
        try:
            groups = search_groups(query)
            if groups:
                for group_name in groups:
                    btn = ft.TextButton(content=ft.Row([ft.Text(group_name)], alignment=ft.MainAxisAlignment.START),
                                        style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE_GREY_50}),
                                        on_click=partial(select_group, group_name))
                    suggestions_list.controls.append(btn)
                suggestions_container.visible = True
            else:
                suggestions_container.visible = False
        except Exception as ex:
            suggestions_list.controls.append(ft.Text(f"Fehler: {ex}"))
            suggestions_container.visible = True
        page.update()

    # --- Mitglieder einer Gruppe laden ---
    def select_group(group_name, e):
        suggestions_container.visible = False
        members_table.rows.clear()
        all_members.clear()
        status_text.value = f"Mitglieder von {group_name}:"
        status_text.update()
        try:
            members = get_group_members(group_name)
            for m in members:
                row = ft.DataRow(cells=[ft.DataCell(ft.Text(m["name"])), ft.DataCell(ft.Text(m["display_name"]))])
                all_members.append(row)
            members_table.rows.extend(all_members)
        except Exception as ex:
            row = ft.DataRow(cells=[ft.DataCell(ft.Text(f"Fehler: {ex}")), ft.DataCell(ft.Text(""))])
            all_members.append(row)
            members_table.rows.append(row)
        page.update()

    # --- Filterfunktion ---
    def filter_members(query):
        query = query.lower()
        members_table.rows.clear()
        if query == "":
            members_table.rows.extend(all_members)
        else:
            filtered = [row for row in all_members if query in row.cells[0].content.value.lower() or query in row.cells[1].content.value.lower()]
            members_table.rows.extend(filtered)
        page.update()

    # --- Export ---
    def export_to_csv(e):
        try:
            members_data = [{"name": row.cells[0].content.value, "display_name": row.cells[1].content.value} for row in all_members]
            file_path = export_members_to_csv(members_data)
            status_text.value = f"✅ Export erfolgreich: {file_path}"
        except Exception as ex:
            status_text.value = f"❌ Fehler beim Export: {ex}"
        page.update()

    return ft.Column([
        ft.Text("AD Gruppen Suche", size=24, weight=ft.FontWeight.BOLD),
        search_field,
        suggestions_container,
        status_text,
        ft.Row(controls=[
            ft.Text("Mitglieder:", size=18, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Export als CSV", icon=ft.Icons.DOWNLOAD, on_click=export_to_csv),
        ]),
        member_search_field,
        members_container
    ])