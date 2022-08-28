import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility
from tkinter import messagebox
from pathlib import Path
from forms.SettingsForm import SettingsForm
from adapters.MyPsutil import MyPsutil
from adapters.ClientMqtt import ClientMqtt
from adapters.MyJSON import MyJSON


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
        self.label_status_process = None
        self.label_status_connection = None
        self.process_values = None
        self.resultview = None
        self.photoimages = []

        self.associate_icons()
        self.init_combobox_process()
        self.create_buttonbar()
        self.create_label_frame()
        self.create_label_path()
        self.create_memoria_frame()
        self.create_status_frame()
        self.read_config()

    def associate_icons(self):
        image_files = {
            'play': 'icons8-reproduzir-24.png',
            'stop': 'icons8-parar-24.png',
            'settings-light': 'icons8-configuracoes-24.png',
            'refresh': 'icons8-actualizar-24.png'
        }

        imgpath = Path(__file__).parent / '../assets'
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
        label_frame.pack(fill="x", padx=10, pady=(10, 5))

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=20)

        label = ttk.Label(frame, text="Processo")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E)

        self.combobox_process = ttk.Combobox(frame, width=50, textvariable=self.process, values=self.process_values)
        self.combobox_process.grid(row=0, column=1, padx=2, sticky=ttk.W)

    def create_label_path(self):
        label_frame = ttk.Labelframe(self, text='Monitoração Arquivos Pasta')
        label_frame.pack(fill="x", padx=10, pady=5)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=20)

        label = ttk.Label(frame, text="Pasta")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=10)

        path = ttk.Entry(frame, width=50, state="disabled")
        path.grid(row=0, column=1, padx=2, sticky=ttk.W, pady=10)

        button = ttk.Button(frame, text="Selecionar Pasta", bootstyle=(INFO, OUTLINE))
        button.grid(row=0, column=2, padx=2, pady=10)

    def create_memoria_frame(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x")

        frame_grid = ttk.Frame(frame)
        frame_grid.grid(row=0, column=0, sticky=ttk.W)

        label_frame = ttk.Labelframe(frame_grid, text='Memória')
        label_frame.pack(fill="x", padx=10, pady=5)

        meter = ttk.Meter(
            master=label_frame,
            metersize=100,
            padding=5,
            amountused=25,
            metertype="full",
            interactive=True,
        )
        meter.pack(fill="x")

        frame_grid = ttk.Frame(frame)
        frame_grid.grid(row=0, column=1, sticky=ttk.W)

        label_frame = ttk.Labelframe(frame_grid, text='CPU')
        label_frame.pack(fill="x", padx=10, pady=5)

        meter = ttk.Meter(
            master=label_frame,
            metersize=100,
            padding=5,
            amountused=25,
            metertype="full",
            interactive=True,
        )
        meter.pack(fill="x")

        frame_grid = ttk.Frame(frame)
        frame_grid.grid(row=0, column=2, sticky=ttk.W)

        label_frame = ttk.Labelframe(frame_grid, text='HD Sistema')
        label_frame.pack(fill="x", padx=10, pady=5)

        meter = ttk.Meter(
            master=label_frame,
            metersize=100,
            padding=5,
            amountused=25,
            metertype="full",
            interactive=True,
        )
        meter.pack(fill="x")

        frame_grid = ttk.Frame(frame)
        frame_grid.grid(row=0, column=3, sticky=ttk.W)

    def create_status_frame(self):
        label_frame = ttk.Labelframe(self, text='Status')
        label_frame.pack(fill="x", padx=10, pady=(5, 10))

        frame = ttk.Frame(label_frame, borderwidth=1, relief="sunken")
        frame.pack(fill="both", padx=10, pady=10)

        label = ttk.Label(frame, text=" Descrição", font='Arial 8 bold', width=50, bootstyle="inverse-primary")
        label.grid(row=0, column=0, sticky=ttk.W)

        label = ttk.Label(frame, text=" Status", font='Arial 8 bold', width=30, bootstyle="inverse-primary")
        label.grid(row=0, column=1, sticky=ttk.W)

        label = ttk.Label(frame, text=" Conexão Broker")
        label.grid(row=1, column=0, sticky=ttk.W)

        self.label_status_connection = ttk.Label(frame, text=" Desconectado", font='Arial 8 bold', bootstyle="danger")
        self.label_status_connection.grid(row=1, column=1, sticky=ttk.W)

        label = ttk.Label(frame, text=" Processo")
        label.grid(row=2, column=0, sticky=ttk.W)

        self.label_status_process = ttk.Label(frame, text=" Não executando", font='Arial 8 bold', bootstyle="danger")
        self.label_status_process.grid(row=2, column=1, sticky=ttk.W)

        label = ttk.Label(frame, text=" Arquivos Pasta")
        label.grid(row=3, column=0, sticky=ttk.W)

        pasta = ttk.Label(frame, text=" Falha", font='Arial 8 bold', bootstyle="danger")
        pasta.grid(row=3, column=1, sticky=ttk.W)

    def on_settings(self) -> None:
        if not self.start:
            setting_form = ttk.Toplevel(self)
            setting_form.title("Configurações")
            setting_form.grab_set()
            setting_form.resizable(False, False)
            SettingsForm(setting_form, self.configuration)
        else:
            messagebox.showwarning(title="Atenção", message="Para abrir a janela de configurações é necessário antes "
                                                            "parar a monitoração clicando no botão Parar.")

    def read_config(self) -> None:
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

    def change_button_action_to_start(self, value: bool) -> None:
        if value:
            self.button_action['image'] = 'play'
            self.button_action['text'] = 'Iniciar'
        else:
            self.button_action['image'] = 'stop'
            self.button_action['text'] = 'Parar'

    def change_label_connection_to_connected(self, value: bool) -> None:
        if value:
            self.label_status_connection["bootstyle"] = "success"
            self.label_status_connection["text"] = " Conectado"
        else:
            self.label_status_connection["bootstyle"] = "danger"
            self.label_status_connection["text"] = " Desconectado"

    def change_label_process_to_executing(self, value: bool) -> None:
        if value:
            self.label_status_process["bootstyle"] = "success"
            self.label_status_process["text"] = " Executando"
        else:
            self.label_status_process["bootstyle"] = "danger"
            self.label_status_process["text"] = " Não executando"

    def validate(self) -> bool:
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

    def validate_combobox_process(self) -> bool:
        if self.process.get() == "" or self.process.get() is None:
            return False
        return True

    def change_state_action(self, value: bool) -> None:
        if value:
            self.combobox_process["state"] = "disabled"
            self.change_button_action_to_start(False)
            self.change_label_process_to_executing(False)
            self.start = True
        else:
            self.combobox_process["state"] = "normal"
            self.change_button_action_to_start(True)
            self.change_label_process_to_executing(False)
            self.start = False

