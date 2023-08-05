import serial
import time
import binascii
from serial.tools import list_ports

# version
MAJOR_VERSION = 1
MINOR_VERSION = 1
BUGFIX_VERSION = 6
VERSION = str(MAJOR_VERSION) + "." + str(MINOR_VERSION) + "." + str(BUGFIX_VERSION)

# Firmata

REPORT_VERSION = 0x79

# parameters
SERVO_ROT_NUM           = 0
SERVO_LEFT_NUM          = 1
SERVO_RIGHT_NUM         = 2
SERVO_HAND_ROT_NUM      = 3

SERVO_ROT_ANALOG_PIN    = 2
SERVO_LEFT_ANALOG_PIN   = 0
SERVO_RIGHT_ANALOG_PIN  = 1
SERVO_HAND_ROT_ANALOG_PIN = 3

# communication protocol
START_SYSEX = 0xF0
UARM_CODE = 0xAA
END_SYSEX = 0xF7

READ_ANGLE                  = 0X10
WRITE_ANGLE                 = 0X11
READ_COORDS                 = 0X12
WRITE_COORDS                = 0X13
READ_DIGITAL                = 0X14
WRITE_DIGITAL               = 0X15
READ_ANALOG                 = 0X16
WRITE_ANALOG                = 0X17
READ_EEPROM                 = 0X1A
WRITE_EEPROM                = 0X1B
DETACH_SERVO                = 0X1C
PUMP_STATUS                 = 0X1D
WRITE_STRETCH               = 0X1E
WRITE_LEFT_RIGHT_ANGLE      = 0X1F
GRIPPER_STATUS              = 0X20

CALIBRATION_FLAG                    = 10
CALIBRATION_LINEAR_FLAG             = 11
CALIBRATION_SERVO_FLAG              = 12
CALIBRATION_STRETCH_FLAG            = 13

LINEAR_INTERCEPT_START_ADDRESS      = 70
LINEAR_SLOPE_START_ADDRESS          = 50
OFFSET_START_ADDRESS                = 30
OFFSET_STRETCH_START_ADDRESS        = 20


EEPROM_DATA_TYPE_BYTE               = 1
EEPROM_DATA_TYPE_FLOAT              = 4

BUTTON_D7 = 7
BUTTON_D4 = 4
BUTTON_D2 = 2

PULL_UP = 1
INPUT = 0

UARM_HWID_KEYWORD = "USB VID:PID=0403:6001"

# global variables

def list_uarms():
    uarm_ports = []
    for i in list_ports.comports():
        if i.hwid[0:len(UARM_HWID_KEYWORD)] == UARM_HWID_KEYWORD:
            uarm_ports.append(i[0])
    return uarm_ports

#Get First uArm Port instance
def get_uarm():
    uarm_ports = list_uarms()
    if len(uarm_ports) > 0:
        return uArm(uarm_ports[0])
    else:
        print "No uArm Port Founds"

class uArm(object):

    firmware_major_version  = 0

    def __init__(self,port):
        self.port = port
        self.sp = serial.Serial(port,baudrate=57600)
        self.setFirmwareVersion()

    def isConnected(self):
        if self.sp.isOpen() == False:
            return False
        else:
            return True

    def disconnect(self):
        self.sp.close()

    def reconnect(self):
        if not self.isConnected():
            self.sp.open()
            self.setFirmwareVersion()

    def setFirmwareVersion(self):
        try:
            msg = bytearray([START_SYSEX, REPORT_VERSION, END_SYSEX])
            self.sp.write(msg)
            while self.sp.readable():
                readData = ord(self.sp.read(1))
                received_data = []
                if readData == START_SYSEX:
                    readData = ord(self.sp.read(1))
                    if readData == REPORT_VERSION:
                        self.firmware_major_version = ord(self.sp.read(1))
                        self.firmware_minor_version = ord(self.sp.read(1))
                        break
        except Exception as e:
            print "Serial Exception: ",e.strerror

    def readServoAngle(self,servo_add,data_offset):
        msg = bytearray([START_SYSEX, UARM_CODE, READ_ANGLE])
        msg.extend(getValueAsOne7bitBytes(servo_add))
        msg.extend(getValueAsOne7bitBytes(data_offset))
        msg.append(END_SYSEX)
        # print binascii.hexlify(bytearray(msg))

        self.sp.write(msg)
        while self.sp.readable():
            readData = ord(self.sp.read(1))
            received_data = []
            if (readData == START_SYSEX):
                readData = ord(self.sp.read(1))
                if (readData == UARM_CODE):
                    readData = ord(self.sp.read(1))
                    while readData != END_SYSEX:
                        received_data.append(readData)
                        readData = ord(self.sp.read(1))
                    if received_data[0] == servo_add:
                        return received_data[2]*128+received_data[1]+received_data[3]/100.00

    def readEEPROM(self,data_type, eeprom_add):
        msg = bytearray([START_SYSEX, UARM_CODE, READ_EEPROM])
        msg.append(data_type)
        msg.extend(getValueAsTwo7bitBytes(eeprom_add))
        msg.append(END_SYSEX)
        # print binascii.hexlify(bytearray(msg))

        self.sp.write(msg)
        while self.sp.readable():
            readData = ord(self.sp.read(1))
            received_data = []
            if (readData == START_SYSEX):
                readData = ord(self.sp.read(1))
                if (readData == UARM_CODE):
                    readData = ord(self.sp.read(1))
                    if (readData == READ_EEPROM):
                        readData = ord(self.sp.read(1))
                        while readData != END_SYSEX:
                            received_data.append(readData)
                            readData = ord(self.sp.read(1))
                        res_eeprom_add = received_data[1]*128 + received_data[0]
                        # print res_eeprom_add
                        if res_eeprom_add == eeprom_add:
                            if data_type == EEPROM_DATA_TYPE_BYTE:
                                return (received_data[3]<<7)+received_data[2]
                            if data_type == EEPROM_DATA_TYPE_FLOAT:
                                val = (received_data[4]<<7)+received_data[3]+float(received_data[5])/100.00
                                val =  val if received_data[2] == 0 else -val
                                return val

    def readDigital(self,pin_number, pin_mode):
        pin_number = int (pin_number)#(sys.argv[2])
        pin_mode = (int(pin_mode) == 1 )and 1 or 0  # 1means pullup 0 means input
        msg = bytearray([START_SYSEX, UARM_CODE, READ_DIGITAL])
        msg.extend(getValueAsOne7bitBytes(pin_number))
        msg.extend(getValueAsOne7bitBytes(pin_mode))
        msg.append(END_SYSEX)

        self.sp.write(msg)
        while self.sp.readable():
            readData = ord(self.sp.read(1))
            received_data = []
            if (readData == START_SYSEX):
                readData = ord(self.sp.read(1))
                if (readData == UARM_CODE):
                    readData = ord(self.sp.read(1))
                    while readData != END_SYSEX:
                        received_data.append(readData)
                        readData = ord(self.sp.read(1))
                    if received_data[0] == pin_number:
                        return received_data[1]

    def readAnalog(self,pin_num):
        msg = bytearray([START_SYSEX, UARM_CODE, READ_ANALOG])
        msg.extend(getValueAsOne7bitBytes(pin_num))
        msg.append(END_SYSEX)
        # print binascii.hexlify(bytearray(msg))

        self.sp.write(msg)
        while self.sp.readable():
            readData = ord(self.sp.read(1))
            received_data = []
            if (readData == START_SYSEX):
                readData = ord(self.sp.read(1))
                if (readData == UARM_CODE):
                    readData = ord(self.sp.read(1))
                    while readData != END_SYSEX:
                        received_data.append(readData)
                        readData = ord(self.sp.read(1))
                    if received_data[0] == pin_num:
                        return received_data[2]*128+received_data[1]


    def readCoords(self,pin_num):
        msg = bytearray([START_SYSEX, UARM_CODE, READ_COORDS])
        msg.extend(getValueAsOne7bitBytes(pin_num))
        msg.append(END_SYSEX)
        self.sp.write(msg)
        while self.sp.readable():
            readData = ord(self.sp.read(1))
            received_data = []
            coords = []
            coords_val = []
            if (readData == START_SYSEX):
                readData = ord(self.sp.read(1))
                if (readData == UARM_CODE):
                    readData = ord(self.sp.read(1))
                    while readData != END_SYSEX:
                        received_data.append(readData)
                        readData = ord(self.sp.read(1))
                    for i in range(0,3):
                        coords_sign = (received_data[i*4] == 1 and -1 or 1)
                        if i == 1 or i == 2:
                            coords_sign = -coords_sign
                        coords_val = received_data[2+4*i]*128+received_data[1+4*i]+received_data[3+4*i]/100.00
                        coords.append(coords_sign*coords_val)
                    return coords

    def writeEEPROM(self,data_type, eeprom_add, eeprom_val):
        msg = bytearray([START_SYSEX, UARM_CODE, WRITE_EEPROM, data_type])
        msg.extend(getValueAsTwo7bitBytes(eeprom_add))
        if data_type == EEPROM_DATA_TYPE_BYTE:
            msg.extend(getValueAsTwo7bitBytes(eeprom_val))
        if data_type == EEPROM_DATA_TYPE_FLOAT:
            msg.extend(getValueAsFour7bitBytes(eeprom_val))
            # print getValueAsFour7bitBytes(eeprom_val)[0]
        msg.append(END_SYSEX)
        self.sp.write(msg)

    def writeAnalog(self,pin_number,pin_value):
        msg = bytearray([START_SYSEX, UARM_CODE, WRITE_ANALOG])
        msg.extend(getValueAsOne7bitBytes(pin_number))
        msg.extend(getValueAsTwo7bitBytes(pin_value))
        msg.append(END_SYSEX)
        self.sp.write(msg)

    def writeDigital(self,pin_number,pin_mode):
        pin_number = int (pin_number)
        pin_mode = ((int (pin_mode)) ==1) and 1 or 0

        msg = bytearray([START_SYSEX, UARM_CODE, WRITE_DIGITAL])
        msg.extend(getValueAsOne7bitBytes(pin_number))
        msg.extend(getValueAsOne7bitBytes(pin_mode))
        msg.append(END_SYSEX)
        self.sp.write(msg)

    def detachAll(self):
        msg = bytearray([START_SYSEX, UARM_CODE, DETACH_SERVO, END_SYSEX])
        self.sp.write(msg)

    def writeServoAngle(self,servo_number,servo_angle,writeWithoffset):
        servo_number = int(servo_number)
        servo_angle = float(servo_angle)
        writeWithoffset = int(writeWithoffset)
        msg = bytearray([START_SYSEX, UARM_CODE, WRITE_ANGLE])
        msg.extend(getValueAsOne7bitBytes(servo_number))
        msg.extend(getValueAsThree7bitBytes(servo_angle))
        msg.extend(getValueAsOne7bitBytes(writeWithoffset))
        msg.append(END_SYSEX)
        # print binascii.hexlify(bytearray(msg))
        self.sp.write(msg)

    def writeLeftRightServoAngle(self, servo_left_angle, servo_right_angle, writeWithoffset):
        writeWithoffset = int(writeWithoffset)
        servo_left_angle = float(servo_left_angle)
        servo_right_angle = float(servo_right_angle)
        msg = bytearray([START_SYSEX, UARM_CODE, WRITE_LEFT_RIGHT_ANGLE])
        msg.extend(getValueAsThree7bitBytes(servo_left_angle))
        msg.extend(getValueAsThree7bitBytes(servo_right_angle))
        msg.extend(getValueAsOne7bitBytes(writeWithoffset))
        msg.append(END_SYSEX)
        # print binascii.hexlify(bytearray(msg))
        self.sp.write(msg)

    def move(self,x,y,z):
        x,y,z = float(x), float(y), float(z)
        self.moveToOpts(x,y,z,0,1,0,0,0)

    def moveTo(self,x,y,z):
        x,y,z = float(x), float(y), float(z)
        self.moveToOpts(x,y,z,0,0,0,0,0)

    def pumpStatus(self, val):
        pump_status = 1 if val else 0
        msg = bytearray([START_SYSEX, UARM_CODE, PUMP_STATUS])
        msg.extend(getValueAsOne7bitBytes(pump_status))
        msg.append(END_SYSEX)
        self.sp.write(msg)

    def gripperStatus(self, val):
        gripper_status = 1 if val else 0
        msg = bytearray([START_SYSEX, UARM_CODE, GRIPPER_STATUS])
        msg.extend(getValueAsOne7bitBytes(gripper_status))
        msg.append(END_SYSEX)
        self.sp.write(msg)

    def moveToOpts(self,x,y,z,hand_angle,relative_flags,time_spend,path_type,ease_type):
        msg = bytearray([START_SYSEX, UARM_CODE, WRITE_COORDS])
        msg.extend(getValueAsFour7bitBytes(x))
        msg.extend(getValueAsFour7bitBytes(y))
        msg.extend(getValueAsFour7bitBytes(z))
        msg.extend(getValueAsThree7bitBytes(hand_angle))
        msg.extend(getValueAsOne7bitBytes(relative_flags))
        msg.extend(getValueAsThree7bitBytes(time_spend))
        msg.extend(getValueAsOne7bitBytes(path_type))
        msg.extend(getValueAsOne7bitBytes(ease_type))
        # msg.append(1 if enable_hand else 0)
        msg.append(END_SYSEX)
        time.sleep(0.01)
        self.sp.write(msg)

    def moveToSimple(self,x,y,z,hand_angle,relative_flags,time_spend):
        self.moveToOpts(x,y,z,hand_angle,relative_flags,time_spend,0,0, True)

    def writeStretch(self,length,height):
        length = float(length)
        height = float(height)

        msg = bytearray([START_SYSEX, UARM_CODE, WRITE_STRETCH])
        msg.extend(getValueAsFour7bitBytes(length))
        msg.extend(getValueAsFour7bitBytes(height))
        msg.append(END_SYSEX)
        self.sp.write(msg)

class ConnectError(RuntimeError):
   def __init__(self, arg):
      self.args = arg

def getValueAsOne7bitBytes(val):
    return bytearray([val])

def getValueAsTwo7bitBytes(val):
    int_val = int(val)
    return bytearray([abs(int_val) % 128, abs(int_val) >> 7])

def getValueAsThree7bitBytes(val):
    int_val = int(val)
    decimal_val = int(round((val - int_val) * 100))
    # print decimal_val
    return bytearray([abs(int_val) % 128, abs(int_val) >> 7, abs(decimal_val)])

def getValueAsFour7bitBytes(val):
    int_val = int(val)
    decimal_val = int(round((val - int_val) * 100))
    # print "decimal_val: ", decimal_val
    return bytearray([0 if val > 0 else 1, abs(int_val) % 128, abs(int_val) >> 7, abs(decimal_val)])
