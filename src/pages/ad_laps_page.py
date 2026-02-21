import flet as ft
from utils.ad_laps import get_laps_group_members
from datetime import datetime

def ad_laps_page(page: ft.Page):

    status_text = ft.Text("", size=14)

    # ---------------------------------------------------------
    # Daten laden
    # ---------------------------------------------------------
    def load_group(e):
        members_table.rows.clear()
        page.update()

        group_name = f"{filter_field.value}{server_field.value}".strip()

        if group_name == "":
            status_text.value = "Bitte einen gültigen Gruppenfilter eingeben."
            page.update()
            return

        status_text.value = f"Lade Mitglieder von '{group_name}' ..."
        page.update()

        try:
            members = get_laps_group_members(group_name)

            if not members:
                status_text.value = "Keine Daten erhalten."
                page.update()
                return

            # --- Zeilen aufbauen ---
            for m in members:
                name = m.get("name", "")
                display_name = m.get("display_name", "")
                ttl = m.get("ttl_expiry", "")

                # TTL-Farbmarkierung
                text_color = None
                if ttl and ttl != "N/A":
                    try:
                        expiry_dt = datetime.strptime(ttl, "%Y-%m-%d %H:%M:%S")
                        remaining = (expiry_dt - datetime.now()).total_seconds()

                        if remaining < 0:
                            text_color = ft.Colors.RED_700
                        elif remaining < 3600:  # <1h = tiefrot
                            text_color = ft.Colors.RED
                        elif remaining < 86400:  # <24h = orange
                            text_color = ft.Colors.ORANGE
                    except:
                        pass

                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(ft.Text(display_name)),
                        ft.DataCell(ft.Text(ttl, color=text_color))
                    ]
                )

                members_table.rows.append(row)

            status_text.value = f"Mitglieder von {group_name}: {len(members_table.rows)} gefunden."

        except Exception as ex:
            status_text.value = f"Fehler: {ex}"

        page.update()

    # Tabelle vorbereiten
    members_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Display Name")),
            ft.DataColumn(ft.Text("TTL Ablaufzeit"))
        ],
        rows=[],
        heading_row_color=ft.Colors.BLUE_GREY_100,
        data_row_color={ft.ControlState.HOVERED: ft.Colors.BLUE_GREY_50},
        column_spacing=20,
    )

    members_container = ft.Container(
        content=ft.Column(controls=[members_table], scroll=ft.ScrollMode.AUTO),
        height=500,
        padding=10
    )

    # Eingabefelder
    server_field = ft.TextField(label="Servername", width=300, on_submit=load_group)
    filter_field = ft.TextField(label="AD Filter", value="F_TIER1-SRV_", width=300)

    # ---------------------------------------------------------
    # Layout zurückgeben
    # ---------------------------------------------------------
    return ft.Column([
        ft.Text("AD LAPS Übersicht", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(height=10),
        ft.Row([
            server_field,
            filter_field,
            ft.ElevatedButton("Laden", on_click=load_group)
        ]),
        ft.Divider(height=5),
        status_text,
        members_container
    ])
