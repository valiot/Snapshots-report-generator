import os
from .config import setup_gql
from src.reports.B1.Mill.rawMaterial import rm_report
from src.reports.B1.Mill.waterFlow import wf_report

def main_menu():
  print()
  print("--- Generacion de Reportes ---")
  print()
  print("Opciones:")
  print("Materia Prima\t[MP]")
  print("Caudal de Agua\t[CA]")
  print("Salir\t\t[E]")
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
  else:
    print("Opcion no disponible")
