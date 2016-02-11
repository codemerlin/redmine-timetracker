from PySide import QtGui
from HelpMeTrack.UI.PySideMain import HelpMeTrack
import sys
from pprint import pprint

try:
    qt_app = QtGui.QApplication(sys.argv)
    app = HelpMeTrack()
    app.run(qt_app)
except Exception, e:
    pprint(vars(e))
    # print "I/O error({0}): {1}".format(e.errno, e.strerror)
    raise
else:
    pass
finally:
    pass
