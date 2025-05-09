import flet as ft
import time
from helpers import read_google_sheets, send_to_printer, filter_data_today, read_var_google_sheets, convert_to_hexadecimal, get_content, check_internet_connection, read_json, update_json
import os
import datetime
from components import Button_, Indicator_, Text_, Container_, DateColumn_, Submenu_, TextField_,AppBar_
import config


def main(page: ft.Page):
    
    # global variables
    global active
    global number
    global delta
    global path
    global end
    global data_today
    global text
    global printer_name
    global data
    global column_data
    global act_modal
    global url_qr
    global ip
    global name_GoogleSheet
    printer_name = "" 
    text = "Visitas del día"
    number = 0
    delta = 0
    end = False
    active = False
    url_qr = ""
    ip = ""
    name_GoogleSheet = ""
    column_data = []# read_var_google_sheets()
    # data config
    path_config_json = config.DATA_CONFIG
    data_config = read_json(path_config_json)
    act_modal = data_config["var"]
    data_config = data_config["data"]
    path_dat = data_config["path_dat"]

    def active_service(delta):
        """
        An active service that checks every X seconds for new records in the Google Sheets document; 
        if there are new records, it prints them. If there is no internet, 
        it changes the internet icon to red.
        
        Parameters
        ----------
        delta : int
            N mero de filas que se van a imprimir
        
        Returns
        -------
        None
        """
        global active
        global end
        global data_search
        global path
        global number
        global data
        while active:
            check_internet = check_internet_connection()
            if check_internet:
                internet.icon = ft.Icons.NETWORK_WIFI_ROUNDED
                internet.icon_color = ft.Colors.GREEN_900
                path = path
                if os.path.exists(path):
                    os.remove(path)
                data = read_google_sheets()
                number = delta
                try:
                    delta = len(data)
                except Exception as e:
                    delta = 0
                data_print = []
                if delta != number:
                    try:
                        data_print = data.iloc[number:delta]
                        properties_printer(data_print)
                    except Exception as e:
                        data_print = []

                if len(data_print) > 0:
                    data_print = data_print.rename(
                        columns={"Teléfono": "Telefono", "Pasión": "Pasion"}
                    )
                    data_print.to_csv(path, index=False, sep="\t")

                text_register.value = number
                active_data_today()
            else:
                internet.icon = ft.Icons.SIGNAL_WIFI_CONNECTED_NO_INTERNET_4_OUTLINED
                internet.icon_color = ft.Colors.RED_900             
            page.update()
            time.sleep(5)
            if end:
                active = False
                break

    # functions
    def search_phone_input(_):
        """
        Handles input for phone search.

        This function updates the UI components related to the phone search input. 
        It sets the border color of the input search field to black, hides any warning text, 
        disables the print button, enables the search button, and updates the global 
        variable `data_search` with the input value.

        Parameters
        ----------
        _ : object
            An object that contains a control with a value used for the phone search.
        """
        global data_search
        input_search.border_color =  ft.Colors.BLACK
        btn_print.visible = False
        search_button.visible = True
        text_warning.visible = False
        page.update()
        data_search = _.control.value

    def search_phone():
        """
        Handles phone search button click.

        This function searches for a phone number in the dataframe loaded from the Google Sheets document.
        If a match is found, it updates the UI components to show the print button and hide the search button,
        and makes the input search field empty and black.
        If no match is found, it updates the UI components to show a warning text and sets the border color of the
        input search field to red.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        global data_search
        global data
        try:
            data = read_google_sheets()
            data["Teléfono"] = data["Teléfono"].astype(str)
            data = data[data["Teléfono"].str.contains(f"^{data_search}$")]
        except Exception as e:
            data = []

        if len(data) > 0:
            btn_print.visible = True
            search_button.visible = False
            data = data.iloc[[0]]
            page.update()

        else:
            text_warning.visible = True
            input_search.value = ""
            input_search.border_color =  ft.Colors.RED_900
            page.update()

    

    def print_now(_):
        """
        Prints the first record of the data to the printer.

        This function is called when the print button is clicked. It prints the first record of the data to the printer. If there is no printer selected, it changes the border color of the select printer dropdown to red.

        Parameters
        ----------
        _ : object
            An object that contains the control with the print button.

        Returns
        -------
        None
        """
        global data
        global ip
        element = data.iloc[0]
        name = element[data_config["var_value_1"]]
        name = name.upper()
        name = convert_to_hexadecimal(name)
        idx = element.name + 1
        email = element[data_config["var_value_2"]]
        phone = element[data_config["var_value_4"]]
        pasion = element[data_config["var_value_3"]]
        pasion = pasion.upper()
        pasion = convert_to_hexadecimal(pasion)
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        content = get_content(id=idx, name=name, email=email, phone=phone, pasion=pasion, date=date, business=data_config['bussiness_name'])
        if ip == "":
            printer_select.border_color = ft.Colors.RED_900
        else:
            printer_select.border_color = ft.Colors.BLACK
            send_to_printer(ip=ip, port=9100, content=content)      
            page.update()
            
        page.update()

    def for_in_data(data, column_register):
        """
        Populates a column register with rows of data.

        Iterates through the given data and appends rows to the specified column register. 
        Each row represents a record in the data, with cells containing the index and 
        specific data values extracted from the data configuration.

        Parameters
        ----------
        data : DataFrame
            The data to be iterated over, containing records to populate the column register.
        
        column_register : Component
            The UI component where the rows will be appended. Each row corresponds to a record 
            in the data, and cells are populated with specific data values.
        
        Returns
        -------
        None
        """

        for i in range(len(data)):
            element = data.iloc[i]
            column_register.rows.append(
                
                    ft.DataRow(
                        cells=[
                        ft.DataCell(ft.Text(str(i + 1))),
                        ft.DataCell(ft.Text(str(element[data_config["var_value_1"]]))),
                        ft.DataCell(ft.Text(str(element[data_config["var_value_2"]]))),
                        ft.DataCell(ft.Text(str(element[data_config["var_value_3"]]))),
                        ft.DataCell(ft.Text(str(element[data_config["var_value_4"]]))),
                        ]
                    ) 
            )
        page.update()    
        

    def active_data_today():
        """
        Activates the data today feature.

        Retrieves the data for today, populates the UI component with the data, and updates the UI.
        The data is filtered from the Google Sheets document and the UI component is populated with the
        filtered data. The number of records is displayed in another UI component.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        global data_today
        global text
        data_today = filter_data_today()
        text_rgisters_today.value = len(data_today)
        if data_today is not None and text == "Visitas del día":
            column_register_today.visible = True
            column_register_today.rows = []
            for_in_data(data_today, column_register_today)
        page.update()

    def init_service(delta=0):
        """
        Initializes the service that prints new records from Google Sheets.
        
        Parameters
        ----------
        delta : int, optional
            The number of records to print. Defaults to 0.
        
        Returns
        -------
        None
        """
        global end
        global data
        global number
        global printer_name
        global active
        end = False
        if ip == "":
            printer_select.border_color = ft.Colors.RED_900
            page.update()
        else:
            printer_select.border_color = ft.Colors.BLACK
            page.update()
            conection = check_internet_connection()
            if conection:
                internet.icon = ft.Icons.NETWORK_WIFI_ROUNDED
                internet.icon_color = ft.Colors.GREEN_900
                active_data_today()
                btn_desactive.visible = True
                btn_active.visible = False
                page.update()
                if number == 0:
                    data = read_google_sheets()
                    number = len(data)
                delta = number
                if not active:
                    active = True
                    active_service(delta=number)
                    
            else:
                internet.icon = ft.Icons.SIGNAL_WIFI_CONNECTED_NO_INTERNET_4_OUTLINED
                internet.icon_color = ft.Colors.RED_900  
            page.update()

    def stop_service():
        """
        Stops the service that prints new records from Google Sheets.
        
        This function stops the service that prints new records from Google Sheets.
        It sets the variable `end` to `True` and updates the visibility of the buttons
        to start and stop the service.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        global end
        end = True
        btn_desactive.visible = False
        btn_active.visible = True
        page.update()

    def properties_printer(d=None):
        """
        Processes and sends a print job for each record in the given dataframe.

        This function iterates through the records in the provided dataframe, extracts
        relevant information such as name, email, phone, and pasion, converts them 
        into a specific format, and then sends each record as a print job to the
        designated printer.

        Parameters
        ----------
        d : pandas.DataFrame, optional
            A dataframe containing records to be printed. Each record should have 
            fields corresponding to the keys in the `data_config` dictionary.

        Returns
        -------
        None
        """
        global printer_name
        global ip
        if d is not None:
            for i in range(len(d)):
                element = d.iloc[i]
                name = element[data_config["var_value_1"]]
                name = name.upper()
                name = convert_to_hexadecimal(name)
                idx = element.name + 1
                email = element[data_config["var_value_2"]]
                phone = element[data_config["var_value_4"]]
                pasion = element[data_config["var_value_3"]]
                pasion = pasion.upper()
                date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                content = get_content(id=idx, name=name, email=email, phone=phone, pasion=pasion, date=date, business=data_config['bussiness_name'])
                send_to_printer(ip=ip, port=9100, content=content)

    def action_profile(t):
        """
        Handles navigation between different sections of the application.
        
        This function changes the visibility of UI components based on the value of the
        `text` parameter. It can show or hide the profile, search, data today, historic data,
        help, and about sections.
        
        Parameters
        ----------
        t : str
            The name of the section to show or hide.
        
        Returns
        -------
        None
        """
        global text
        global act_modal
        alert.open = False
        text = t
        if t == "Datos históricos" and act_modal:
            data_historics()
            column_register_today.visible = True
            input_search.visible = True
            help_section.visible = False
            about.visible = False
            btn_print.visible = False
        elif t == "Ayuda":
            input_search.visible = False
            column_register_today.visible = False
            menubar.visible = True
            help_section.visible = True
            about.visible = False
            btn_print.visible = False
        elif t == "Acerca de":
            input_search.visible = False
            column_register_today.visible = False
            about.visible = True
            help_section.visible = False
            btn_print.visible = False

        else:
            column_register_today.visible = True
            help_section.visible = False

        page.update()

    
    def onChange_ip(e):
        global ip
        ip = e.control.value
        page.update()
    # selects
    printer_select = ft.TextField(label="IP de la impresora", on_change= onChange_ip, width=200, height=40)

    #alert
    alert = ft.AlertDialog(
        modal=True,
        title=ft.Text("Configuración"),
        content=ft.Text("Seleccione las variables"),
        actions=[
            ft.TextButton("Configurar", on_click=lambda _: action_profile(t="Mi Perfil")),
        ]
    )
    alert.open = act_modal

    # path of the file
    path = path_dat


    # buttons
    btn_active = Button_(on_click=lambda _: init_service(), text="Iniciar servicios", bgcolor= ft.Colors.BLUE_900, color= ft.Colors.WHITE, icon= ft.Icons.PLAY_ARROW_ROUNDED, width=200, height=40).create()
    btn_desactive = Button_(on_click=lambda _: stop_service(), text="Detener servicios", bgcolor= ft.Colors.RED_900, color= ft.Colors.WHITE, icon= ft.Icons.STOP_ROUNDED, height=40, width=200).create()
    btn_desactive.visible = False
    
    #indicators
    internet = Indicator_().create()

    page.title = "Control de visitas v.1.0"
    page.scroll = True

    # text
    text_register = Text_(value=0).create()
    text_rgisters_today = Text_(value=0).create()
    text_warning = Text_(value="* No se encontró el registro", color= ft.Colors.RED_900).create()
    text_warning.visible = False
 
    # containers, columns and rows
    container_register = Container_(bgcolor= ft.Colors.GREEN_900, text=text_register, title="Registros: ", height=50, width=200).create()
    
    column_register_today = ft.DataTable(
        col={"sm": 6, "md": 4, "xl": 2},
    columns=[
            DateColumn_("Id").create(),
            DateColumn_(data_config["var_value_1"]).create(),
            DateColumn_(data_config["var_value_2"]).create(),
            DateColumn_(data_config["var_value_3"]).create(),
            DateColumn_(data_config["var_value_4"]).create(),
        ], expand=True
    )

    menubar = ft.MenuBar(
        expand=True,
        style=ft.MenuStyle(
            alignment=ft.alignment.top_left,
            bgcolor="#19647E",
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
            },
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Datos", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                controls=[
                    Submenu_(content="Datos históricos", leading=ft.Icon(ft.Icons.DATASET), on_click=lambda _: action_profile(t="Datos históricos")).create(),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Configuración", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                controls=[
                    Submenu_(content="Ayuda", leading=ft.Icon(ft.Icons.HELP_ROUNDED), on_click=lambda _: action_profile(t="Ayuda")).create(),
                    Submenu_(content="Acerca de", leading=ft.Icon(ft.Icons.INFO), on_click=lambda _: action_profile(t="Acerca de")).create(),
                ],
            ),
        ],
    )

    # inputs & buttons
    input_search = TextField_(on_click=lambda _: search_phone(), label="Buscar por teléfono", on_change=lambda _: search_phone_input(_)).create()
    search_button = ft.ElevatedButton("Buscar", on_click=lambda _: search_phone(), bgcolor= "#19647E", height=50,
                                      color= ft.Colors.WHITE, icon= ft.Icons.SEARCH, icon_color= ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)))
    
    btn_print = ft.ElevatedButton("Imprimir", on_click=lambda _: print_now(_), bgcolor= ft.Colors.GREEN_900, height=50,
                                      color= ft.Colors.WHITE, icon= ft.Icons.LOCAL_PRINT_SHOP, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)))
    btn_print.visible = False
    
    #help
    help_section = ft.Column(
        controls=[
            ft.Text(value=data_config["help"], col={"sm": 6, "md": 4, "xl": 3}, size=14, weight=ft.FontWeight.BOLD, color= ft.Colors.BLACK54),
        ]
    )
    about = ft.Column(
        controls=[
            ft.Text(value=f"Autor:  {data_config["about"]["author"]}", col={"sm": 6, "md": 4, "xl": 3}, size=14, weight=ft.FontWeight.BOLD, color= ft.Colors.BLACK54),
            ft.Text(value=f"Versión:  {data_config["about"]['version']}", col={"sm": 6, "md": 4, "xl": 3}, size=14, weight=ft.FontWeight.BOLD, color= ft.Colors.BLACK54),
            ft.Text(value=f"Soporte:  {data_config['about']['support']}", col={"sm": 6, "md": 4, "xl": 3}, size=14, weight=ft.FontWeight.BOLD, color= ft.Colors.BLACK54),
        ]
    )
    about.visible = False


    # HISTORICS DATA
    def data_historics():
        data = read_google_sheets()
        column_register_today.rows = []
        for_in_data(data, column_register_today)
        page.update()

    # page structure
    page.appbar = AppBar_(
        controls=[internet, printer_select, btn_active, btn_desactive, ft.Image(src=data_config["path_logo"])], name=data_config["bussiness_name"]
    ).create()

    # add the page to the app
    page.add(
        ft.Column(
            controls=[
                ft.ResponsiveRow(controls=[menubar]),
                ft.Row(controls=[container_register, input_search, search_button, btn_print]),
                ft.Row(controls=[text_warning]),
                ft.Row(controls=[column_register_today]),
            ],
            expand=True,
        ),
    )
ft.app(main, assets_dir="assets", upload_dir="uploads")