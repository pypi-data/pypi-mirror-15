from Products.GenericSetup.PythonScripts.exportimport \
     import PythonScriptBodyAdapter

from Products.CMFFormController.interfaces import IControllerPythonScript


class ControllerPythonScriptBodyAdapter(PythonScriptBodyAdapter):
    """
    Body im- and exporter for ControllerPythonScript.
    """
    __used_for__ = IControllerPythonScript

    suffix = '.cpy'

    def _exportBody(self):
        """Export the object as a file body.  Don't export FS versions.
        """
        if self.context.meta_type == 'Controller Python Script':
            return PythonScriptBodyAdapter._exportBody(self)
        return None

    body = property(_exportBody, PythonScriptBodyAdapter._importBody)
