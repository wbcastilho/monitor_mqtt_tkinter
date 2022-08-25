import psutil as ps
import os


class MyPsutil:

    @staticmethod
    def show_activate_processess() -> list:
        process_set = set()

        try:
            for proc in ps.process_iter():
                info = proc.as_dict(attrs=['pid', 'name'])
                process_set.add(info['name'])
            return sorted(process_set)
        except Exception:
            raise Exception("Erro ao listar processos.")

    @staticmethod
    def check_process_exist(process_name: str) -> bool:
        try:
            return process_name in (i.name() for i in ps.process_iter())
        except Exception:
            raise Exception("Erro ao localizar processo.")

    @staticmethod
    def check_files_size(path: str, max_size: float) -> bool:
        try:
            files_list = os.scandir(path)
            for file in files_list:
                if file.is_file():
                    file_size = file.stat().st_size
                    if file_size < max_size:
                        print("Gera alarme")
                        return False
                    else:
                        print("Sem alarme")
                        return True
            return True
        except Exception:
            raise Exception("Falha inesperada ao checar tamenho dos arquivos do diretório selecionado.")

