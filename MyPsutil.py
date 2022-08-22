import psutil as ps


class MyPsutil:

    @staticmethod
    def show_activate_processess() -> list:
        process_set = set()

        for proc in ps.process_iter():
            info = proc.as_dict(attrs=['pid', 'name'])
            process_set.add(info['name'])
        return sorted(process_set)

    @staticmethod
    def check_process_exist(process_name: str) -> bool:
        return process_name in (i.name() for i in ps.process_iter())

