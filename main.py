from PySide import QtGui
from HelpMeTrack.UI.PySideMain import HelpMeTrack
import sys
import logging
import traceback



def log_uncaught_exceptions(exception_type, exception, tb):

    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(exception_type, exception))

sys.excepthook = log_uncaught_exceptions

try:
    qt_app = QtGui.QApplication(sys.argv)
    app = HelpMeTrack()
    app.run(qt_app)
except:
    # pprint(e)
    print "Unexpected error:", sys.exc_info()[0]
    # print "I/O error({0}): {1}".format(e.errno, e.strerror)
    raise
else:
    pass
finally:
    pass
