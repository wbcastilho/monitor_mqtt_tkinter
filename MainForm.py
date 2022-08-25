import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from pathlib import Path
from MyPsutil import MyPsutil
from ClientMqtt import ClientMqtt
from MyJSON import MyJSON
from SettingsForm import SettingsForm


class MainForm(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)
        self.start = False
        self.client_mqtt = None
        self.configuration = {
            'server': ttk.StringVar(),
            'port': ttk.StringVar(),
            'application_topic': ttk.StringVar(),
            'service_topic': ttk.StringVar(),
        }
        self.process = ttk.StringVar()
        self.afterid = ttk.StringVar()
        self.button_action = None
        self.button_settings = None
        self.combobox_process = None
        self.label_process = None
        self.label_connection = None
        self.process_values = None
        self.photoimages = []

        self.associate_icons()
        self.init_combobox_process()
        self.create_buttonbar()
        self.create_label_frame()
        self.create_statusbar()
        self.read_config()

    def associate_icons(self):
        image_files = {
            'play': 'icons8-reproduzir-24.png',
            'stop': 'icons8-parar-24.png',
            'settings-light': 'icons8-configuracoes-24.png',
            'refresh': 'icons8-actualizar-24.png'
        }

        imgpath = Path(__file__).parent / 'assets'
        for key, val in image_files.items():
            _path = imgpath / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

    def init_combobox_process(self):
        self.process_values = MyPsutil.show_activate_processess()

    def create_buttonbar(self):
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=X, pady=1, side=TOP)

        self.button_action = ttk.Button(
            master=buttonbar, text='Iniciar',
            image='play',
            compound=LEFT,
            command=self.on_action
        )
        self.button_action.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        btn = ttk.Button(
            master=buttonbar,
            text='Configurações',
            image='settings-light',
            compound=LEFT,
            command=self.on_settings
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

    def create_label_frame(self):
        label_frame = ttk.Labelframe(self, text='Monitoração Processo')
        label_frame.pack(fill="x", padx=10, pady=20)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=20)

        label = ttk.Label(frame, text="Processo")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=10)

        self.combobox_process = ttk.Combobox(frame, width=50, textvariable=self.process, values=self.process_values)
        self.combobox_process.grid(row=0, column=1, padx=2, sticky=ttk.W, pady=10)

    def create_statusbar(self):
        statusbar = ttk.Frame(self, style='secondary.TFrame')
        statusbar.pack(fill=X, side=BOTTOM)

        self.label_connection = ttk.Label(statusbar, bootstyle="inverse-danger", text=" Desconectado do broker ",
                                          font='Arial 8 bold')
        self.label_connection.pack(side=LEFT, padx=10, pady=5)

        self.label_process = ttk.Label(statusbar, bootstyle="inverse-success", text=" Processo em execução ",
                                       font='Arial 8 bold')
        self.label_process.pack_forget()

    def on_settings(self):
        if not self.start:
            setting_form = ttk.Toplevel(self)
            setting_form.title("Configurações")
            setting_form.grab_set()
            setting_form.resizable(False, False)
            SettingsForm(setting_form, self.configuration)
        else:
            messagebox.showwarning(title="Atenção", message="Para abrir a janela de configurações é necessário antes "
                                                            "parar a monitoração clicando no botão Parar.")

    def read_config(self):
        try:
            my_json = MyJSON('config.json', self.configuration)
            my_json.read()
        except PermissionError as err:
            messagebox.showwarning(title="Atenção", message=err)
        except FileNotFoundError as err:
            messagebox.showwarning(title="Atenção", message=err)
        except Exception as err:
            messagebox.showwarning(title="Atenção", message=err)

    def on_action(self):
        if not self.start:
            if self.validate():
                try:
                    self.client_mqtt = ClientMqtt("MONITOR_MQTT", self.configuration['application_topic'].get(),
                                                  self.configuration["server"].get(),
                                                  int(self.configuration["port"].get()))
                    self.change_label_connection_to_connected(True)
                    self.change_state_action(True)
                    self.after(0, self.loop)
                except Exception as err:
                    self.change_state_action(False)
                    messagebox.showerror(title="Erro", message=err)
        else:
            try:
                self.client_mqtt.loop_stop_and_disconnect()
                self.change_label_connection_to_connected(False)
                self.after_cancel(self.afterid.get())
            except Exception as err:
                messagebox.showerror(title="Atenção", message=err)
            finally:
                self.change_state_action(False)

    def loop(self):
        def mqtt_connection(cls):
            try:
                cls.client_mqtt = ClientMqtt("MONITOR_MQTT", cls.configuration['application_topic'].get(),
                                             cls.configuration["server"].get(),
                                             int(cls.configuration["port"].get()))
                cls.change_label_connection_to_connected(True)
            except Exception:
                cls.change_label_connection_to_connected(False)

        try:
            process_exist = MyPsutil.check_process_exist(self.process.get())
        except Exception:
            process_exist = False

        if process_exist:
            print("Sem alarme")
            self.change_label_process_to_executing(True)

            if self.client_mqtt.connected:
                self.client_mqtt.publish(self.configuration["service_topic"].get(), '0')
            else:
                mqtt_connection(self)
        else:
            print("Gera alarme")
            self.change_label_process_to_executing(False)

            if self.client_mqtt.connected:
                self.client_mqtt.publish(self.configuration["service_topic"].get(), '1')
            else:
                mqtt_connection(self)

        self.afterid.set(self.after(5000, self.loop))

    def change_button_action_to_start(self, value):
        if value:
            self.button_action['image'] = 'play'
            self.button_action['text'] = 'Iniciar'
        else:
            self.button_action['image'] = 'stop'
            self.button_action['text'] = 'Parar'

    def change_label_connection_to_connected(self, value):
        if value:
            self.label_connection["bootstyle"] = "inverse-success"
            self.label_connection["text"] = "Conectado ao broker"
        else:
            self.label_connection["bootstyle"] = "inverse-danger"
            self.label_connection["text"] = "Desconectado do broker"

    def change_label_process_to_executing(self, value):
        if value:
            self.label_process["bootstyle"] = "inverse-success"
            self.label_process["text"] = " Processo em execução "
        else:
            self.label_process["bootstyle"] = "inverse-danger"
            self.label_process["text"] = " Processo não encontrado "

    def validate(self):
        if not self.validate_configuration():
            messagebox.showwarning(title="Atenção", message="Há alguns campos das configurações que não foram "
                                                            "preenchidos, clique no botão configurações antes "
                                                            "de iniciar.")
            return False
        elif not self.validate_combobox_process():
            messagebox.showwarning(title="Atenção", message="Um processo deve ser selecionado.")
            return False

        return True

    def validate_configuration(self) -> bool:
        if self.configuration["server"].get() == "":
            return False
        elif self.configuration["port"].get() == "":
            return False
        elif self.configuration["application_topic"].get() == "":
            return False
        elif self.configuration["service_topic"].get() == "":
            return False
        return True

    def validate_combobox_process(self):
        if self.process.get() == "" or self.process.get() is None:
            return False
        return True

    def change_state_action(self, value):
        if value:
            self.label_process.pack(side=LEFT, padx=0, pady=5)
            self.combobox_process["state"] = "disabled"
            self.change_button_action_to_start(False)
            self.start = True
        else:
            self.label_process.pack_forget()
            self.combobox_process["state"] = "normal"
            self.change_button_action_to_start(True)
            self.start = False

