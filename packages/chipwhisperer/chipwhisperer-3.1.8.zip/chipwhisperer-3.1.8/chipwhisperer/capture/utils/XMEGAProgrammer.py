# -*- coding: utf-8 -*-
#
# Copyright (c) 2014, NewAE Technology Inc
# All rights reserved.
#
# Authors: Colin O'Flynn
#
# Find this and more at newae.com - this file is part of the chipwhisperer
# project, http://www.assembla.com/spaces/chipwhisperer
#
#    This file is part of chipwhisperer.
#
#    chipwhisperer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    chipwhisperer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with chipwhisperer.  If not, see <http://www.gnu.org/licenses/>.
#=================================================

import os.path
import time
from datetime import datetime

from PySide.QtCore import *
from PySide.QtGui import *
from chipwhisperer.hardware.naeusb.programmer_xmega import supported_xmega
from chipwhisperer.capture.utils.IntelHex import IntelHex
import chipwhisperer.common.utils.qt_tweaks as QtFixes
from chipwhisperer.common.ui.CWMainGUI import CWMainGUI


class XMEGAProgrammerDialog(QtFixes.QDialog):
    def __init__(self):
        super(XMEGAProgrammerDialog, self).__init__(CWMainGUI.getInstance())
        # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.xmega = XMEGAProgrammer()

        self.setWindowTitle("ChipWhisperer-Lite XMEGA Programmer")
        layout = QVBoxLayout()

        layoutFW = QHBoxLayout()
        self.flashLocation = QtFixes.QLineEdit()
        flashFileButton = QPushButton("Find")
        flashFileButton.clicked.connect(self.findFlash)
        layoutFW.addWidget(QLabel("FLASH File"))
        layoutFW.addWidget(self.flashLocation)
        layoutFW.addWidget(flashFileButton)
        layout.addLayout(layoutFW)

        self.flashLocation.setText(QSettings().value("xmega-flash-location"))

        # Add buttons
        readSigBut = QPushButton("Check Signature")
        readSigBut.clicked.connect(self.readSignature)
        verifyFlashBut = QPushButton("Verify FLASH")
        verifyFlashBut.clicked.connect(self.verifyFlash)
        verifyFlashBut.setEnabled(False)
        progFlashBut = QPushButton("Erase/Program/Verify FLASH")
        progFlashBut.clicked.connect(self.writeFlash)

        layoutBut = QHBoxLayout()
        layoutBut.addWidget(readSigBut)
        layoutBut.addWidget(verifyFlashBut)
        layoutBut.addWidget(progFlashBut)
        layout.addLayout(layoutBut)

        # Add status stuff
        self.statusLine = QPlainTextEdit()
        self.statusLine.setReadOnly(True)
        # self.statusLine.setFixedHeight(QFontMetrics(self.statusLine.font()).lineSpacing() * 5 + 10)
        self.statusLine.append = self.statusLine.appendPlainText
        layout.addWidget(self.statusLine)

        self.xmega._logging = self.statusLine.append

        # Set dialog layout
        self.setLayout(layout)

    def findFlash(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Find FLASH File', QSettings().value("xmega-flash-location"), '*.hex')
        if fname:
            self.flashLocation.setText(fname)
            QSettings().setValue("xmega-flash-location", fname)

    def readSignature(self, close=True):
        self.xmega.find()
        if close:
            self.xmega.close()

    def verifyFlash(self):
        pass

    def writeFlash(self, erase=True, verify=True):

        status = "FAILED"

        fname = self.flashLocation.text()
        self.statusLine.append("***Starting FLASH program process at %s***" % datetime.now().strftime('%H:%M:%S'))
        if (os.path.isfile(fname)):
            self.statusLine.append("File %s last changed on %s" % (fname, time.ctime(os.path.getmtime(fname))))
            QCoreApplication.processEvents()

            try:
                self.statusLine.append("Entering Programming Mode")
                QCoreApplication.processEvents()
                self.readSignature(close=False)

                if erase:
                    try:
                        self.statusLine.append("Erasing Chip")
                        QCoreApplication.processEvents()
                        self.xmega.erase()
                    except IOError:
                        self.statusLine.append("**chip-erase timeout, erasing application only**")
                        QCoreApplication.processEvents()
                        self.xmega.xmega.enablePDI(False)
                        self.xmega.xmega.enablePDI(True)
                        self.xmega.erase("app")

                QCoreApplication.processEvents()
                self.xmega.program(self.flashLocation.text(), memtype="flash", verify=verify)
                QCoreApplication.processEvents()
                self.statusLine.append("Exiting programming mode")
                self.xmega.close()
                QCoreApplication.processEvents()
                
                status = "SUCCEEDED"

            except IOError, e:
                self.statusLine.append("FAILED: %s" % str(e))
                try:
                    self.xmega.close()
                except IOError:
                    pass
                
        else:
            self.statusLine.append("%s does not appear to be a file, check path" % fname)
            
        self.statusLine.append("***FLASH Program %s at %s***" % (status, datetime.now().strftime('%H:%M:%S')))

    def setUSBInterface(self, iface):
        self.xmega.setUSBInterface(iface)


class XMEGAProgrammer(object):
    
    def __init__(self):
        super(XMEGAProgrammer, self).__init__()
        self.supported_chips = supported_xmega
        self._logging = None
        self._foundchip = False

    def setUSBInterface(self, iface):
        self._foundchip = False
        self.xmega = iface
        self.xmega.setChip(self.supported_chips[0])

    def find(self):
        self._foundchip = False

        self.xmega.setParamTimeout(400)
        self.xmega.enablePDI(True)

        # Read signature bytes
        data = self.xmega.readMemory(0x01000090, 3, "signature")

        # Check if it's one we know about?
        for t in self.supported_chips:
            if ((data[0] == t.signature[0]) and
                (data[1] == t.signature[1]) and
                (data[2] == t.signature[2])):

                self._foundchip = True

                self.log("Detected %s" % t.name)
                self.xmega.setChip(t)
                break

        # Print signature of unknown device
        if self._foundchip == False:
            self.log("Detected Unknown Chip, sig=%2x %2x %2x" % (data[0], data[1], data[2]))

    def erase(self, memtype="chip"):

        if memtype == "app":
            self.xmega.eraseApp()
        elif memtype == "chip":
            self.xmega.eraseChip()
        else:
            raise ValueError("Invalid memtype: %s" % memtype)

    def program(self, filename, memtype="flash", verify=True):
        f = IntelHex(filename)

        startaddr = self.xmega._chip.memtypes[memtype]["offset"]
        maxsize = self.xmega._chip.memtypes[memtype]["size"]
        fsize = f.maxaddr() - f.minaddr()

        if fsize > maxsize:
            raise IOError("File %s appears to be %d bytes, larger than %s size of %d" % (filename, fsize, memtype, maxsize))

        self.log("XMEGA Programming %s..." % memtype)
        QCoreApplication.processEvents()
        fdata = f.tobinarray(start=0)
        self.xmega.writeMemory(startaddr, fdata, memtype)  # , erasePage=True
        
        self.log("XMEGA Reading %s..." % memtype)
        QCoreApplication.processEvents()
        #Do verify run
        rdata = self.xmega.readMemory(startaddr, len(fdata), memtype)

        for i in range(0, len(fdata)):
            if fdata[i] != rdata[i]:
                raise IOError("Verify failed at 0x%04x, %x != %x" % (i, fdata[i], rdata[i]))

        self.log("Verified %s OK, %d bytes" % (memtype, fsize))
    
    def close(self):
        self.xmega.enablePDI(False)

    def log(self, text):
        if self._logging is None:
            print text
        else:
            self._logging(text)
