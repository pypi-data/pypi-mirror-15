**************************************
Ascetic Command Runner
**************************************

.. image:: https://api.travis-ci.org/sergeyglazyrindev/asceticcmdrunner.svg
   :target: https://travis-ci.org/sergeyglazyrindev/asceticcmdrunner
   :alt: Travis CI status

.. image:: https://coveralls.io/repos/github/sergeyglazyrindev/asceticcmdrunner/badge.svg?branch=master
   :target: https://coveralls.io/github/sergeyglazyrindev/asceticcmdrunner?branch=master
   :alt: Coveralls status
           
Not all of our projects are using either django or another *God* framework.
So, once we start our hobby project, would be great to put into the game some commands.
For example, maybe we need for our hobby project simple command test which loads custom TestRunner, etc
In this case this package maybe handy for you!

**************************************
Installation
**************************************

Simply run in your bash:

.. code-block:: bash
                
    pip install acmdrunner

**************************************
Usage
**************************************

In your **django like manage.py** command loader, you need to trigger following:

.. code-block:: python
                
    import os
    from acmdrunner import Loader

    ...
    make all your preparations, initialize project settings, etc
    ...

    Loader.load_from_directory(os.path.dirname(__file__))
    Loader.load_from_package('rit.app')

Loader will search recursively in passed folder for folders with name management.
And try to load from folders found file acr_commands.py

An example of the file acr_commands.py:

.. code-block:: python
                
    from acmdrunner.dispatcher import CommandDispatcher
    command_dispatcher = CommandDispatcher()


    def execute(*args):
        pass

    command_dispatcher.register_command('test', execute)

**register_command** registers specific command and handler for this command.
Your commands should implement execute method. Better to inherit from BaseCommand.
But as it is ascetic, you can simply pass class with execute method implemented.
That's all!

To run command, please trigger following call:

.. code-block:: python
                
    from your_package_place import command_dispatcher
    command_dispatcher.execute_command(command_name, *args, **kwargs)


**************************************
Real usage example
**************************************

If you want to load all commands from specific namespace, you can implement following:

.. code-block:: python

    packages_to_traverse = ('rit.app', 'rit.core')
    for package in packages_to_traverse:
        Loader.load_from_package(package[0])
    Loader.load_from_directory(os.path.dirname(os.getcwd()))
