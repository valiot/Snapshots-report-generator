import xlsxwriter
from ...modules import queries as q
from datetime import datetime, timedelta


def bd_report(date):
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
        
        b2_bd_sn = "BURNER_DAMPER_SNAPSHOT"
        current_snapshots = q.getSnapshots(b2_bd_sn, date_init, date_end)
        
        if current_snapshots:
            dates = []
            data = []
            performance = []
            humidity = []
            burner_damper = []
            performance_sp = []
            humidity_sp = []
            burner_damper_ctrl = []
            burner_damper_nn = []
            
            if type(current_snapshots).__name__ == "list":
                for i, x in enumerate(current_snapshots):
                    dates.append(x["insertedAt"])
                    data.append(x["data"])
            else:
                dates = [current_snapshots["insertedAt"]]
                data = [current_snapshots["data"]]
            
            for i, x in enumerate(data):
                for j, y in enumerate(x):
                    if y["variable"]["code"] == "Atomizador_Rendimiento":
                        performance.append(y["value"])
                    elif y["variable"]["code"] == "Atomizador_Humedad_PolvoAtomizado":
                        humidity.append(y["value"])
                    elif y["variable"]["code"] == "Atomizador_Apertura_CompuertaQuemador":
                        burner_damper.append(y["value"])
                    elif y["variable"]["code"] == "Atomizador_Humedad_PolvoAtomizado_setpoint":
                        humidity_sp.append(y["value"])
                    elif y["variable"]["code"] == "Atomizador_Rendimiento_setpoint":
                        performance_sp.append(y["value"])
                    elif y["variable"]["code"] == "Atomizador_Apertura_CompuertaQuemador_CTRL":
                        burner_damper_ctrl.append(y["value"])
                    elif y["variable"]["code"] == "Atomizador_Apertura_CompuertaQuemador_NN":
                        burner_damper_nn.append(y["value"])
            
            # Generate Excel Workbook
            workbook = xlsxwriter.Workbook('Reporte Apertura Compuerta Quemador.xlsx')
            worksheet = workbook.add_worksheet('Bloque 2')
            
            # Cell formatting
            merge_format = workbook.add_format({'align': 'center', 'bold': True, 'border': 2})
            cell_format = workbook.add_format({'align': 'center', 'bold': False, 'border': 2})
            
            # Adding information to cells
            worksheet.merge_range('B1:C1', 'Variables', merge_format)
            worksheet.merge_range('D1:E1', 'Setpoints', merge_format)
            worksheet.merge_range('G1:H1', 'Controladores', merge_format)
            worksheet.write('F1', 'Estado Actual', cell_format)
            worksheet.write('A2', 'Fecha', cell_format)
            worksheet.write('B2', 'Humedad', cell_format)
            worksheet.write('C2', 'Rendimiento', cell_format)
            worksheet.write('D2', 'Humedad', cell_format)
            worksheet.write('E2', 'Rendimiento', cell_format)
            worksheet.write('F2', 'Comp. Quemador', cell_format)
            worksheet.write('G2', 'FL', cell_format)
            worksheet.write('H2', 'NN', cell_format)
            
            for i in range(len(dates)):
                pos = i + 3
                worksheet.write('A{}'.format(pos), str(dates[i]))
            
            for i in range(len(humidity)):
                pos = i + 3
                worksheet.write('B{}'.format(pos), str(humidity[i]))
            
            for i in range(len(performance)):
                pos = i + 3
                worksheet.write('C{}'.format(pos), str(performance[i]))
            
            for i in range(len(humidity_sp)):
                pos = i + 3
                worksheet.write('D{}'.format(pos), str(humidity_sp[i]))
            
            for i in range(len(performance_sp)):
                pos = i + 3
                worksheet.write('E{}'.format(pos), str(performance_sp[i]))
            
            for i in range(len(burner_damper)):
                pos = i + 3
                worksheet.write('F{}'.format(pos), str(burner_damper[i]))
            
            for i in range(len(burner_damper_ctrl)):
                pos = i + 3
                worksheet.write('G{}'.format(pos), str(burner_damper_ctrl[i]))
            
            for i in range(len(burner_damper_nn)):
                pos = i + 3
                worksheet.write('H{}'.format(pos), str(burner_damper_nn[i]))
            
            workbook.close()
            print("Finished report")
        
        else:
            print("No report was generated")
    
    except Exception as e:
        print("An error occurred with ", e.__class__)
