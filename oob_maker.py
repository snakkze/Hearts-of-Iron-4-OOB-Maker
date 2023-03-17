import pyautogui
from pynput import mouse, keyboard
import csv

# Flags
started = False

# Lists
chosen_provinces = [] # A list of provinces that the user has clicked on
provinces = [] # A list of colors of provinces that the user has clicked on
rows = [] # A list of rows from the definition.csv file
provinceIDs = [] # A list of province IDs corresponding to the colors of provinces that the user has clicked on
new_provinceIDs = [] # A list of unique province IDs
final_provinces = [] # A list of final province IDs that will be written to the output file

# User input
template = input("Enter Division Template: ")

# Output file
f = open("20s_oob.txt", "w+")

# Writing the division template to the output file
f.write("division_template = {\n")
f.write(f'	name = "{template}"\n')
f.write("	is_locked = yes\n")
f.write("    \n")
f.write("	division_names_group = GER_Inf_01\n")
f.write("    \n")
f.write("	regiments = {\n")
f.write("		infantry = { x = 0 y = 0 }\n")
f.write("		infantry = { x = 0 y = 1 }\n")
f.write("		infantry = { x = 0 y = 2 }\n")
f.write("	}\n")
f.write("}\n")
f.write("    \n")
f.write("units = {\n")

# Function to convert the colors of provinces to province IDs
def convertColorToProvinceID():
    for province in provinces:
        color = str(province)
        color = color.replace(" ", "")
        color = color.replace("(", "")
        color = color.replace(")", "")
        color = color.replace(",", ";")
        chosen_provinces.append(color)

# Function to remove duplicates from the list of province IDs
def removeDuplicates():
    for i in provinceIDs:
        if i not in new_provinceIDs:
            new_provinceIDs.append(i)

# Function to convert rows from the definition.csv file to province IDs
def convertRowToProvinceID():
    removeDuplicates()
    for element in new_provinceIDs:
        province = str(element)
        province = province.replace("", "")
        province = province.replace("[", "").replace("]", "").replace("'", "")
        my_list = province.split(";")
        province = my_list[0]
        final_provinces.append(province)

# Function to check if the colors of provinces that the user clicked on correspond to any province IDs in the definition.csv file
def checkCSV():
    print("Checking CSV")
    convertColorToProvinceID()

    with open('definition.csv', 'r') as file_obj:
        csv_file = csv.reader(file_obj)
        for row in csv_file:
            rows.append(row)

        for row in rows:
            for element in chosen_provinces:
                if str(element) in str(row):
                    provinceIDs.append(row)
        convertRowToProvinceID()
    print("Checking CSV is done!")

# Function to handle mouse clicks
def on_click(x, y, button, pressed):
    global started
    # Toggle the started flag on middle mouse button click
    if button == mouse.Button.middle and pressed:
        started = not started
        print(f"Started: {started}")
    # Add selected provinces on left mouse button click
    elif button == mouse.Button.left and pressed and started:
        # Get the color of the pixel at the clicked position
        color = pyautogui.pixel(x, y)
        print(color)
        provinces.append(color)

# Function to handle keyboard presses
def on_press(key):
    if key == keyboard.Key.esc:
        # Close the file and exit on ESC key press
        f.write("}")
        f.close()
        print("File is Ready")
    elif key == keyboard.Key.shift_r:
        # Check the selected provinces against the definition.csv file
        checkCSV()
        unit_count = 0
        count = 0
        # Write the selected provinces to the file as divisions
        for x in final_provinces:
            unit_count += 1
            f.write('   division = {\n')
            f.write(f'      name = "{unit_count}. {template}"\n')
            f.write(f'      location = "{final_provinces[count]}"\n')
            f.write(f'      division_template = "{template}"\n')
            f.write("   }\n")
            count += 1
        print("Added units to File. Press ESC to save.")

# Start listening for mouse clicks and keyboard presses
with mouse.Listener(on_click=on_click) as mouse_listener, keyboard.Listener(on_press=on_press) as keyboard_listener:
    mouse_listener.join()
    keyboard_listener.join()