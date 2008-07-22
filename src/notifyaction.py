import pynotify

class PreludeNotify:
        def __init__(self):
                pynotify.init("PreludeNotify")

        def run(self, imageuri, title, message):
                n = pynotify.Notification(title, message, imageuri)
                n.show()

