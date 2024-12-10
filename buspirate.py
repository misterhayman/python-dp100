import serial
import traceback
import DP100API

BUSPIRATE_PORT = "COM8"


def send(ser, cmd, silent=False):
    """
    send the command and listen to the response.
    returns a list of the returned lines.
    The first item is always the command sent.
    """
    ser.flush()
    ser.write((cmd + "\r\n").encode("ascii"))  # send our command
    ser.flush()
    lines = []
    for line in ser.readlines():
        line = line.decode("utf8").strip()
        if not silent:
            print(line)
        lines.append(line)
    return lines


def get_colors():
    lines = send(ser, "[0x72 0x94 [0x73 rrrrrrrr]", silent=True)  # read data
    for line in lines:
        if line.startswith("RX: "):
            vals = line.split()
            c = int(vals[3], 0) * 0x100 + int(vals[1], 0)
            # r = int(vals[7], 0) * 0x100 + int(vals[5], 0)
            # g = int(vals[11], 0) * 0x100 + int(vals[9], 0)
            # b = int(vals[15], 0) * 0x100 + int(vals[13], 0)
            return c  # , r, g, b


dp100 = DP100API.DP100()
dp100.connect()

# the speed of sequential commands is determined by this timeout
ser = serial.Serial(BUSPIRATE_PORT, 115200, timeout=0.5)

send(ser, "n", silent=True)
send(ser, "m", silent=True)
send(ser, "5", silent=True)
send(ser, "n", silent=True)
send(ser, "4", silent=True)
send(ser, "1", silent=True)
send(ser, "W", silent=True)
send(ser, "3.3", silent=True)
send(ser, "200", silent=True)
send(ser, "[0x72 0x80 0x03]", silent=True)  # enable sensor
send(ser, "[0x72 0x8F 0x03]", silent=True)  # set gain to 64x
send(ser, "[0x72 0x81 246]", silent=True)  # set integral time to 10ms

counter = 0
is_dp100_on = dp100.get_state()["output"]

try:
    with open("c:/Users/alex/Desktop/colors.txt", "w", buffering=1) as f:
        while True:
            # c, r, g, b = get_colors()
            # printme = f"{c},{r},{g},{b}"
            c = get_colors()
            printme = f"{c}"
            print(printme)
            print(printme, file=f)

            if is_dp100_on:
                if c > 8200:
                    counter += 1
                    if counter > 10:
                        dp100.set_output(False)
                        is_dp100_on = False
                else:
                    counter = 0
            else:
                counter += 1
                if counter > 4:
                    counter = 0
                    dp100.set_output(True)
                    is_dp100_on = True
except Exception:
    traceback.print_exc()
finally:
    ser.close()  # disconnect so we can access it from another app
    dp100.disconnect()
