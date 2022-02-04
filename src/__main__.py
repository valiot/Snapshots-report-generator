import os
from .config import setup_gql
from src.reports.B1.Mill.rawMaterial import rm_report
from src.reports.B1.Mill.waterFlow import wf_report
from src.reports.B2.Atomizer.burnerDamper import bd_report
from src.reports.B2.Atomizer.pumpPressure import pp_report

def main_menu():
  print()
  print("--- Generacion de Reportes ---")
  print()
  print("Opciones:")
  print("Materia Prima\t\t[MP]")
  print("Caudal de Agua\t\t[CA]")
  print("Compuerta de Quemador\t[CQ]")
  print("Presion de Bomba\t[PB]")
  print("Salir\t\t\t[E]")
  ans  = input(">> ")
  return ans


def date_menu():
  print()
  print("Ingrese la fecha deseada:")
  ans = input(">> ")
  return ans


gql = setup_gql()
opt = "BEGIN"

while opt.upper() != "E":
  opt = main_menu()
  if opt.upper() == "MP":
    date = date_menu()
    rm_report(date)
  elif opt.upper() == "CA":
    date = date_menu()
    wf_report(date)
  elif opt.upper() == "CQ":
    date = date_menu()
    bd_report(date)
  elif opt.upper() == "PB":
    date = date_menu()
    pp_report(date)
  elif opt.upper() == "E":
    print("Programa terminado")
  else:
    print("Opcion no disponible")
