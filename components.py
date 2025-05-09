import flet as ft
from helpers import check_internet_connection, read_json
import config

#data config 
data_config = read_json(config.DATA_CONFIG)
data_config = data_config["data"]
bussiness_name = data_config["bussiness_name"]
path_dat = data_config["path_dat"]
path_logo = data_config["path_logo"]

class Container_():
    def __init__(self, bgcolor: ft.Colors, text:ft.Text, title: str, height=60):
        self.bgcolor = bgcolor
        self.text = text
        self.title = title
        self.height = height

    def create(self):
        return ft.Container(
        col={"sm": 6, "md": 4, "xl": 3},
        bgcolor= self.bgcolor,
        border_radius=5,
        height=self.height,
        padding=10,
        alignment=ft.alignment.center,
        content=ft.Column(
            width=200,
            controls=[
                ft.Row(
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value=self.title,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color= ft.Colors.WHITE,
                ),
                self.text

            ],
        ),
            ]
        )
    )

class TextField_:
    def __init__(self, on_click, on_change, label: str):
        self.label = label
        self.on_click = on_click
        self.on_change = on_change
    def create(self):
        return ft.TextField(
        expand=True,
        on_submit=self.on_click,
        label=self.label,
        on_change=self.on_change,
        col={"sm": 6, "md": 4, "xl": 3},
    )

class InputFile_():
    def __init__(self, on_click):
        self.on_click = on_click
    def create(self):
        return ft.ElevatedButton("Selecccione archivo...",
    on_click=self.on_click, width=200)

class Button_():
    def __init__(self, on_click, text: str, bgcolor: ft.Colors, color:ft.Colors, icon=ft.Icons, width=None, height=None):
        self.bgcolor = bgcolor
        self.text = text
        self.icon = icon
        self.on_click = on_click
        self.color = color
        self.width = width
        self.height = height

    def create(self):
        return ft.ElevatedButton(
        col={"sm": 6, "md": 4, "xl": 2},
        text=self.text,
        on_click=self.on_click,
        icon_color=ft.Colors.WHITE,
        bgcolor= self.bgcolor,
        color= self.color,
        icon= self.icon,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
        ),
        width=self.width,
        height=self.height

    )

class Submenu_():
    def __init__(self, content:str, leading:ft.Icons, on_click=lambda _: print(_)):
        self.content = content
        self.leading = leading
        self.on_click = on_click
    
    def create(self):
        return ft.MenuItemButton(
                        content=ft.Text(value=self.content),
                        leading=self.leading,
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.HOVERED: "#1F2041"},
                            color={ft.ControlState.HOVERED: ft.Colors.WHITE},
                            icon_color={ft.ControlState.HOVERED: ft.Colors.WHITE},
                            shape={ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=0)},
                        ),
                        on_click=self.on_click,
                    )


class DateColumn_():
    def __init__(self, text:str):
        self.text = text

    def create(self):
        return ft.DataColumn(
                ft.Text(
                    self.text,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color= ft.Colors.BLACK54,
                    col={"sm": 6, "md": 4, "xl": 2},               
                ), 
                )

class Text_():
    def __init__(self, value, color=ft.Colors.WHITE):
        self.value = value
        self.color = color

    def create(self):
        return ft.Text(
        value=self.value,
        size=20,
        weight=ft.FontWeight.BOLD,
        color= self.color,
    )

class Indicator_():
    def __init__(self):
        self.conect = check_internet_connection()

    def create(self):
        if self.conect:
            icon = ft.Icons.NETWORK_WIFI_ROUNDED
            bgcolor = ft.Colors.GREEN_900
            tooltip = "Conectado"
        else:
            icon = ft.Icons.SIGNAL_WIFI_CONNECTED_NO_INTERNET_4_OUTLINED
            bgcolor = ft.Colors.RED_900
            tooltip = "Desconectado"
        return ft.IconButton(
            icon=icon,
            tooltip= tooltip,
            icon_color=bgcolor
        )

class Select_():
    def __init__(self, on_click, options, label: str, value=None):
        self.on_click = on_click
        self.options = options
        self.label = label
        self.value = value

    def create(self):
        o = []
        for option in self.options:
            o.append(ft.dropdown.Option(option))

        return ft.Dropdown(
            label=self.label,
            options=o,
            on_change=self.on_click,
            text_size=12,
            label_style=ft.TextStyle(size=12),
            width=200,
            value=self.value
        )

class AppBar_():
    def __init__(self,controls, name):
        self.controls = controls
        self.name = name

    def create(self):
        return ft.AppBar(
        elevation=1,
        leading_width=50,
        bgcolor= ft.Colors.GREY_300,
        title=ft.Text(
            spans=[
                ft.TextSpan(
                    self.name,
                    ft.TextStyle(
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (0, 200), (400, 200), ["#000000", "#000010"]
                            )
                        ),
                    ),
                ),
            ],
        ),
        actions=[
            ft.Row(controls=self.controls, spacing=20),
        ],
    )