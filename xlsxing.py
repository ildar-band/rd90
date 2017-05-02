from openpyxl import Workbook, load_workbook

def list_from_xlsx(file_path):
    wb = load_workbook(file_path)
    ws = wb.active
    val_list = []
    for row_number, row in enumerate(ws.rows):
        val_list.append([])
        for cell in row:
            val_list[row_number].append(cell.value.replace(',', '.').replace('-', '').replace('*', ''))
    return val_list

# list_from_xlsx(path)