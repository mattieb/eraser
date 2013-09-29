`eraser`
========

**WARNING**: I do not take any responsibility for any destruction this
program may cause. I mean it! Read the license!

Yes, I have written a unit-tested program specifically for cautiously
"zeroing" a file-like object--in this case, Flash storage of some sort.

`eraser` reads the entire device a block at a time, and if said block
is not already erased, seeks backward and erases it.

I used this code to erase my Kindle Touch's FAT partition (`disk2s1`,
once unmounted) before passing the device on.  **NOTE**: I didn't
check if the Touch would format its internal storage by itself.
You probably want to make sure you do that before releasing USB
Drive Mode.

