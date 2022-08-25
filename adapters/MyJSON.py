import json
from models.Config import Config


class MyJSON:
    def __init__(self, file, configuration):
        self.file = file
        self.configuration = configuration

    def write(self) -> None:
        config = Config(self.configuration['server'].get(), self.configuration['port'].get(),
                        self.configuration['application_topic'].get(),
                        self.configuration['service_topic'].get())

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
                self.configuration['service_topic'].set(config.service_topic)
        except PermissionError:
            raise PermissionError("Sem permissão para abrir o arquivo de configuração.")
        except FileNotFoundError:
            raise FileNotFoundError("Arquivo de configuração não encontrado.")
        except Exception:
            raise Exception("Falha ao abir arquivo de configuração.")