#! /usr/bin/env python
# vim:ts=2:sw=2:et:ai:sts=2
#
# Copyright 2011, Ansgar Burchardt <ansgar@debian.org>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import .
import sql

import argparse
import sys

def pet_update()
    parser = argparse.ArgumentParser(
        description='create and update database schema for PET')

    parser.add_argument('-c', '--create', dest='create', action='store_true',
                        default=False)

    parser.add_argument('-nc', '--no-cert', dest='no_cert', action='store_true',
                        default=False)

    options = parser.parse_args(sys.argv[1:])

    pet.sql.DBUpdater().run(engine=pet.engine(options.no_cert),
                            create_database=options.create)
