from modules.manager import Manager
from modules.generate import gen
from termcolor import colored
from getpass import getpass
import readline
import pyperclip
import sqlite3
import os


h_text = """
  1. readall      read all entries
  2. read         read a password
  3. add          add a password
  4. update       update a password
  5. updateuser   update a user
  6. delete       delete a password
  7. deleteall    delete the database
  8. clear        clear screen
  9. reset        reset all changes
 10. master       change master-password
 11. help         show this help-menu
 12. exit         save & end the programm
"""

def main():
  os.system("clear")

  print(colored("Welcome to Pyword-manager!\n", "cyan"))

  file = input(colored("Path to database: ", "blue"))
  pwd = getpass(colored("Master-password for database: ", "blue"))

  if not file.endswith(".db"): file += ".db"

  m = Manager(file, pwd)
  if not m.exists():
    rpwd = getpass(colored("Repeate Master-password for database: ", "blue"))
    if pwd != rpwd: pass
  print()