"""Constants for lux_heatpump component."""

from enum import IntEnum

DOMAIN = "lux_heatpump"

POLL_INTERVAL = 5  # seconds


class HeatPumpType(IntEnum):
    """Heatpump type."""

    ERC = 0
    SW1 = 1
    SW2 = 2
    WW1 = 3
    WW2 = 4
    L1I = 5
    L2I = 6
    L1A = 7
    L2A = 8
    KSW = 9
    KLW = 10
    SWC = 11
    ALPHA_INNOTEC_LWC = 12
    L2G = 13
    WZS = 14
    L1I407 = 15
    L2I407 = 16
    L1A407 = 17
    L2A407 = 18
    L2G407 = 19
    LWC407 = 20
    L1AREV = 21
    L2AREV = 22
    WWC1 = 23
    WWC2 = 24
    L2G404 = 25
    WZW = 26
    L1S = 27
    L1H = 28
    L2H = 29
    WZWD = 30
    WWB_20 = 40
    LD5 = 41
    LD7 = 42
    UNKNOWN = -1
