"""

"""
import time
import logging
import inspect
import datetime
import threading

LOG = logging.getLogger()


class Scheduler(object):
    """
    Scheduler executing given functions at given time
    """
    callbacks = {}

    def __init__(self):
        self.enabled = True

        self.thread = threading.Thread(target=self.__main_loop)
        self.thread.deamon = True

    def __main_loop(self):
        while self.enabled:
            now = datetime.datetime.now()
            to_run = [name for name, call in self.callbacks.items() if call['when'] < now]
            for name in to_run:
                call = self.callbacks.pop(name)
                LOG.info("Run callback {}".format(str(call)))
                call['callback'](*call['args'], **call['kwargs'])
            time.sleep(60)

    def run(self):
        """
        Starts the main loop
        """
        LOG.debug("Start scheduler instance")
        self.thread.start()

    @classmethod
    def add_callback(cls, when, callback, name, *args, **kwargs):
        """
        Register callback

        Args:
            when (datetime.datetime): specify the moment when the callback function is beeing
                                      executed
            callback (function): trigger function to execute on given time
            name (str): name of callback used as id of a trigger

        """
        # [l.pop(index) for index in reversed(range(len(l))) if l[index] < 5]
        msg = "Replacing '{name}' callback with" if name in cls.callbacks else "Adding new callback"
        msg += ": {name} on {when:%d.%m.%Y %H:%M.%S} calls {fce} with args:{args} kwargs:{kwargs}"
        LOG.info(msg.format(name=name, when=when, fce=callback, args=args, kwargs=kwargs))

        cls.callbacks[name] = {'when': when, 'callback': callback, 'args': args, 'kwargs': kwargs}


def get_context_manager(*args):
    """
    Insert base_conext into with_metadata
    """
    def with_metadata(context):
        """
        Update context by view metadata needed to render several things properly
        """
        currentframe = inspect.currentframe()
        outerframe = inspect.getouterframes(currentframe, 1)

        # get the name of function which called this one
        caller_name = outerframe[1][3]
        # get the name of function which called this one
        caller_app = outerframe[1][1].replace("\\", "/").split('/')[-2]

        for app_specific_data in args:
            context.update(app_specific_data)

        context['metadata_active_view'] = caller_name
        context['metadata_active_app'] = caller_app
        return context
    return with_metadata
