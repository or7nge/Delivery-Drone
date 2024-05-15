class Directive:
    def __init__(self, command="NO ARUKO", value=None):
        self.command = command
        self.value = value

    def __str__(self):
        if self.value:
            return f"{self.command} {self.value}"
        return self.command

    def color(self):
        if self.command == "NO ARUKO":
            return (100, 100, 100)
        elif self.command == "DESCEND":
            return (0, 255, 0)
        else:
            return (0, 0, 255)
