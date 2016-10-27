#!/usr/bin/env python
import serial
import time
import encodings
import unicodedata, re, sys
import subprocess
import pickle


class Mar345():
    def __init__(self):
        self.dumpfile = "/home/mar345/mar345.pickle"
        self.mode = None
        self.directory = None
        self.root = None
        self.format = None
        self.comfile = None
        self.scan345 = None
        self.distance = None
        self.wavelength = None
        self.wavelength = None
        self.phi = None
        self.omega = None
        self.chi = None
        self.theta = None
        self.time = None
        try:
            mar345dump = self.loaddata()
            self.mode = mar345dump["mode"]
            self.directory = mar345dump["directory"]
            self.root = mar345dump["root"]
            self.format = mar345dump["format"]
            self.comfile = mar345dump["comfile"]
            self.distance = mar345dump["distance"]
            self.wavelength = mar345dump["wavelength"]
            self.phi = mar345dump["phi"]
            self.omega = mar345dump["omega"]
            self.chi = mar345dump["chi"]
            self.theta = mar345dump["theta"]
            self.time = mar345dump["time"]
        except:
            self.mode = '1'
            self.directory = "/home/mar345/data"
            self.root = "testauto_001"
            self.format = "MAR345"
            self.comfile = "/home/mar345/log/mar.com"
            self.distance = "100"
            self.wavelength = "0.7105"
            self.phi = "0 1 1"
            self.omega = "0 0 0"
            self.chi = '0'
            self.theta = '0'
            self.time = "60.0"

    def setmode(self, mode_):
        self.mode = mode_

    def loaddata(self):
        with open(self.dumpfile, "rb") as file:
            mar345dump = pickle.load(file)
        return mar345dump

    def makedump(self):
        mar345dump = {
            "mode": self.mode,
            "directory": self.directory,
            "root": self.root,
            "format": self.format,
            "comfile": self.comfile,
            "distance": self.distance,
            "wavelength": self.wavelength,
            "phi": self.phi,
            "omega": self.omega,
            "theta": self.theta,
            "chi": self.chi,
            "time": self.time
        }
        return mar345dump

    def savedata(self):
        with open(self.dumpfile, "wb") as file:
            pickle.dump(self.makedump(), file)

    def setformat(self, format_):
        self.format = format_

    def setdistance(self, distance_):
        self.distance = distance_

    def setdirectory(self, directory_):
        self.directory = directory_

    def setroot(self, root_):
        self.root = root_

    def setwavelength(self, wavelength_):
        self.wavelength = wavelength_

    def setphi(self, phi_):
        self.phi = phi_

    def setomega(self, omega_):
        self.omega = omega_

    def settheta(self, theta_):
        self.theta = theta_

    def setchi(self, chi_):
        self.chi = chi_

    def settime(self, time_):
        self.time = time_

    def run(self, visible_=False):
        if visible_:
            self.scan345 = subprocess.Popen(["scan345", "-host", "mar345", "-s", "5001"])
        else:
            self.scan345 = subprocess.Popen(["scan345", "-host", "mar345", "-s", "5001"], stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT, shell=True)

    def end(self):
        try:
            # scan345.terminate()
            self.scan345.kill()
        except:
            pass

    def makecommand(self, command_, printmode_=False):
        result = ''
        result += "MODE " + self.mode + "\r\n"
        result += "ROOT " + self.root + "\r\n"
        result += "DISTANCE " + self.distance + "\r\n"
        result += "DIRECTORY " + self.directory + "\r\n"
        result += "FORMAT " + self.format + "\r\n"
        result += "WAVELENGTH " + self.wavelength + "\r\n"
        result += "PHI " + self.phi + "\r\n"
        result += "CHI " + self.chi + "\r\n"
        result += "OMEGA " + self.omega + "\r\n"
        result += "THETA " + self.theta + "\r\n"
        result += "TIME " + self.time + "\r\n"
        result += "USE STATUS" + "\r\n"
        if printmode_ == False: result += "COMMAND " + command_ + "\r\n"
        return result

    def sendcommand(self, command_):
        if "connect" == command_:
            self.run()
            return
        elif "connectv" == command_:
            self.run(True)
            return
        elif "dcnct" == command_:
            self.end(True)
            return
        elif "MODE " in command_:
            self.setmode(command_.replace("MODE ", ''))
            self.savedata()
            return
        elif "DIRECTORY " in command_:
            self.setdirectory(command_.replace("DIRECTORY ", ''))
            self.savedata()
            return
        elif "print" in command_:
            # print self.makedump()
            print
            self.makecommand(command_, True)
            return
        elif "ROOT " in command_:
            self.setroot(command_.replace("ROOT ", ''))
            self.savedata()
            return
        elif "WAVELENGTH " in command_:
            self.setwavelength(command_.replace("WAVELENGTH ", ''))
            self.savedata()
            return
        elif "PHI " in command_:
            self.setphi(command_.replace("PHI ", ''))
            self.savedata()
            return
        elif "OMEGA " in command_:
            self.setomega(command_.replace("OMEGA ", ''))
            self.savedata()
            return
        elif "CHI " in command_:
            self.setchi(command_.replace("CHI ", ''))
            self.savedata()
            return
        elif "THETA " in command_:
            self.settheta(command_.replace("THETA ", ''))
            self.savedata()
            return
        elif "TIME " in command_:
            self.settime(command_.replace("TIME ", ''))
            self.savedata()
            return
        elif "FORMAT " in command_:
            self.setformat(command_.replace("FORMAT ", ''))
            self.savedata()
            return
        elif "DISTANCE " in command_:
            self.setdistance(command_.replace("DISTANCE ", ''))
            self.savedata()
            return
        else:
            with open(self.comfile, 'w') as comfile:
                comfile.write(self.makecommand(command_))
        return


if __name__ == "__main__":
    mar345 = Mar345()
    if len(sys.argv) > 1:
        mar345.sendcommand(sys.argv[1])
    else:
        # command = raw_input()
        while command != "disconnect":
            command = raw_input()
            mar345.sendcommand(command)
