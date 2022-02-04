import xlsxwriter
from ...modules import queries as q
from datetime import datetime, timedelta


def pp_report(date):
    print()
    print("Beginning Burner Damper report generation")
    print()
    
    try:
        date_begin = datetime.strptime(date, "%d/%m/%y")
        date_init = date_begin.date().strftime("%Y-%m-%dT") + "00:30:00Z"
        date_begin += timedelta(days=1)
        date_end = date_begin.date().strftime("%Y-%m-%dT") + "00:30:00Z"
        
        print("Begin date: ", date_init)
        print("End date: ", date_end)
        
        b2_bd_sn = "PUMP_PRESSURE_SNAPSHOT"
        current_snapshots = q.getSnapshots(b2_bd_sn, date_init, date_end)
        
        if current_snapshots:
            dates = []
            data = []
            humidity = []
            pump_pressure = []
            humidity_sp = []
            pump_pressure_ctrl = []
            pump_pressure_nn = []
            
            if type(current_snapshots).__name__ == "list":
                for i, x in enumerate(current_snapshots):
                    dates.append(x["insertedAt"])
                    data.append(x["data"])
            else:
                dates = [current_snapshots["insertedAt"]]
                data = [current_snapshots["data"]]
            
            for i, x in enumerate(data):
                for j, y in enumerate(x):
                    if y["variable"]["code"] == "Atomizador_Humedad_PolvoAtomizado":
                        humidity.append(y["value"])
                    elif y["variable"]["code"] == "Atomizador_Presion_Torre":
                        pump_pressure.append(y["value"])
                    elif y["variable"]["code"] == "Atomizador_Humedad_PolvoAtomizado_setpoint":
                        humidity_sp.append(y["value"])
                    elif y["variable"]["code"] == "Atomizador_Presion_Torre_CTRL":
                        pump_pressure_ctrl.append(y["value"])
                    elif y["variable"]["code"] == "Atomizador_Presion_Torre_NN":
                        pump_pressure_nn.append(y["value"])
            
            # Generate Excel Workbook
            workbook = xlsxwriter.Workbook('Reporte Presion de Bomba.xlsx')
            worksheet = workbook.add_worksheet('Bloque 2')
            
            # Cell formatting
            merge_format = workbook.add_format({'align': 'center', 'bold': True, 'border': 2})
            cell_format = workbook.add_format({'align': 'center', 'bold': False, 'border': 2})
            
            # Adding information to cells
            worksheet.write('B1', 'Variables', cell_format)
            worksheet.write('C1', 'Setpoints', cell_format)
            worksheet.merge_range('E1:F1', 'Controladores', merge_format)
            worksheet.write('D1', 'Estado Actual', cell_format)
            worksheet.write('A2', 'Fecha', cell_format)
            worksheet.write('B2', 'Humedad', cell_format)
            worksheet.write('C2', 'Humedad', cell_format)
            worksheet.write('D2', 'Comp. Quemador', cell_format)
            worksheet.write('E2', 'FL', cell_format)
            worksheet.write('F2', 'NN', cell_format)
            
            for i in range(len(dates)):
                pos = i + 3
                worksheet.write('A{}'.format(pos), str(dates[i]))
            
            for i in range(len(humidity)):
                pos = i + 3
                worksheet.write('B{}'.format(pos), str(humidity[i]))
            
            for i in range(len(humidity_sp)):
                pos = i + 3
                worksheet.write('D{}'.format(pos), str(humidity_sp[i]))
            
            for i in range(len(pump_pressure)):
                pos = i + 3
                worksheet.write('F{}'.format(pos), str(pump_pressure[i]))
            
            for i in range(len(pump_pressure_ctrl)):
                pos = i + 3
                worksheet.write('G{}'.format(pos), str(pump_pressure_ctrl[i]))
            
            for i in range(len(pump_pressure_nn)):
                pos = i + 3
                worksheet.write('H{}'.format(pos), str(pump_pressure_nn[i]))
            
            workbook.close()
            print("Finished report")
        
        else:
            print("No report was generated")
    
    except Exception as e:
        print("An error occurred with ", e.__class__)
