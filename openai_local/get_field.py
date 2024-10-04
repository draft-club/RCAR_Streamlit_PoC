# main.py

from expropriation_data_handler import ExpropriationDataHandler

# Create an instance of the handler
data_handler = ExpropriationDataHandler()

# Get the main prompt
main_prompt = data_handler.get_main_prompt()
print(main_prompt)

# Get a specific field prompt
field_prompt = data_handler.get_field_prompt("Nom / Prénom")
print(field_prompt)

master_promt

# If you try to access a non-existing field
non_existing_field_prompt = data_handler.get_field_prompt("Non-existing field")
print(non_existing_field_prompt)
