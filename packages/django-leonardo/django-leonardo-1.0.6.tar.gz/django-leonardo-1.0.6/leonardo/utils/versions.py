
import pprint
import logging
from django.utils import six
try:
    import pkg_resources
except ImportError:
    pkg_resources = None  # NOQA
import sys

logger = logging.getLogger('leonardo.system')

pp = pprint.PrettyPrinter(indent=4)


def varmap(func, var, context=None, name=None):
    """
    Executes ``func(key_name, value)`` on all values
    recurisively discovering dict and list scoped
    values.
    """
    if context is None:
        context = {}
    objid = id(var)
    if objid in context:
        return func(name, '<...>')
    context[objid] = 1
    if isinstance(var, dict):
        ret = dict((k, varmap(func, v, context, k)) for k, v in six.iteritems(var))
    elif isinstance(var, (list, tuple)):
        ret = [varmap(func, f, context, name) for f in var]
    else:
        ret = func(name, var)
    del context[objid]
    return ret

# We store a cache of module_name->version string to avoid
# continuous imports and lookups of modules
_VERSION_CACHE = {}


def get_version_from_app(module_name, app):
    version = None
    if hasattr(app, 'get_version'):
        version = app.get_version
    elif hasattr(app, '__version__'):
        version = app.__version__
    elif hasattr(app, 'VERSION'):
        version = app.VERSION
    elif hasattr(app, 'version'):
        version = app.version

    if callable(version):
        version = version()

    if not isinstance(version, (six.string_types, list, tuple)):
        version = None

    if version is None:
        if pkg_resources is None:
            return None
        # pull version from pkg_resources if distro exists
        try:
            version = pkg_resources.get_distribution(module_name).version
        except pkg_resources.DistributionNotFound:
            return None

    if isinstance(version, (list, tuple)):
        version = '.'.join(map(str, version))

    return str(version)


def get_versions(module_list=None):
    if not module_list:
        return {}

    ext_module_list = set()
    for m in module_list:
        parts = m.split('.')
        ext_module_list.update('.'.join(parts[:idx]) for idx in range(1, len(parts) + 1))

    versions = {}
    for module_name in ext_module_list:
        if module_name not in _VERSION_CACHE:
            try:
                __import__(module_name)
            except ImportError:
                continue

            try:
                app = sys.modules[module_name]
            except KeyError:
                continue

            try:
                version = get_version_from_app(module_name, app)
            except Exception as e:
                logger.exception(e)
                version = None

            _VERSION_CACHE[module_name] = version
        else:
            version = _VERSION_CACHE[module_name]
        if version is None:
            continue
        versions[module_name] = version
    return versions
