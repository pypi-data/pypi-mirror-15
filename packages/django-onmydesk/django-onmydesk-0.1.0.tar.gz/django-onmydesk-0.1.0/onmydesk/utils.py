"""Module with common utilities to this package"""
import re
from datetime import timedelta
import importlib


def my_import(class_name):
    """
    Usage example::

        Report = my_import('myclass.models.Report')

        model_instance = Report()
        model_instance.name = 'Test'
        model_instance.save()

    :param str class_name: Class name
    :returns: Class object
    """

    *packs, class_name = class_name.split('.')

    try:
        module = importlib.import_module('.'.join(packs))
        klass = getattr(module, class_name)
        return klass
    except (ImportError, AttributeError) as e:
        msg = 'Could not import "{}" from {}: {}.'.format(
            class_name, e.__class__.__name__, e)
        raise ImportError(msg)


def str_to_date(value, reference_date):
    '''
    Convert a string like 'D-1' to a "reference_date - timedelta(days=1)"

    :param str value: String like 'D-1', 'D+1', 'D'...
    :param date reference_date: Date to be used as 'D'
    :returns: Result date
    :rtype: date
    '''

    n_value = value.strip(' ').replace(' ', '').upper()

    if not re.match('^D[\-+][0-9]+$|^D$', n_value):
        raise ValueError('Wrong value "{}"'.format(value))

    if n_value == 'D':
        return reference_date
    elif n_value[:2] == 'D-':
        days = int(n_value[2:])
        return reference_date - timedelta(days=days)
    elif n_value[:2] == 'D+':
        days = int(n_value[2:])
        return reference_date + timedelta(days=days)
