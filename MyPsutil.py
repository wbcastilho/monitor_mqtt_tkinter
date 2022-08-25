import psutil as ps


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

