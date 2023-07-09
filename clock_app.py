import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from datetime import datetime
from kivy.clock import Clock


class ClockApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Label para exibir a hora
        self.time_label = Label(text='00:00:00', font_size=50)
        layout.add_widget(self.time_label)

        # Botões para controlar o cronômetro e o temporizador
        self.start_button = Button(text='Iniciar', on_press=self.start_timer)
        self.stop_button = Button(text='Parar', on_press=self.stop_timer, disabled=True)
        self.timer_button = Button(text='Temporizador', on_press=self.show_timer_popup)
        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)
        layout.add_widget(self.timer_button)

        # Criação do menu
        self.menu = DropDown()
        self.menu_button = Button(text='Menu', on_release=self.menu.open)
        self.menu.bind(on_select=self.menu_option_selected)
        self.menu.add_widget(Button(text='Opção 1', size_hint_y=None, height=40))
        self.menu.add_widget(Button(text='Opção 2', size_hint_y=None, height=40))
        self.menu.add_widget(Button(text='Opção 3', size_hint_y=None, height=40))
        layout.add_widget(self.menu_button)

        return layout

    def update_time(self, dt):
        # Atualiza o label da hora
        now = datetime.now()
        self.time_label.text = now.strftime('%H:%M:%S')

    def start_timer(self, instance):
        # Inicia o cronômetro
        self.timer_event = Clock.schedule_interval(self.update_time, 1)
        self.start_button.disabled = True
        self.stop_button.disabled = False

    def stop_timer(self, instance):
        # Para o cronômetro
        self.timer_event.cancel()
        self.start_button.disabled = False
        self.stop_button.disabled = True

    def show_timer_popup(self, instance):
        # Exibe o popup para configurar o temporizador
        content = GridLayout(cols=2, spacing='10dp')
        content.add_widget(Label(text='Tempo (segundos):'))
        self.timer_input = TextInput(multiline=False)
        content.add_widget(self.timer_input)
        content.add_widget(Button(text='Iniciar', on_press=self.start_timer_countdown))
        content.add_widget(Button(text='Cancelar', on_press=self.dismiss_popup))
        self.popup = Popup(title='Configurar Temporizador', content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()

    def start_timer_countdown(self, instance):
        # Inicia a contagem regressiva do temporizador
        try:
            seconds = int(self.timer_input.text)
            if seconds <= 0:
                raise ValueError
            self.dismiss_popup()
            self.timer_event = Clock.schedule_interval(self.update_timer_countdown, 1)
            self.timer_countdown = seconds
            self.timer_button.disabled = True
        except ValueError:
            self.dismiss_popup()
            self.show_error_popup('Valor inválido', 'Digite um valor inteiro maior que zero.')

    def update_timer_countdown(self, dt):
        # Atualiza a contagem regressiva do temporizador
        if self.timer_countdown > 0:
            self.time_label.text = f'Temporizador: {self.timer_countdown}'
            self.timer_countdown -= 1
        else:
            self.timer_event.cancel()
            self.time_label.text = 'Temporizador finalizado'
            self.timer_button.disabled = False

    def dismiss_popup(self, instance=None):
        # Fecha o popup
        self.popup.dismiss()

    def show_error_popup(self, title, message):
        # Exibe um popup de erro
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        ok_button = Button(text='OK', size_hint=(None, None), size=(100, 40))
        content.add_widget(ok_button)
        self.error_popup = Popup(title=title, content=content, size_hint=(None, None), size=(300, 200))
        ok_button.bind(on_press=self.dismiss_error_popup)
        self.error_popup.open()

    def dismiss_error_popup(self, instance):
        # Fecha o popup de erro
        self.error_popup.dismiss()

    def menu_option_selected(self, instance, option):
        # Ação quando uma opção do menu é selecionada
        self.menu_button.text = option
        self.menu.dismiss()

if __name__ == '__main__':
    ClockApp().run()
