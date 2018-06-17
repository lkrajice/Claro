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
                call['call'](*call['args'], **call['kwargs'])
            time.sleep(60)

    def run(self):
        """
        Starts the main loop
        """
        LOG.debug("Start scheduler instance")
        self.thread.start()

    @classmethod
    def add_callback(cls, when, callback, name, force_run=False,
                     always_remove=False, *args, **kwargs):
        """
        Register callback

        Args:
            when (datetime.datetime): specify the moment when the callback function is beeing
                executed
            callback (function): trigger function to execute on given time
            name (str): name of callback used as id of a trigger
            force_run (bool): callback is thrown away if it's time had already happened. If
                force_run is true, callback is executed immediately.
            always_remove (bool): when received callback that should replace it's old one, but new
                one is thrown away or executed immediately, it's decided if old one be deleted or
                not. If true, old callback is deleted, othervise it remains.

        """
        msg = ("{name:20s} | New call on {when:%d.%m.%Y %H:%M.%S} calls {fce} with "
               "args:{args} kwargs:{kwargs}")
        LOG.info(msg.format(name=name, when=when, fce=callback, args=args, kwargs=kwargs))

        if isinstance(when, datetime.date):
            when = datetime.datetime.combine(when, datetime.datetime.min.time())

        if name in cls.callbacks:
            LOG.info("{name:20s} | Callback is already set, replacing".format(name=name))

        now = datetime.datetime.now()
        if now < when:
            cls.callbacks[name] = {'when': when, 'call': callback, 'args': args, 'kwargs': kwargs}
        else:
            msg = "{name:20s} | New callback seems delayed - "
            if force_run:
                msg += 'executed immediately.'
                callback(*args, **kwargs)
            else:
                msg += 'skipping.'

            if always_remove:
                msg += ' Old callback was deleted.'
                cls.callbacks.pop(name, None)  # in case that
            else:
                msg += ' Old callback remained.'
            LOG.info(msg.format(name=name))


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
