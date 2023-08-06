#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2014, NewAE Technology Inc
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

import chipwhisperer.capture.scopes.cwhardware.ChipWhispererDigitalPattern as ChipWhispererDigitalPattern
import chipwhisperer.capture.scopes.cwhardware.ChipWhispererExtra as ChipWhispererExtra
import chipwhisperer.capture.scopes.cwhardware.ChipWhispererSAD as ChipWhispererSAD
import _qt as openadc_qt
from _base import ScopeTemplate
from chipwhisperer.capture.scopes.openadc_interface.naeusbchip import OpenADCInterface_NAEUSBChip
from chipwhisperer.common.utils import util, timer, pluginmanager
from chipwhisperer.common.utils.parameter import Parameter, setupSetParam


#TODO - Rename this or the other OpenADCInterface - not good having two classes with same name
class OpenADCInterface(ScopeTemplate):
    _name = "ChipWhisperer/OpenADC"

    def __init__(self, parentParam=None):
        ScopeTemplate.__init__(self, parentParam)

        self.qtadc = openadc_qt.OpenADCQt()
        self.qtadc.dataUpdated.connect(self.doDataUpdated)
        # Bonus Modules for ChipWhisperer
        self.advancedSettings = None
        self.advancedSAD = None
        self.digitalPattern = None
        self.refreshTimer = timer.runTask(self.dcmTimeout, 1)

        scopes = pluginmanager.getPluginsInDictFromPackage("chipwhisperer.capture.scopes.openadc_interface", True, False, self, self.qtadc)
        self.scopetype = scopes[OpenADCInterface_NAEUSBChip._name]
        self.params.addChildren([
            {'name':'Connection', 'key':'con', 'type':'list', 'values':scopes, 'get':self.getCurrentScope, 'set':self.setCurrentScope, 'childmode':'parent'},
            {'name':'Auto-Refresh DCM Status', 'type':'bool', 'value':True, 'action':self.setAutorefreshDCM}
        ])
        self.params.init()
        self.params.append(self.qtadc.getParams())

    def dcmTimeout(self):
        try:
            self.qtadc.sc.getStatus()
            # The following happen with signals, so a failure will likely occur outside of the try...except
            # For this reason we do the call to .getStatus() to verify USB connection first
            Parameter.setParameter(['OpenADC', 'Clock Setup', 'Refresh Status', None], blockSignal=True)
            Parameter.setParameter(['OpenADC', 'Trigger Setup', 'Refresh Status', None], blockSignal=True)
        except Exception as e:
            self.dis()
            raise e

    def setAutorefreshDCM(self, parameter):
        if parameter.getValue():
            self.refreshTimer.start()
        else:
            self.refreshTimer.stop()

    def getCurrentScope(self):
        return self.scopetype

    @setupSetParam("Connection")
    def setCurrentScope(self, scope):
        self.scopetype = scope

    def _con(self):
        if self.scopetype is not None:
            self.scopetype.con()
            self.refreshTimer.start()

            # TODO Fix this hack
            if hasattr(self.scopetype, "ser") and hasattr(self.scopetype.ser, "_usbdev"):
                self.qtadc.sc.usbcon = self.scopetype.ser._usbdev

            if "ChipWhisperer" in self.qtadc.sc.hwInfo.versions()[2]:

                if "Lite" in self.qtadc.sc.hwInfo.versions()[2]:
                    cwtype = "cwlite"
                else:
                    cwtype = "cwrev2"

                #For OpenADC: If we have CW Stuff, add that now
                #TODO FIXME - this shouldn't be needed, but if you connect/disconnect you can no longer
                #             use self.api.setParameter(...) with CWExtra-specific settings. The OpenADC
                #             settings will work, but not CWExtra ones? For now this works, but doesn't let
                #             you change the OpenADC type.
                #if self.advancedSettings is None:
                self.advancedSettings = ChipWhispererExtra.ChipWhispererExtra(self, cwtype, self.scopetype, self.qtadc.sc)
                self.params.append(self.advancedSettings.getParams())

                util.chipwhisperer_extra = self.advancedSettings

                if "Lite" not in self.qtadc.sc.hwInfo.versions()[2]:
                    self.advancedSAD = ChipWhispererSAD.ChipWhispererSAD(self.qtadc.sc)
                    self.params.append(self.advancedSAD.getParams())

                    self.digitalPattern = ChipWhispererDigitalPattern.ChipWhispererDigitalPattern(self.qtadc.sc)
                    self.params.append(self.digitalPattern.getParams())

            return True
        return False

    def _dis(self):
        if self.scopetype is not None:
            self.refreshTimer.stop()
            self.scopetype.dis()
            if self.advancedSettings is not None:
                self.advancedSettings.getParams().remove()
                self.advancedSettings = None
                util.chipwhisperer_extra = None

            if self.advancedSAD is not None:
                self.advancedSAD.getParams().remove()
                self.advancedSAD = None

            if self.digitalPattern is not None:
                self.digitalPattern.getParams().remove()
                self.digitalPattern = None

        # TODO Fix this hack
        if hasattr(self.scopetype, "ser") and hasattr(self.scopetype.ser, "_usbdev"):
            self.qtadc.sc.usbcon = None
        return True

    def doDataUpdated(self, l, offset=0):
        self.datapoints = l
        self.offset = offset
        if len(l) > 0:
            self.dataUpdated.emit(l, offset)

    def arm(self):
        if self.connectStatus.value() is False:
            raise Warning("Scope \"" + self.getName() + "\" is not connected. Connect it first...")
        if self.advancedSettings:
            self.advancedSettings.armPreScope()

        try:
            self.qtadc.arm()
        except Exception as e:
            self.dis()
            raise e

        if self.advancedSettings:
            self.advancedSettings.armPostScope()

    def capture(self, update=True, NumberPoints=None):
        """Raises IOError if unknown failure, returns 'True' if timeout, 'False' if no timeout"""
        return self.qtadc.capture(update, NumberPoints)
