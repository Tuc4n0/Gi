import flet as ft
import ipaddress

def main(page: ft.Page):
    page.title = "Calculadora de IP"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.scroll = ft.ScrollMode.ALWAYS
    page.window_width = 550
    page.window_height = 750

    # Alternar tema
    def mudar_tema(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        tema_btn.icon = (
            ft.Icons.WB_SUNNY_ROUNDED if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE_ROUNDED
        )
        page.update()

    ip_input = ft.TextField(
        label="Endereço IP",
        hint_text="Ex: 192.168.0.0",
        border_radius=12,
        prefix_icon=ft.Icons.LAN_OUTLINED,
        expand=True,
    )
    mask_dropdown = ft.Dropdown(
        label="Máscara",
        options=[ft.dropdown.Option(f"/{i}") for i in range(8, 31)],
        value="/24",
        expand=True,
        border_radius=12,
    )

    resultado = ft.Text(value="", selectable=True, size=14)
    lista_subredes = ft.Column(spacing=8, scroll=ft.ScrollMode.ALWAYS)

    # Calcular
    def calcular(e):
        try:
            rede_str = ip_input.value.strip()
            mask_str = mask_dropdown.value.strip()
            if not rede_str:
                resultado.value = "Insira um endereço IP válido!"
                lista_subredes.controls.clear()
                page.update()
                return

            rede = ipaddress.ip_network(rede_str + mask_str, strict=False)
            hosts = list(rede.hosts())
            primeiro = hosts[0] if hosts else "N/A"
            ultimo = hosts[-1] if hosts else "N/A"

            resultado.value = (
                f"🌐 Rede: {rede.network_address}\n"
                f"📡 Broadcast: {rede.broadcast_address}\n"
                f"💻 Total de Hosts: {len(hosts)}\n"
                f"🔹 Primeiro Host: {primeiro}\n"
                f"🔹 Último Host: {ultimo}\n"
            )

            # Gerar sub-redes da própria rede
            subredes = list(rede.subnets(new_prefix=rede.prefixlen))
            total_subredes = len(subredes)

            if total_subredes > 256:
                lista_subredes.controls.clear()
                lista_subredes.controls.append(
                    ft.Text(
                        f"⚠️ Muitas sub-redes ({total_subredes}) foram geradas.\n"
                        f"Mostrando apenas as primeiras 10.",
                        color="orange",
                        size=13,
                    )
                )
                subredes = subredes[:10]

            lista_subredes.controls.clear()
            lista_subredes.controls.append(
                ft.Text(f"📘 Sub-redes ({mask_str}):", weight="bold", size=16)
            )

            for s in subredes:
                lista_subredes.controls.append(
                    ft.Container(
                        content=ft.Text(
                            f"🔸 {s.network_address} - {s.broadcast_address}",
                            size=13,
                        ),
                        bgcolor=ft.Colors.with_opacity(0.08, "primary"),
                        padding=10,
                        border_radius=12,
                    )
                )

            if total_subredes > len(subredes):
                lista_subredes.controls.append(
                    ft.Text(f"... e mais {total_subredes - len(subredes)} sub-redes ocultas.", italic=True, size=12)
                )

        except Exception:
            resultado.value = "⚠️ Erro! Tente mudar o IP ou a máscara."
            lista_subredes.controls.clear()

        page.update()

    # Copiar
    def copiar(e):
        if resultado.value:
            page.set_clipboard(resultado.value)
            page.snack_bar = ft.SnackBar(ft.Text("Copiados! ✧"), open=True)
            page.update()

    # Limpar
    def limpar(e):
        ip_input.value = ""
        resultado.value = ""
        lista_subredes.controls.clear()
        page.update()

    calcular_btn = ft.ElevatedButton(
        "Calcular", icon=ft.Icons.CALCULATE_ROUNDED, on_click=calcular, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )
    limpar_btn = ft.OutlinedButton(
        "Excluir", icon=ft.Icons.CLEAR_ROUNDED, on_click=limpar, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )
    copiar_btn = ft.IconButton(icon=ft.Icons.COPY_ALL_ROUNDED, tooltip="Copiar", on_click=copiar)
    tema_btn = ft.IconButton(icon=ft.Icons.DARK_MODE_ROUNDED, tooltip="Mudar tema", on_click=mudar_tema)

    card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("CALCUIP", size=28, weight="bold", text_align="center"),
                    ft.Divider(),
                    ip_input,
                    mask_dropdown,
                    ft.Row([calcular_btn, limpar_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Container(resultado, padding=10, border_radius=10),
                    lista_subredes,
                    ft.Divider(),
                    ft.Row([copiar_btn, tema_btn], alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=18,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=25,
            border_radius=25,
        ),
        elevation=10,
    )

    page.add(
        ft.Column(
            [card],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=None, port=8080)
