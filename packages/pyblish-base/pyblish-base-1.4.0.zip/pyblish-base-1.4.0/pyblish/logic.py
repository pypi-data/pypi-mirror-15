"""Shared processing logic"""

import sys
import inspect
import traceback

from . import _registered_test, lib
from .plugin import Validator


class TestFailed(Exception):
    def __init__(self, msg, vars):
        super(TestFailed, self).__init__(msg)
        self.vars = vars


def default_test(**vars):
    r"""Evaluate whether or not to continue processing

    The test determines whether or not to proceed from one
    plug-in to the next. The `vars` are updated everytime
    a plug-in is about to be processed with information about
    the upcoming plug-in.

    Returning any value means failure, whereas 0, False and None
    represents success. Similar to return/exit codes. You can provide
    a message along with a failure, such as specifying why the test
    failed. The message can then be used by process handlers,
    such as a GUI.

    You can provide your own test by registering it, see example below.

    Contents of `vars`:
        nextOrder (int): Order of next plugin
        ordersWithError (list): Orders at which an error has occured

    """

    offset = 0.5
    validation_order = Validator.order

    # If validation is done
    if vars["nextOrder"] >= validation_order + offset:
        for order in vars["ordersWithError"]:
            if lib.inrange(order,
                           base=validation_order,
                           offset=offset):
                return "failed validation"


def register_test(test):
    """Register test used to determine when to abort processing

    Arguments:
        test (callable): Called with argument `vars` and returns
            either True or False. True means to continue,
            False to abort.

    Example:
        >>> # Register custom test
        >>> def my_test(**vars):
        ...   return 1
        ...
        >>> register_test(my_test)
        >>>
        >>> # Run test
        >>> if my_test(order=1, ordersWithError=[]):
        ...   print("Test passed")
        Test passed
        >>>
        >>> # Restore default
        >>> deregister_test()

    """

    _registered_test["default"] = test


def registered_test():
    """Return the currently registered test"""
    return _registered_test["default"]


def deregister_test():
    """Restore default test"""
    register_test(default_test)


def plugins_by_family(plugins, family):
    """Return compatible plugins `plugins` to family `family`

    Arguments:
        plugins (list): List of plugins
        family (str): Family with which to compare against

    Returns:
        List of compatible plugins.

    """

    compatible = list()

    for plugin in plugins:
        if any(x in plugin.families for x in (family, "*")):
            compatible.append(plugin)

    return compatible


def plugins_by_families(plugins, families):
    """Same as :func:`plugins_by_family` except it takes multiple families

    Arguments:
        plugins (list): List of plugins
        families (list): Families with which to compare against

    Returns:
        List of compatible plugins.

    """

    compatible = list()

    for plugin in plugins:
        if any(x in plugin.families for x in families + ["*"]):
            compatible.append(plugin)

    return compatible


def plugins_by_instance(plugins, instance):
    """Conveinence function for :func:`plugins_by_family`

    Arguments:
        plugins (list): Plug-ins to assess
        instance (Instance): Instance with which to compare against

    Returns:
        List of compatible plugins

    """

    return plugins_by_family(plugins, instance.data["family"])


def plugins_by_host(plugins, host):
    """Return compatible plugins `plugins` to host `host`

    Arguments:
        plugins (list): List of plugins
        host (str): Host with which compatible plugins are returned

    Returns:
        List of compatible plugins.

    """

    compatible = list()

    for plugin in plugins:
        # TODO(marcus): Expand to take partial wildcards e.g. "*Mesh"
        if any(x in getattr(plugin, "hosts", None) for x in (host, "*")):
            compatible.append(plugin)

    return compatible


def instances_by_plugin(instances, plugin):
    """Return compatible instances `instances` to plugin `plugin`

    Arguments:
        instances (list): List of instances
        plugin (Plugin): Plugin with which to compare against

    Returns:
        List of compatible instances

    Invariant:
        Order of remaining plug-ins must remain the same

    """

    compatible = list()

    for instance in instances:
        family = instance.data["family"]

        if any(x in plugin.families for x in (family, "*")):
            compatible.append(instance)

        elif set(plugin.families) & set(instance.data.get("families", [])):
            compatible.append(instance)

    return compatible


def _extract_traceback(exception):
    """Append traceback to `exception`

    This function safely extracts a traceback while being
    careful not to leak memory.

    Arguments:
        exception (Exception): Append traceback to here
            as "traceback" attribute.

    """

    exc_type = exc_value = exc_traceback = None

    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        exception.traceback = traceback.extract_tb(exc_traceback)[-1]

    except:
        pass

    finally:
        del(exc_type, exc_value, exc_traceback)


def Iterator(plugins, context):
    """Primary iterator

    This is the brains of publishing. It handles logic related
    to which plug-in to process with which Instance or Context,
    in addition to stopping when necessary.

    Arguments:
        plugins (list): Plug-ins to consider
        context (list): Instances to consider

    """

    for plugin in plugins:
        instances = instances_by_plugin(context, plugin)

        if plugin.__instanceEnabled__:
            for instance in instances:
                yield plugin, instance

        else:
            yield plugin, None


@lib.deprecated
def process(func, plugins, context, test=None):
    r"""Primary processing logic

    Takes callables and data as input, and performs
    logical operations on them until the currently
    registered test fails.

    If `plugins` is a callable, it is called early, before
    processing begins. If `context` is a callable, it will
    be called once per plug-in.

    Arguments:
        func (callable): Callable taking three arguments;
             plugin(Plugin), context(Context) and optional
             instance(Instance). Each must provide a matching
             interface to their corresponding objects.
        plugins (list, callable): Plug-ins to process. If a
            callable is provided, the return value is used
            as plug-ins. It is called with no arguments.
        context (Context, callable): Context whose instances
            are to be processed. If a callable is provided,
            the return value is used as context. It is called
            with no arguments.
        test (callable, optional): Provide custom test, defaults
            to the currently registered test.

    Yields:
        A result per complete process. If test fails,
        a TestFailed exception is returned, containing the
        variables used in the test. Finally, any exception
        thrown by `func` is yielded. Note that this is
        considered a bug in *your* code as you are the one
        supplying it.

    """

    __plugins = plugins
    __context = context

    if test is None:
        test = registered_test()

    if hasattr(__plugins, "__call__"):
        plugins = __plugins()

    def gen(plugin, instances):
        if plugin.__instanceEnabled__ and len(instances) > 0:
            for instance in instances:
                yield instance
        else:
            yield None

    vars = {
        "nextOrder": None,
        "ordersWithError": list()
    }

    # Clear introspection values
    # TODO(marcus): Return *next* pair, this currently
    #   returns the current pair.
    self = process
    self.next_plugin = None
    self.next_instance = None

    for plugin in plugins:
        self.next_plugin = plugin
        vars["nextOrder"] = plugin.order

        if not test(**vars):
            if hasattr(__context, "__call__"):
                context = __context()

            args = inspect.getargspec(plugin.process).args

            # Backwards compatibility with `asset`
            if "asset" in args:
                args.append("instance")

            instances = instances_by_plugin(context, plugin)

            # Limit processing to plug-ins with an available instance
            if not instances and "*" not in plugin.families:
                continue

            for instance in gen(plugin, instances):
                if instance is None and "instance" in args:
                    continue

                # Provide introspection
                self.next_instance = instance

                try:
                    result = func(plugin, context, instance)

                except Exception as exc:
                    # Any exception occuring within the function
                    # you pass is yielded, you are expected to
                    # handle it.
                    yield exc

                else:
                    # Make note of the order at which
                    # the potential error error occured.
                    if result["error"]:
                        if plugin.order not in vars["ordersWithError"]:
                            vars["ordersWithError"].append(plugin.order)
                    yield result

            # Clear current
            self.next_instance = None

        else:
            yield TestFailed(test(**vars), vars)
            break


process.next_plugin = None
process.next_instance = None
