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
            'service_topic': ttk.StringVar(),
        }
        self.entry_server = None
        self.entry_port = None
        self.entry_application_topic = None
        self.entry_service_topic = None
        self.button_save = None
        self.button_cancel = None

        masked_int = MaskedInt()
        self.digit_func = self.register(masked_int.mask_number)

        masked_entry = MaskedEntry()
        self.vcmd = self.register(masked_entry.mask_ip)

        self.init_configuration()
        self.create_form_config()
        self.create_form_monitoracao()
        self.create_buttons()

    def create_form_config(self):
        label_frame = ttk.Labelframe(self, text='Configurações MQTT')
        label_frame.pack(fill="x", padx=10, pady=10)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=20)

        label = ttk.Label(frame, text="Servidor")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_server = ttk.Entry(frame,
                                      textvariable=self.local_configuration['server'],
                                      justify="center",
                                      width=30,
                                      validate="key",
                                      validatecommand=(self.vcmd, '%S')
                                      )
        self.entry_server.grid(row=0, column=1, padx=2, sticky=ttk.W, pady=10)

        label = ttk.Label(frame, text="Porta")
        label.grid(row=1, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_port = ttk.Entry(frame,
                                    textvariable=self.local_configuration['port'],
                                    justify="center",
                                    width=10,
                                    validate="key",
                                    validatecommand=(self.digit_func, '%S', '%d')
                                    )
        self.entry_port.grid(row=1, column=1, padx=2, sticky=ttk.W, pady=10)

        label = ttk.Label(frame, text="Tópico da Aplicação")
        label.grid(row=2, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_application_topic = ttk.Entry(frame, textvariable=self.local_configuration['application_topic'],
                                                 width=70)
        self.entry_application_topic.grid(row=2, column=1, padx=2, sticky=ttk.W, pady=10)

    def create_form_monitoracao(self):
        label_frame = ttk.Labelframe(self, text='Monitoração Processo')
        label_frame.pack(fill="x", padx=10, pady=10)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=20)

        label = ttk.Label(frame, text="Tópico do Serviço")
        label.grid(row=3, column=0, padx=1, sticky=ttk.E, pady=10)

        entry = ttk.Entry(frame, width=70, textvariable=self.local_configuration['service_topic'])
        entry.grid(row=3, column=1, padx=2, sticky=ttk.W, pady=10)

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
        self.local_configuration["service_topic"].set(self.configuration["service_topic"].get())

    def change_configuration(self) -> None:
        self.configuration["server"].set(self.local_configuration["server"].get())
        self.configuration["port"].set(self.local_configuration["port"].get())
        self.configuration["application_topic"].set(self.local_configuration["application_topic"].get())
        self.configuration["service_topic"].set(self.local_configuration["service_topic"].get())

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
        elif self.local_configuration["service_topic"].get() == "":
            return False
        return True
