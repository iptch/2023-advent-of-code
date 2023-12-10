class Trebuchet:
    def run(self):
        print(f'Part 1: {self.get_sum("input", 0)}')
        print(f'Part 2: {self.get_sum("input", 1)}')
        print(f'Part 1: {self.get_sum("input2", 0)}')
        print(f'Part 2: {self.get_sum("input2", 1)}')

    def get_numbers(self, code, mode):
        if mode == 0:
            return ''.join([char for char in code if char.isdigit()])
        elif mode == 1:
            return self.replace_word_with_number(code)
        else:
            raise ValueError('Mode must be 0 or 1')

    def get_sum(self, file_name, mode):
        codes = (self.read_file(file_name))
        code_sum = 0
        for code2 in codes:
            code = self.get_numbers(code2, mode)
            value = self.get_value_of_code(code)
            code_sum += int(value)
        return code_sum

    @staticmethod
    def read_file(file_name):
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines]
                return lines
        except FileNotFoundError:
            print(f'The file {file_name} was not found.')
            return []
        except Exception as error:
            print(f'An error occurred: {error}')
            return []

    @staticmethod
    def get_value_of_code(number):
        if number == "":
            new_number = "0"
        elif int(number) < 10:
            new_number = number[0] + number[0]
        elif int(number) > 99:
            new_number = number[0] + number[len(number) - 1]
        else:
            return int(number)
        return int(new_number)

    @staticmethod
    def replace_word_with_number(code):
        replacements = {
            'one': '1',
            'two': '2',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9'
        }

        i = 0
        while i < len(code):
            for word, number in replacements.items():
                if code[i:i+len(word)] == word:
                    code = code[:i] + number + code[i:]
                    i += 1
                    break
            i += 1

        return ''.join([char for char in code if char.isdigit()])


if __name__ == '__main__':
    trebuchet = Trebuchet()
    trebuchet.run()
