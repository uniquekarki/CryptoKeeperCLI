import os

def main():
    os.system('clear')
    print("WELCOME TO CRYPTO KEEPER: A Secure Password Manager")
    print("===================================================\n")
    print("Options:")
    print("  add       : Add a new password")
    print("  update    : Update an existing password")
    print("  retrieve  : Retrieve a password")
    print("  change    : Change the root password")
    print("  delete    : List all stored passwords")
    print("  list      : List all stored passwords")
    print("  exit      : List all stored passwords")
    print("===================================================")
    
    while True:
        user_option = input("\nEnter your option: ").strip().lower()
        print(f"option selected: {user_option}")
        if user_option == "exit":
            break
        elif user_option == "add":
            pass
        elif user_option == "update":
            pass
        elif user_option == "retrieve":
            pass
        elif user_option == "change":
            pass
        elif user_option == "delete":
            pass
        elif user_option == "list":
            pass


if __name__ == '__main__':
    main()