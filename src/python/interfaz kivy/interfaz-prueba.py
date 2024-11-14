#// interfaz kivy/interfaz-prueba.py
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.animation import Animation
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
import threading
from threading import Event
from threading import Thread
from audio_capture_spl import start_audio_stream_spl

class AnimatedButton(Button):
    def __init__(self, **kwargs):
        super(AnimatedButton, self).__init__(**kwargs)
        self.original_size = (self.width, self.height)

    def on_press(self):
        Animation.cancel_all(self)
        self.size = self.original_size

        anim = Animation(size=(self.width * 0.95, self.height * 0.95), duration=0.05)
        anim.start(self)

    def on_release(self):
        anim = Animation(size=self.original_size, duration=0.05)
        anim.start(self)

class SPLMeterPopup(Popup):
    def __init__(self, **kwargs):
        super(SPLMeterPopup, self).__init__(**kwargs)
        self.title = "SPL Meter"
        self.size_hint = (0.8, 0.8)
        with self.canvas.before:
            self.bg_rect = Rectangle(source='gradiente.png', size=self.size, pos=self.pos)
        self.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.decibel_label = Label(text="60 dB", font_size=50, color=(1, 1, 1, 1), size_hint=(1, 0.4), valign="middle", halign="center")
        layout.add_widget(self.decibel_label)

        self.recording_label = Label(text="Grabando", font_size=30, color=(1, 0, 0, 1), size_hint=(1, 0.2), valign="middle", halign="center")
        self.recording_label.opacity = 0
        layout.add_widget(self.recording_label)

        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        self.start_button = AnimatedButton(text="Grabar", size_hint=(0.33, 1), background_normal='boton.png', background_down='boton.png')
        self.start_button.bind(on_release=self.start_recording)
        
        self.stop_button = AnimatedButton(text="Stop", size_hint=(0.33, 1), background_normal='boton.png', background_down='boton.png')
        self.stop_button.bind(on_release=self.stop_recording)
        
        self.close_button = AnimatedButton(text="Cerrar", size_hint=(0.33, 1), background_normal='boton.png', background_down='boton.png')
        self.close_button.bind(on_release=self.dismiss)

        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.stop_button)
        button_layout.add_widget(self.close_button)
        
        layout.add_widget(button_layout)
        self.add_widget(layout)

    def update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def start_recording(self, instance):
        self.recording_label.opacity = 1
        self.stop_event = Event()  # Crea un nuevo stop_event para controlar el flujo
        spl_values = [0]  # Inicializa la lista para almacenar valores SPL
        
        # Iniciar el hilo de captura de audio con stop_event
        threading.Thread(target=start_audio_stream_spl, args=(1, 1, 44100, spl_values, 500, self, self.stop_event)).start()

    def stop_recording(self, instance):
        self.recording_label.opacity = 0
        if self.stop_event:
            self.stop_event.set()  # Activa el stop_event para detener la grabación

    def update_decibels(self, db_value):
        print(f"Actualizar los decibelios a {db_value} dB")
        self.decibel_label.text = f"{db_value:.2f} dB"  # Actualiza el valor en la interfaz gráfica

class T60Popup(Popup):
    def __init__(self, **kwargs):
        super(T60Popup, self).__init__(**kwargs)
        self.title = "T60"
        self.size_hint = (0.8, 0.8)
        
        with self.canvas.before:
            self.bg_rect = Rectangle(source='gradiente.png', size=self.size, pos=self.pos)
        
        self.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.decibel_label = Label(text="60 dB", font_size=50, color=(1, 1, 1, 1), size_hint=(1, 0.3), valign="middle", halign="center")
        layout.add_widget(self.decibel_label)
        
        self.recording_label = Label(text="Grabando", font_size=30, color=(1, 0, 0, 1), size_hint=(1, 0.2), valign="middle", halign="center")
        self.recording_label.opacity = 0
        layout.add_widget(self.recording_label)
        
        self.input_field = TextInput(hint_text="Número de grabaciones", font_size=20, multiline=False, input_filter='int', size_hint=(1, 0.2))
        layout.add_widget(self.input_field)

        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        
        self.start_button = AnimatedButton(text="Grabar", size_hint=(0.33, 1), background_normal='boton.png', background_down='boton.png')
        self.start_button.bind(on_release=self.start_recording)
        
        self.stop_button = AnimatedButton(text="Stop", size_hint=(0.33, 1), background_normal='boton.png', background_down='boton.png')
        self.stop_button.bind(on_release=self.stop_recording)
        
        self.close_button = AnimatedButton(text="Cerrar", size_hint=(0.33, 1), background_normal='boton.png', background_down='boton.png')
        self.close_button.bind(on_release=self.dismiss)

        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.stop_button)
        button_layout.add_widget(self.close_button)
        
        layout.add_widget(button_layout)
        
        self.add_widget(layout)

    def update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def start_recording(self, instance):
        try:
            value = int(self.input_field.text)
            if value > 0:
                self.recording_label.opacity = 1
                #Aqui se pasa el valor ingresado al backend(n o i)
                self.send_t60_value(value)
            else:
                self.recording_label.opacity = 0
        except ValueError:
            self.recording_label.opacity = 0

    def stop_recording(self, instance):
        self.recording_label.opacity = 0

    #Funcion para enviar el valor de T60 (vacia de momento)
    def send_t60_value(self, value):
        print(f"Enviar valor T60 al backend: {value}")
        #Aqui va la conexion al backend para enviar el valor de T60

class MyGrid(BoxLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        with self.canvas.before:
            self.bg_rect = Rectangle(source='gradiente.png', size=self.size, pos=self.pos)

        self.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        self.add_widget(Label(text="Bienvenido a RevCal", font_size=40, halign="center", size_hint=(1, 0.1)))

        button_layout = GridLayout(cols=1, rows=2, spacing=20, size_hint=(None, None), width=400)
        button_layout.bind(minimum_height=button_layout.setter('height'))
        button_layout.pos_hint = {'center_x': 0.55}

        self.spl_button = AnimatedButton(text="SPL Meter", size_hint=(None, None), size=(300, 100),
                                         background_normal='boton.png', background_down='boton.png')
        self.spl_button.bind(on_release=self.show_spl_meter)
        button_layout.add_widget(self.spl_button)

        self.t30_button = AnimatedButton(text="T60", size_hint=(None, None), size=(300, 100),
                                         background_normal='boton.png', background_down='boton.png')
        self.t30_button.bind(on_release=self.show_t60_meter)
        button_layout.add_widget(self.t30_button)

        button_container = BoxLayout(orientation='vertical', padding=[0, 150], size_hint=(1, 0.4))
        button_container.add_widget(button_layout)
        self.add_widget(button_container)

        watermark = Label(text="©Creado por tetralogiamarina", font_size=15,
                          halign="left", valign="bottom", size_hint=(None, None), size=(200, 50),
                          pos_hint={'x': 0, 'y': 0})
        self.add_widget(watermark)

    def update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def show_spl_meter(self, instance):
        spl_popup = SPLMeterPopup()
        spl_popup.open()

    def show_t60_meter(self, instance):
        t60_popup = T60Popup()
        t60_popup.open()

class SPLMeterApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    SPLMeterApp().run()