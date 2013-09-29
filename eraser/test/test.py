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


from StringIO import StringIO
import unittest

import eraser


"""Tests for eraser"""


class WriteTrackingStringIO(StringIO):
    """StringIO that tracks the ranges of writes"""

    def __init__(self):
        StringIO.__init__(self)
        self.reset()


    def reset(self):
        """
        Clear the write_ranges list which tracks byte offsets that have
        been written to, and seek to 0.

        """
        self.write_ranges = []
        self.seek(0)


    def write(self, s):
        pos = self.tell()
        self.write_ranges.append((pos, pos + len(s)))
        StringIO.write(self, s)


class EraserTestCase(unittest.TestCase):
    """Test case for eraser"""

    
    def setUp(self):
        self.f = WriteTrackingStringIO()


    def test_writeTracking(self):
        """Verify WriteTrackingStringIO is functioning properly"""

        self.f.write('foobar')
        self.assertEqual(self.f.write_ranges, [(0, 6)])
        self.f.reset()
        self.f.seek(3)
        self.f.write('bar')
        self.assertEqual(self.f.write_ranges, [(3, 6)])


    def test_eraseFourFullBlocks(self):
        """Erase four full blocks"""

        for block in range(4):
            self.f.write('\x55' * 512)
        self.f.reset()

        eraser.erase(self.f)
        self.assertEqual(
            self.f.write_ranges,
            [(0, 512), (512, 1024), (1024, 1536), (1536, 2048)]
        )
        self.assertEqual(self.f.getvalue(), '\xff' * 2048)


    def test_eraseAlternatingBlocks(self):
        """Erase alternating blocks"""

        for block in range(4):
            if block % 2 == 0:
                self.f.write('\x55' * 512)
            else:
                self.f.write('\xff' * 512)
        self.f.reset()

        eraser.erase(self.f)
        self.assertEqual(self.f.write_ranges, [(0, 512), (1024, 1536)])
        self.assertEqual(self.f.getvalue(), '\xff' * 2048)


    def test_eraseIrregularLength(self):
        """Erase a file of irregular length"""

        for block in range(4):
            if block % 2 == 0:
                self.f.write('\x55' * 512)
            else:
                self.f.write('\xff' * 512)
        self.f.write('\x55' * 256)
        self.f.reset()

        eraser.erase(self.f)
        self.assertEqual(
            self.f.write_ranges, [(0, 512), (1024, 1536), (2048, 2304)]
        )
        self.assertEqual(self.f.getvalue(), '\xff' * 2304)


    def test_eraseOverlappingData(self):
        """Erase a file where the data overlaps block boundaries"""

        self.f.write('\xff' * 256)
        self.f.write('\x55' * 512)
        self.f.write('\xff' * 768)
        self.f.write('\x55' * 256)
        self.f.reset()

        eraser.erase(self.f)
        self.assertEqual(
            self.f.write_ranges, [(0, 512), (512, 1024), (1536, 1792)]
        )
        self.assertEqual(self.f.getvalue(), '\xff' * 1792)


    def test_eraseWithAlternateZero(self):
        """Erase a file with an alternate zero_char"""

        self.f.write('\xff' * 256)
        self.f.write('\x00' * 768)
        self.f.write('\xff' * 512)
        self.f.reset()

        eraser.erase(self.f, zero_char='\x00')
        self.assertEqual(self.f.write_ranges, [(0, 512), (1024, 1536)])
        self.assertEqual(self.f.getvalue(), '\x00' * 1536)


    def test_eraseWithAlternateBlocksize(self):
        """Erase a file with an alternate blocksize"""

        self.f.write('\xff' * 512)
        self.f.write('\x55' * 4096)
        self.f.write('\xff' * 8192)
        self.f.write('\x55' * 512)
        self.f.reset()

        eraser.erase(self.f, blocksize=4096)
        self.assertEqual(
            self.f.write_ranges, [(0, 4096), (4096, 8192), (12288, 13312)]
        )
        self.assertEqual(self.f.getvalue(), '\xff' * 13312)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
