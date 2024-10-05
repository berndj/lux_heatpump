# Home assistant integration for Luxtronik-v1 based heatpump sensors.


### Prerequisites
Luxtronik-v1 board RS-232 is connected to with ser2net.

Example ser2net configuration file, normally located undr /etc/2net.yaml
```yaml
define: &banner \r\nser2net port \p device \d [\B] (Debian GNU/Linux)\r\n\r\n
connection: &heatpump_rs233
    accepter: tcp,4322
    Enable: on
    options:
        kickolduser: true
    connector: serialdev,
               /dev/serial/by-id/usb-FTDI_FT232R_USB_UART_B0028CZ9-if00-port0,
               57600n81,local
```

### Installation

Copy this folder to `<config_dir>/custom_components/lux_heatpump/`.

Add the following to your `<config_dir>/configuration.yaml` file:

```yaml
# Entry in configuration.yaml entry
sensor:
  - platform: lux_heatpump
```

### TODO

- [ ] Add ser2net host:port configuration to configuration.yaml (Currently in sensor.py, line peer = Peer("hostname", 4711)
- [ ] Add configuration workflow for hostname,port
- [ ] Add mode indication (off,party,auto)
- [ ] Add mode configuration (off,party,auto)
