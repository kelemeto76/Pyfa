import wx

import gui.mainFrame
from eos.saveddata.drone import Drone as DroneType
from eos.saveddata.fighter import Fighter as FighterType
from eos.saveddata.fit import Fit as FitType
from eos.saveddata.module import Module as ModuleType
from gui import globalEvents as GE
from service.fit import Fit
from .calc.fitToggleProjectedDrone import FitToggleProjectedDroneCommand
from .calc.fitToggleProjectedFighter import FitToggleProjectedFighterCommand
from .calc.fitToggleProjectedFit import FitToggleProjectedFitCommand
from .calc.fitToggleProjectedModule import FitToggleProjectedModuleCommand


class GuiToggleProjectedCommand(wx.Command):

    def __init__(self, fitID, thing, click):
        wx.Command.__init__(self, True, "Toggle Projected Item")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        fit = Fit.getInstance().getFit(self.fitID)
        if isinstance(thing, FitType):
            self.commandType = FitToggleProjectedFitCommand
            self.args = (self.fitID, thing.ID)
        elif isinstance(thing, ModuleType):
            position = fit.projectedModules.index(thing)
            self.commandType = FitToggleProjectedModuleCommand
            self.args = (self.fitID, position, click)
        elif isinstance(thing, DroneType):
            position = fit.projectedDrones.index(thing)
            self.commandType = FitToggleProjectedDroneCommand
            self.args = (self.fitID, position)
        elif isinstance(thing, FighterType):
            position = fit.projectedFighters.index(thing)
            self.commandType = FitToggleProjectedFighterCommand
            self.args = (self.fitID, position)
        else:
            self.commandType = None
            self.args = ()

    def Do(self):
        if self.commandType is None:
            return False
        if not self.internal_history.Submit(self.commandType(*self.args)):
            return False
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True