from MainForm import MainForm
import ttkbootstrap as ttk


if __name__ == '__main__':
    app = ttk.Window(
        title="Monitor MQTT",
    )
    MainForm(app)

    app.mainloop()
