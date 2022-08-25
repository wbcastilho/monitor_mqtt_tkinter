class MaskedInt:
    def __init__(self):
        self.count = 0

    def max_length(self, type_action):
        if int(type_action) == 1:
            if self.count < 6:
                self.count += 1
                return True
            return False
        else:
            if self.count > 0:
                self.count -= 1
            return True

    def mask_number(self, value, type_action) -> bool:
        if value.isdigit():
            return self.max_length(type_action)
        elif value == "":
            return True
        return False
