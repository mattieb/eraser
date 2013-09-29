#!/usr/bin/python
#
# Copyright (c) 2013 Matt Behrens <matt@zigg.com>
#
# Permission to use, copy, modify, and distribute this software for any
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


def erase(f, blocksize=512, zero_char='\xff', err=None):
    """
    Erase the given file-like object by scanning each block of size
    blocksize to see if it is filled with zero_char and overwriting
    the blocks that are not.

    blocksize defaults to 512 and is the block size to scan and write.

    zero_char defaults to '\\xff' and is the character to "zero" the
    file with.

    err, if supplied, is a file-like object (e.g. `sys.stderr`) that
    verbose messages are fed to.

    """
    def is_blank(block):
        """Scan the supplied block to see if it is blank."""

        for c in block:
            if c != zero_char:
                return False
        return True
    

    def write_err(message):
        if err:
            err.write(message)
            err.write('\n')


    while True:
        block = f.read(blocksize)
        blocklen = len(block)
        if not is_blank(block):
            f.seek(-blocklen, 1)
            write_err(
                'erasing block at 0x{:x} (len 0x{:x})'.format(f.tell(),
                                                                blocklen))
            f.write(zero_char * blocklen)
        else:
            write_err(
                'skipping block at 0x{:x} (len 0x{:x})'.format(f.tell(),
                                                               blocklen)
            )
        if blocklen < blocksize:
            break #EOF


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
