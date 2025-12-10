import pandas as pd                 # Se utiliza para manipular y analizar datos en tablas (DataFrames).
import numpy as np                  # Se utiliza para operaciones numéricas y manejar valores nulos (np.nan).
import matplotlib.pyplot as plt     # Se utiliza para generar gráficos visuales (barras, quesitos, etc.).
import pyperclip                    # Se utiliza para interactuar con el portapapeles (copiar/pegar texto).
from datetime import date           # Se utiliza para obtener la fecha actual y operar con calendarios.
import os                           # Se utiliza para obtener las rutas y trabajar con rutas relativas.

# Rutas del proyecto y carpeta 'data' donde se encuentran los CSV
RUTA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_DATA = os.path.join(os.path.dirname(RUTA_ACTUAL), 'data')

# Función principal que gestiona el menú y la interacción con el usuario
def main():
    # Carga los datos desde archivos CSV
    df_multas_old, df_jugadores, df_motivos = obtenerInfo()
    # Copia del DataFrame de multas para trabajar sin modificar el original
    df_multas_new = df_multas_old.copy()

    # Validación de que los CSV de jugadores y motivos no estén vacíos
    if any(df.empty for df in [df_jugadores, df_motivos]):
        print("Los motivos y jugadores no pueden estar vacíos")
    else:
        print("Información cargada correctamente")
        seguir = True
        while seguir:
            # Menú de opciones para el usuario
            opc = input("¿Qué quieres hacer?\n\t1 - Crear una nueva multa \
            \n\t2 - Marcar una multa como pagada\n\t3 - Doblar una multa\n\t4 - Copiar el mensaje\n\t5 - Mostrar estadísticas \
            \n\tS/Save/Guardar - Guardar la información modificada\n\tE/Exit/Salir - Salir\n").upper()
            # Cada opción llama a la función correspondiente y opcionalmente guarda cambios
            if opc == '1':
                df_multas_new, guardar = crearMulta(df_multas_new, df_jugadores, df_motivos)
                if guardar is not None and guardar:
                    guardarInformacion(df_multas_old, df_multas_new)
            elif opc == '2':
                df_multas_new, guardar = marcarPagado(df_multas_new)
                if guardar is not None and guardar:
                    guardarInformacion(df_multas_old, df_multas_new)
            elif opc == '3':
                df_multas_new, guardar = doblarMulta(df_multas_new)
                if guardar is not None and guardar:
                    guardarInformacion(df_multas_old, df_multas_new)
            elif opc == '4':
                copiarMensaje(df_multas_new)
            elif opc == '5':
                mostrarEstadisticas(df_multas_new, df_jugadores, df_motivos)
            elif opc in ['S', "SAVE", "GUARDAR"]:
                guardarInformacion(df_multas_old, df_multas_new)
            elif opc in ['E', "EXIT", "SALIR"]:
                seguir = False
            else:
                print(f'"{opc}" no es una opción válida')

# Función para cargar la información desde los CSV
def obtenerInfo() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df_multas = pd.read_csv(os.path.join(RUTA_DATA, "multas.csv"), encoding='utf-8')
    df_jugadores = pd.read_csv(os.path.join(RUTA_DATA, "jugadores.csv"), encoding='utf-8')
    df_motivos = pd.read_csv(os.path.join(RUTA_DATA, "motivos.csv"), encoding='utf-8')

    return df_multas, df_jugadores, df_motivos

# Función para crear una nueva multa
def crearMulta(df_multas: pd.DataFrame, df_jugadores: pd.DataFrame, df_motivos: pd.DataFrame) -> tuple[pd.DataFrame, bool] | tuple[None, None]:
    jugadorId, motivoId, fecha = None, None, None
    cancel, seguir = False, True

    # Selección del jugador
    while seguir and not cancel:
        entrada = input(f"Escribe el código del jugador (Cancel/C para salir):\n {df_jugadores['NOMBRE'].to_string(index = True)}\n").strip()
        if entrada.upper() in ['C', "CANCEL"]:
            cancel = True
        elif not entrada.isdigit() or int(entrada) not in df_jugadores.index.to_list():
            print(f'"{entrada}" no es un índice de la lista de jugadores')
        else:
            jugadorId = int(entrada)
            seguir = False

    # Selección del motivo
    seguir = True
    while seguir and not cancel:
        entrada = input(f"Escribe el código del motivo (Cancel/C para salir):\n {df_motivos['MOTIVO'].to_string(index = True)}\n")
        if entrada.upper() in ['C', "CANCEL"]:
            cancel = True
        elif not entrada.isdigit() or int(entrada) not in df_motivos.index.to_list():
            print(f'"{entrada}" no es un índice de la lista de motivos')
        else:
            motivoId = int(entrada)
            seguir = False

    # Ingreso de la fecha de la multa
    seguir = True
    while seguir and not cancel:
        fecha = input(f"Introduce la fecha en la que se ha impuesto la multa en formato (dd/mm/yyyy) (Cancel/C para salir)\n")
        if fecha.upper() in ['C', "CANCEL"]:
            cancel = True
        elif len(fecha) != 10 or fecha[2] != '/' or fecha[5] != '/':
            print("El formato de la fecha no es correcto, introdúcela en formato (dd/mm/yyyy); EJ: (26/11/2025)")
        else:
            seguir = False
    
    # Si se cancela la operación
    if cancel:
        print("Operación cancelada correctamente")
        return df_multas, None
    else:
        # Crear nueva multa y añadir al DataFrame
        nuevaMulta = pd.Series({"NOMBRE": df_jugadores.loc[jugadorId, 'NOMBRE'], "FECHA": fecha, "FECHA_PAGADO": np.nan, "MOTIVO": df_motivos.loc[motivoId, 'MOTIVO'], "DINERO": df_motivos.loc[motivoId, 'PRECIO'], "¿PAGADO?": "NO"})
        df_multas = pd.concat([df_multas, nuevaMulta.to_frame().T], ignore_index = True)
        # Preguntar si desea guardar cambios inmediatamente
        res = input("Información modificada correctamente, quieres guardar la información en la base de datos directamente? (S/N)").upper()
        return df_multas, res in ['S', 'Y', "SI", "YES", "TRUE"]

# Función para marcar una multa como pagada
def marcarPagado(df_multas: pd.DataFrame) -> tuple[pd.DataFrame, bool | None]:
    multaId, fecha = None, None
    seguir, cancel = True, False

    # Filtra las multas no pagadas
    mask = df_multas["¿PAGADO?"] == "NO"

    # Selección de la multa a pagar
    while seguir and not cancel:
        entrada = input(f"Escribe el código de la multa para pagar (Cancel/C para salir):\n {df_multas[mask].to_string()}\n")
        if entrada.upper() in ['C', "CANCEL"]:
            cancel = True
        elif not entrada.isdigit() or int(entrada) not in df_multas[mask].index.to_list():
            print(f'"{entrada}" no es un índice de la lista de multas sin pagar')
        else:
            multaId = int(entrada)
            seguir = False
    
    # Ingreso de la fecha de pago
    seguir = True
    while seguir and not cancel:
        fecha = input(f"Introduce la fecha en la que se ha pagado la multa en formato (dd/mm/yyyy) (Cancel/C para salir)\n")
        if fecha.upper() in ['C', "CANCEL"]:
            cancel = True
        elif len(fecha) != 10 or fecha[2] != '/' or fecha[5] != '/':
            print("El formato de la fecha no es correcto, introdúcela en formato (dd/mm/yyyy); EJ: (26/11/2025)")
        else:
            seguir = False

    # Si se cancela la operación
    if cancel:
        print("Operación cancelada correctamente")
        return df_multas, None
    else:
        # Actualiza la multa con la fecha de pago y marca como pagada
        df_multas.loc[multaId, "FECHA_PAGADO"] = fecha
        df_multas.loc[multaId, "¿PAGADO?"] = "SI"
        # Preguntar si desea guardar cambios inmediatamente
        res = input("Información modificada correctamente, quieres guardar la información en la base de datos directamente? (S/N)").upper()
        return df_multas, res in ['S', 'Y', "SI", "YES", "TRUE"]

# Función para doblar el valor de una multa
def doblarMulta(df_multas: pd.DataFrame) -> tuple[pd.DataFrame, bool | None]:
    multaId = None
    cancel, seguir = False, True
    hoy = date.today()

    # Filtra multas no pagadas y cuya fecha sea anterior a hoy
    mask = (df_multas["¿PAGADO?"] == "NO") & (df_multas["FECHA"].str[3:5].astype(int) < hoy.month) & (df_multas["FECHA"].str[:2].astype(int) <= hoy.day)

    # Selección de la multa a doblar
    while seguir and not cancel:
        entrada = input(f"Escribe el código de la multa para pagar:\n {df_multas[mask].to_string()}\n")
        if entrada.upper() in ['C', "CANCEL"]:
            cancel = True
        elif not entrada.isdigit() or int(entrada) not in df_multas[mask].index.to_list():
            print(f'"{entrada}" no es un índice de la lista de multas sin pagar')
        else:
            multaId = int(entrada)
            seguir = False

    # Si se cancela la operación
    if cancel:
        print("Operación cancelada correctamente")
        return df_multas, None
    else:
        # Duplicar el valor de la multa seleccionada
        df_multas.loc[multaId, "DINERO"] *= 2
        # Preguntar si desea guardar cambios inmediatamente
        res = input("Información modificada correctamente, quieres guardar la información en la base de datos directamente? (S/N)").upper()
        return df_multas, res in ['S', 'Y', "SI", "YES", "TRUE"]

# Función para copiar todas las multas al portapapeles como texto
def copiarMensaje(df_multas: pd.DataFrame):
    msg = ""

    multas = df_multas.values.tolist()
    # Crear el mensaje
    for i in range(len(multas)):
        msg += f"Multa {i+1}\n\t- Nombre: {multas[i][0]}\n\t- Fecha: {multas[i][1]}"
        if pd.notna(multas[i][2]):
            msg += f"\n\t- Fecha pagado: {multas[i][2]}"
        msg+= f"\n\t- Motivo: {multas[i][3]}\n\t- Dinero: {multas[i][4]}€\n\t- ¿Pagado?: {multas[i][5]}\n"
    
    # Copia el mensaje al portapapeles
    pyperclip.copy(msg)
    print(f"Se ha copiado el siguiente mensaje:\n{msg}")

# Función para mostrar estadísticas gráficas de las multas
def mostrarEstadisticas(df_multas: pd.DataFrame):
    num_multas = df_multas["NOMBRE"].value_counts()
    nombres = [i.split(" ")[0] for i in num_multas.index.tolist()] # Se usa el primer nombre
    cant = num_multas.values.tolist()

    # Crear gráficos de barras y pastel
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.bar(nombres, cant)
    ax1.set_title("Cantidad de Multas")
    ax2.pie(cant, labels=nombres)
    ax2.set_title("Reparto de Infracciones")
    plt.tight_layout()
    plt.show()

# Función para guardar la información modificada en CSV
def guardarInformacion(df_multas_old: pd.DataFrame, df_multas_new: pd.DataFrame):
    if df_multas_new.equals(df_multas_old):
        print("No se ha modificado ninguna información, realiza algún cambio para poder guardar.")
    else:
        df_multas_new.to_csv(os.path.join(RUTA_DATA, "multas.csv"), index = False, sep = ',', encoding='utf-8')
        print("Información guardada correctamente.")

# Ejecuta la función principal si se ejecuta el script
if __name__ == "__main__":
    main()