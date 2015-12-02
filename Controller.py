"""Code responsible for application logic"""


class BaseController:
    """Work as a protocol,need to be subclassed."""
    def get_text(self, file_name):
        pass

    @staticmethod
    def get_segmentation():
        return "Not complemented yet!"


class MainController(BaseController):
    """The main controller of app activity"""
    pass
