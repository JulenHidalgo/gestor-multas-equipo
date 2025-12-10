# ⚽ Gestor de Multas del Equipo

> Una herramienta CLI (Command Line Interface) en Python para administrar, visualizar y controlar las sanciones económicas de equipos deportivos.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=flat-square&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c?style=flat-square)

## 📖 Descripción

Este proyecto nació de la necesidad de automatizar la gestión de multas de mi equipo de fútbol. Permite llevar un control riguroso de las infracciones, generar estadísticas visuales y facilitar la comunicación de las deudas a través de mensajería instantánea.

Utiliza **Pandas** y **NumPy** para la manipulación eficiente de datos relacionales (CSV) y **Matplotlib** para la generación de reportes gráficos.

## ✨ Funcionalidades Principales

* **📝 Gestión de Multas:** Creación de nuevas sanciones asignando jugador, motivo y fecha.
* **💰 Control de Pagos:** Marcado de multas como pagadas con registro de fecha.
* **⚖️ Doblado de Multas:** Funcionalidad automática para duplicar el importe de multas impagadas tras un periodo de tiempo.
* **📋 Integración con Portapapeles:** Generación automática de mensajes de texto formateados con el resumen de deudas, listos para pegar en WhatsApp/Discord usando `pyperclip`.
* **📊 Estadísticas Visuales:** Generación de gráficos (barras y sectores) para analizar quién es el jugador más multado o qué infracciones son las más comunes.

## 🚀 Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/JulenHidalgo/gestor-multas-equipo.git](https://github.com/JulenHidalgo/gestor-multas-equipo.git)
    cd gestor-multas-equipo
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar los datos:**
    En la carpeta `data/` encontrarás archivos terminados en `-template.csv`.
    
    Elimina el sufijo `-template` del nombre de cada archivo para empezar a usarlos:
    * `jugadores-template.csv` ➡️ `jugadores.csv`
    * `motivos-template.csv` ➡️ `motivos.csv`
    * `multas-template.csv` ➡️ `multas.csv`

4.  **Ejecutar la herramienta:**
    ```bash
    python src/main.py
    ```

## 🔮 Próximas Mejoras (Roadmap)

Este proyecto está en evolución constante. Las siguientes características están planificadas:

- [ ] **Mejora de UX/UI:** Migrar de la consola a una interfaz gráfica (GUI).
- [ ] **Formato de Fechas:** Implementar selectores de fecha automáticos y validación robusta para evitar errores manuales.
- [ ] **Base de Datos:** Migrar de archivos CSV a un gestor de base de datos para mejorar la integridad de los datos.
- [ ] **Bot de Notificaciones:** Integración directa con la API de Telegram/WhatsApp para enviar recordatorios automáticos.

## 📂 Estructura del Proyecto

```text
gestor-multas-equipo/
├── data/               # Archivos CSV de datos y templates
├── src/
│   ├── main.py         # Lógica principal y menús
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación
```

---

<br>
<div align="center">
  <h3>Hecho por Julen Hidalgo</h3>
  <p>Desarrollador de Aplicaciones Multiplataforma | Estudiante de IA & Big Data</p>
  
  <a href="https://github.com/JulenHidalgo">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
  <a href="https://www.linkedin.com/in/julen-hidalgo-chamero-11a70a2bb/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  <a href="https://julenhidalgo.github.io/portfolio-julenhidalgo/Portfolio/html/portfolioJulenHidalgo.html">
    <img src="https://img.shields.io/badge/Portfolio-Visitar_Web-2ea44f?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Portfolio"/>
  </a>
  <a href="mailto:julenhidalgo2005@gmail.com">
    <img src="https://img.shields.io/badge/Email-Contactame-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/>
  </a>
  <a href="https://julenhidalgo.github.io/portfolio-julenhidalgo/Portfolio/assets/cv/JulenHidalgo_CV.pdf">
    <img src="https://img.shields.io/badge/CV-Descargar-FF5722?style=for-the-badge&logo=adobe-acrobat-reader&logoColor=white" alt="CV"/>
  </a>
</div>