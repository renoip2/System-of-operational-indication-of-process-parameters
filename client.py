# -*- coding: utf-8 -*-
import sys
import os
import time
import socket
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListView
from kivy.uix.listview import ListItemButton
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock

Window.clearcolor = (1, 1, 1, 1)
Config.set('graphics', 'resizable', 0)
Window.size = (540, 960)
Address = []
alarm_list = []
global do_par, di_par, ai_par, hr_par, send_info
do_par = '0, 0, 100'
di_par = '1, 0, 100'
ai_par = '3, 0, 100'
hr_par = '4, 0, 100'
send_info = hr_par


class EmailApp(App):
    def clear_all(self):
        child = self.root.children[:]
        for i in child:
            time.sleep(0.01)
            self.root.remove_widget(i)

    def dismiss_popup(self, instance):
        self._popup.dismiss()

    def do_set(self, instance):
        global do_par, di_par, ai_par, hr_par, send_info
        self.titl.text = 'Цифровые выходы'
        self.but_0x.color = [0, 0, 0, 1]
        self.but_1x.color = [1, 1, 1, 1]
        self.but_3x.color = [1, 1, 1, 1]
        self.but_4x.color = [1, 1, 1, 1]
        send_info = do_par

    def di_set(self, instance):
        global do_par, di_par, ai_par, hr_par, send_info
        self.titl.text = 'Цифровые входы'
        self.but_0x.color = [1, 1, 1, 1]
        self.but_1x.color = [0, 0, 0, 1]
        self.but_3x.color = [1, 1, 1, 1]
        self.but_4x.color = [1, 1, 1, 1]
        send_info = di_par

    def ai_set(self, instance):
        global do_par, di_par, ai_par, hr_par, send_info
        self.titl.text = 'Аналоговые входы'
        self.but_0x.color = [1, 1, 1, 1]
        self.but_1x.color = [1, 1, 1, 1]
        self.but_3x.color = [0, 0, 0, 1]
        self.but_4x.color = [1, 1, 1, 1]
        send_info = ai_par

    def hr_set(self, instance=0):
        global do_par, di_par, ai_par, hr_par, send_info
        self.titl.text = 'Регистры временного\nхранения информации'
        self.but_0x.color = [1, 1, 1, 1]
        self.but_1x.color = [1, 1, 1, 1]
        self.but_3x.color = [1, 1, 1, 1]
        self.but_4x.color = [0, 0, 0, 1]
        send_info = hr_par

    def alarm_popup(self, message):
        b2 = BoxLayout(orientation='vertical', padding=10, spacing=10)
        I1 = Image(source='E:\images\Alarm1.png')
        b2.add_widget(I1)
        popup = Popup(title=message, title_size=22, content=b2,
                      auto_dismiss=False, size_hint=(0.9, 0.5))
        b2.add_widget(Button(text='Принять', on_release=popup.dismiss, font_size=20, size_hint=(1, 0.2)))
        popup.open()

    def error_popup(self, message):
        b2 = BoxLayout(orientation='vertical')
        popup = Popup(title='Ошибка', title_size=22, content=b2, size_hint=(0.9, 0.3))
        b2.add_widget(Label(text=message, font_size=20))
        b2.add_widget(Button(text='OK', on_release=popup.dismiss, size_hint=(1, 0.3)))
        popup.open()

    def alarm_set(self, instance):
        global reg_num
        try:
            flag = False
            if self.down_alarm.text == '':
                flag = True
            else:
                int(self.down_alarm.text)
            if self.up_alarm.text == '':
                flag = True
            else:
                int(self.up_alarm.text)
            if flag == False:
                if int(self.down_alarm.text) >= int(self.up_alarm.text): raise ValueError
            for i in alarm_list:
                if i[0] == reg_num[4:9]:
                    i[1] = self.up_alarm.text
                    i[2] = self.down_alarm.text
                    i[3] = 0
                    break
            else:
                alarm_list.append([reg_num[4:9], self.up_alarm.text, self.down_alarm.text, 0])
                if self.up_alarm.text == '' and self.down_alarm.text == '':
                    alarm_list.pop()
        except ValueError:
            self.error_popup('Неправильно указаны границы')

    def show_popup(self):
        g1 = GridLayout(cols=2, spacing=30, padding=10)
        g1.add_widget(Label(text='Верхняя граница:', font_size=20, halign='left', size_hint=(.6, .1)))
        self.up_alarm = (TextInput(multiline=False, font_size=20))
        g1.add_widget(self.up_alarm)
        g1.add_widget(Label(text='Нижняя граница:', font_size=20, halign='left', size_hint=(.6, .1)))
        self.down_alarm = (TextInput(multiline=False, font_size=20))
        g1.add_widget(self.down_alarm)

        b2 = BoxLayout(orientation='vertical', padding=10)
        b3 = BoxLayout(orientation='horizontal', padding=10, size_hint=(1, .5))
        b3.add_widget(Button(text='Назад', on_release=self.dismiss_popup, font_size=20))
        choose_but = Button(text='Принять', font_size=20, on_press=self.alarm_set, on_release=self.dismiss_popup)
        b3.add_widget(choose_but)
        b2.add_widget(g1)
        b2.add_widget(b3)
        self._popup = Popup(title="Настройка сигнализации", title_size=20, content=b2, size_hint=(0.9, 0.3))
        self._popup.open()

    class list_but(ListItemButton):
        def get_num(self):
            global reg_num
            reg_num = (self.text)

        on_press = get_num

    def save_set(self, instance):
        try:
            global do_par, di_par, ai_par, hr_par, send_info
            do_par = ', '.join(['0', self.do_adr.text, self.do_num.text])
            di_par = ', '.join(['1', self.di_adr.text, self.di_num.text])
            ai_par = ', '.join(['3', self.ai_adr.text, self.ai_num.text])
            hr_par = ', '.join(['4', self.hr_adr.text, self.hr_num.text])
            int(self.do_adr.text)
            int(self.do_num.text)
            int(self.di_adr.text)
            int(self.di_num.text)
            int(self.ai_adr.text)
            int(self.ai_num.text)
            int(self.hr_adr.text)
            int(self.hr_num.text)
        except ValueError:
            self.error_popup('Неправильно указаны настройки')
        else:
            self.rebuild()

    def rebuild_set(self, instance):
        try:
            self.clear_all()
            global do_par, di_par, ai_par, hr_par, send_info
            b2 = BoxLayout(orientation='vertical')
            b3 = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))

            g1 = GridLayout(cols=2, spacing=30, padding=25, size_hint=(1, .175))
            g2 = GridLayout(cols=2, spacing=30, padding=25, size_hint=(1, .175))
            g3 = GridLayout(cols=2, spacing=30, padding=25, size_hint=(1, .175))
            g4 = GridLayout(cols=2, spacing=30, padding=25, size_hint=(1, .175))

            g1.add_widget(Label(text='Количество', font_size=20, halign='left', size_hint=(.2, .1), color=[0, 0, 0, 1]))
            self.do_num = (TextInput(text=do_par.split(', ')[2], multiline=False, font_size=20))
            g1.add_widget(self.do_num)
            g1.add_widget(Label(text='Адрес', font_size=20, halign='left', size_hint=(.2, .1), color=[0, 0, 0, 1]))
            self.do_adr = (TextInput(text=do_par.split(', ')[1], multiline=False, font_size=20))
            g1.add_widget(self.do_adr)

            g2.add_widget(Label(text='Количество', font_size=20, halign='left', size_hint=(.2, .1), color=[0, 0, 0, 1]))
            self.di_num = (TextInput(text=di_par.split(', ')[2], multiline=False, font_size=20))
            g2.add_widget(self.di_num)
            g2.add_widget(Label(text='Адрес', font_size=20, halign='left', size_hint=(.2, .1), color=[0, 0, 0, 1]))
            self.di_adr = (TextInput(text=di_par.split(', ')[1], multiline=False, font_size=20))
            g2.add_widget(self.di_adr)

            g3.add_widget(Label(text='Количество', font_size=20, halign='left', size_hint=(.2, .1), color=[0, 0, 0, 1]))
            self.ai_num = (TextInput(text=ai_par.split(', ')[2], multiline=False, font_size=20))
            g3.add_widget(self.ai_num)
            g3.add_widget(Label(text='Адрес', font_size=20, halign='left', size_hint=(.2, .1), color=[0, 0, 0, 1]))
            self.ai_adr = (TextInput(text=ai_par.split(', ')[1], multiline=False, font_size=20))
            g3.add_widget(self.ai_adr)

            g4.add_widget(Label(text='Количество', font_size=20, halign='left', size_hint=(.2, .1), color=[0, 0, 0, 1]))
            self.hr_num = (TextInput(text=hr_par.split(', ')[2], multiline=False, font_size=20))
            g4.add_widget(self.hr_num)
            g4.add_widget(Label(text='Адрес', font_size=20, halign='left', size_hint=(.2, .1), color=[0, 0, 0, 1]))
            self.hr_adr = (TextInput(text=hr_par.split(', ')[1], multiline=False, font_size=20))
            g4.add_widget(self.hr_adr)

            but_back = Button(on_release=self.save_set, font_size=24, background_color=[0, 0.6, 0, 1],
                              background_normal='',
                              size_hint=(0.2, 1))
            I1 = Image(source='E:\images\menu2.png')
            but_back.add_widget(I1)
            b3.add_widget(but_back)
            b3.add_widget(
                Button(text='Настройки', bold=True, font_size=28, background_color=[0, 0.6, 0, 1], background_normal='',
                       background_down=''))
            b3.add_widget(
                Button(font_size=28, background_color=[0, 0.6, 0, 1], background_normal='',
                       background_down='', size_hint=(0.2, 1)))

            b2.add_widget(b3)
            b2.add_widget(
                Label(text='Цифровые выходы:', font_size=24, halign='center', size_hint=(1, 0.05), color=[0, 0, 0, 1]))
            b2.add_widget(g1)
            b2.add_widget(
                Label(text='Цифровые входы:', font_size=24, halign='center', size_hint=(1, 0.05), color=[0, 0, 0, 1]))
            b2.add_widget(g2)
            b2.add_widget(
                Label(text='Аналоговые входы:', font_size=24, halign='center', size_hint=(1, 0.05), color=[0, 0, 0, 1]))
            b2.add_widget(g3)
            b2.add_widget(
                Label(text='Регистры временного хранения информации:', font_size=24, halign='center',
                      size_hint=(1, 0.05), color=[0, 0, 0, 1]))
            b2.add_widget(g4)

            I1.x = 0 - I1.width * 0.125
            I1.y = Window.height - I1.height * 0.9
            self.root.add_widget(b2)
        finally:
            pass

    def restart(self, instance):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def rebuild(self):
        self.clear_all()
        b2 = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        b3 = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        but_off = Button(font_size=24, background_color=[0, 0.6, 0, 1], background_normal='',
                         size_hint=(0.2, 1), on_release=self.restart)
        I1 = Image(source='E:\images\off2.png')
        but_off.add_widget(I1)
        b2.add_widget(but_off)
        self.titl = Button(text='Индикация параметров', halign='left', bold=True, font_size=24,
                           background_color=[0, 0.6, 0, 1], background_normal='',
                           background_down='')
        b2.add_widget(self.titl)

        but_set = Button(on_release=self.rebuild_set, font_size=24, background_color=[0, 0.6, 0, 1],
                         background_normal='',
                         size_hint=(0.2, 1))
        I2 = Image(source='E:\images\set2.png')
        but_set.add_widget(I2)
        b2.add_widget(but_set)

        self.list_button = self.list_but
        self.list_adapter = ListAdapter(data=[], cls=self.list_button, allow_empty_selection=False)

        self.list_view = ListView(adapter=self.list_adapter)
        self.list_button.background_color = [1, 1, 1, 1]
        self.list_button.background_normal = ''
        self.list_button.on_release = self.show_popup
        self.list_view.container.spacing = 10
        self.list_button.font_size = 24
        self.list_button.font_name = 'arialbd'
        self.list_button.bold = True
        self.list_button.color = [0, 0, 0, 1]
        self.list_button.padding = 30
        self.list_button.halign = 'left'
        self.list_button.text_size = (Window.width, 0)
        self.list_adapter.data = []

        I1.x = 0 - I2.width * 0.125
        I1.y = Window.height - I2.height * 0.9
        I2.x = Window.width - I2.width * 0.9
        I2.y = Window.height - I2.height * 0.9
        self.root.add_widget(b2)
        self.root.add_widget(self.list_view)

        self.but_0x = Button(on_release=self.do_set, text='0x', bold=True, font_size=28,
                             background_color=[0, 0.6, 0, 1], background_normal='')

        self.but_1x = Button(on_release=self.di_set, text='1x', bold=True, font_size=28,
                             background_color=[0, 0.6, 0, 1], background_normal='')

        self.but_3x = Button(on_release=self.ai_set, text='3x', bold=True, font_size=28,
                             background_color=[0, 0.6, 0, 1], background_normal='')

        self.but_4x = Button(on_release=self.hr_set, text='4x', bold=True, font_size=28,
                             background_color=[0, 0.6, 0, 1], background_normal='')
        b3.add_widget(self.but_0x)
        b3.add_widget(self.but_1x)
        b3.add_widget(self.but_3x)
        b3.add_widget(self.but_4x)
        self.root.add_widget(b3)
        self.hr_set()
        Clock.schedule_interval(self.update, 1)

    class SocketManager:

        def __init__(self, address):
            self.address = address

        def __enter__(self):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(self.address)
            return self.sock

        def __exit__(self, *ignore):
            self.sock.close()

    def handle_request(self):
        try:
            with self.SocketManager(tuple(Address)) as sock:
                global send_info
                sock.send(bytes(send_info, 'utf-8'))
                data = sock.recv(1024)

        except socket.error as err:
            print("Connection Error".format(err))
        else:
            return (data)

    def update(self, *args):
        global send_info
        recv = self.handle_request()
        recv = recv.decode("utf-8")
        recv = recv[1:-1].split(', ')
        parameters = []
        send = send_info.split(', ')
        for i in range(len(recv)):
            param = send_info[0] + '0' * (4 - len(str(i + int(send[1])))) + str(i + int(send[1]))
            s = '    ' + param + ' = ' + recv[i]
            for j in alarm_list:
                if (param == j[0]):
                    if j[1] == '':
                        max = 10000
                    else:
                        max = int(j[1])
                    if j[2] == '':
                        min = -10000
                    else:
                        min = int(j[2])
                    s += (' ' * (14 - 2 * len(recv[i]))) + 'max = ' + j[1] + (' ' * (10 - 2 * len(j[1]))) + 'min = ' + \
                         j[2]
                    if (int(recv[i]) < max) and (int(recv[i]) > min) and (j[3] == 1):
                        j[3] = 0
                    if ((int(recv[i]) >= max) or (int(recv[i]) <= min)) and (j[3] == 0):
                        if int(recv[i]) >= int(j[1]):
                            mes = param + ' превысил верхнюю границу!'
                        else:
                            mes = param + ' ниже нижней границы!'
                        self.alarm_popup(mes)
                        j[3] = 1
                    if ((int(recv[i]) >= max) or (int(recv[i]) <= min)):
                        if int(recv[i]) >= int(j[1]):
                            s += (' ' * (10 - 2 * len(j[2]))) + '▲'
                        else:
                            s += (' ' * (10 - 2 * len(j[2]))) + '▼'
            parameters.append(s)
        for i in range(10): parameters.append('')
        self.list_adapter.data = parameters

    def connect(self, instance):
        try:
            Address.append(self.ip_in.text)
            Address.append(int(self.port_in.text))
            s = self.handle_request()
            if s == None: raise ConnectionError
        except ValueError:
            self.error_popup('Неправильно указан порт')
        except ConnectionError:
            self.error_popup('Не удалось подключиться к серверу')
        else:
            self.rebuild()

    def build(self):

        b1 = BoxLayout(orientation='vertical')
        b2 = BoxLayout(orientation='vertical', padding=25, size_hint=[1, 0.8])
        g1 = GridLayout(cols=2, spacing=20, padding=25)

        g1.add_widget(Label(text='IP адрес', font_size=20, halign='left', size_hint=(.2, .1), color=[0, 0, 0, 1]))
        self.ip_in = (TextInput(multiline=False, text='192.168.0.101', font_size=20))
        g1.add_widget(self.ip_in)
        g1.add_widget(Label(text='Порт', font_size=20, halign='left', size_hint=(.2, .1), color=[0, 0, 0, 1]))
        self.port_in = (TextInput(multiline=False, text='5005', font_size=20))
        g1.add_widget(self.port_in)

        b1.add_widget(
            Button(text='Индикация параметров', bold=True, font_size=28, background_color=[0, 0.6, 0, 1],
                   background_normal='',
                   background_down='', size_hint=[1, 0.5]))
        b1.add_widget(BoxLayout(orientation='vertical'))
        b1.add_widget(BoxLayout(orientation='vertical'))
        b1.add_widget(g1)
        b1.add_widget(BoxLayout(orientation='vertical'))
        b1.add_widget(BoxLayout(orientation='vertical'))
        b2.add_widget(
            Button(text='Подключение', bold=True, font_size=28, background_color=[0, 0.6, 0, 1], background_normal='',
                   on_release=self.connect))
        b1.add_widget(b2)
        return b1


if __name__ == "__main__":
    App.icon = 'E:\images\logo1_256.png'
    App().run()
