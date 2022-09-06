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
    OK = 0
    FAIL = 1
    NONE = 3
    DISABLED = 0
    ENABLED = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)
        self.start = False
        self.client_mqtt = None
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
        self.create_meters_frame()
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

    def create_meters_frame(self):
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
        label_frame.pack(fill="x", padx=10, pady=(5, 20))

        frame_size = ttk.Frame(label_frame, width=60)
        frame_size.pack()

        frame = ttk.Frame(frame_size, borderwidth=1, relief="sunken")
        frame.pack(fill="both", padx=10, pady=(10, 20))

        label = ttk.Label(frame, text=" Descrição", font='Arial 8 bold', width=40, bootstyle="inverse-primary")
        label.grid(row=0, column=0, sticky=ttk.W)

        label = ttk.Label(frame, text=" Status", font='Arial 8 bold', width=20, bootstyle="inverse-primary")
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

    def on_browse(self) -> None:
        path = filedialog.askdirectory(initialdir=r'c:\\', title="Selecionar Pasta")
        if path:
            self.path.set(path)

    def on_action(self) -> None:
        if not self.start:
            if self.validate():
                try:
                    self.client_mqtt = ClientMqtt("MONITOR_MQTT", self.configuration['application_topic'].get(),
                                                  self.configuration["server"].get(),
                                                  int(self.configuration["port"].get()))
                    self.change_state_action(True)
                    self.after(0, self.loop)
                except Exception as err:
                    self.change_state_action(False)
                    messagebox.showerror(title="Erro", message=err)
        else:
            try:
                self.client_mqtt.loop_stop_and_disconnect()
                self.after_cancel(self.afterid.get())
            except Exception as err:
                messagebox.showerror(title="Atenção", message=err)
            finally:
                self.change_state_action(False)

    def loop(self) -> None:
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

        def check_process(cls):
            if cls.configuration["enable_topic_1"].get() == cls.ENABLED:
                process_exist = False
                try:
                    process_exist = MyPsutil.check_process_exist(cls.process.get())
                except Exception:
                    process_exist = False
                finally:
                    if process_exist:
                        print("Sem alarme")
                        cls.change_state_of_label_process(cls.OK)
                        mqtt_publish(cls, cls.configuration["service_topic_1"].get(), '0')
                    else:
                        print("Gera alarme")
                        cls.change_state_of_label_process(cls.FAIL)
                        mqtt_publish(cls, cls.configuration["service_topic_1"].get(), '1')

        def check_file_size(cls):
            if cls.configuration["enable_topic_2"].get() == cls.ENABLED:
                file_size_ok = False
                try:
                    file_size_ok = MyPsutil.check_files_size(cls.path.get(), 10000)
                except Exception:
                    file_size_ok = False
                finally:
                    if file_size_ok:
                        cls.change_state_of_label_path(cls.OK)
                        mqtt_publish(cls, cls.configuration["service_topic_2"].get(), '0')
                    else:
                        cls.change_state_of_label_path(cls.FAIL)
                        mqtt_publish(cls, cls.configuration["service_topic_2"].get(), '1')

        def check_memory(cls):
            if cls.configuration["enable_topic_3"].get() == cls.ENABLED:
                try:
                    memory = MyPsutil.show_virtual_memory()
                    cls.memory_meter.configure(amountused=memory.percent)
                    mqtt_publish(cls, cls.configuration["service_topic_3"].get(), str(memory.percent))
                except Exception:
                    pass

        def check_cpu(cls):
            if cls.configuration["enable_topic_4"].get() == cls.ENABLED:
                try:
                    cpu = MyPsutil.show_cpu_percent()
                    cls.cpu_meter.configure(amountused=cpu)
                    mqtt_publish(cls, cls.configuration["service_topic_4"].get(), str(cpu))
                except Exception:
                    pass

        def check_disk(cls):
            if cls.configuration["enable_topic_5"].get() == cls.ENABLED:
                try:
                    disk = MyPsutil.show_disk_usage("c:")
                    cls.disk_meter.configure(amountused=disk.percent)
                    mqtt_publish(cls, cls.configuration["service_topic_5"].get(), str(disk.percent))
                except Exception:
                    pass

        check_process(self)
        check_file_size(self)
        check_memory(self)
        check_cpu(self)
        check_disk(self)

        five_seconds = 5000
        self.afterid.set(self.after(five_seconds, self.loop))

    def change_state_of_label_connection(self, value: bool) -> None:
        if value:
            self.label_status_connection["bootstyle"] = "success"
            self.label_status_connection["text"] = " Conectado"
        else:
            self.label_status_connection["bootstyle"] = "danger"
            self.label_status_connection["text"] = " Desconectado"

    def change_state_of_label_process(self, value: int) -> None:
        if value == self.OK:
            self.label_status_process["bootstyle"] = "success"
            self.label_status_process["text"] = " Executando"
        elif value == self.FAIL:
            self.label_status_process["bootstyle"] = "danger"
            self.label_status_process["text"] = " Não executando"
        else:
            self.label_status_process["bootstyle"] = "danger"
            self.label_status_process["text"] = " -"

    def change_state_of_label_path(self, value: int) -> None:
        if value == self.OK:
            self.label_status_path["bootstyle"] = "success"
            self.label_status_path["text"] = " Ok"
        elif value == self.FAIL:
            self.label_status_path["bootstyle"] = "danger"
            self.label_status_path["text"] = " Falha"
        else:
            self.label_status_path["bootstyle"] = "danger"
            self.label_status_path["text"] = " -"

    def validate(self) -> bool:
        def validate_configuration(cls) -> bool:
            if cls.configuration["server"].get() == "":
                return False
            elif cls.configuration["port"].get() == "":
                return False
            elif cls.configuration["application_topic"].get() == "":
                return False
            return True

        def validate_combobox_process(cls) -> bool:
            if cls.configuration["enable_topic_1"].get() == 1 and (
                    cls.process.get() == "" or cls.process.get() is None):
                return False
            return True

        def validate_entry_path(cls) -> bool:
            if cls.configuration["enable_topic_2"].get() == 1 and (cls.path.get() == "" or cls.path.get() is None):
                return False
            return True

        if not validate_configuration(self):
            messagebox.showwarning(title="Atenção", message="Há alguns campos das configurações que não foram "
                                                            "preenchidos, clique no botão configurações antes "
                                                            "de iniciar.")
            return False
        elif not validate_combobox_process(self):
            messagebox.showwarning(title="Atenção", message="Um processo deve ser selecionado.")
            return False
        elif not validate_entry_path(self):
            messagebox.showwarning(title="Atenção", message="Uma pasta deve ser selecionada.")
            return False
        return True

    def change_state_action(self, value: bool) -> None:
        def change_state_of_combobox_process(cls):
            if value:
                cls.combobox_process.config(state="disabled")
            else:
                cls.combobox_process.config(state="normal")

        def change_state_of_label_monitoring(cls) -> None:
            if value:
                cls.label_status_monitoring["bootstyle"] = "success"
                cls.label_status_monitoring["text"] = " Rodando"
            else:
                cls.label_status_monitoring["bootstyle"] = "danger"
                cls.label_status_monitoring["text"] = " Parado"

        def change_state_of_button_action(cls) -> None:
            if value:
                cls.button_action['image'] = 'stop'
                cls.button_action['text'] = 'Parar'
            else:
                cls.button_action['image'] = 'play'
                cls.button_action['text'] = 'Iniciar'

        def check_state_of_config_service(cls):
            if cls.configuration["enable_topic_1"].get() == cls.ENABLED:
                cls.change_state_of_label_process(cls.OK)

            if cls.configuration["enable_topic_2"].get() == cls.ENABLED:
                cls.change_state_of_label_path(cls.OK)

            if cls.configuration["enable_topic_3"].get() == cls.DISABLED:
                cls.memory_meter["bootstyle"] = "secondary"

            if cls.configuration["enable_topic_4"].get() == cls.DISABLED:
                cls.cpu_meter["bootstyle"] = "secondary"

            if cls.configuration["enable_topic_5"].get() == cls.DISABLED:
                cls.disk_meter["bootstyle"] = "secondary"

        def change_state_of_button_brower_path(cls):
            if value:
                cls.button_browse["state"] = "disabled"
            else:
                cls.button_browse["state"] = "normal"

        if value:
            self.change_state_of_label_connection(True)
            check_state_of_config_service(self)
            self.start = True
        else:
            self.change_state_of_label_connection(False)
            self.change_state_of_label_process(self.NONE)
            self.change_state_of_label_path(self.NONE)
            self.reset_meters()
            self.start = False

        change_state_of_combobox_process(self)
        change_state_of_label_monitoring(self)
        change_state_of_button_action(self)
        change_state_of_button_brower_path(self)

    def reset_meters(self):
        self.memory_meter.configure(amountused=0)
        self.cpu_meter.configure(amountused=0)
        self.disk_meter.configure(amountused=0)

        self.memory_meter["bootstyle"] = "primary"
        self.cpu_meter["bootstyle"] = "primary"
        self.disk_meter["bootstyle"] = "primary"

