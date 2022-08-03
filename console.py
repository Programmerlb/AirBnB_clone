#!/usr/bin/env python3
"""This module defines the entry point of the command interpreter.

It defines one class, `HBNBCommand()`, which sub-classes the `cmd.Cmd` class.
This module defines abstractions that allows us to manipulate a powerful
storage system (FileStorage / DB). This abstraction will also allow us to
change the type of storage easily without updating all of our codebase.

It allows us to interactively and non-interactively:
    - create a data model
    - manage (create, update, destroy, etc) objects via a console / interpreter
    - store and persist objects to a file (JSON file)

Typical usage example:

    $ ./console
    (hbnb)

    (hbnb) help
    Documented commands (type help <topic>):
    ========================================
    EOF  create  help  quit

    (hbnb)
    (hbnb) quit
    $
"""
import cmd
from models import storage
from models.base_model import BaseModel

current_classes = {'BaseModel': BaseModel}


class HBNBCommand(cmd.Cmd):
    """The command interpreter.

    This class represents the command interpreter, and the control center
    of this project. It defines function handlers for all commands inputted
    in the console and calls the appropriate storage engine APIs to manipulate
    application data / models.

    It sub-classes Python's `cmd.Cmd` class which provides a simple framework
    for writing line-oriented command interpreters.
    """

    prompt = "(hbnb) "

    def do_help(self, arg):
        """To get help on a command, type help <topic>\n"""
        return super().do_help(arg)

    def do_EOF(self, line):
        """Inbuilt EOF command to gracefully catch errors\n"""
        return True

    def do_quit(self, arg):
        """Quit command to exit the program\n"""
        return True

    def emptyline(self):
        """Override default `empty line + return` behaviour\n"""
        pass

    def do_create(self, arg):
        """Creates a new <classname> instance"""
        args = arg.split()
        if not validate_classname(args):
            return

        new_obj = current_classes[args[0]]()
        new_obj.save()
        print(new_obj.id)

    def help_create(self):
        """Prints the help message for the `create` command"""
        print('\n'.join([
            "Usage: create <classname>",
            "\nCreates a new <classname> instance\n"]))

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()

        if not validate_classname(args, check_id=True):
            return

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)

        if req_instance is None:
            print("** no instance found **")
            return

        print(req_instance)

    def help_show(self):
        """Prints the help message for the `show` command"""
        print('\n'.join([
            "Usage: show <classname> <id>",
            "\nPrints the string representation of an instance\n"]))

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()

        if not validate_classname(args, check_id=True):
            return

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)

        if req_instance is None:
            print("** no instance found **")
            return

        del instance_objs[key]
        storage.save()

    def help_destroy(self):
        """Prints the help message for the `destroy` command"""
        print('\n'.join([
            "Usage: destroy <classname> <id>",
            "\nDeletes an instance based on the <class name> and <id>\n"]))

    def do_all(self, arg):
        """Prints string representation of all instances based
        or not on the class name
        """
        args = arg.split()
        all_objs = storage.all()

        if len(args) < 1:
            print(["{}".format(str(v)) for _, v in all_objs.items()])
            return
        if args[0] not in current_classes.keys():
            print("** class doesn't exist ** ")
            return
        else:
            print(["{}".format(str(v))
                  for _, v in all_objs.items() if type(v).__name__ == args[0]])
            return

    def help_all(self):
        """Prints the help message for the `all` command"""
        print('\n'.join([
            "Usage: all <classname>",
            "\nPrints a list of str(<class>) for all objects, or objects",
            "matching <classname>\n"]))


def validate_classname(args, check_id=False):
    """Runs checks on arg to validate classname entry."""
    if len(args) < 1:
        print("** class name missing ** ")
        return False
    if args[0] not in current_classes.keys():
        print("** class doesn't exist ** ")
        return False
    if len(args) < 2 and check_id:
        print("** instance id missing **")
        return False
    return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
