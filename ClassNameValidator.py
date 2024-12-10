class ClassNameValidator:
    @staticmethod
    def validate(inp: str) -> bool:
        if len(inp) == 1 and inp.isdigit() and inp != '0':
            return True  # '7' shall be valid
        elif len(inp) == 2 and inp[0].isdigit() and not inp[1].isdigit() and inp[0] != '0':
            return True  # '1A' shall be valid
        elif len(inp) == 2 and inp.isdigit() and int(inp) < 13 and inp[0] != '0':
            return True  # '12' shall be valid
        elif len(inp) == 3 and inp[0:2].isdigit() and not inp[2].isdigit() and int(inp[0:2]) < 13 and inp[0] != '0':
            return True  # '12C' shall be valid
        else:
            return False
    