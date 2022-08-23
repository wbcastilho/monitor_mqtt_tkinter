import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from pathlib import Path
from MyPsutil import MyPsutil
from Config import Config
from MyJSON import MyJSON
from SettingsForm import SettingsForm


class MainForm(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)
        self.start = False
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
            'settings-light': 'icons8-configuracoes-24.png'
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

        label = ttk.Label(statusbar, bootstyle="inverse-danger", text=" Conectado ao broker ", font='Arial 8 bold')
        label.pack(side=LEFT, padx=10, pady=5)

        label = ttk.Label(statusbar, bootstyle="inverse-success", text=" Processo em execução ", font='Arial 8 bold')
        label.pack(side=LEFT, padx=0, pady=5)

    def on_action(self):
        if not self.start:
            self.button_action['image'] = 'stop'
            self.button_action['text'] = 'Parar'
        else:
            self.button_action['image'] = 'play'
            self.button_action['text'] = 'Iniciar'

        self.start = not self.start

    def on_settings(self):
        setting_form = ttk.Toplevel(self)
        setting_form.title("Configurações")
        setting_form.grab_set()
        setting_form.resizable(False, False)
        SettingsForm(setting_form, self.configuration)

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


