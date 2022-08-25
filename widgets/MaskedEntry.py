class MaskedEntry:
    # def __init__(self):
    # self.count_point = 0
    # self.count_number = 0

    @staticmethod
    def mask_number(value) -> bool:
        if value.isdigit():
            return True
        elif value == "":
            return True
        else:
            return False

    @staticmethod
    def mask_ip(self, value, type_action):
        if value.isdigit():
            '''if int(type_action) == 1:
                if self.count_number < 3:
                    self.count_number += 1
                    return True
                else:
                    return False'''
            return True
        elif value == ".":
            '''if int(type_action) == 1:
                if self.count_point < 3:
                    self.count_point += 1
                    self.count_number = 0
                    return True
                else:
                    return False'''
            return True
        else:
            return False

