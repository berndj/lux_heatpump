"""Heatpump engine module."""

import socket
import time


class heatpump_engine:
    """Engine talking to the heatpump over ser2net."""

    def __init__(self):
        """Init heatpump connection."""
        self.heating_circuit_flow_temp = 0.0
        self.heating_circuit_return_flow_temp_actual = 0.0
        self.heating_circuit_return_flow_temp_setpoint = 0.0
        self.domestic_hot_water_temp_setpoint = 0.0
        self.domestic_hot_water_temp_actual = 0.0
        self.outdoor_temp = 0.0
        self.polls = 0
        self.polls_skipped = 0
        self.epoch_time = int(time.time())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = None
        self.port = None

    def align_peer(self, host, port):
        """Update host and port information."""
        if port != self.port or host != self.host:
            self.host = host
            self.port = port

    def maintain_socket(self, host, port):
        """Check and repair socket."""

        if self.is_socket_closed(self.sock) or port != self.port or host != self.host:
            self.align_peer(host, port)
            self.sock.close()
            self.sock = None
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))

    def poll_for_stats(self, host, port):
        """Poll sensor data."""

        new_time = int(time.time())
        if new_time - self.epoch_time > 5 or self.polls == 0:
            self.maintain_socket(host, port)
            self.trigger_stats()
            self.readlines()
            self.epoch_time = new_time
            self.polls += 1
        else:
            self.polls_skipped += 1

    def is_socket_closed(self, sock: socket.socket) -> bool:
        """Check socket closed state."""
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except Exception:  # noqa: BLE001
            return False  # socket was closed for some other reason
        return False

    def connect(self):
        """Connect to ser2net socket."""
        try:
            self.sock.connect((self.host, self.port))
        except ConnectionError:
            # print("Connection Failed")
            return

    def readlines(self):
        """Read answer from ser2net/heatpump."""
        self.sock.settimeout(0.1)
        while True:
            try:
                data = self.sock.recv(1024)
            except TimeoutError:
                break
            except ConnectionAbortedError:
                break
            lines = data.split(b"\r\n")
            if len(data) == 0:
                break
            for line in lines:
                self.extract_temp(line)

    def trigger_stats(self):
        """Trigger response from heatpump."""
        # buf = "1800\n\r" # most stats
        buf = "1100\n\r"  # temperature stats only
        self.sock.send(buf.encode(encoding="utf-8"))

    def extract_temp(self, line):
        """Extract temperature values from response."""

        ser_str = line.decode("utf-8")
        tokens = ser_str.split(";")
        try:
            cat1 = int(tokens[0])
            if len(tokens) > 1:
                cat2 = int(tokens[1])
            else:
                return
        except ValueError:
            return

        if cat1 == 1100 and cat2 == 12 and len(tokens) >= 9:
            tokens.pop(0)
            tokens.pop(0)
            #            for token in tokens:
            #                print(token)
            try:
                self.heating_circuit_flow_temp = float(tokens[0]) / 10
                self.heating_circuit_return_flow_temp_actual = float(tokens[1]) / 10
                self.heating_circuit_return_flow_temp_setpoint = float(tokens[2]) / 10
                self.outdoor_temp = float(tokens[4]) / 10
                self.domestic_hot_water_temp_actual = float(tokens[5]) / 10
                self.domestic_hot_water_temp_setpoint = float(tokens[6]) / 10
            except ValueError:
                return


# pylint: disable=pointless-string-statement'
"""
        def print_sensors(self):
        print(
            "=============================================================================="
        )
        print()
        print("Poll=" + str(self.polls) + " Polls_skipped=" + str(self.polls_skipped))
        print("Outdoor temperature\t\t\t\t\t = %.1f" % (self.outdoor_temp))
        print()
        print(
            "heating circuit flow temperature \t\t\t = %.1f"
            % (self.heating_circuit_flow_temp)
        )
        print(
            "heating circuit return flow temperature (actual)\t = %.1f"
            % (self.heating_circuit_return_flow_temp_actual)
        )
        print(
            "heating circuit return flow temperature (setpoint)\t = %.1f"
            % (self.heating_circuit_return_flow_temp_setpoint)
        )
        print(
            "domestic hot water temperature (actual)\t\t\t = %.1f"
            % (self.domestic_hot_water_temp_actual)
        )
        print(
            "domestic hot water temperature (setpoint)\t\t = %.1f"
            % (self.domestic_hot_water_temp_setpoint)
        )
"""

my_heatpump_engine = heatpump_engine()


if __name__ == "__main__":
    conn = heatpump_engine()
    while True:
        conn.poll_for_stats("baba-cafe", 4322)
        #        conn.print_sensors()
        time.sleep(4)
