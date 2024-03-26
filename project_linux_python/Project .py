import subprocess
import xml.etree.ElementTree as ET
import difflib


class CommandManualGenerator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.command_manuals = []

    # function to red command from file each command in line
    def read_commands(self):
        with open(self.input_file, "r") as file:
            return file.read().splitlines()

    # function to retern the description for commands
    def command_description(self, command_name):
        try:
            # using man to return the descriptin manual
            command_descrption = subprocess.check_output(
                ["man", command_name], universal_newlines=True
            )
            # search for NAME
            command_name = command_descrption.find("NAME")
            # get command description
            command_des = command_descrption.find("DESCRIPTION", command_name)
            descrption = command_descrption[command_name:command_des].strip()

            # print first paragraph 
            descrption = descrption.split("\n\n")[0]
            return descrption

        except Exception as e:
            # print error
            print(f" error occurred: {e}")

    # function to return the version for commands
    def command_version(self, command_name):
        try:
            # using '--version' to return the the version of commands
            command_version = subprocess.check_output(
                [command_name, "--version"], universal_newlines=True
            )
            # print only the first line
            version = command_version.strip().split("\n")[0]
            return version

        except Exception as e:
            # print error
            print(f"An unexpected error occurred: {e}")

    # function to return the example for commands
    def command_example(self, command_name):
        try:
            # using '--help' to return the example of commands
            example_command = subprocess.check_output(
                [command_name, "--help"], universal_newlines=True
            )
            # return the first line example for command
            return example_command.strip().split("\n")[0]

        except Exception as e:
            # print error
            print(f"An unexpected error occurred: {e}")

    # function to return the related command for commands
    def related_command(self, command_name):
        try:
            # use the 'compgen -c' to return the related commands
            related_command = subprocess.check_output(
                ["bash", "-c", "compgen -c"], universal_newlines=True
            )

            all_related_commands = related_command.strip().split("\n")
            # list to add related commands
            related_commands = []
            for i in all_related_commands:
                if i.startswith(command_name):
                    # add related command to list
                    related_commands.append(i)

            # return list of commands
            return related_commands

        except Exception as e:
            # print error
            print(f"An unexpected error occurred: {e}")

    # function to create manual for commands
    def generate_commands_manuals(self):
        # read command from file
        commands = self.read_commands()
        for command in commands:
            if command.strip():  # Check if the command is not empty

                command_manual = CommandManual(
                    command,
                    descrption=self.command_description(command),
                    command_version=self.command_version(command),
                    example_command=self.command_example(command),
                    related_commands=self.related_command(command),
                )
                self.command_manuals.append(command_manual)
    

    # function to convert for xml format
    def serialize_to_xml(self):
        number_of_command = 0
        for command_manual in self.command_manuals:
            manual_of_command = XmlSerializer.serialize(command_manual)
            tree = ET.ElementTree(manual_of_command)

            inputfile = f"{command_manual.command_name}.xml"
            tree.write(inputfile)
            number_of_command += 1
            print(f"{number_of_command}) {inputfile}")
        print(f"the number of generatet commands is {number_of_command}")

    # function to verify between commands
    def verify_command(self, command_name):
        # create old and new manual
        old_manual = f"{command_name}.xml"
        new_manual = f"{command_name}_new.xml"

        # read the content for old command
        old_content = self.read_file(old_manual)

        # read the content for new command
        new_content = self.generate_new_manuals(command_name, new_manual)

        if old_content == new_content:
            print("No change between the command manuals")
        else:
            print("Changes detected:")
            self.difference(old_content, new_content)
            

    # function to read command from file
    def read_file(self, inputfile):
        try:
            with open(inputfile, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File '{inputfile}' not found.")
            return

    # function to generate new manuals for commands
    def generate_new_manuals(self, command_name, inputfile):
        new_manual = CommandManual(
            command_name,
            descrption=self.command_description(command_name),
            command_version=self.command_version(command_name),
            example_command=self.command_example(command_name),
            related_commands=self.related_command(command_name),
        )

        manual_of_command = XmlSerializer.serialize(new_manual)

        tree = ET.ElementTree(manual_of_command)
        tree.write(inputfile)
        print(f"Generated {inputfile}")

        with open(inputfile, "r") as file:
            return file.read()

    # function to display different for command command_manual
    def difference(self, old_manual, new_manual):
        diff_content = difflib.Differ()  # use diff library to find the difference
        final_result = diff_content.compare(
            old_manual.splitlines(), new_manual.splitlines()
        )
        for i in final_result:  # print the old and new manual
            if i.startswith("-") or i.startswith("+"):
                print(i)

    def suggestion_comands(self, command_name):
        try:
            # Use shell command for found the related commands "compgen -c"
            list_of_commands = subprocess.check_output(
                ["bash", "-c", f"compgen -c {command_name}"], universal_newlines=True
            )
            related_command_found = list_of_commands.strip().split("\n")

            # list to add related command into
            list_of_commands = []
            for i in related_command_found:
                if i != command_name:
                    list_of_commands.append(i)

            # if found related command print in screen
            if list_of_commands:
                print(f"Recommended commands for '{command_name}':")
                for i in list_of_commands:
                    print(i)
            else:
                print(f"No recommended commands found for '{command_name}'.")

        except Exception as e:
            print(f"error occurred: {e}")

    # function to search for command command_manual
    def search_command_manuals(self, command_name):
        # Search through command manuals for the command name
        found_manuals = []
        for i in self.command_manuals:
            if command_name == i.command_name:  # if exist return manual
                found_manuals.append(i)
        return found_manuals


# function to display the menu
def menu():
    print("Select Option from(1-5):")
    print("1. Generate Command Manuals")
    print("2. Verify Command")
    print("3. Search Command Manuals")
    print("4. Recommend Command")
    print("5. Exit")


# this class contain the attributes for command command_manual
class CommandManual:
    def __init__(
        self,
        command_name,
        descrption="",
        command_version="",
        example_command="",
        related_commands=[],
    ):
        # Assigning parameters to object attributes
        self.command_name = command_name
        self.descrption = descrption
        self.command_version = command_version
        self.example_command = example_command
        self.related_commands = related_commands


class XmlSerializer:
    def serialize(command_manual):
        manual_of_command = ET.Element("CommandManual")

        # add name of command
        command_name = ET.SubElement(manual_of_command, "CommandName")
        command_name.text = command_manual.command_name

        # add Description of command
        descrption = ET.SubElement(manual_of_command, "CommandDescription")
        descrption.text = command_manual.descrption

        # add version of command
        command_version = ET.SubElement(manual_of_command, "VersionHistory")
        command_version.text = command_manual.command_version

        # add example of command
        command_example = ET.SubElement(manual_of_command, "Example")
        command_example.text = command_manual.example_command

        # add list of related command
        related_command = ET.SubElement(manual_of_command, "RelatedCommands")
        related_command.text = ", ".join(command_manual.related_commands)

        # return the manual for commands
        return manual_of_command



if __name__ == "__main__":
    inputFile = "commands.txt"  # read command from file
    generate_manual = CommandManualGenerator(
        inputFile
    )  # generate command_manual for commands

    while True:
        menu()  # display menu
        choice = input("Enter your choice: ")  # select option

        if (
            choice == "1"
        ):  # if select 1 the will generate command_manual foe command and print the command generated
            print("---------------------------------------------")
            print("The command generated are :")
            generate_manual.generate_commands_manuals()
            generate_manual.serialize_to_xml()
            print("---------------------------------------------")

        elif choice == "2":
            print("---------------------------------------------")
            command_name = input("Enter command name to verify: ")
            generate_manual.verify_command(command_name)
            print("---------------------------------------------")
            
        elif choice == "3":  # select 3 to search for command command_manual
            print("---------------------------------------------")
            command = input("Enter full command name to search: ")
            command_manual = generate_manual.search_command_manuals(command)
            if command_manual:  # if command exist display information
                for command_manual in command_manual:
                    print(f"Command Name: {command_manual.command_name}")
                    print(f"Description: {command_manual.descrption}")
                    print(f"Version History: {command_manual.command_version}")
                    print(f"Example: {command_manual.example_command}")
                    print(
                        f"Related Commands: {', '.join(command_manual.related_commands)}"
                    )

            else:
                print("No manuals found for the command.")
            print("---------------------------------------------")
        elif choice == "4":  # select 4 for display recommend for command
            print("---------------------------------------------")
            command = input("Enter command name to recommend: ")
            generate_manual.suggestion_comands(command)
            print("---------------------------------------------")

        elif choice == "5":  # select 5 to finish
            print("---------------------------------------------")
            print("Finish")
            print("---------------------------------------------")
            break
        else:
            print("---------------------------------------------")
            print("Invalid choice. Please enter again.")
            print("---------------------------------------------")