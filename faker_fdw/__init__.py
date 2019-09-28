#
# Copyright (c) 2016-2019 Dickson S. Guedes.
#
# This module is free software; you can redistribute it and/or modify it under
# the [PostgreSQL License](http://www.opensource.org/licenses/postgresql).
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose, without fee, and without a written agreement is
# hereby granted, provided that the above copyright notice and this paragraph
# and the following two paragraphs appear in all copies.
#
# In no event shall Dickson S. Guedes be liable to any party for direct,
# indirect, special, incidental, or consequential damages, including lost
# profits, arising out of the use of this software and its documentation, even
# if Dickson S. Guedes has been advised of the possibility of such damage.
#
# Dickson S. Guedes specifically disclaims any warranties, including, but not
# limited to, the implied warranties of merchantability and fitness for a
# particular purpose. The software provided hereunder is on an "as is" basis,
# and Dickson S. Guedes has no obligations to provide maintenance, support,
# updates, enhancements, or modifications.
#
from multicorn import ForeignDataWrapper, TableDefinition, ColumnDefinition
from multicorn.utils import log_to_postgres, DEBUG
from faker import Faker
from functools import lru_cache


class FakerForeignDataWrapper(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(FakerForeignDataWrapper, self).__init__(options, columns)
        log_to_postgres("call __init__()", DEBUG)

        self.columns = {}

        try:
            self.limit = int(options['max_results'])
        except Exception:
            self.limit = 100

        try:
            self.locale = options['locale']
        except Exception:
            self.locale = 'en_US'

        try:
            self.seed = int(options['seed'])
        except Exception:
            self.seed = None

        faker = Faker(self.locale)
        faker.seed(self.seed)

        for column, definition in columns.items():
            log_to_postgres('column {} def {}'.format(column, type(definition.options)), DEBUG)
            func = getattr(faker, column, lambda: None)

            self.columns[column] = {'function': func, 'args': definition.options}

    def execute(self, quals, columns):
        log_to_postgres("call execute()", DEBUG)

        for i in range(0, self.limit):
            line = {}

            for column in columns:
                func = self.columns[column]['function']
                args = self.columns[column]['args']
                args = {k: self._try_convert(v) for k, v in args.items()}

                line[column] = func(**args)

            yield line

    def get_rel_size(self, quals, columns):
        # very very very magic number
        return (self.limit, len(columns) * 42)

    @classmethod
    def import_schema(self, schema, srv_options, options,
                      restriction_type, restricts):

        tables = []

        for provider in Faker().providers:
            columns = []

            schema_name, provider_name = self._destructure_class_name(provider)
            for field in filter(lambda x: not x.startswith('_'), dir(provider)):

                if field.startswith('random') or field.endswith('ify') or field == 'generator':
                    continue

                columns.append(ColumnDefinition(
                    column_name=field,
                    type_name="varchar"))

            tables.append(TableDefinition(
                table_name=provider_name,
                schema=schema,
                columns=columns,
                options=options))

        return tables

    @classmethod
    def _destructure_class_name(self, cn):
        try:
            schema, _, provider, _ = cn.__module__.split('.', maxsplit=3)
        except ValueError:
            schema, _, provider = cn.__module__.split('.', maxsplit=3)

        return schema, provider

    @classmethod
    @lru_cache(maxsize=32)
    def _try_convert_to_int(self, value):
        try:
            value = int(value)
        except ValueError:
            value = None

        return value

    @classmethod
    @lru_cache(maxsize=32)
    def _try_convert_to_float(self, value):
        try:
            value = float(value)
        except ValueError:
            value = None

        return value

    @classmethod
    @lru_cache(maxsize=3)
    def _try_convert_to_bool(self, value):
        if value in ['True', 'true', 't']:
            return True
        elif value in ['False', 'false', 'f']:
            return False
        else:
            return None

    @classmethod
    @lru_cache(maxsize=32)
    def _try_convert(self, value):

        if self._try_convert_to_int(value):
            value = self._try_convert_to_int(value)
        elif self._try_convert_to_float(value):
            value = self._try_convert_to_float(value)
        elif self._try_convert_to_bool(value) is not None:
            value = self._try_convert_to_bool(value)

        return value
