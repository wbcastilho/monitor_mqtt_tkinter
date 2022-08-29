import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from adapters.MyJSON import MyJSON
from widgets.MaskedEntry import MaskedEntry
from widgets.MaskedInt import MaskedInt
from helpers.Validator import Validator


class SettingsForm(ttk.Frame):
    def __init__(self, master, configuration):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.master = master
        self.configuration = configuration
        self.local_configuration = {
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
        self.entry_server = None
        self.entry_port = None
        self.entry_application_topic = None
        self.button_save = None
        self.button_cancel = None

        masked_int = MaskedInt()
        self.digit_func = self.register(masked_int.mask_number)

        masked_entry = MaskedEntry()
        self.vcmd = self.register(masked_entry.mask_ip)

        self.init_configuration()
        self.create_form_config()
        self.create_form_monitoring_process()
        self.create_form_monitoring_path()
        self.create_form_monitoring_memory()
        self.create_form_monitoring_cpu()
        self.create_form_monitoring_hd()
        self.create_buttons()

    def create_form_config(self):
        label_frame = ttk.Labelframe(self, text='Configurações MQTT')
        label_frame.pack(fill="x", padx=10, pady=5)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=10)

        label = ttk.Label(frame, text="Servidor")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=5)

        self.entry_server = ttk.Entry(frame,
                                      textvariable=self.local_configuration['server'],
                                      justify="center",
                                      width=30,
                                      validate="key",
                                      validatecommand=(self.vcmd, '%S')
                                      )
        self.entry_server.grid(row=0, column=1, padx=2, sticky=ttk.W, pady=5)

        label = ttk.Label(frame, text="Porta")
        label.grid(row=1, column=0, padx=1, sticky=ttk.E, pady=5)

        self.entry_port = ttk.Entry(frame,
                                    textvariable=self.local_configuration['port'],
                                    justify="center",
                                    width=10,
                                    validate="key",
                                    validatecommand=(self.digit_func, '%S', '%d')
                                    )
        self.entry_port.grid(row=1, column=1, padx=2, sticky=ttk.W, pady=5)

        label = ttk.Label(frame, text="Tópico da Aplicação")
        label.grid(row=2, column=0, padx=1, sticky=ttk.E, pady=5)

        self.entry_application_topic = ttk.Entry(frame, textvariable=self.local_configuration['application_topic'],
                                                 width=70)
        self.entry_application_topic.grid(row=2, column=1, padx=2, sticky=ttk.W, pady=5)

    def create_form_monitoring_process(self):
        label_frame = ttk.Labelframe(self, text='Monitoração Processo')
        label_frame.pack(fill="x", padx=10, pady=5)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=10)

        check_button = ttk.Checkbutton(frame, variable=self.local_configuration["enable_topic_1"], onvalue=1,
                                       offvalue=0)
        check_button.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=5)

        label = ttk.Label(frame, text="Tópico do Serviço")
        label.grid(row=0, column=1, padx=1, sticky=ttk.E, pady=5)

        entry = ttk.Entry(frame, width=70, textvariable=self.local_configuration['service_topic_1'])
        entry.grid(row=0, column=2, padx=2, sticky=ttk.W, pady=5)

    def create_form_monitoring_path(self):
        label_frame = ttk.Labelframe(self, text='Monitoração Arquivos Pasta')
        label_frame.pack(fill="x", padx=10, pady=5)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=10)

        check_button = ttk.Checkbutton(frame, variable=self.local_configuration["enable_topic_2"], onvalue=1,
                                       offvalue=0)
        check_button.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=5)

        label = ttk.Label(frame, text="Tópico do Serviço")
        label.grid(row=0, column=1, padx=1, sticky=ttk.E, pady=5)

        entry = ttk.Entry(frame, width=70, textvariable=self.local_configuration['service_topic_2'])
        entry.grid(row=0, column=2, padx=2, sticky=ttk.W, pady=5)

    def create_form_monitoring_memory(self):
        label_frame = ttk.Labelframe(self, text='Monitoração Memória')
        label_frame.pack(fill="x", padx=10, pady=5)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=10)

        check_button = ttk.Checkbutton(frame, variable=self.local_configuration["enable_topic_3"], onvalue=1,
                                       offvalue=0)
        check_button.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=5)

        label = ttk.Label(frame, text="Tópico do Serviço")
        label.grid(row=0, column=1, padx=1, sticky=ttk.E, pady=5)

        entry = ttk.Entry(frame, width=70, textvariable=self.local_configuration['service_topic_3'])
        entry.grid(row=0, column=2, padx=2, sticky=ttk.W, pady=5)

    def create_form_monitoring_cpu(self):
        label_frame = ttk.Labelframe(self, text='Monitoração CPU')
        label_frame.pack(fill="x", padx=10, pady=5)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=10)

        check_button = ttk.Checkbutton(frame, variable=self.local_configuration["enable_topic_4"], onvalue=1,
                                       offvalue=0)
        check_button.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=5)

        label = ttk.Label(frame, text="Tópico do Serviço")
        label.grid(row=0, column=1, padx=1, sticky=ttk.E, pady=5)

        entry = ttk.Entry(frame, width=70, textvariable=self.local_configuration['service_topic_4'])
        entry.grid(row=0, column=2, padx=2, sticky=ttk.W, pady=5)

    def create_form_monitoring_hd(self):
        label_frame = ttk.Labelframe(self, text='Monitoração HD Sistema')
        label_frame.pack(fill="x", padx=10, pady=5)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=10)

        check_button = ttk.Checkbutton(frame, variable=self.local_configuration["enable_topic_5"], onvalue=1,
                                       offvalue=0)
        check_button.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=5)

        label = ttk.Label(frame, text="Tópico do Serviço")
        label.grid(row=0, column=1, padx=1, sticky=ttk.E, pady=5)

        entry = ttk.Entry(frame, width=70, textvariable=self.local_configuration['service_topic_5'])
        entry.grid(row=0, column=2, padx=2, sticky=ttk.W, pady=5)

    def create_buttons(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=10, pady=5)

        self.button_cancel = ttk.Button(frame, text="Cancelar", bootstyle="danger", command=self.on_cancel)
        self.button_cancel.pack(side=RIGHT, padx=5, pady=10)

        self.button_save = ttk.Button(frame, text="Salvar", bootstyle="success", command=self.on_save)
        self.button_save.pack(side=RIGHT, padx=5, pady=10)

    def init_configuration(self) -> None:
        self.local_configuration["server"].set(self.configuration["server"].get())
        self.local_configuration["port"].set(self.configuration["port"].get())
        self.local_configuration["application_topic"].set(self.configuration["application_topic"].get())
        self.local_configuration["service_topic_1"].set(self.configuration["service_topic_1"].get())
        self.local_configuration["enable_topic_1"].set(self.configuration["enable_topic_1"].get())
        self.local_configuration["service_topic_2"].set(self.configuration["service_topic_2"].get())
        self.local_configuration["enable_topic_2"].set(self.configuration["enable_topic_2"].get())
        self.local_configuration["service_topic_3"].set(self.configuration["service_topic_3"].get())
        self.local_configuration["enable_topic_3"].set(self.configuration["enable_topic_3"].get())
        self.local_configuration["service_topic_4"].set(self.configuration["service_topic_4"].get())
        self.local_configuration["enable_topic_4"].set(self.configuration["enable_topic_4"].get())
        self.local_configuration["service_topic_5"].set(self.configuration["service_topic_5"].get())
        self.local_configuration["enable_topic_5"].set(self.configuration["enable_topic_5"].get())

    def change_configuration(self) -> None:
        self.configuration["server"].set(self.local_configuration["server"].get())
        self.configuration["port"].set(self.local_configuration["port"].get())
        self.configuration["application_topic"].set(self.local_configuration["application_topic"].get())
        self.configuration["service_topic_1"].set(self.local_configuration["service_topic_1"].get())
        self.configuration["enable_topic_1"].set(self.local_configuration["enable_topic_1"].get())
        self.configuration["service_topic_2"].set(self.local_configuration["service_topic_2"].get())
        self.configuration["enable_topic_2"].set(self.local_configuration["enable_topic_2"].get())
        self.configuration["service_topic_3"].set(self.local_configuration["service_topic_3"].get())
        self.configuration["enable_topic_3"].set(self.local_configuration["enable_topic_3"].get())
        self.configuration["service_topic_4"].set(self.local_configuration["service_topic_4"].get())
        self.configuration["enable_topic_4"].set(self.local_configuration["enable_topic_4"].get())
        self.configuration["service_topic_5"].set(self.local_configuration["service_topic_5"].get())
        self.configuration["enable_topic_5"].set(self.local_configuration["enable_topic_5"].get())

    def on_save(self) -> None:
        try:
            if self.validate():
                self.change_configuration()
                my_json = MyJSON('config.json', self.configuration)
                my_json.write()
                self.master.destroy()
        except Exception as err:
            messagebox.showerror(title="Erro", message=err)

    def on_cancel(self) -> None:
        self.master.destroy()

    def validate(self):
        if not self.validate_empty():
            messagebox.showwarning(title="Erro", message="Todos os campos devem ser preenchidos.")
            return False
        elif not Validator.validate_ip(self.local_configuration["server"].get()):
            messagebox.showwarning(title="Erro", message="Ip informado inválido no campo Server.")
            return False
        return True

    def validate_empty(self) -> bool:
        if self.local_configuration["server"].get() == "":
            return False
        elif self.local_configuration["port"].get() == "":
            return False
        elif self.local_configuration["application_topic"].get() == "":
            return False
        elif self.local_configuration["enable_topic_1"].get() == 1 and \
                self.local_configuration["service_topic_1"].get() == "":
            return False
        elif self.local_configuration["enable_topic_2"].get() == 1 and \
                self.local_configuration["service_topic_2"].get() == "":
            return False
        elif self.local_configuration["enable_topic_3"].get() == 1 and \
                self.local_configuration["service_topic_3"].get() == "":
            return False
        elif self.local_configuration["enable_topic_4"].get() == 1 and \
                self.local_configuration["service_topic_4"].get() == "":
            return False
        elif self.local_configuration["enable_topic_5"].get() == 1 and \
                self.local_configuration["service_topic_5"].get() == "":
            return False
        return True
