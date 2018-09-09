#
# Copyright (c) 2016-2018 Dickson S. Guedes.
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

        for column in columns:
            func = getattr(faker, column, lambda: None)
            self.columns[column] = func

    def execute(self, quals, columns):
        log_to_postgres("call execute()", DEBUG)

        for i in range(0, self.limit):
            line = {}

            for column in columns:
                line[column] = self.columns[column]()

            yield line
