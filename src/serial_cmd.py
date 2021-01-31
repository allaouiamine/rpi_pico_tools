import serial
from time import sleep


class SerialCmd:
    def __init__(self, tty_name, eol='\r\n', encoding='ascii'):
        self._tty_name = tty_name
        self._eol = eol
        self._encoding = encoding
        self._ser = None

    @property
    def ser(self):
        if self._ser is None:
            self._ser = serial.Serial(self._tty_name, timeout=1)
        return self._ser

    def _decode(self, line):
        line = line.decode(self._encoding)
        return line.strip('\n').strip('\r')

    def _read_output(self):
        return [
            self._decode(o) for o in self.ser.readlines()
            if not self._decode(o).strip().endswith('>')
        ]

    def send_bin(self, byte_array):
        self.ser.write(byte_array)
        sleep(.5)
        return self._read_output()

    def send_code(self, code_to_run):
        # Interrupt the current code execution
        # End of Text ETX -- CANCEL  -- \x03 CTRL+C  
        self.send_bin(b'\x03')
        sleep(3)

        # Start Paste mode
        # End of Transmission EOT -- REBOOT \x04 CTRL+D
        self.send_bin(b'\x05')

        # Send code
        # Enquiry ENQ -- PASTE MODE -- \x04 CTRL+E
        o = self.send_bin(code_to_run.encode('ascii'))

        # End Paste mode CTRL+D
        # End of Transmission EOT -- REBOOT \x04 CTRL+D
        # Can also used for soft reboot
        o = self.send_bin(b'\x04')
        print('\n'.join(o))

        # Soft reboot to run main.py
        o = self.send_bin(b'\x04')
        print('\n'.join(o))

        return self._read_output()

    def close(self):
        self.ser.close()
