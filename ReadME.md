# Basic GNSS Logger

A Python script to log GNSS NMEA data from a serial connection.

## 🚀 Features
- Reads GNSS data from serial (USB/UART).
- Filters and logs valid NMEA sentences.
- Saves data to a structured log file.
- Automatically creates log directories if they don’t exist.
- Handles serial connection errors gracefully.
- Provides configurable logging duration.

## 🔧 Requirements
- Python 3.x
- `pyserial` library
- `pytest` (for running tests)

## 📌 Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/gnss-logger.git
   cd gnss-logger
   ```

2. Install Dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set your serial and file configs in `basicgnsslogger.py`:
   ```python
   port = "/dev/ttyUSB0"
   baudrate = 115200
   logtime = 10  # Logging duration in seconds
   ```

4. Run the logger:
   ```sh
   python basicgnsslogger.py
   ```

## 🛠 Running Tests
Run unit and integration tests using:
```sh
pytest test_basicgnsslogger.py -v
```

## 📜 License
MIT License

