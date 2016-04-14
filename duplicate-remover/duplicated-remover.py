#!/usr/bin/env python3

#-*- coding: utf-8 -*-

try:
  import hashlib
  import sqlite3
  import os

  import logging
  import logging.config

  # parse the configuration file
  import configparser

except ImportError as e:
  print(e.message)

import pdb

# two things:
#   2. move these to a configuration file

# logging
logging.config.fileConfig("log.conf")
logger = logging.getLogger("example01")

# configuration file
CONFIGFILE="duplicated-remover.conf"
config = configparser.ConfigParser()
config.read(CONFIGFILE)
logger.info("Loading configuration file " + CONFIGFILE)

# file type to check
try:
  file_types = []
  prefixes = config.items("prefixes")
  for prefix in prefixes:
    file_types.append(prefix[1])
  logger.debug("The file types are " + str(file_types))

  # database file name
  database_name = config.get("database", "name")
  logger.debug("database name is " + database_name)

  # SQL statement to create the table
  # TODO(adamas): get it when needed
  table_creation_sql = config.get("database", "table_creation_sql")
  logger.debug("SQL to create the table is \'" + table_creation_sql + "\'")

  index_creation_sql = config.get("database", "index_creation_sql")
  logger.debug("SQL to create the index is \'" + index_creation_sql + "\'")

  table_insertion_sql = config.get("database", "table_insertion_sql")
  logger.debug("SQL to insert into the table is \'" + table_insertion_sql + "\'")

  find_duplicated_key_sql = config.get("database", "find_duplicated_key_sql")
  logger.debug("SQL to find the duplicated key is \'" + find_duplicated_key_sql + "\'")

  find_duplicated_path_sql = config.get("database", "find_duplicated_path_sql")
  logger.debug("SQL to find the duplicated path is \'" + find_duplicated_path_sql + "\'")

  remove_duplicated_path_sql = config.get("database", "remove_duplicated_path_sql")
  logger.debug("SQL to remove the duplicated path is \'" + remove_duplicated_path_sql + "\'")

  # command file name
  commands_file = config.get("output", "commands_file")
  logger.debug("commands name is \'" + commands_file + "\'")

except configparser.NoOptionError as error:
  logger.critical(error.message)

def create_database_and_table(_database_name, _table_creation_sql, _index_creation_sql):
  # if the database doosn't exist,
  # create the database, and add all the files

  # TODO(adamas): check the database doesn't exist
  # create the database
  conn = sqlite3.connect(_database_name)

  # TODO(adamas): check the table doesn't exist
  # create the table

  conn.execute(_table_creation_sql)
  conn.execute(_index_creation_sql)

  conn.commit();
  # TODO(adamas): output the database name
  logging.info("Database created")

  return conn

# calculate the sha1sum
def sha1sum_func(_path):
  sha1 = hashlib.sha1()
  f = open(_path, 'rb')

  while True:
    data = f.read(4096*10)
    if not data:
      break

    sha1.update(data)

  return sha1.hexdigest()

def dir_walker(_root_path, _file_types, _check_newer=False, _criterion=0):
  for root, dirs, files in os.walk(_root_path):
    # check all files in this directory
    for file in files:
      # check if it ends with the suffix in file_types
      file_type = file[file.rfind("."):]

      if file_type in _file_types:
        
        # get the full path
        full_path = "/".join([root, file])
        # TODO(adamas): check whether it exists

        if _check_newer and os.path.getctime(full_path) <= _criterion:
          logging.debug("Timestamp for file %s is %f, and _criterion is %f, so break" % 
            (full_path, os.path.getctime(full_path), _criterion))
          continue

        logging.debug("Timestamp for file %s is %f, and _criterion is %f, so append it" %
            (full_path, os.path.getctime(full_path), _criterion))
        logging.info("Add file " + full_path)
        yield (file_type, full_path)

def insert_into_database(_conn, _file_type, _full_path):
  sha1sum = sha1sum_func(_full_path)

  logging.debug("Insert into database, filetype: %s, full_path: %s" % (file_types, full_path))
  try:
    conn.execute(table_insertion_sql, (_file_type, sha1sum, _full_path))
    conn.commit()
  except sqlite3.IntegrityError:
    # this happen when this file, which was already added to the database,
    # was touched, and became newer than the database file.
    logging.warning("File %s would not be added to the database for the second time" % _full_path)
    os.utime(database_name)   # update the timestamp of the database file
    conn.rollback()  

if __name__ == "__main__":

  logging.info("Go...")
  if not os.access(database_name, os.R_OK):
    logging.debug("Database doesn't exist, create it.")
    # database doesn't exist, create it
    conn = create_database_and_table(database_name, table_creation_sql, index_creation_sql)

    # add all the intended files into the database
    for (file_types, full_path) in dir_walker(".", file_types):
      logging.debug("Inserting " + full_path + " into the database")
      insert_into_database(conn, file_types, full_path)

    conn.close();

  else:
    logging.debug("Database exists, insert into it.")

    conn = sqlite3.connect(database_name)
    logging.debug("Connect to the database")

    # find the newer files out, and add it to the database
    for (file_types, full_path) in dir_walker(".", file_types, True, os.path.getctime(database_name)):
      logging.debug("Inserting " + full_path + " into the database")
      insert_into_database(conn, file_types, full_path)
    logging.debug("All new files were inserted into the database")

    conn.close();
    logging.debug("Close the connection to the database")

  # find all the duplicated keys,
  conn = sqlite3.connect(database_name)
  key_results = conn.execute(find_duplicated_key_sql)
  logging.info("Search the duplicated files")

  commands_f = open(commands_file, 'a')
  for key_result in key_results.fetchall():
    duplicate_key = key_result[0]
    logging.debug("Duplicate key is %s" % duplicate_key)

    #pdb.set_trace()
    duplicate_file_list = []
    duplicate_files = conn.execute(find_duplicated_path_sql, (duplicate_key,))

    for duplicate_file in duplicate_files.fetchall():
      duplicate_file_path = duplicate_file[0]
      logging.debug("duplicated file is %s" % duplicate_file_path)

      # remove non-existing files in database
      # lazy way, do not remove the deleted items in database
      # until we find its sha1sum key is same to some one.
      # TODO(adamas): should we check the existance of the file
      # and then remove the deleted items in database?
      if not os.access(duplicate_file_path, os.R_OK):
        conn.execute(remove_duplicated_path_sql, (duplicate_file_path,))
        conn.commit()
        logging.debug("File" + duplicate_file_path + " doesn\'t exist, remove it")
        continue

      duplicate_file_list.append(duplicate_file_path)

    # output the *rm* command.
    if len(duplicate_file_list) > 1:
      for duplicate_file in duplicate_file_list:
        command_str = 'rm -rf "' + duplicate_file + '"\n'
        commands_f.write(command_str)
        logging.debug("Command: " + command_str)
      commands_f.write('\n')

  # close the file
  commands_f.close()
  logging.info("Command file is closed")

  conn.close()
  logging.info("Connection to database is closed\n")

  print("Finish")
