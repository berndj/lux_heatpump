# Luxtronik-v1 based heatpump sensor home assistant integration.

This is a home assistant integration for Luxtronik-v1 based heatpumps.

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

Add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
sensor:
  - platform: lux_heatpump
```

