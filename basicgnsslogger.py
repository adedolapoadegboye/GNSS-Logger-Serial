import os
import serial
import time
import logging

DEVMODE = False

from serial.serialutil import SerialException
logging.basicConfig(filename="errors.log", level=logging.ERROR, filemode="a+")

class BasicGnssLogger:
    """
    A class to log GNSS data from a serial connection.

    Attributes:
        port (str): Serial port name (e.g., "/dev/ttyUSB0").
        baudrate (int): Baud rate for communication (e.g., 115200).
        timeout (float): Read timeout in seconds.
        filename (str): Path to the output log file.
        logtime (int): Duration for logging in seconds.
    """

    def __init__(self, port, baudrate, timeout, filename, logtime):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.filename = filename
        self.logtime = logtime
        self.serial_connection = None

    def connect_to_serial_port(self):
        """
        Establishes a serial connection to the GNSS module.

        Raises:
            serial.SerialException: If the connection fails.
        """

        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, self.timeout)
            print("Serial connection successful") if DEVMODE else None
        except serial.SerialException as e:
            print(e) if DEVMODE else None
            logging.error(msg=f"Serial error: {e}")

    def read_data(self):
        """
        Reads data from the GNSS module for a specified number of seconds.

        :raises:
            OSError: If the file input fails.

        :returns:
            -1 : If there is no serial connection to read from.
        """

        if not self.serial_connection or not self.serial_connection.is_open:
            print("Serial connection is not available.") if DEVMODE else None
            return

        start = time.time()
        now = time.time()
        try:
            os.makedirs("logs", exist_ok=True)
            with open(file=self.filename, mode="w+") as file:
                while (now - start) < self.logtime:
                    data = self.serial_connection.readline().decode("utf-8")
                    if data and data[0:1] == "$":
                        file.write(data)
                        print(data) if DEVMODE else None
                        now = time.time()
                    else:
                        continue
                self.close_file(file)
        except OSError as e:
            print(e) if DEVMODE else None
            logging.error(msg=f"File I/O error: {e}")

    def disconnect_from_serial_port(self):
        """
        Disconnects and closes serial connection.

        :raises:
            SerialException: If the attempt to disconnect and close connection fails.
        """
        try:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
                print("Serial connection closed") if DEVMODE else None
        except SerialException as e:
            print(e) if DEVMODE else None
            logging.error(msg=f"Error closing serial connection of NoneType. {e}")

    def close_file(self, file):
        """ Safely close the serial connection. """

        try:
            print(f"File {self.filename} closed") if DEVMODE else None
        except Exception as e:
            print(e) if DEVMODE else None

    def run(self):
        """ Execute the full GNSS logging process. """

        self.connect_to_serial_port()
        self.read_data()
        self.disconnect_from_serial_port()

if __name__ == "__main__":
    timestamp = int(time.time())
    port = "/dev/tty.usbserial-1470"
    baudrate = 115200
    timeout = 1
    filename = f"logs/{timestamp}_basic_gnss_logger.txt"
    logtime = 5
    logger = BasicGnssLogger(port, baudrate, timeout, filename, logtime)
    logger.run()