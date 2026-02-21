import flet as ft

# -----------------------------------------------------
# Footer
# -----------------------------------------------------
def app_footer():
    return ft.Container(
        content=ft.Text("© 2025 Christian Ewert", size=12),
        alignment=ft.alignment.center,
        padding=10,
    )
