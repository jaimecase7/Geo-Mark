import FreeSimpleGUI as sg
import simplekml
from geopy.geocoders import Nominatim
import geopy

# Setting theme to black theme because dark themes are cool
sg.theme("Black")

# Getting rid of the geopy.geocdoers timeout feature so the program will run
geopy.geocoders.options.default_timeout = 7

# Setting up the location class to use the geopy features on our addresses
loc = Nominatim(user_agent="Geopy Library")

# Create a kml map instance we can append changes to and later save
my_map=simplekml.Kml()

# Show that the file is in process of being created by processing each address one at a time
output_array=[]

# Building the elements for the program window
label1 = sg.Text("Enter the name of your file: (No need to add .kml extension)")
input_box = sg.InputText(size=[50,1])
label2 = sg.Text('Enter addresses below: (No need to add "City, State")')
label_city = sg.Text("City:")
city = sg.InputText(tooltip="Enter City Here", size=[15,1], key="city")
label_state = sg.Text("State:")
state = sg.InputText(tooltip="Enter State Here", size=[15,1], key="state")
address_box = sg.Multiline(size=([50,20]))
label3 = sg.Text("Select destination folder:")
destination = sg.FolderBrowse()
button = sg.Button("Create KML File", key="submit")
label4 = sg.Text("File processing:")
output_box = sg.Listbox(values=output_array,
                    key="output",
                    enable_events=True,
                    size=([50,4]),
                    expand_y=True)


# Describing the program window with all the elements defined above
window = sg.Window("Geo-Marker",
                   layout=[ [label1],
                            [input_box],
                            [label_city, city, label_state, state],
                            [label2],
                            [address_box],
                            [label3,destination],
                            [button],
                            [label4],
                            [output_box]
                   ],
                   font=('Helvetica', 10),
                   icon="2969398_location_map_marker_navigation_icon.ico",
                   titlebar_icon="2969398_location_map_marker_navigation_icon_LPLBLUE.ico")

# Build the program loop that displays the window and responds to user commands
while True:
    event, values = window.read(timeout=200)

    match event:

        # When the user presses the "Create KML File" button, process the command
        case "submit":
            error_toggle=0
            output_array.clear()
            filepath = f"{values["Browse"]}/{values[0]}.kml"

            address_array = values[1].splitlines()
            print(address_array)

            for address in address_array:
                output_array.append(str(address) + " " + values["city"] + " " + values["state"])
                window['output'].update(values=output_array)
                window.read(timeout=200)
                # print(str(address) + " Lubbock TX")
                getLoc = loc.geocode(str(address) + " " + values["city"] + " " + values["state"])
                # print(getLoc)


                if (getLoc is None):
                    sg.popup(f"Please Check the name and spelling of {address} and the other addresses in the list and try again", title="ERROR", text_color="red", icon="2969398_location_map_marker_navigation_icon.ico")
                    error_toggle=1
                    break

                my_map.newpoint(name=f"{address}",coords=[(getLoc.longitude, getLoc.latitude)])
                print(getLoc, getLoc.longitude, getLoc.latitude)


            if not error_toggle:
                my_map.save(filepath)
                sg.popup("Your map has been created!", title="SUCCESS!", text_color="green", icon="2969398_location_map_marker_navigation_icon.ico")

        # When the user presses the exit button, close the window with no errors from FreeSimpleGUI
        case sg.WIN_CLOSED:
            break

window.close()