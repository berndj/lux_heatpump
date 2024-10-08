"""Heatpump engine module."""

import socket
import time
from enum import IntEnum

class HeatPumpMode(IntEnum):
    AUTO = 0
    ZWE = 1
    PARTY = 2
    VACATION = 3
    OFF = 4
    UNKNOWN = 5

class HeatPumpFunction(IntEnum):
    TEMPERATURE = 1100
    HEAT_CIRC = 3405
    HOT_WATER = 3505
    UNKNOWN = -1

    
class heatpump_engine:
    """Engine talking to the heatpump over ser2net."""

    def __init__(self):
        """Init heatpump connection."""
        self.heating_circuit_flow_temp = None
        self.heating_circuit_return_flow_temp_actual = None
        self.heating_circuit_return_flow_temp_setpoint = None
        self.domestic_hot_water_temp_setpoint = None
        self.domestic_hot_water_temp_actual = None
        self.outdoor_temp = None
        self.polls = 0
        self.polls_skipped = 0
        self.epoch_time = int(time.time())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = None
        self.port = None
        self.hot_water_mode = HeatPumpMode.UNKNOWN
        self.hot_heat_circ_mode = HeatPumpMode.UNKNOWN


    def align_peer(self, host, port):
        """Update host and port information."""
        if port != self.port or host != self.host:
            self.host = host
            self.port = port

    def maintain_socket(self, host, port):
        """Check and repair socket."""

        if True == self.is_socket_closed(self.sock) or port != self.port or host != self.host:
            self.align_peer(host, port)
            self.sock.close()
            self.sock = None
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(0.1)
            if -1 == self.connect():
                return -1
        return 0

    def poll_for_stats(self, host, port):
        """Poll sensor data."""

        new_time = int(time.time())
        if new_time - self.epoch_time > 5 or self.polls == 0:
            if 0 == self.maintain_socket(host, port):
                if 0 != self.trigger_stats(HeatPumpFunction.TEMPERATURE):
                    return -1
                self.readlines(HeatPumpFunction.TEMPERATURE)

                if 0 != self.trigger_stats(HeatPumpFunction.HOT_WATER):
                    return -1
                self.readlines(HeatPumpFunction.HOT_WATER)

                if 0 != self.trigger_stats(HeatPumpFunction.HEAT_CIRC):
                    return -1
                self.readlines(HeatPumpFunction.HEAT_CIRC)

                self.epoch_time = new_time
                self.polls += 1
        else:
            self.polls_skipped += 1

    def is_socket_closed(self, sock: socket.socket) -> bool:
        """Check socket closed state."""
        sock.settimeout(0.1)
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return False
        except BlockingIOError:
            return True  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except Exception:  # noqa: BLE001
            return True  # socket was closed for some other reason
        return True

    def connect(self):
        """Connect to ser2net socket."""
        try:
            self.sock.connect((self.host, self.port))
        except TimeoutError:
            print('oops timeout')
            return -1
        except ConnectionAbortedError:
            print('oops abortr')
            return -1
        except socket.gaierror:
            print('oops gaierror')
            return -1
        print('connect ok')
        return 0

    def readlines(self, function):
        """Read answer from ser2net/heatpump."""
        data = b""
        self.sock.settimeout(0.5)
        while True:
            try:
                new_data = self.sock.recv(1024)
            except TimeoutError:
                break
            except ConnectionAbortedError:
                break
            data += new_data
            if len(new_data) == 0:
                break

        lines = data.split(b"\r\n")
        for line in lines:
            if function == HeatPumpFunction.TEMPERATURE:
                self.extract_temp(line)
            else:
                self.extract_mode(line, function)
                
    def trigger_stats(self, function):
        """Trigger response from heatpump."""
        # buf = "1800\n\r" # most stats
        buf = "" + str(function.value) + "\n\r"  # temperature stats only
        print(buf)
        try:
            self.sock.send(buf.encode(encoding="utf-8"))
        except BrokenPipeError:
            return -1
        return 0

    def extract_temp(self, line):
        """Extract temperature values from response."""

        ser_str = line.decode("utf-8")
        tokens = ser_str.split(";")
        try:
            cat1 = int(tokens[0])
            if len(tokens) > 1:
                nr_tokens = int(tokens[1])
            else:
                return
        except ValueError:
            return

        if cat1 == 1100 and nr_tokens == 12 and len(tokens) == nr_tokens+2:
            for token in tokens:
                print(token)
            tokens.pop(0)
            tokens.pop(0)
            print(ser_str)
            try:
                self.heating_circuit_flow_temp = float(tokens[0]) / 10.0
                self.heating_circuit_return_flow_temp_actual = float(tokens[1]) / 10.0
                self.heating_circuit_return_flow_temp_setpoint = float(tokens[2]) / 10.0
                self.outdoor_temp = float(tokens[4]) / 10.0
                self.domestic_hot_water_temp_actual = float(tokens[5]) / 10.0
                self.domestic_hot_water_temp_setpoint = float(tokens[6]) / 10.0
            except ValueError:
                return

    def extract_mode(self, line, function):
        """Extract temperature values from response."""

        if function == HeatPumpFunction.HEAT_CIRC or function == HeatPumpFunction.HOT_WATER:  
            ser_str = line.decode("utf-8")
            tokens = ser_str.split(";")
            try:
                cat1 = int(tokens[0])
                if len(tokens) > 1:
                    nr_tokens = int(tokens[1])
                else:
                    return -1
            except ValueError:
                return -1
        else:
            return -1

        if cat1 == function.value and nr_tokens == 1 and len(tokens) == nr_tokens+2:
            for token in tokens:
                print(token)
            tokens.pop(0)
            tokens.pop(0)
            print(ser_str)
            if function == HeatPumpFunction.HEAT_CIRC:
                self.heat_circ_mode = HeatPumpMode(int(tokens[0]))
            else:
                self.hot_water_mode = HeatPumpMode(int(tokens[0]))

            
    def print_sensors(self):
        print(
            "=============================================================================="
        )
        print()
        print("Heating mode:   \t" + str(self.heat_circ_mode.name))
        print("Hot water mode: \t" + str(self.hot_water_mode.name))
        
        print()
        print("Poll=" + str(self.polls) + " Polls_skipped=" + str(self.polls_skipped))
        print("Outdoor temperature\t\t\t\t\t = %s" % (str(self.outdoor_temp)))
        print()
        print(
            "heating circuit flow temperature \t\t\t = %s"
            % (str(self.heating_circuit_flow_temp))
        )
        print(
            "heating circuit return flow temperature (actual)\t = %s"
            % (self.heating_circuit_return_flow_temp_actual)
        )
        print(
            "heating circuit return flow temperature (setpoint)\t = %s"
            % (self.heating_circuit_return_flow_temp_setpoint)
        )
        print(
            "domestic hot water temperature (actual)\t\t\t = %s"
            % (self.domestic_hot_water_temp_actual)
        )
        print(
            "domestic hot water temperature (setpoint)\t\t = %s"
            % (self.domestic_hot_water_temp_setpoint)
        )
        print(
            "=============================================================================="
        )



my_heatpump_engine = heatpump_engine()


if __name__ == "__main__":
    conn = heatpump_engine()
    while True:
        conn.poll_for_stats("baba-cafe.local", 4322)
        conn.print_sensors()
        time.sleep(4)





        
