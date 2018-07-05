# coding=utf-8
"""
Poniżej znajduje się implementacja CLI (command line interface) do modułu
turtle, czyli Pythonowego odpowiednika LOGO. Wykorzystano tutaj wzorzec Template
Method (metoda szablonowa).
W pierwszym, obowiązkowym zadaniu, należy dodać wsparcie dla makr, tak aby można
było nagrać ciąg komend, a następnie odtworzyć ten sam ciąg przy pomocy
komendy "playback". W tym celu, należy dodać następujące komendy:
- record -- rozpoczyna nagrywanie makra
- stop -- kończy nagrywanie makra
- playback -- wykonuje makro, tzn. wszystkie komendy po komendzie "record", aż
  do komendy "stop".
Podpowiedź: Użyj wzorca Command (polecenie).
W drugim, nieobowiązkowym zadaniu, zastanów się, jak można zastosować wzorzec
Composite (kompozyt) do tych makr i spróbuj zastosować go.
Rozwiązania wysyłamy tak samo, jak prework, tylko że w jednym Pull Requeście.
"""

import cmd, sys
import turtle

class Macro(object):
    prompt = '(turtle-macro) '
    def __init__(self, shell):
        self.shell = shell
        self._precmd = self.shell.precmd
        self.commands = []

    def start_recording_cmd(self, line):
        command = line.strip().split(' ', 1)
        if hasattr(self.shell, 'do_'+ command[0]) and 'playback' not in line:
            self.commands.append(command)
        return line

    def record(self):
        self.commands = []
        self.shell.precmd = self.start_recording_cmd
        self.shell.prompt = self.prompt

    def stop_recording(self):
        self.shell.precmd = self._precmd
        self.shell.prompt = TurtleShell.prompt

    def playback(self, times=1):
        print('Running macro {} time(s)'.format(' '.join(times)))
        for i in range(times):
            self.run_macro()

    def run_macro(self):
        for command in self.commands:
            f = self.get_command(command)
            print('Running command: {}'.format(' '.join(command)))
            self.run_command(command, f)

    def get_command(self, command):
        f = getattr(self.shell, 'do_' + command[0])
        return f

    def run_command(self, command, f):
        f(' '.join(command[1:]))


class TurtleShell(cmd.Cmd):
    intro = 'Welcome to the turtle shell.   Type help or ? to list commands.\n'
    prompt = '(turtle) '
    makro = None

    # ----- basic turtle commands -----
    def do_forward(self, arg):
        'Move the turtle forward by the specified distance:  FORWARD 10'
        turtle.forward(int(arg))

    def do_right(self, arg):
        'Turn turtle right by given number of degrees:  RIGHT 20'
        turtle.right(int(arg))

    def do_left(self, arg):
        'Turn turtle left by given number of degrees:  LEFT 90'
        turtle.left(int(arg))

    def do_home(self, arg):
        'Return turtle to the home position:  HOME'
        turtle.home()

    def do_circle(self, arg):
        'Draw circle with given radius an options extent and steps:  CIRCLE 50'
        turtle.circle(int(arg))

    def do_position(self, arg):
        'Print the current turtle position:  POSITION'
        print('Current position is %d %d\n' % turtle.position())

    def do_heading(self, arg):
        'Print the current turtle heading in degrees:  HEADING'
        print('Current heading is %d\n' % (turtle.heading(),))

    def do_reset(self, arg):
        'Clear the screen and return turtle to center:  RESET'
        turtle.reset()

    def do_bye(self, arg):
        'Close the turtle window, and exit:  BYE'
        print('Thank you for using Turtle')
        turtle.bye()
        return True

    def do_record(self, arg):
        self.makro = Macro(self)
        self.makro.record()

    def do_stop(self, arg):
        self.makro.stop_recording()

    def do_playback(self, arg):
        self.makro.playback(times=int(arg) if arg else 1)

if __name__ == '__main__':
    TurtleShell().cmdloop()
