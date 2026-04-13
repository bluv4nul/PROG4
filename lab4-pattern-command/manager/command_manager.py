from commands.base import Command


class CommandManager:

    def __init__(self):
        self._commands_history = []

    def dispatch(self, command: Command):

        result = command.execute()

        self._commands_history.append(command.describe())

        return result

    @property
    def history(self):
        return self._commands_history
