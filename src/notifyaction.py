import pynotify

class PreludeNotify:
        def __init__(self):
                pynotify.init("PreludeNotify")

        def run(self, title, message):
                n = pynotify.Notification(title, message)
                n.show()

