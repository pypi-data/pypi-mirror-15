# vim:ts=2:sw=2:et:ai:sts=2
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

import sqlalchemy
# from serve import pet_serve

def engine(no_cert):
    if(no_cert):
        print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        return sqlalchemy.create_engine('postgresql://pet@bmdb1.debian.org:5435/pet')
    else:
        print("YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSss")
        return sqlalchemy.create_engine('postgresql://pet@bmdb1.debian.org:5435/pet?sslmode=verify-full&sslrootcert=/etc/ssl/debian/certs/ca.crt')
