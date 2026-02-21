import flet as ft
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime


# -----------------------------------
# Subject pretty-print with abbreviations
# -----------------------------------
SUBJECT_MAP = {
    "countryName": "C",
    "stateOrProvinceName": "ST",
    "localityName": "L",
    "organizationName": "O",
    "organizationalUnitName": "OU",
    "commonName": "CN",
    "emailAddress": "email",
}


def format_subject(subject):
    rdns = subject.rdns
    parts = []

    for rdn in rdns:
        for attr in rdn:
            oid_name = attr.oid._name
            short = SUBJECT_MAP.get(oid_name, oid_name)
            parts.append(f"{short} = {attr.value}")

    return "\n".join(parts)


def decode_page(page: ft.Page):

    # -----------------------------------
    # UI Elements
    # -----------------------------------

    selected_file = ft.Text("Keine Datei ausgewählt", size=14)

    result_container = ft.Column(expand=True, spacing=10)

    # Reusable info row (supports multi-line)
    def info_row(title, value, multiline=False):
        return ft.Column([
            ft.Text(title, weight=ft.FontWeight.BOLD, size=16),
            ft.Text(
                value,
                selectable=True,
                size=14,
                no_wrap=not multiline,
            ),
            ft.Divider(),
        ])

    # -----------------------------------------------------------------------------
    # FilePicker Setup
    # -----------------------------------------------------------------------------

    def on_file_picked(e: ft.FilePickerResultEvent):
        if not e.files:
            selected_file.value = "Keine Datei ausgewählt"
            selected_file.update()
            return

        picked_path = e.files[0].path
        selected_file.value = picked_path
        selected_file.update()

        decode_certificate(picked_path)

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    # -----------------------------------------------------------------------------
    # Certificate Decoding Logic
    # -----------------------------------------------------------------------------

    def decode_certificate(path: str):
        try:
            with open(path, "rb") as f:
                cert_data = f.read()

            cert = x509.load_pem_x509_certificate(cert_data, default_backend())

            # Subject
            subject_pretty = format_subject(cert.subject)

            # SAN
            try:
                san_ext = cert.extensions.get_extension_for_class(
                    x509.SubjectAlternativeName
                ).value
                san_list = san_ext.get_values_for_type(x509.DNSName)
                san_pretty = "\n".join(san_list)
            except Exception:
                san_pretty = "Keine vorhanden"

            # Validity dates (German format)
            not_before = cert.not_valid_before.strftime("%d.%m.%Y %H:%M")
            not_after = cert.not_valid_after.strftime("%d.%m.%Y %H:%M")

            # Serial
            serial_hex = hex(cert.serial_number)[2:].upper()

            # Clear UI
            result_container.controls.clear()

            # Add formatted result
            result_container.controls.extend([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Zertifikatsdetails", size=22, weight=ft.FontWeight.BOLD),
                            info_row("Subject", subject_pretty, multiline=True),
                            info_row("SAN", san_pretty, multiline=True),
                            info_row("Gültig von", not_before),
                            info_row("Gültig bis", not_after),
                            info_row("Seriennummer", serial_hex),
                        ]),
                        padding=20
                    )
                )
            ])

            page.update()

        except Exception as ex:
            result_container.controls.clear()
            result_container.controls.append(
                ft.Text(f"Fehler beim Lesen des Zertifikats: {ex}", color="red")
            )
            page.update()

    # -----------------------------------------------------------------------------
    # UI Layout
    # -----------------------------------------------------------------------------

    pick_button = ft.ElevatedButton(
        "Zertifikat auswählen",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["pem", "crt", "cer"]
        )
    )

    return ft.Column(
        [
            ft.Text("Zertifikat dekodieren", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("Wähle ein Zertifikat (.pem / .crt / .cer), um dessen Inhalte anzuzeigen."),
            ft.Row([pick_button], spacing=20),
            selected_file,
            ft.Divider(),
            result_container,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=20,
    )
