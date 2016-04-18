Run
  ./duplicate-remove.py
to add the file and its sha1sum into the database,
and then a
  commands.sh
is generated, holding the commands to delete the
duplicate files(N.B. you have to modify the content
to decide which to delete).

TODO:
    * make it a library interface, to check a file against the database:
        duplicated_checker = Duplicated_checker(directory = 'xxx',
                                                database = 'xxx',
                                                ...)
        is_duplicated = duplicated_checker.check(file = 'xxx')
        if not is_duplicated:
            xxx

    * Deal with the link to a file
        Hard link, just remove like normal file,
        Soft link, remove the link.
