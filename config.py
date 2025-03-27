class AppConfig:
    def __init__(self, template_folder="../templates", static_folder="../static"):
        self.TEMPLATE_FOLDER = template_folder
        self.STATIC_FOLDER = static_folder

DEBUG = True
