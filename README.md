`eraser`
========

**WARNING**: I do not take any responsibility for any destruction this
program may cause. I mean it! Read the license!

`eraser` is a tool for "zeroing" a file-like object with minimal
impact.  It was written to work on a Kindle Touch's FAT partition.
It reads the entire device a block at a time, and if said block
is not already erased, seeks backward and erases it.

