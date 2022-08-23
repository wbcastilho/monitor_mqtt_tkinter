import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from Config import Config
import json


class SettingsForm(ttk.Frame):
    def __init__(self, master, configuration):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.master = master
        self.configuration = configuration
        self.entry_server = None
        self.entry_port = None
        self.entry_application_topic = None
        self.entry_service_topic = None
        self.button_save = None
        self.button_cancel = None

        self.create_form_config()
        self.create_buttons()

    def create_form_config(self):
        label_frame = ttk.Labelframe(self, text='Configurações MQTT')
        label_frame.pack(fill="x", padx=10, pady=10)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=20)

        label = ttk.Label(frame, text="Servidor")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_server = ttk.Entry(frame,
                                      textvariable=self.configuration['server'],
                                      justify="center",
                                      width=30,
                                      )
        self.entry_server.grid(row=0, column=1, padx=2, sticky=ttk.W, pady=10)

        label = ttk.Label(frame, text="Porta")
        label.grid(row=1, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_port = ttk.Entry(frame,
                                    textvariable=self.configuration['port'],
                                    justify="center",
                                    width=10
                                    )
        self.entry_port.grid(row=1, column=1, padx=2, sticky=ttk.W, pady=10)

        label = ttk.Label(frame, text="Tópico da Aplicação")
        label.grid(row=2, column=0, padx=1, sticky=ttk.E, pady=10)

        self.entry_application_topic = ttk.Entry(frame, textvariable=self.configuration['application_topic'], width=70)
        self.entry_application_topic.grid(row=2, column=1, padx=2, sticky=ttk.W, pady=10)

        label = ttk.Label(frame, text="Tópico do Serviço")
        label.grid(row=3, column=0, padx=1, sticky=ttk.E, pady=10)

        entry = ttk.Entry(frame, width=70, textvariable=self.configuration['service_topic'])
        entry.grid(row=3, column=1, padx=2, sticky=ttk.W, pady=10)

    def create_buttons(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=10, pady=5)

        self.button_cancel = ttk.Button(frame, text="Cancelar", bootstyle="danger", command=self.on_cancel)
        self.button_cancel.pack(side=RIGHT, padx=5, pady=10)

        self.button_save = ttk.Button(frame, text="Salvar", bootstyle="success", command=self.on_save)
        self.button_save.pack(side=RIGHT, padx=5, pady=10)

    def on_save(self):
        config = Config(self.configuration['server'].get(),
                        self.configuration['port'].get(),
                        self.configuration['application_topic'].get(),
                        self.configuration['service_topic'].get())

        try:
            with open('config.json', 'w') as f:
                json.dump(config.__dict__, f)

                messagebox.showinfo(title="Info", message="Configuração salva com sucesso.")
        except Exception:
            messagebox.showerror(title="Erro", message="Falha ao salvar arquivo de configuração.")

        self.master.destroy()

    def on_cancel(self):
        self.master.destroy()
