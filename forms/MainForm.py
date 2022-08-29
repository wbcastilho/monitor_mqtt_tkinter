import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from pathlib import Path
from forms.SettingsForm import SettingsForm
from adapters.MyPsutil import MyPsutil
from adapters.ClientMqtt import ClientMqtt
from adapters.MyJSON import MyJSON
from tkinter import filedialog


class MainForm(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)
        self.start = False
        self.client_mqtt = None
        '''self.configuration = {
            'server': ttk.StringVar(),
            'port': ttk.StringVar(),
            'application_topic': ttk.StringVar(),
            'service_topic': ttk.StringVar(),
        }'''
        self.configuration = {
            'server': ttk.StringVar(),
            'port': ttk.StringVar(),
            'application_topic': ttk.StringVar(),
            'service_topic_1': ttk.StringVar(),
            'enable_topic_1': ttk.IntVar(),
            'service_topic_2': ttk.StringVar(),
            'enable_topic_2': ttk.IntVar(),
            'service_topic_3': ttk.StringVar(),
            'enable_topic_3': ttk.IntVar(),
            'service_topic_4': ttk.StringVar(),
            'enable_topic_4': ttk.IntVar(),
            'service_topic_5': ttk.StringVar(),
            'enable_topic_5': ttk.IntVar(),
        }
        self.process = ttk.StringVar()
        self.path = ttk.StringVar()
        self.afterid = ttk.StringVar()
        self.memory_meter = None
        self.cpu_meter = None
        self.disk_meter = None

        self.button_action = None
        self.button_settings = None
        self.button_browse = None
        self.combobox_process = None
        self.label_status_monitoring = None
        self.label_status_connection = None
        self.label_status_process = None
        self.label_status_path = None
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
        frame.pack(fill="x", padx=20, pady=15)

        label = ttk.Label(frame, text="Processo")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E)

        self.combobox_process = ttk.Combobox(frame, width=50, textvariable=self.process, values=self.process_values)
        self.combobox_process.grid(row=0, column=1, padx=2, sticky=ttk.W)

    def create_label_path(self):
        label_frame = ttk.Labelframe(self, text='Monitoração Arquivos Pasta')
        label_frame.pack(fill="x", padx=10, pady=5)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=15)

        label = ttk.Label(frame, text="Pasta")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E)

        path = ttk.Entry(frame, width=50, textvariable=self.path, state="disabled")
        path.grid(row=0, column=1, padx=2, sticky=ttk.W)

        self.button_browse = ttk.Button(frame, text="Selecionar Pasta", bootstyle=(INFO, OUTLINE),
                                        command=self.on_browse)
        self.button_browse.grid(row=0, column=2, padx=2)

    def create_memoria_frame(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x")

        frame_grid = ttk.Frame(frame)
        frame_grid.grid(row=0, column=0, sticky=ttk.W)

        label_frame = ttk.Labelframe(frame_grid, text='Memória')
        label_frame.pack(fill="x", padx=10, pady=5)

        self.memory_meter = ttk.Meter(
            master=label_frame,
            metersize=135,
            amounttotal=100,
            padding=(10, 10),
            amountused=0,
            metertype="full",
            subtext="",
            subtextfont='-size 1',
            interactive=False
        )
        self.memory_meter.pack(fill="x")

        frame_grid = ttk.Frame(frame)
        frame_grid.grid(row=0, column=1, sticky=ttk.W)

        label_frame = ttk.Labelframe(frame_grid, text='CPU')
        label_frame.pack(fill="x", padx=10, pady=5)

        self.cpu_meter = ttk.Meter(
            master=label_frame,
            metersize=135,
            amounttotal=100,
            padding=(10, 10),
            amountused=0,
            metertype="full",
            subtext="",
            subtextfont='-size 1',
            interactive=False,
        )
        self.cpu_meter.pack(fill="x")

        frame_grid = ttk.Frame(frame)
        frame_grid.grid(row=0, column=2, sticky=ttk.W)

        label_frame = ttk.Labelframe(frame_grid, text='HD Sistema')
        label_frame.pack(fill="x", padx=10, pady=5)

        self.disk_meter = ttk.Meter(
            master=label_frame,
            metersize=135,
            amounttotal=100,
            padding=(10, 10),
            amountused=0,
            metertype="full",
            subtext="",
            subtextfont='-size 1',
            interactive=False,
        )
        self.disk_meter.pack(fill="x")

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

        label = ttk.Label(frame, text=" Monitoração")
        label.grid(row=1, column=0, sticky=ttk.W)

        self.label_status_monitoring = ttk.Label(frame, text=" Parado", font='Arial 8 bold', bootstyle="danger")
        self.label_status_monitoring.grid(row=1, column=1, sticky=ttk.W)

        label = ttk.Label(frame, text=" Conexão Broker")
        label.grid(row=2, column=0, sticky=ttk.W)

        self.label_status_connection = ttk.Label(frame, text=" Desconectado", font='Arial 8 bold', bootstyle="danger")
        self.label_status_connection.grid(row=2, column=1, sticky=ttk.W)

        label = ttk.Label(frame, text=" Processo")
        label.grid(row=3, column=0, sticky=ttk.W)

        self.label_status_process = ttk.Label(frame, text=" -", font='Arial 8 bold', bootstyle="danger")
        self.label_status_process.grid(row=3, column=1, sticky=ttk.W)

        label = ttk.Label(frame, text=" Arquivos Pasta")
        label.grid(row=4, column=0, sticky=ttk.W)

        self.label_status_path = ttk.Label(frame, text=" -", font='Arial 8 bold', bootstyle="danger")
        self.label_status_path.grid(row=4, column=1, sticky=ttk.W)

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

    def on_settings(self) -> None:
        if not self.start:
            setting_form = ttk.Toplevel()
            setting_form.title("Configurações")
            setting_form.grab_set()
            setting_form.resizable(False, False)
            SettingsForm(setting_form, self.configuration)
        else:
            messagebox.showwarning(title="Atenção", message="Para abrir a janela de configurações é necessário antes "
                                                            "parar a monitoração clicando no botão Parar.")

    def on_browse(self):
        path = filedialog.askdirectory(initialdir=r'c:\\', title="Selecionar Pasta")
        if path:
            self.path.set(path)

    def on_action(self):
        if not self.start:
            if self.validate():
                try:
                    self.client_mqtt = ClientMqtt("MONITOR_MQTT", self.configuration['application_topic'].get(),
                                                  self.configuration["server"].get(),
                                                  int(self.configuration["port"].get()))
                    self.change_label_connection_to_connected(True)
                    self.change_state_action(True)
                    self.change_label_monitoring_to_running(True)
                    self.change_button_brower_path(False)
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
                self.change_label_monitoring_to_running(False)
                self.change_button_brower_path(True)

    def loop(self):
        def mqtt_connection(cls):
            try:
                cls.client_mqtt = ClientMqtt("MONITOR_MQTT", cls.configuration['application_topic'].get(),
                                             cls.configuration["server"].get(),
                                             int(cls.configuration["port"].get()))
                cls.change_label_connection_to_connected(True)
            except Exception:
                cls.change_label_connection_to_connected(False)

        def mqtt_publish(cls, topic: str, value: str):
            if cls.client_mqtt.connected:
                cls.client_mqtt.publish(topic, value)
            else:
                mqtt_connection(cls)

        if self.configuration["enable_topic_1"].get() == 1:
            process_exist = False
            try:
                process_exist = MyPsutil.check_process_exist(self.process.get())
            except Exception:
                process_exist = False
            finally:
                if process_exist:
                    print("Sem alarme")
                    self.change_label_process_to_executing(0)
                    mqtt_publish(self, self.configuration["service_topic_1"].get(), '0')
                else:
                    print("Gera alarme")
                    self.change_label_process_to_executing(1)
                    mqtt_publish(self, self.configuration["service_topic_1"].get(), '1')

        if self.configuration["enable_topic_2"].get() == 1:
            file_size_ok = False
            try:
                file_size_ok = MyPsutil.check_files_size(self.path.get(), 10000)
            except Exception:
                file_size_ok = False
            finally:
                if file_size_ok:
                    self.change_label_path_to_ok(0)
                    mqtt_publish(self, self.configuration["service_topic_2"].get(), '0')
                else:
                    self.change_label_path_to_ok(1)
                    mqtt_publish(self, self.configuration["service_topic_2"].get(), '1')

        if self.configuration["enable_topic_3"].get() == 1:
            try:
                memory = MyPsutil.show_virtual_memory()
                self.memory_meter.configure(amountused=memory.percent)
                mqtt_publish(self, self.configuration["service_topic_3"].get(), str(memory.percent))
            except Exception:
                pass

        if self.configuration["enable_topic_4"].get() == 1:
            try:
                cpu = MyPsutil.show_cpu_percent()
                self.cpu_meter.configure(amountused=cpu)
                mqtt_publish(self, self.configuration["service_topic_4"].get(), str(cpu))
            except Exception:
                pass

        if self.configuration["enable_topic_5"].get() == 1:
            try:
                disk = MyPsutil.show_disk_usage("c:")
                self.disk_meter.configure(amountused=disk.percent)
                mqtt_publish(self, self.configuration["service_topic_5"].get(), str(disk.percent))
            except Exception:
                pass

        self.afterid.set(self.after(5000, self.loop))

    def change_button_action_to_start(self, value: bool) -> None:
        if value:
            self.button_action['image'] = 'play'
            self.button_action['text'] = 'Iniciar'
        else:
            self.button_action['image'] = 'stop'
            self.button_action['text'] = 'Parar'

    def change_button_brower_path(self, value):
        if value:
            self.button_browse["state"] = "normal"
        else:
            self.button_browse["state"] = "disabled"

    def change_label_monitoring_to_running(self, value: bool) -> None:
        if value:
            self.label_status_monitoring["bootstyle"] = "success"
            self.label_status_monitoring["text"] = " Rodando"
        else:
            self.label_status_monitoring["bootstyle"] = "danger"
            self.label_status_monitoring["text"] = " Parado"

    def change_label_connection_to_connected(self, value: bool) -> None:
        if value:
            self.label_status_connection["bootstyle"] = "success"
            self.label_status_connection["text"] = " Conectado"
        else:
            self.label_status_connection["bootstyle"] = "danger"
            self.label_status_connection["text"] = " Desconectado"

    def change_label_process_to_executing(self, value: int) -> None:
        if value == 0:
            self.label_status_process["bootstyle"] = "success"
            self.label_status_process["text"] = " Executando"
        elif value == 1:
            self.label_status_process["bootstyle"] = "danger"
            self.label_status_process["text"] = " Não executando"
        else:
            self.label_status_process["bootstyle"] = "danger"
            self.label_status_process["text"] = " -"

    def change_label_path_to_ok(self, value: int) -> None:
        if value == 0:
            self.label_status_path["bootstyle"] = "success"
            self.label_status_path["text"] = " Ok"
        elif value == 1:
            self.label_status_path["bootstyle"] = "danger"
            self.label_status_path["text"] = " Falha"
        else:
            self.label_status_path["bootstyle"] = "danger"
            self.label_status_path["text"] = " -"

    def validate(self) -> bool:
        if not self.validate_configuration():
            messagebox.showwarning(title="Atenção", message="Há alguns campos das configurações que não foram "
                                                            "preenchidos, clique no botão configurações antes "
                                                            "de iniciar.")
            return False
        elif not self.validate_combobox_process():
            messagebox.showwarning(title="Atenção", message="Um processo deve ser selecionado.")
            return False
        elif not self.validate_entry_path():
            messagebox.showwarning(title="Atenção", message="Uma pasta deve ser selecionada.")
            return False

        return True

    def validate_configuration(self) -> bool:
        if self.configuration["server"].get() == "":
            return False
        elif self.configuration["port"].get() == "":
            return False
        elif self.configuration["application_topic"].get() == "":
            return False
        return True

    def validate_combobox_process(self) -> bool:
        if self.configuration["enable_topic_1"].get() == 1 and (self.process.get() == "" or self.process.get() is None):
            return False
        return True

    def validate_entry_path(self) -> bool:
        if self.configuration["enable_topic_2"].get() == 1 and (self.path.get() == "" or self.path.get() is None):
            return False
        return True

    def change_state_action(self, value: bool) -> None:
        if value:
            self.combobox_process.config(state="disabled")
            self.change_button_action_to_start(False)
            self.check_config_service_is_enabled()
            self.start = True
        else:
            self.combobox_process.config(state="normal")
            self.change_button_action_to_start(True)
            self.change_label_process_to_executing(2)
            self.change_label_path_to_ok(2)
            self.reset_meters()
            self.start = False

    def reset_meters(self):
        self.memory_meter.configure(amountused=0)
        self.cpu_meter.configure(amountused=0)
        self.disk_meter.configure(amountused=0)

        self.memory_meter["bootstyle"] = "primary"
        self.cpu_meter["bootstyle"] = "primary"
        self.disk_meter["bootstyle"] = "primary"

    def check_config_service_is_enabled(self):
        if self.configuration["enable_topic_1"].get() == 0:
            self.change_label_process_to_executing(2)

        if self.configuration["enable_topic_2"].get() == 0:
            self.change_label_path_to_ok(2)

        if self.configuration["enable_topic_3"].get() == 0:
            self.memory_meter["bootstyle"] = "secondary"

        if self.configuration["enable_topic_4"].get() == 0:
            self.cpu_meter["bootstyle"] = "secondary"

        if self.configuration["enable_topic_5"].get() == 0:
            self.disk_meter["bootstyle"] = "secondary"

