import gi
import os
import pandas as pd
import numpy as np
from enfermedad import Enfermedad
from persona import Persona
from comunidad import Comunidad
from simulacion import Simulacion
from gi.repository import GLib


gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio

def run_simulation():
  
    covid = Enfermedad(nombre='COVID-19', prob_infeccion_familia=0.3, prob_infeccion_conocido=0.1, prom_pasos=80)

  
    personas = Persona.leer_csv_y_crear_personas('ciudadanos.csv', covid)

    comunidades = Comunidad.generar_comunidades(personas, max_personas_por_comunidad=100)
    Comunidad.conectar_personas(personas, max_conocidos= 8)

   
    todas_las_personas = []
    for comunidad in comunidades:
        todas_las_personas.extend(comunidad.personas)

   
    simulacion = Simulacion(covid, todas_las_personas)
    simulacion.simular_sir(dias=400)


class Gtk4TestWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title='Gtk.TreeView Test')

        self.resultados = pd.read_csv('resultados_simulacion.csv')
        self.dia_actual = 0 
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=20,
            margin_top=20, margin_bottom=20,
            margin_start=30, margin_end=30
        )
        self.set_child(box)


        header_bar = Gtk.HeaderBar()
        header_bar.set_show_title_buttons(True)
        self.set_titlebar(header_bar)
        self.set_title("Experimento N°2.131")

        self.tiempo_mas = Gtk.Button(label="Pasar un día")
        self.tiempo_mas.connect("clicked", self.on_clicked_tiempo_mas_dia)
        header_bar.pack_end(self.tiempo_mas)

        self.tiempo_mas = Gtk.Button(label="Pasar un mes")
        self.tiempo_mas.connect("clicked", self.on_clicked_tiempo_mas_mes)
        header_bar.pack_end(self.tiempo_mas)

        self.tiempo_menos = Gtk.Button(label="Retroceder un día")
        self.tiempo_menos.connect("clicked", self.on_clicked_tiempo_menos_dia)
        header_bar.pack_start(self.tiempo_menos)

        self.tiempo_mas = Gtk.Button(label="Retroceder un mes")
        self.tiempo_mas.connect("clicked", self.on_clicked_tiempo_menos_mes)
        header_bar.pack_start(self.tiempo_mas)

        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        header_bar.pack_end(menu_button)

        menu = Gio.Menu()
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.show_about_dialog)
        self.add_action(about_action)
        menu.append("Acerca de", "win.about")
        menu_button.set_menu_model(menu)

        
        self.liststore = Gtk.ListStore(str, str)

        treeview = Gtk.TreeView(model=self.liststore, vexpand=True)
        treeview.connect('cursor_changed', self.on_cursor_changed)

        for i, column_title in enumerate(['Campo', 'Valor']):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title=column_title, cell_renderer=renderer, text=i)
            treeview.append_column(column)

        box.append(treeview)

        
        
        self.image_view = Gtk.Image.new_from_file('grafico_simulacion.png')
        self.image_view.set_property("hexpand", True) 
        self.image_view.set_property("vexpand", True)  
        self.image_view.set_property("width_request", 600)  
        self.image_view.set_property("height_request", 400) 
        box.append(self.image_view)

        self.mostrar_dia(self.dia_actual)

    def mostrar_dia(self, dia):
        self.liststore.clear()
        dia_data = self.resultados.iloc[dia]
        for i, value in dia_data.items():
            self.liststore.append([i, str(value)])

    def on_clicked_tiempo_mas_dia(self, button):
        if self.dia_actual < len(self.resultados) - 1:
            self.dia_actual += 1
            self.mostrar_dia(self.dia_actual)
        else:
            print("No hay más días para avanzar.")

    def on_clicked_tiempo_mas_mes(self, button):
        nuevo_dia = self.dia_actual + 30
        if nuevo_dia >= len(self.resultados):
            self.dia_actual = len(self.resultados) - 1
        else:
            self.dia_actual = nuevo_dia
        self.mostrar_dia(self.dia_actual)

    def on_clicked_tiempo_menos_dia(self, button):
        if self.dia_actual > 0:
            self.dia_actual -= 1
            self.mostrar_dia(self.dia_actual)
        else:
            print("No hay más días para retroceder.")

    def on_clicked_tiempo_menos_mes(self, button):
        nuevo_dia = self.dia_actual - 30
        if nuevo_dia < 0:
            self.dia_actual = 0
        else:
            self.dia_actual = nuevo_dia
        self.mostrar_dia(self.dia_actual)

    def on_cursor_changed(self, treeview):
        print("TreeView cursor changed")

    def show_about_dialog(self, action, param):
        about_dialog = Gtk.AboutDialog(
            transient_for=self,
            modal=True,
            program_name="proyecto",
            authors=["Diego Brizuela Calaf"],
            copyright="© 2024 Diego Ignacio Brizuela Calaf",
            version="1.0",
            license_type=Gtk.License.GPL_3_0,
        )
        about_dialog.show()

class Gtk4TestApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='org.example.myapp', flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = Gtk4TestWindow(self)
        win.present()

def main():
    run_simulation()
    app = Gtk4TestApp()
    try:
        app.run(None)
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()
