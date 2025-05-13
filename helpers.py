import pandas as pd
import gspread
import base64
import datetime
import platform
import subprocess
import socket
import flet as ft
import json
import config
import win32print


def read_json(path):
    """
    Reads a JSON file and returns a dictionary with the data and a boolean
    indicating whether all required variables have values.

    Parameters
    ----------
    path : str
        The path to the JSON file.

    Returns
    -------
    dict
        A dictionary with the data and a boolean indicating whether all required
        variables have values. The boolean value is True if all required variables
        have values, and False otherwise.
    """
    data = json.dumps(path, indent=4, ensure_ascii=False)
    data = json.loads(data)
    if data["var_value_1"] == "" or data["var_value_2"] == "" or data["var_value_3"] == "" or data["var_value_4"] == "":
        var = False
    else:
        var = True
    return {"data": data, "var": var}

#data config
data_config = read_json(config.DATA_CONFIG)
data_config = data_config["data"]

def update_json(data, path):
    """
    Updates a JSON file with the provided data.

    This function writes the given dictionary data to a JSON file at the specified path.
    The data is saved in a human-readable format with an indent of 4 spaces.

    Parameters
    ----------
    data : dict
        The data to be written to the JSON file.
    path : str
        The path to the JSON file where the data should be saved.

    Returns
    -------
    None
    """
    d = config.DATA_CONFIG = data
    print(d)
    # with open(path, "w") as f:
    #     json.dump(config.DATA_CONFIG, f, indent=4)

# def process_printer(printer_handle, content):
#         """
#         Sends a raw print job to the printer.

#         This function sends a raw print job to the printer specified by the printer handle.
#         The content of the print job must be a byte string. The function handles the
#         printer spooler to send the job to the printer.

#         Parameters
#         ----------
#         printer_handle : int
#             The handle of the printer obtained from win32print.OpenPrinter.
#         content : bytes
#             The content of the print job.

#         Returns
#         -------
#         None
#         """
#         try:

#             hJob = win32print.StartDocPrinter(
#                 printer_handle, 1, ("Etiqueta", None, "RAW")
#             )
#             win32print.StartPagePrinter(printer_handle)

#             win32print.WritePrinter(printer_handle, content.encode("utf-8"))

#             win32print.EndPagePrinter(printer_handle)
#             win32print.EndDocPrinter(printer_handle)
#         finally:

#             win32print.ClosePrinter(printer_handle)

def get_data(path):
    """
    Reads a CSV file and returns a pandas DataFrame with the data.

    This function reads a CSV file and returns a pandas DataFrame with the data.

    Parameters
    ----------
    path : str
        The path to the CSV file.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame with the data from the CSV file.
    """
    file = pd.read_csv(path)
    return file


def read_google_sheets():
    """
    Reads a Google Sheets and returns a pandas DataFrame with the data.

    This function reads a Google Sheets using the credentials in the file specified
    in the `data_config` dictionary's `jsonFile` key. The data is read from the first
    worksheet in the spreadsheet and returned as a pandas DataFrame.

    Parameters
    ----------
    None

    Returns
    -------
    pd.DataFrame or None
        A pandas DataFrame with the data from the Google Sheets. If an error occurs
        while reading the sheet, the function returns None.
    """
    filename = data_config["jsonFile"]
    
    try:
        client = gspread.service_account(filename=filename)
        working_sheet = client.open("Networking & Conferencia de Inteligencia Artificial")
        wb_1 =  working_sheet.get_worksheet(0)
        wb_1_names = pd.DataFrame(wb_1.get_all_records())
    except Exception as e:
        wb_1_names = []
    return wb_1_names

def read_var_google_sheets():
    """
    Reads a Google Sheets and returns a list with the names of the variables.

    This function reads a Google Sheets using the credentials in the file specified
    in the `data_config` dictionary's `jsonFile` key. The data is read from the first
    worksheet in the spreadsheet and returned as a list of strings with the names of
    the variables in the first row. If an error occurs while reading the sheet, the
    function returns None.

    Parameters
    ----------
    None

    Returns
    -------
    list or None
        A list with the names of the variables. If an error occurs while reading the
        sheet, the function returns None.
    """
    filename = data_config["jsonFile"]
    
    try:
        client = gspread.service_account(filename=filename)
        working_sheet = client.open("Networking & Conferencia de Inteligencia Artificial")
        wb_1 =  working_sheet.get_worksheet(0)
        wb_1_names = pd.DataFrame(wb_1.row_values(1))
        flat_list = [item for sublist in wb_1_names.values.tolist() for item in sublist]
        wb_1_names = flat_list
    except Exception as e:
        wb_1_names = []
    return wb_1_names


def get_base_64_format(path):
    """
    Gets the base64 string from a given image path.

    Parameters
    ----------
    path : str
        The path to the image file.

    Returns
    -------
    str
        The base64 string of the image file.
    """
    image_path = path

    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_string

def filter_data_today():
    """
    Filters data entries from Google Sheets for today's date.

    This function reads data from Google Sheets and filters out the entries
    that have a Marca temporal matching today's date in the format 'MM/DD/YYYY'.
    If an error occurs during the process, an empty list is returned.

    Returns
    -------
    list
        A list of data entries from Google Sheets for today's date or an empty list if an error occurs.
    """

    today = datetime.datetime.now()
    today = f"{today.month}/{today.day}/{today.year}"
    try:
        data = read_google_sheets()
        data = data[data['Marca temporal'].str.contains(f'^{today}')]
    except Exception as e:
        data = []
    return data

def filter_data_yesterday():
    """
    Filters data entries from Google Sheets for yesterday's date.

    This function reads data from Google Sheets and filters out the entries
    that have a Marca temporal matching yesterday's date in the format 'MM/DD/YYYY'.
    If an error occurs during the process, an empty list is returned.

    Returns
    -------
    list
        A list of data entries from Google Sheets for yesterday's date or an empty list if an error occurs.
    """

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%m/%d/%Y')
    try:  
        data = read_google_sheets()
        data = data[data['Marca temporal'].str.contains(f'^{yesterday}')]
    except Exception as e:
        data = []
    return data


def convert_to_hexadecimal(text):
    """
    Converts a given text to hexadecimal format.

    This function takes a string as input, converts it to uppercase, and returns it as the hexadecimal representation of the string.

    Parameters
    ----------
    text : str
        The string to be converted into hexadecimal format.

    Returns
    -------
    str
        The hexadecimal representation of the input string.
    """
    text = text.upper() 
    return text

def content_qr(url, bussiness_name):
    bar = "\\"
    bussiness_name = convert_to_hexadecimal(bussiness_name)
    content = f"""
        ^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR5,5~SD15^JUS^LRN^CI0^XZ
        ^XA
        ^MMT
        ^PW609
        ^LL0406
        ^LS0
        ^FT150,74^A0N,28,28^FH{bar}^FD{bussiness_name}^FS
        ^FT200,331^BQN,3,9
        ^FH{bar}^FDMA,{url}^FS
        ^PQ1,0,1,Y^XZ
            """
    return content

def get_content(tables, id, name, email, phone, pasion, date, business):
    """
    Generates the content for a PDF417 barcode based on the given data.

    This function takes the given data and formats it according to the
    Zebra Programming Language (ZPL) to generate a PDF417 barcode.

    Parameters
    ----------
    id : str
        The ID of the person.
    name : str
        The name of the person.
    email : str
        The email of the person.
    phone : str
        The phone number of the person.
    pasion : str
        The pasion of the person.
    date : str
        The date of the event.

    Returns
    -------
    str
        The content of the PDF417 barcode in ZPL format.
    """
    bar = "\\"
    if tables == 0:
        tables = id%8 if id%8 != 0 else int(id/8)
    max_length = 60
    passion_lines = [pasion[i:i+30] for i in range(0, len(pasion), 30)]

    if len(pasion) > max_length:
        truncated_passion = pasion[:max_length - 3] + "..."
        passion_lines = [truncated_passion[i:i+30] for i in range(0, len(truncated_passion), 30)]

    passion_content = ""
    y_position = 359
    for line in passion_lines:
        passion_content += f"^FT21,{y_position}^A0N,24,24^FH{bar}^FD{line}^FS\n"
        y_position += 40

    names = name.split(" ")
    if len(names) > 2:
        name = f"{names[0]} {names[1]}"
    else:
        name = name

    content = f"""
                ^XA
                ~TA000
                ~JSN
                ^LT0
                ^MNW
                ^MTD
                ^PON
                ^PMN
                ^LH0,0
                ^JMA
                ^PR8,8
                ~SD15
                ^JUS
                ^LRN
                ^CI27
                ^PA0,1,1,0
                ^XZ
                ^XA
                ^MMT
                ^PW609
                ^LL0406
                ^LS0
                ^FB570,2,0,C
                ^FT10,59^A0N,51,51^FB634,1,13,C^FH{bar}^CI28^FD{business}^FS^CI27
                ^FB570,2,0,C
                ^FT33,183^A0N,55,68^FH{bar}^CI28^FD{name}^FS
                ^CI27
                ^FT30,235^A0N,31,28^FH{bar}^CI28^FD{email}^FS^CI27
                ^FT30,276^A0N,31,28^FH{bar}^CI28^FD{date}^FS^CI27
                ^FT30,318^A0N,31,28^FH{bar}^CI28^FDID: {id}^FS^CI27
                ^FT450,330^BQN,2,5
                ^FH{bar}^FDLA,https://wa.me/{phone}^FS
                ^FT21,172^A0N,57,68^FH{bar}^CI28^FD^FS^CI27
                ^LRY^FO0,7^GB640,0,62^FS^LRN
                ^PQ1,,,Y
                ^XZ
                """
    name = convert_to_hexadecimal(name)
    text_email = ""
    if len(email) > 27:
        text_email = f"^FT645,156^A0I,24,24^FH\^FDCorreo: {email}^FS"
    else:
        text_email = f"^FT645,156^A0I,28,28^FH\^FDCorreo: {email}^FS"

    number_split = business.split(" ")
    if len(number_split) > 2:
        business = f"{number_split[0]} {number_split[1]}"
    content2 = f"""
        ^XA
        ^CI28
        ^POI
        ^LH10,0
        ^PR8,8
        ^MMT
        ^PW655
        ^LL0360
        ^LS0
        ^FT602,312^A0I,26,26^FH\^FDNetworking & Conferencia de Inteligencia Artificial^FS
        ^FT528,231^A0I,41,40^FH\^FD{name}^FS
        ^FT30,240^BQN,2,7
        ^FH\^FDLA,https://wa.me/{phone}^FS
        {text_email}
        ^FT645,110^A0I,28,28^FH\^FDFecha: {date}^FS
        ^FT645,65^A0I,28,28^FH\^FDEmpresa: {business}^FS
        ^FT645,26^A0I,28,28^FH\^FDMesa: {tables}^FS
        ^LRY^FO20,291^GB635,0,59^FS^LRN
        ^CI27
        ^PQ1,,,Y
        ^XZ




        """
    return content2



def list_active_printers():
    """
    Returns a list of active printers on the system.

    This function uses different methods for Windows, Linux, and macOS to
    determine which printers are active. On Windows, it uses the win32print
    module to query the print spooler. On Linux and macOS, it uses the
    lpstat command to get the status of the printers.

    Returns an empty list if no active printers are found or if the
    system is not supported.

    :return: A list of active printer names
    """
    system = platform.system()
    if system == "Windows":
        import win32print
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        # Filter only active printers
        active_printers = []
        for printer in printers:
            handle = win32print.OpenPrinter(printer[2])
            status = win32print.GetPrinter(handle, 2)  # Level 2 for detailed info
            if status['Status'] == 0:  # Status 0 usually means active/ready
                active_printers.append(printer[2])
            win32print.ClosePrinter(handle)
        return active_printers
    elif system in ["Linux", "Darwin"]:  # Darwin is macOS
        result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            active_printers = [
                line.split(" ")[1]
                for line in lines
                if "idle" in line.lower() or "printing" in line.lower()
            ]
            return active_printers
        else:
            return []
    else:
        return []

def check_internet_connection(host="www.google.com", port=80, timeout=5):
    """Check if there is an active internet connection.

    This function attempts to open a socket to the specified host and port.
    If the connection is successful, it returns True. Otherwise, it returns False.

    Parameters
    ----------
    host : str, default www.google.com
        The host to check for an active internet connection.
    port : int, default 80
        The port to check for an active internet connection.
    timeout : int, default 5
        The timeout in seconds for the socket connection.

    Returns
    -------
    bool
        True if an active internet connection is available, False otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection((host, port))
        return True
    except OSError:
        return False

def on_dialog_result(e: ft.FilePickerResultEvent):
    """Called when the file picker dialog is closed.

    Parameters
    ----------
    e : flet.FilePickerResultEvent
        The event object containing the result of the file picker dialog.

    Notes
    -----
    This function is called when the user selects a file in the file picker dialog
    and clicks the "Open" button. The selected file path is printed to the console.
    """
    file_path = str(e.files[0]).split('path=')[1].split(',')[
        0][1:-1].replace('\\\\', '/')
    
    return file_path


def send_to_printer(printer_handle, content):
    try:

            hJob = win32print.StartDocPrinter(
                printer_handle, 1, ("Etiqueta", None, "RAW")
            )
            win32print.StartPagePrinter(printer_handle)

            win32print.WritePrinter(printer_handle, content.encode("utf-8"))

            win32print.EndPagePrinter(printer_handle)
            win32print.EndDocPrinter(printer_handle)
    finally:

            win32print.ClosePrinter(printer_handle)


def list_active_printers():
    """
    Returns a list of active printers on the system.

    This function uses different methods for Windows, Linux, and macOS to
    determine which printers are active. On Windows, it uses the win32print
    module to query the print spooler. On Linux and macOS, it uses the
    lpstat command to get the status of the printers.

    Returns an empty list if no active printers are found or if the
    system is not supported.

    :return: A list of active printer names
    """
    system = platform.system()
    if system == "Windows":
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        # Filter only active printers
        active_printers = []
        for printer in printers:
            handle = win32print.OpenPrinter(printer[2])
            status = win32print.GetPrinter(handle, 2)  # Level 2 for detailed info
            if status['Status'] == 0:  # Status 0 usually means active/ready
                active_printers.append(printer[2])
            win32print.ClosePrinter(handle)
        return active_printers
    elif system in ["Linux", "Darwin"]:  # Darwin is macOS
        result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            active_printers = [
                line.split(" ")[1]
                for line in lines
                if "idle" in line.lower() or "printing" in line.lower()
            ]
            return active_printers
        else:
            return []
    else:
        return []
    