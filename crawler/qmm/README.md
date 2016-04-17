A crawler to fetch images from qiushimm.com

TODO:
    1. remove the duplicate images,
        by storing their sha1sum, and their url in the database.
        Make sha1sum and url pair as the primary, so there can be
        more than one item in the database for the same sha1sum(
        same url cannot lead to varied sha1sum). If one url becomes invalid,
        the image can be got by another url with the same sha1sum.

        or make it a independant process, with package *watchdog*?

    2. classify the images by their prefix, resolution and so on.
        get the meta info from the output of *file* command.
