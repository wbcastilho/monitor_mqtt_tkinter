import json
from models.Config import Config


class MyJSON:
    def __init__(self, file, configuration):
        self.file = file
        self.configuration = configuration

    def write(self) -> None:
        config = Config(self.configuration['server'].get(),
                        self.configuration['port'].get(),
                        self.configuration['application_topic'].get(),
                        self.configuration['service_topic_1'].get(),
                        self.configuration['enable_topic_1'].get(),
                        self.configuration['service_topic_2'].get(),
                        self.configuration['enable_topic_2'].get(),
                        self.configuration['service_topic_3'].get(),
                        self.configuration['enable_topic_3'].get(),
                        self.configuration['service_topic_4'].get(),
                        self.configuration['enable_topic_4'].get(),
                        self.configuration['service_topic_5'].get(),
                        self.configuration['enable_topic_5'].get())

        try:
            with open(self.file, 'w') as f:
                json.dump(config.__dict__, f)
        except Exception:
            raise Exception("Erro ao salvar arquivo de configuração.")

    def read(self) -> None:
        try:
            with open(self.file, 'r') as f:
                data = json.load(f)
                config = Config(**data)
                self.configuration['server'].set(config.server)
                self.configuration['port'].set(config.port)
                self.configuration['application_topic'].set(config.application_topic)
                self.configuration['service_topic_1'].set(config.service_topic_1)
                self.configuration['enable_topic_1'].set(config.enable_topic_1)
                self.configuration['service_topic_2'].set(config.service_topic_2)
                self.configuration['enable_topic_2'].set(config.enable_topic_2)
                self.configuration['service_topic_3'].set(config.service_topic_3)
                self.configuration['enable_topic_3'].set(config.enable_topic_3)
                self.configuration['service_topic_4'].set(config.service_topic_4)
                self.configuration['enable_topic_4'].set(config.enable_topic_4)
                self.configuration['service_topic_5'].set(config.service_topic_5)
                self.configuration['enable_topic_5'].set(config.enable_topic_5)
        except PermissionError:
            raise PermissionError("Sem permissão para abrir o arquivo de configuração.")
        except FileNotFoundError:
            raise FileNotFoundError("Arquivo de configuração não encontrado.")
        except Exception:
            raise Exception("Falha ao abir arquivo de configuração.")