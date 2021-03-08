import re

WHITESPACE_BINARY = '1000000'


class HackerLanguage:
    _message = ''

    # - all letters and whitespaces will be converted into their ASCII codes and than into the binary numbers.
    #
    # Except
    # the whitespaces - their binary form should be '1000000' not '100000'.
    #
    # - numbers, dates (in the 'dd.mm.yyyy'
    # format), time (in the 'hh:mm' format)
    #
    # and special signs ('.', ':', '!', '?', '@', '$', '%') won't be converted.

    def scan(self, message):

        tokens = []

        def write_date(_, token):
            tokens.append(token)

        def write_time(_, token):
            tokens.append(token)

        def write_whitespace(_, token):
            tokens.append('1000000')

        def write_other(_, token):
            tokens.append(f'{ord(token):<07b}')

        scanner = re.Scanner([(r'\d{2}\.\d{2}\.\d{4}', write_date),
                              (r'\d{2}\:\d{2}', write_time),
                              (r'\w|\s', write_other)])
        scanner.scan(message)

        print('Tokens:', tokens)

    @staticmethod
    def encode(message):
        print('Encode message:', message)

        encoded_message = ''
        for symbol in message:
            if symbol == ' ':
                binary = WHITESPACE_BINARY
            else:
                binary = f'{ord(symbol):b}'
            print('Binary:', binary)
            encoded_message += binary
        return encoded_message

    @staticmethod
    def decode(message):
        return message

    def write(self, text):
        self._message += text

    def delete(self, symbol_count):
        self._message = self._message[:len(self._message) - symbol_count]

    def send(self):
        return self.encode(self._message)

    def read(self, text):
        return self.decode(text)


if __name__ == '__main__':
    message_1 = HackerLanguage()
    message_1.scan('te st')

    # message_1.write("secrit")
    # message_1.delete(2)
    # message_1.write("et")
    # message_2 = HackerLanguage()
    #
    # assert message_1.send() == "111001111001011100011111001011001011110100"
    # assert message_2.read("11001011101101110000111010011101100") == "email"