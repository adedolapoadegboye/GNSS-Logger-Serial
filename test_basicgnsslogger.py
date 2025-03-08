import os
import pytest
import serial
from unittest.mock import MagicMock, patch
from basicgnsslogger import BasicGnssLogger

# Test Constants
TEST_PORT = "/dev/ttyUSB0"
TEST_BAUDRATE = 115200
TEST_TIMEOUT = 1
TEST_LOGTIME = 2
TEST_FILENAME = "logs/test_gnss_logger.txt"


### ====================== UNIT TESTS ====================== ###

def test_logger_initialization():
    """Test if BasicGnssLogger initializes correctly."""
    logger = BasicGnssLogger(TEST_PORT, TEST_BAUDRATE, TEST_TIMEOUT, TEST_FILENAME, TEST_LOGTIME)

    assert logger.port == TEST_PORT
    assert logger.baudrate == TEST_BAUDRATE
    assert logger.timeout == TEST_TIMEOUT
    assert logger.filename == TEST_FILENAME
    assert logger.logtime == TEST_LOGTIME
    assert logger.serial_connection is None


@patch("serial.Serial")
def test_connect_to_serial_port_success(mock_serial):
    """Test successful serial connection."""
    mock_serial.return_value = MagicMock()

    logger = BasicGnssLogger(TEST_PORT, TEST_BAUDRATE, TEST_TIMEOUT, TEST_FILENAME, TEST_LOGTIME)
    logger.connect_to_serial_port()

    assert logger.serial_connection is not None


@patch("serial.Serial", side_effect=serial.SerialException("Serial Error"))
def test_connect_to_serial_port_failure(mock_serial):
    """Test serial connection failure."""
    logger = BasicGnssLogger(TEST_PORT, TEST_BAUDRATE, TEST_TIMEOUT, TEST_FILENAME, TEST_LOGTIME)
    logger.connect_to_serial_port()

    assert logger.serial_connection is None  # Connection should fail


### ====================== INTEGRATION TEST ====================== ###

@patch("serial.Serial")
def test_full_logger_run(mock_serial):
    """Test running the logger with mocked serial input."""
    mock_serial_instance = MagicMock()
    mock_serial_instance.readline.return_value = b"$GNGGA,123519.00,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\n"
    mock_serial.return_value = mock_serial_instance

    logger = BasicGnssLogger(TEST_PORT, TEST_BAUDRATE, TEST_TIMEOUT, TEST_FILENAME, TEST_LOGTIME)
    logger.run()

    assert os.path.exists(TEST_FILENAME)  # Log file should be created
