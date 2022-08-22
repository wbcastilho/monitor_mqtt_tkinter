import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pathlib import Path
from CollapsingFrame import CollapsingFrame


class MainForm(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        image_files = {
            'play': 'icons8-reproduzir-24.png',
            'stop': 'icons8-parar-24.png',
            'settings-light': 'icons8-configuracoes-24.png'
        }

        self.photoimages = []
        imgpath = Path(__file__).parent / 'assets'
        for key, val in image_files.items():
            _path = imgpath / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

        # buttonbar
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=X, pady=1, side=TOP)

        btn = ttk.Button(
            master=buttonbar, text='Iniciar',
            image='play',
            compound=LEFT
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        btn = ttk.Button(
            master=buttonbar,
            text='Parar',
            image='stop',
            compound=LEFT
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        btn = ttk.Button(
            master=buttonbar,
            text='Configurações',
            image='settings-light',
            compound=LEFT
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        label_frame = ttk.Labelframe(self, text='Monitoração Processo')
        label_frame.pack(fill="x", padx=10, pady=20)

        frame = ttk.Frame(label_frame)
        frame.pack(fill="x", padx=20, pady=20)

        label = ttk.Label(frame, text="Processo")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E, pady=10)

        self.combobox_process = ttk.Combobox(frame, width=50)
        self.combobox_process.grid(row=0, column=1, padx=2, sticky=ttk.W, pady=10)

        statusbar = ttk.Frame(self, style='secondary.TFrame')
        statusbar.pack(fill=X, side=BOTTOM)

        # danger colored inverse label style
        label = ttk.Label(statusbar, bootstyle="inverse-danger", text=" Conectado ao broker ", font='Arial 8 bold')
        label.pack(side=LEFT, padx=10, pady=5)

        label = ttk.Label(statusbar, bootstyle="inverse-success", text=" Processo ativo ", font='Arial 8 bold')
        label.pack(side=LEFT, padx=0, pady=5)


