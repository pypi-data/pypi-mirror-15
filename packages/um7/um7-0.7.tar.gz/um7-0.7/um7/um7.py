"""Module to interface with CHR UM7 IMU.  Contains class that handles serial interface and communication. Currently only
   captures processed accel, gyro, euler data.  Data broadcast rates must be set in CHR Serial Interface Program or other
   library
   Useful functions:
        object.catchsample()
            Catches and parses whatever data packets the sensor is broadcasting.  Updates the sensor object's internal
            data state with the new data and adds a timestamp

        object.grabsample(datatype)
            ONLY WORKS IF BROADCAST RATES ARE SET TO 0. Specifically requests data types passed to function. Updates
            sensor object's state and adds a timestamp

        object.zerogyros()
            zeros sensor's internal gyros

        object.resetekf()
            resets sensor's internal EKF

        object.checkinputbuffer()
            returns number of bytes waiting in serial port input buffer

    Important Notes:
        Timestamps are based on OS time, not sensor's internal timer
        Sensor object's most recent data points are stored in sensor.state (dict)
        Most functions return False if invalid data type is found
        This module does not check incoming data checksums
        Valid arguments for object.grabsample(datatype) can be found below

"""

# Daniel Kurek
# d'Arbeloff Lab, MIT
# January, 2016
# Module that holds UM7 class
# Creates serial objects, contains functions to parse serial data

#####################################################################
# TODO: Broadcast Rate Settings
#####################################################################


import serial
import time
import binascii
import struct


class UM7(object):
    """ Class that handles UM7 interfacing. Creates serial object for communication, contains functions to request specific
        data samples, catch any incoming data, check input buffer, and set various data broadcast rates. Currently only
        handles processed accel, gyro, and euler angle data.  Data is timed by OS.
    """

    def __init__(self, name, port, baud=115200):
        """Create new UM7 serial object.
        Defuault Baud Rate = 115200
        Byte Size = 8 bits
        No Parity, 1 Stop Bit, 0 second timeout
        Initializes port, name, OS timer, and sensor state (dict)
        :param port: Virtual COM port to which the IMU is connected (str)
                name: name of object (str)
        :return: UM7 Object
        """
        self.name = name
        self.t0 = time.time()
        self.state = {}
        try:
            self.serial = serial.Serial(port, baudrate=baud, bytesize=8, parity='N', stopbits=1, timeout=5)  # Open serial device
            print 'Successfully connected to %s UM7!' % self.name
        except OSError:
            print 'Could not connect to %s UM7. Is it plugged in or being used by another program?' % self.name

    def __del__(self):
        """Closes virtual com port

        :return: None
        """
        self.serial.close()
        print '%s serial device closed' % self.name

    def __name__(self):
        return self.name

    def catchsample(self):
        """Function that catches and parses incoming data, and then updates the sensor's state to include new data. Old
        data in state is overwritten. Data is timed by OS

        :return: Newly obtained data, and updates internal sensor state
        """
        [foundpacket, hasdata, startaddress, data, commandfailed] = self.readpacket()
        if not foundpacket:
            return False
        sample = parsedatabatch(data, startaddress, self.name)
        if sample:
            t = 'time'
            sample.update({t: time.time() - self.t0})
            self.state.update(sample)
        return sample

    def grabsample(self, datatype):
        """Function that flushes buffers and then requests and then waits for specific datatype. ONLY WORKS IF BROADCAST
        SETTINGS FOR REQUESTED DATA TYPE ARE ALREADY SET TO ZERO. Generally much slower than catchsample()

        :param datatype: 'xaccel', 'yaccel', 'zaccel', 'xgyro', 'ygyro', 'zgyro', 'rollpitch', 'yaw', 'rollpitchrate',
         and/or 'yawrate', given in list form
        :return: Newly obtained data, and updates internal sensor state
        """
        sample = {}
        for i in datatype:
            address = name2hex_reg[i]
            returnaddress = []
            self.serial.flushInput()
            self.request(i)
            while address != returnaddress:
                [foundpacket, hasdata, returnaddress, data, commandfailed] = self.readpacket()
                print data
            sample.update(parsedata(data, returnaddress, self.name))
        if sample:
            t = 'time'
            sample.update({t: time.time() - self.t0})
            self.state.update(sample)
        return sample

    def readpacket(self):
        """Scans for and partially parses new data packets. Binary data can then be sent to data parser

        :return: Parsed packet info
        """
        foundpacket = 0
        t0 = time.time()
        timeout = 1
        while time.time() - t0 < timeout:
            byte = self.serial.read(size=1)
            if byte == 's':
                byte2 = self.serial.read(size=1)
                if byte2 == 'n':
                    byte3 = self.serial.read(size=1)
                    if byte3 == 'p':
                        foundpacket = 1
                        break
        if foundpacket == 0:
            hasdata = 0
            commandfailed = 0
            startaddress = 0
            data = 0
        else:
            ptbyte = bin(int(binascii.hexlify(self.serial.read(size=1)), 16))[2:]
            ptbyte = ptbyte.zfill(8)
            hasdata = int(ptbyte[0], 2)
            numdatabytes = (int(ptbyte[2:6], 2))*4+4
            commandfailed = int(ptbyte[7], 2)
            startaddress = int(binascii.hexlify(self.serial.read(size=1)), 16)
            if hasdata:
                data = binascii.hexlify(self.serial.read(size=numdatabytes))
            else:
                data = False
        return [foundpacket, hasdata, startaddress, data, commandfailed]

    def request(self, datatype):
        """Sends data or command request to sensor.  Does not wait for any sort of response

        :param: Same as grab sample
        :return: Nothing
        """
        init = [0x73, 0x6e, 0x70, 0x00]
        address = name2hex_reg[datatype]
        decimalchecksum = 337 + address
        decimalchecksum1, decimalchecksum2 = divmod(decimalchecksum, 0x100)
        init.append(address)
        init.append(decimalchecksum1)
        init.append(decimalchecksum2)
        self.serial.write(init)

    def settimer(self, t=False):
        """Resets internal UM7 class timer

        :param t: If given, sets class timer to t.  If not, all new data is timed relative to instant that settimer()
        is called
        :return:
        """
        if t:
            self.t0 = t
        else:
            self.t0 = time.time()

    def checkinputbuffer(self):
        """Checks number of bytes waiting in input buffer

        :return: number of bytes
        """
        return self.serial.inWaiting()

    def zerogyros(self):
        """Sends request to zero gyros and waits for confirmation from sensor

        :return: True or False based on success of request
        """
        print 'Zeroing ' + self.name + ' gyros...'
        self.request('zerogyros')
        timeout = time.time() + 2
        while time.time() < timeout:
            self.request('zerogyros')
            [foundpacket, hasdata, startaddress, data, commandfailed] = self.readpacket()
            if startaddress == name2hex_reg['zerogyros'] and commandfailed == 0:
                print 'Successfully zeroed gyros.'
                return True
        print 'Could not zero gyros.'
        return False

    def resetekf(self):
        """Sends request to reset ekf and waits for confirmation from sensor

        :return: True or False based on success of request
        """
        print 'Resetting ' + self.name + ' EFK...'
        self.request('resetekf')
        timeout = time.time() + 2
        while time.time() < timeout:
            self.request('resetekf')
            [foundpacket, hasdata, startaddress, data, commandfailed] = self.readpacket()
            if startaddress == name2hex_reg['resetekf'] and commandfailed == 0:
                print 'Successfully reset EKF.'
                return True
        print 'Could not reset EKF.'
        return False


def parsedata(data, address, devicename):
    """Function called by class to parse binary data packets

    :param data:
    :param address:
    :param devicename:
    :return:
    """

    datatype = dec2name_reg[address]

    if datatype == 'xgyro' or datatype == 'ygyro' or datatype == 'zgyro':
        data = struct.unpack('!f', data.decode('hex'))[0]
        output = {datatype: data}

    elif datatype == 'xaccel' or datatype == 'yaccel' or datatype == 'zaccel':
        data = struct.unpack('!f', data.decode('hex'))[0]
        output = {datatype: data}

    elif datatype == 'rollpitch':
        datasplit = [data[i:i + 4] for i in range(0, len(data), 4)]
        for j in range(len(datasplit)):
            datasplit[j] = struct.unpack('!h', datasplit[j].decode('hex'))[0] / 91.02222
        output = {'roll': datasplit[0], 'pitch': datasplit[1]}

    elif datatype == 'yaw':
        datasplit = [data[i:i + 4] for i in range(0, len(data), 4)]
        datasplit[0] = struct.unpack('!h', datasplit[0].decode('hex'))[0] / 91.02222
        output = {datatype: datasplit[0]}

    elif datatype == 'rollpitchrate':
        datasplit = [data[i:i + 4] for i in range(0, len(data), 4)]
        for j in range(len(datasplit)):
            datasplit[j] = struct.unpack('!h', datasplit[j].decode('hex'))[0] / 16.0
        output = {'rollrate': datasplit[0], 'pitchrate': datasplit[1]}

    elif datatype == 'yawrate':
        datasplit = [data[i:i + 4] for i in range(0, len(data), 4)]
        datasplit[0] = struct.unpack('!h', datasplit[0].decode('hex'))[0] / 16.0
        output = {datatype: datasplit[0]}

    else:
        return False

    return output


def parsedatabatch(data, startaddress, devicename):
    xg = 'xgyro'
    yg = 'ygyro'
    zg = 'zgyro'
    xa = 'xaccel'
    ya = 'yaccel'
    za = 'zaccel'
    r = 'roll'
    p = 'pitch'
    y = 'yaw'
    rr = 'rollrate'
    pr = 'pitchrate'
    yr = 'yawrate'
    if startaddress == 97:  # Processed Gyro Data
        n = 8
        datasplit = [data[i:i + n] for i
                     in range(0, len(data), n)]  # Split data string into array of data bytes (n hex chars each)
        del datasplit[-1]
        for j in range(len(datasplit)):
            datasplit[j] = struct.unpack('!f', datasplit[j].decode('hex'))[0]  # Convert hex string to IEEE 754 floating point
        output = {xg: datasplit[0], yg: datasplit[1], zg: datasplit[2]}
    elif startaddress == 101:  # Processed Accel Data:
        n = 8
        datasplit = [data[i:i + n] for i
                     in range(0, len(data), n)]  # Split data string into array of data bytes (n hex chars each)
        del datasplit[-1]
        for j in range(len(datasplit)):
            datasplit[j] = struct.unpack('!f', datasplit[j].decode('hex'))[0]  # Convert hex string to IEEE 754 floating point
        output = {xa: datasplit[0], ya: datasplit[1], za: datasplit[2]}
    elif startaddress == 112:  # Processed Euler Data:
        n = 4
        datasplit = [data[i:i + n] for i
                     in range(0, len(data), n)]  # Split data string into array of data bytes (n hex chars each)
        del datasplit[9]
        del datasplit[8]
        del datasplit[7]
        del datasplit[3]  # Delete unused data bytes
        for j in range(len(datasplit)):
            if j < len(datasplit) - 3:  # Euler angle bytes
                datasplit[j] = struct.unpack('!h', datasplit[j].decode('hex'))[0] / 91.02222  # Convert hex str to floating point
                # and convert using constant  # Euler angle rate bytes
            else:
                datasplit[j] = struct.unpack('!h', datasplit[j].decode('hex'))[0] / 16.0  # Convert hex str to floating
                # point and convert using constant
        output = {r: datasplit[0], p: datasplit[1], y: datasplit[2], rr: datasplit[3], yr: datasplit[4], pr: datasplit[5]}
    else:
        return False
    return output


name2hex_reg = {'health': 0x55,
               'xgyro': 0x61,
               'ygyro': 0x62,
               'zgyro': 0x63,
               'xaccel': 0x65,
               'yaccel': 0x66,
               'zaccel': 0x67,
               'rollpitch': 0x70,
               'yaw': 0x71,
               'rollpitchrate': 0x72,
               'yawrate': 0x73,
                'zerogyros': 0xAD,
                'resetekf': 0xB3}

dec2name_reg = {85: 'health',
                97: 'xgyro',
                98: 'ygyro',
                99: 'zgyro',
                101: 'xaccel',
                102: 'yaccel',
                103: 'zaccel',
                112: 'rollpitch',
                113: 'yaw',
                114: 'rollpitchrate',
                115: 'yawrate'}

