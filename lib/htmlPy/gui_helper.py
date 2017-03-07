import htmlPy
from PySide import QtGui
import json


class GUIHelper(htmlPy.Object):
    """ A class which adds some essential functionalities to GUI javascript.

    An instance of this class is binded to GUI javascript by default. Do not
    use this class manually.

    """

    @htmlPy.Slot(str)
    def log_to_console(self, string):
        """ Prints the string to python console.

        The method is binded to GUI javascript. Thus, the string comes from GUI

        Arguments:
            string (str): The string to be printed.
        """
        print(string)

    @htmlPy.Slot(str, str, result=str)
    def file_dialog(self, filemode="file", filters="[]"):
        """ Opens a file selection dialog with given extension filter.

        HTML file inputs cannot be directly used with :py:class:`htmlPy.AppGUI`
        . This function, when binded to GUI javascript, gives a method to open
        a file dialog from javascript. With help of ``binder.js``, this task
        is automated with HTML file input.

        Keyword arguments:
            filemode(str): A string of which style dialog to use. "file" and
                "directory" are currently supported.
            filters (str): A JSON array of javascript objects of type {"title":
                str (Title of the file extension), "extensions": str (space
                separated list of extension wildcards)}. Example ``[{"title":
                "JPEG files", "extensions": "*.jpg *.jpeg"}, {"title":
                "PNG files", "extensions": "*.png"}]``
                Applies only to filemode="file"

        """
        extensions = json.loads(filters)
        extensions_filter = ";;".join(map(lambda e: "{} ({})".format(
            e["title"], e["extensions"]), extensions))
        window = QtGui.QMainWindow()

        dialog = QtGui.QFileDialog(window)

        if filemode == "directory":
            dialog.setFileMode(QtGui.QFileDialog.Directory)
        else:
            dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
            print extensions_filter
            dialog.setFilter(extensions_filter)

        if dialog.exec_():
            filenames = dialog.selectedFiles()
            return filenames[0]
        else:
            return
