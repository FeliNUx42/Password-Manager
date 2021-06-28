from modules.manager import Manager
from modules.generate import gen
from termcolor import colored
from getpass import getpass
import readline
import pyperclip
import os


h_text = """
  1. readall      read all entries
  2. read         read a password
  3. add          add a password
  4. addrandom    add a random password
  5. updatepwd    update a password
  6. updateuser   update a user
  7. delete       delete a password
  8. deletetable  delete the database
  9. clear        clear screen
 10. reset        reset all changes
 11. master       change master-password
 12. help         show this help-menu
 13. exit         save & end the programm
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
    if pwd != rpwd:
      print(colored("\nError: Master-passwords don't match...\n", "red"))
      exit(0)
    m.create()
  
  if not m.isvalid():
    print(colored("\nError: Wrong Master-password...\n", "red"))
    exit(1)
  print()

  readline.clear_history()

  while True:
    command = input(colored(">>> ", "magenta"))

    if command == "readall":
      data = m.readall()
      print()
      print(colored(" Num |{:^20} |{:^25}".format("Website", "User"), "blue"))
      print(colored("\n".join("{:>3}. |{:^20} |{:^25}".format(n+1, *d) for n, d in enumerate(data)), "yellow").replace("|", "\x1b[0m\x1b[34m|\x1b[0m\x1b[33m"))
      print()
    
    elif command == "read":
      w = input(colored("\nWebsite (type '*' to see every password): ", "blue"))
      data = m.read(w)
      print()
      print(colored(" Num |{:^20} |{:^25} |{:^35}".format("Website", "User", "Password"), "blue"))
      print(colored("\n".join("{:>3}. |{:^20} |{:^25} |{:^35}".format(n+1, *d) for n, d in enumerate(data)), "yellow").replace("|", "\x1b[0m\x1b[34m|\x1b[0m\x1b[33m"))
      print()
      if len(data) == 1:
        pyperclip.copy(data[0][-1])
        print(colored("Password copied to clipboard.", "cyan"))
        print()
    
    elif command == "add":
      w = input(colored("\nWebsite: ", "blue"))
      u = input(colored("User: ", "blue"))
      p = getpass(colored("Password: ", "blue"))
      rp = getpass(colored("Repeate password: ", "blue"))
      if rp != p or not p:
        print(colored("\nPasswords don't match...\n", "red"))
        continue
      m.add(w, u, p)
      print()
    
    elif command == "addrandom":
      w = input(colored("\nWebsite: ", "blue"))
      u = input(colored("User: ", "blue"))
      l = input(colored("Length (8-64): ", "blue"))
      try:
        l = int(l)
        if not 8 <= l <= 64: raise TypeError()
      except:
        print(colored("\nInvalid length...\n", "red"))
        continue
      m.addrandom(w, u, l)
      print()
    
    elif command == "updatepwd":
      w = input(colored("\nWebsite: ", "blue"))
      p = getpass(colored("New Password: ", "blue"))
      rp = getpass(colored("Repeate password: ", "blue"))
      if rp != p or not p:
        print(colored("\nPasswords don't match...\n", "red"))
        continue
      m.update(w, "pwd", p)
      print()

    elif command == "updateuser":
      w = input(colored("\nWebsite: ", "blue"))
      u = input(colored("New User: ", "blue"))

      m.update(w, "user", u)
      print()
    
    elif command == "delete":
      w = input(colored("\nWebsite (type 'q' to exit): ", "blue"))
      print()
      if w == "q": continue
      m.delete(w)
    
    elif command == "deletetable":
      if not input(colored("\nDelete this database (all passwords will be lost) [y/N]: ", "red")).lower().startswith("y"):
        print()
        continue

      m.deletetable()
      exit(1)
    
    elif command == "clear":
      os.system("clear")
    
    elif command == "reset":
      if not input(colored("\nReset last changes (all changes will be lost) [y/N]: ", "red")).lower().startswith("y"):
        print()
        continue
      m.reset()
    
    elif command == "master":
      p = getpass(colored("\nNew Password: ", "red"))
      rp = getpass(colored("Repeate password: ", "red"))
      if rp != p or not p:
          print(colored("\nPasswords don't match...\n", "red"))
          continue
      m.pwd = p
      print(colored("\nMaster-password changed successfully.\n", "green"))
    
    elif command == "help":
      print(colored(h_text, "yellow"))
    
    elif command == "exit":
      break

    else:
      print(colored(f"'{command}' doesn't exist. Type 'help' for more information.", "red"))
    
  m.close()
  print(colored("\nDatabase saved successfully. Bye!\n", "green"))
  if not input(colored("Clear screen [Y/n]: ", "yellow")).lower().startswith("n"):
      os.system("clear")
  else:
      print()

if __name__ == "__main__":
  main()