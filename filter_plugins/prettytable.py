#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2018, Noboru Iwamatsu
#

from ansible import errors


def table_to_list(table_string):
    """ Parse prettytable output to a list of dictionaries.
        :param table_string: prettytable output string
        :returns: a list of dictionaries
        Example:
        +--------+--------+--------+-------+
        | key_a  | key_b  | key_c  |  ...  |
        +--------+--------+--------+-------+
        | val_1a | val_1b | val_1c |  ...  |
        | val_2a | val_2b | val_2c |  ...  |
        | val_3a | val_3b | val_3c |  ...  |
        |  ...   |  ...   |  ...   |  ...  |
        +--------+--------+--------+-------+
        to
        [
            {'key_a': 'val_1a', 'key_b': 'val_1b', 'key_c': 'val_1c', ...},
            {'key_a': 'val_2a', 'key_b': 'val_2b', 'key_c': 'val_2c', ...},
            {'key_a': 'val_3a', 'key_b': 'val_3b', 'key_c': 'val_3c', ...},
            {...},
        ]
    """
    table_list = []
    num_of_gridlines = 0
    for line in table_string.splitlines():
        if line.startswith('+') and line.endswith('+'):
            num_of_gridlines += 1
            continue
        if num_of_gridlines == 1:
            if line.startswith('|') and line.endswith('|'):
                keys = [x.strip() for x in line[1:-1].split('|')]
        if num_of_gridlines >= 2:
            if line.startswith('|') and line.endswith('|'):
                values = [x.strip() for x in line[1:-1].split('|')]
                table_list.append(dict(zip(keys, values)))
        if num_of_gridlines == 3:
            break
    return table_list


def table_to_dict(table_string):
    """ Parse prettytable output to a dictionary.
        :param table_string: prettytable output string
        :returns: a list of dictionaries
        Example:
        +--------+--------+
        | Field  | Value  |
        +--------+--------+
        | key_1  | val_1  |
        | key_2  | val_2  |
        |  ...   |  ...   |
        +--------+--------+
        to
        {'key_1': 'val_1', 'key_2': 'val_2', ...}
    """
    table_dict = {}
    num_of_gridlines = 0
    for line in table_string.splitlines():
        if line.startswith('+') and line.endswith('+'):
            num_of_gridlines += 1
            continue
        if num_of_gridlines == 1:
            if line.startswith('|') and line.endswith('|'):
                keys = [x.strip() for x in line[1:-1].split('|')]
                if len(keys) != 2:
                    raise errors.AnsibleFilterError('invalid table')
        if num_of_gridlines >= 2:
            if line.startswith('|') and line.endswith('|'):
                values = [x.strip() for x in line[1:-1].split('|')]
                if len(values) != 2:
                    raise errors.AnsibleFilterError('invalid table')
                table_dict[values[0]] = values[1]
        if num_of_gridlines == 3:
            break
    return table_dict


class FilterModule(object):
    def filters(self):
        return {
            'table_to_list': table_to_list,
            'table_to_dict': table_to_dict,
        }
