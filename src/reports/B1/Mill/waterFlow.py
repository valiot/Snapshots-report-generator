import xlsxwriter
from ...modules import queries as q
from datetime import datetime, timedelta

def wf_report(date):
  print()
  print("Beginning Water Flow report generation")
  print()
  
  try:
    date_begin = datetime.strptime(date,"%d/%m/%y")
    date_init = date_begin.date().strftime("%Y-%m-%dT") + "00:30:00Z"
    date_begin += timedelta(days=1)
    date_end = date_begin.date().strftime("%Y-%m-%dT") + "00:30:00Z"
    
    print("Begin date: ",date_init)
    print("End date: ",date_end)
    
    
    b1_wf_sn = "WATER_FLOW_SNAPSHOT"
    current_snapshots = q.getSnapshots(b1_wf_sn,date_init,date_end)
    if current_snapshots:
      dates = []
      data = []
      density = []
      viscosity=[]
      water_flow=[]
      density_setpoint=[]
      viscosity_setpoint=[]
      water_flow_ctrl=[]
      water_flow_nn=[]
      
      if type(current_snapshots).__name__ == "list":
        for i, x in enumerate(current_snapshots):
          dates.append(x["insertedAt"])
          data.append(x["data"])
      else:
        dates = [current_snapshots["insertedAt"]]
        data = [current_snapshots["data"]]

      for i, x in enumerate(data):
        for j, y in enumerate(x):
          if y["variable"]["code"] == "DENSITY_GRINDING":
            density.append(y["value"])
          elif y["variable"]["code"] == "VISCOSITY_GRINDING":
            viscosity.append(y["value"])
          elif y["variable"]["code"] == "WATER_FLOW_GRINDING":
            water_flow.append(y["value"])
          elif y["variable"]["code"] == "VISCOSITY_GRINDING_SETPOINT":
            viscosity_setpoint.append(y["value"])
          elif y["variable"]["code"] == "DENSITY_GRINDING_SETPOINT":
            density_setpoint.append(y["value"])
          elif y["variable"]["code"] == "WATER_FLOW_GRINDING_CTRL":
            water_flow_ctrl.append(y["value"])
          elif y["variable"]["code"] == "WATER_FLOW_GRINDING_NN":
            water_flow_nn.append(y["value"])
      
      workbook = xlsxwriter.Workbook('Reporte Caudal Agua.xlsx')
      worksheet = workbook.add_worksheet('Bloque 1')
      
      # Merging cells
      merge_format = workbook.add_format({'align': 'center','bold':True,'border':2})
      cell_format = workbook.add_format({'align':'center','bold':False,'border':2})
      worksheet.merge_range('B1:C1', 'Variables', merge_format)
      worksheet.merge_range('D1:E1', 'Setpoints', merge_format)
      worksheet.merge_range('G1:H1', 'Controladores', merge_format)
      worksheet.write('F1','Estado Actual',cell_format)
      worksheet.write('A2','Fecha',cell_format)
      worksheet.write('B2','Viscosidad',cell_format)
      worksheet.write('C2','Densidad',cell_format)
      worksheet.write('D2','Viscosidad',cell_format)
      worksheet.write('E2','Densidad',cell_format)
      worksheet.write('F2','Caudal M.P.',cell_format)
      worksheet.write('G2','FL',cell_format)
      worksheet.write('H2','NN',cell_format)
      
      for i in range(len(dates)):
        pos = i+3
        worksheet.write('A{}'.format(pos),str(dates[i]))
      
      for i in range(len(viscosity)):
        pos = i+3
        worksheet.write('B{}'.format(pos),str(viscosity[i]))
        
      for i in range(len(density)):
        pos = i+3
        worksheet.write('C{}'.format(pos),str(density[i]))
      
      for i in range(len(viscosity_setpoint)):
        pos = i+3
        worksheet.write('D{}'.format(pos),str(viscosity_setpoint[i]))
      
      for i in range(len(density_setpoint)):
        pos = i+3
        worksheet.write('E{}'.format(pos),str(density_setpoint[i]))
      
      for i in range(len(water_flow)):
        pos = i+3
        worksheet.write('F{}'.format(pos),str(water_flow[i]))
      
      for i in range(len(water_flow_ctrl)):
        pos = i+3
        worksheet.write('G{}'.format(pos),str(water_flow_ctrl[i]))

      for i in range(len(water_flow_nn)):
        pos = i+3
        worksheet.write('H{}'.format(pos),str(water_flow_nn[i]))
      
      workbook.close()
    
  except Exception as e:
    print("An error occured with ",e.__class__)
