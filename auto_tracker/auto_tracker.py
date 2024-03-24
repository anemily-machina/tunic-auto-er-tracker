
from copy import deepcopy
import json
import os
import time

DELAY_TIME = 0.5

SPOILER_ENTRACE_SECTION_HEADING = "Entrance Connections"

SAVE_FILE_FIELD_KEY_PREFIX = "randomizer entered portal" 

#edit this if your save folder is not the default	
user_profile = os.environ['USERPROFILE']
save_folder = f"{user_profile}\\AppData\\LocalLow\\Andrew Shouldice\\Secret Legend\\SAVES\\"

randomizer_folder = f"{user_profile}\\AppData\\LocalLow\\Andrew Shouldice\\Secret Legend\\Randomizer\\"

tracker_save_file = f"{user_profile}\\Documents\\2024-1-31_12.50.50_tunic-tracker.txt"

connections = {}

last_file = "test\\1234~1234"

def restart_tracking():
	global visited
	visited = set()

	connections = {}

	load_spoiler()




def load_spoiler():

	shop_count = 1

	spoiler_fname = os.path.join(randomizer_folder, "Spoiler.log")

	with open(spoiler_fname, 'r') as f_in:
		spoiler = f_in.read()

	entrance_start = spoiler.index(SPOILER_ENTRACE_SECTION_HEADING)

	entrance_section = spoiler[entrance_start+len(SPOILER_ENTRACE_SECTION_HEADING)+1:]

	entrance_section = entrance_section.split('\n')[:-1]

	entrance_section = [line[3:] for line in entrance_section]

	for line in entrance_section:

		e1, e2 = line.split(" -- ")

		if e1 == "Shop Portal":
			e1 += f"{shop_count}"
			shop_count+=1

		if e2 == "Shop Portal":
			e2 += f"{shop_count}"
			shop_count+=1

		connections[e1] = e2
		connections[e2] = e1

	"""
	for s in sorted(list(connections.keys())):
		print(f'"{s}":["tunic", "", "", "mark", "", "unknown"],')
	"""




def update_visited(latest_file):

	new_visited = set([])
	
	#can technically be deleted between these two steps
	if os.path.isfile(latest_file):

		#if there is a new savefile
		#if(latest_file.split('\\')[-1].split('~')[0] != last_file.split('\\')[-1].split('~')[0]):
		#	restart_tracking()

		with open(latest_file, 'r') as f_in:
			for line in f_in:

				#remove new line
				line = line[:-1]			

				if SAVE_FILE_FIELD_KEY_PREFIX in line:
					
					exit_name = line[len(SAVE_FILE_FIELD_KEY_PREFIX) +1 : -2]
					new_visited.add(exit_name)

	last_file = latest_file

	return new_visited


def update_tracker_save_file(visited, connections, roomname2savefile_long):

	shop_count = 1

	save_strings = deepcopy(roomname2savefile_long)

	for entrance in visited:

		#many to 1 connection = ick
		if entrance == 'Shop Portal':
			connect = []
			shop_index = 1
			shop_e = f"Shop Portal{shop_index}"
			while shop_e in connections:
				connect.append(shop_e)
				shop_index += 1
				shop_e = f"Shop Portal{shop_index}"
		else:
			connect = [entrance]

		for e in connect:

			connected_entrance = connections[e]

			#update to warp 
			save_strings[e][3] = 'warp'

			#update warp point
			save_strings[e][4] = save_strings[connected_entrance][1]
			save_strings[e][5] = save_strings[connected_entrance][2]	

	save_strings = [','.join(s) for s in save_strings.values()]
	save_string = "#tunic\n" + ",\n".join(save_strings) + ",\n"

	with open(tracker_save_file, 'w') as f_out:
		f_out.write(save_string)


def main():

	global visited
	global roomname2savefile_long
	global connections

	while(True):	

		global last_file

		save_files = [os.path.join(save_folder, fname) for fname in os.listdir(save_folder)]
		latest_file = max(save_files, key=os.path.getctime)

		#if there have been no changes
		if latest_file == last_file:
			time.sleep(DELAY_TIME)
			continue

		last_file = latest_file

		load_spoiler()	

		visited = update_visited(latest_file)

		update_tracker_save_file(visited, connections, roomname2savefile_long)

		time.sleep(DELAY_TIME)



roomname2savefile_long = {
	
	#Overworld
	"West Garden Entrance from Furnace":["tunic", "overworld", "aaaa0", "mark", "", "unknown"],
	"Entrance to Furnace near West Garden":["tunic", "overworld", "aaaa1", "mark", "", "unknown"],
	"Hourglass Cave Entrance":["tunic", "overworld", "hourglass_cave", "mark", "", "unknown"],
	"Entrance to Furnace from Beach":["tunic", "overworld", "beach_furnace", "mark", "", "unknown"],
	"Ruined Shop Entrance":["tunic", "overworld", "ruined_shop", "mark", "", "unknown"],
	"Fountain HC Door Entrance":["tunic", "overworld", "fountain_hc", "mark", "", "unknown"],
	"Town to Far Shore":["tunic", "overworld", "town_portal", "mark", "", "unknown"],
	"Old House Door Entrance":["tunic", "overworld", "house_door", "mark", "", "unknown"],
	"Windmill Entrance":["tunic", "overworld", "windmill", "mark", "", "unknown"],
	"Entrance to Furnace under Windmill":["tunic", "overworld", "aaaa19", "mark", "", "unknown"],
	"Atoll Upper Entrance":["tunic", "overworld", "atoll_upper", "mark", "", "unknown"],
	"Atoll Lower Entrance":["tunic", "overworld", "atoll_lower", "mark", "", "unknown"],
	"Swamp Upper Entrance":["tunic", "overworld", "aaaa22", "mark", "", "unknown"],
	"Swamp Lower Entrance":["tunic", "overworld", "aaaa23", "mark", "", "unknown"],
	"Ruined Passage Not-Door Entrance":["tunic", "overworld", "ruined_hall_not_door", "mark", "", "unknown"],
	"Ruined Passage Door Entrance":["tunic", "overworld", "ruined_hall_door", "mark", "", "unknown"],
	"Temple Door Entrance":["tunic", "overworld", "temple_door", "mark", "", "unknown"],
	"Stairs from Overworld to Mountain":["tunic", "overworld", "aaaa27", "mark", "", "unknown"],
	"Patrol Cave Entrance":["tunic", "overworld", "guard_patrol", "mark", "", "unknown"],
	"Special Shop Entrance":["tunic", "overworld", "special_shop", "mark", "", "unknown"],
	"Overworld to Forest Belltower":["tunic", "overworld", "aaaa30", "mark", "", "unknown"],
	"Cube Cave Entrance":["tunic", "overworld", "cube_cave", "mark", "", "unknown"],
	"Overworld to Quarry Connector":["tunic", "overworld", "aaaa32", "mark", "", "unknown"],
	"Dark Tomb Main Entrance":["tunic", "overworld", "aaaa33", "mark", "", "unknown"],
	"Secret Gathering Place Entrance":["tunic", "overworld", "fairy_cave", "mark", "", "unknown"],
	"Temple Rafters Entrance":["tunic", "overworld", "temple_rafters", "mark", "", "unknown"],	
	"Overworld to Fortress":["tunic", "overworld", "aaaa36", "mark", "", "unknown"],
	"Old House Waterfall Entrance":["tunic", "overworld", "house_back", "mark", "", "unknown"],
	"Spawn to Far Shore":["tunic", "overworld", "spawn_portal", "mark", "", "unknown"],
	"Southeast HC Door Entrance":["tunic", "overworld", "se_hc", "mark", "", "unknown"],
	"Changing Room Entrance":["tunic", "overworld", "changing_room", "mark", "", "unknown"],
	"West Garden Laurels Entrance":["tunic", "overworld", "aaaa41", "mark", "", "unknown"],
	"West Garden Entrance near Belltower":["tunic", "overworld", "aaaa42", "mark", "", "unknown"],
	"Well Ladder Entrance":["tunic", "overworld", "aaaa43", "mark", "", "unknown"],
	"Stick House Entrance":["tunic", "overworld", "stick_house", "mark", "", "unknown"],
	"Caustic Light Cave Entrance":["tunic", "overworld", "rotating_lights", "mark", "", "unknown"],
	"Maze Cave Entrance":["tunic", "overworld", "maze_cave", "mark", "", "unknown"],
	"Entrance to Well from Well Rail":["tunic", "overworld", "well_rail_n", "mark", "", "unknown"],
	"Entrance to Furnace from Well Rail":["tunic", "overworld", "well_rail_s", "mark", "", "unknown"],
	"Purgatory Top Exit":["tunic", "overworld", "purgatory_top", "mark", "", "unknown"],
	"Purgatory Bottom Exit":["tunic", "overworld", "purgatory_bot", "mark", "", "unknown"],
	"Shop Portal1":["tunic", "overworld", "shop1", "mark", "", "unknown"],
	"Shop Portal2":["tunic", "overworld", "shop2", "mark", "", "unknown"],
	"Shop Portal3":["tunic", "overworld", "shop3", "mark", "", "unknown"],
	"Shop Portal4":["tunic", "overworld", "shop4", "mark", "", "unknown"],
	"Shop Portal5":["tunic", "overworld", "shop5", "mark", "", "unknown"],
	"Shop Portal6":["tunic", "overworld", "shop6", "mark", "", "unknown"],

	#Overworld Interior
	"Stick House Exit":["tunic", "overworld_interiors", "stick_house", "mark", "", "unknown"],
	"Caustic Light Cave Exit":["tunic", "overworld_interiors", "rotating_lights", "mark", "", "unknown"],
	"Maze Cave Exit":["tunic", "overworld_interiors", "maze_cave", "mark", "", "unknown"],
	"Ruined Passage Not-Door Exit":["tunic", "overworld_interiors", "ruined_hall_not_door", "mark", "", "unknown"],
	"Ruined Passage Door Exit":["tunic", "overworld_interiors", "ruined_hall_door", "mark", "", "unknown"],
	"Fountain HC Room Exit":["tunic", "overworld_interiors", "fountain_hc", "mark", "", "unknown"],
	"Hourglass Cave Exit":["tunic", "overworld_interiors", "hourglass_cave", "mark", "", "unknown"],
	"Temple Door Exit":["tunic", "overworld_interiors", "temple_door", "mark", "", "unknown"],
	"Temple Rafters Exit":["tunic", "overworld_interiors", "temple_rafters", "mark", "", "unknown"],
	"Special Shop Exit":["tunic", "overworld_interiors", "special_shop", "mark", "", "unknown"],
	"Secret Gathering Place Exit":["tunic", "overworld_interiors", "fairy_cave", "mark", "", "unknown"],
	"Guard Patrol Cave Exit":["tunic", "overworld_interiors", "guard_patrol", "mark", "", "unknown"],
	"Changing Room Exit":["tunic", "overworld_interiors", "changing_room", "mark", "", "unknown"],
	"Cube Cave Exit":["tunic", "overworld_interiors", "cube_cave", "mark", "", "unknown"],
	"Southeast HC Room Exit":["tunic", "overworld_interiors", "se_hc", "mark", "", "unknown"],
	"Old House Door Exit":["tunic", "overworld_interiors", "house_door", "mark", "", "unknown"],
	"Old House to Glyph Tower":["tunic", "overworld_interiors", "house_portal", "mark", "", "unknown"],
	"Old House Waterfall Exit":["tunic", "overworld_interiors", "house_back", "mark", "", "unknown"],
	"Windmill Exit":["tunic", "overworld_interiors", "windmill_front", "mark", "", "unknown"],
	"Windmill Shop":["tunic", "overworld_interiors", "windmill_back", "mark", "", "unknown"],
	"Furnace Exit towards West Garden":["tunic", "overworld_interiors", "aaaa5", "mark", "", "unknown"],
	"Furnace Exit to Beach":["tunic", "overworld_interiors", "aaaa6", "mark", "", "unknown"],
	"Furnace Exit to Dark Tomb":["tunic", "overworld_interiors", "aaaa7", "mark", "", "unknown"],
	"Furnace Exit under Windmill":["tunic", "overworld_interiors", "aaaa8", "mark", "", "unknown"],
	"Furnace Exit towards Well":["tunic", "overworld_interiors", "aaaa9", "mark", "", "unknown"],
	"Glyph Tower Exit":["tunic", "overworld_interiors", "glyph_tower", "mark", "", "unknown"],
	"Ruined Shop Exit":["tunic", "overworld_interiors", "ruined_shop", "mark", "", "unknown"],

	#East forest
	"Forest Belltower to Overworld":["tunic", "east_forest", "aaaa0", "mark", "", "unknown"],
	"Forest Belltower to Guard Captain Room":["tunic", "east_forest", "aaaa1", "mark", "", "unknown"],
	"Forest Belltower to Forest":["tunic", "east_forest", "aaaa2", "mark", "", "unknown"],
	"Forest Belltower to Fortress":["tunic", "east_forest", "aaaa3", "mark", "", "unknown"],
	"Guard House 1 to Guard Captain Room":["tunic", "east_forest", "aaaa4", "mark", "", "unknown"],
	"Guard House 1 Upper Forest Exit":["tunic", "east_forest", "aaaa5", "mark", "", "unknown"],
	"Guard House 1 Dance Fox Exit":["tunic", "east_forest", "aaaa6", "mark", "", "unknown"],
	"Guard House 1 Lower Exit":["tunic", "east_forest", "aaaa7", "mark", "", "unknown"],
	"Guard House 2 Upper Exit":["tunic", "east_forest", "aaaa8", "mark", "", "unknown"],
	"Guard House 2 Lower Exit":["tunic", "east_forest", "aaaa9", "mark", "", "unknown"],
	"East Forest Hero's Grave":["tunic", "east_forest", "aaaa10", "mark", "", "unknown"],
	"Forest Grave Path Upper Exit":["tunic", "east_forest", "aaaa11", "mark", "", "unknown"],
	"Forest Grave Path Lower Exit":["tunic", "east_forest", "aaaa12", "mark", "", "unknown"],
	"Forest Grave Path Lower Entrance":["tunic", "east_forest", "aaaa13", "mark", "", "unknown"],
	"Forest Grave Path Upper Entrance":["tunic", "east_forest", "aaaa14", "mark", "", "unknown"],
	"Forest Guard House 2 Upper Entrance":["tunic", "east_forest", "aaaa15", "mark", "", "unknown"],
	"Forest Guard House 2 Lower Entrance":["tunic", "east_forest", "aaaa16", "mark", "", "unknown"],
	"Forest Guard House 1 Gate Entrance":["tunic", "east_forest", "aaaa17", "mark", "", "unknown"],
	"Forest to Belltower":["tunic", "east_forest", "aaaa18", "mark", "", "unknown"],
	"Forest Dance Fox Outside Doorway":["tunic", "east_forest", "aaaa19", "mark", "", "unknown"],
	"Forest to Far Shore":["tunic", "east_forest", "forest_portal", "mark", "", "unknown"],
	"Forest Guard House 1 Lower Entrance":["tunic", "east_forest", "guard_house_1_lower", "mark", "", "unknown"],
	"Guard Captain Room Non-Gate Exit":["tunic", "east_forest", "boss_front", "mark", "", "unknown"],
	"Guard Captain Room Gate Exit":["tunic", "east_forest", "boss_back", "mark", "", "unknown"],

	#Dark Tomb
	"Dark Tomb to Overworld":["tunic", "dark_tomb", "aaaa0", "mark", "", "unknown"],
	"Dark Tomb to Checkpoint":["tunic", "dark_tomb", "aaaa1", "mark", "", "unknown"],
	"Dark Tomb to Furnace":["tunic", "dark_tomb", "aaaa2", "mark", "", "unknown"],
	

	#Bottom of the well
	"Well to Well Boss":["tunic", "bottom_of_the_well", "aaaa1", "mark", "", "unknown"],
	"Well Exit towards Furnace":["tunic", "bottom_of_the_well", "aaaa2", "mark", "", "unknown"],
	"Well Boss to Well":["tunic", "bottom_of_the_well", "boss_to_well", "mark", "", "unknown"],
	"Checkpoint to Dark Tomb":["tunic", "bottom_of_the_well", "dt_checkpoint", "mark", "", "unknown"],
	"Well Ladder Exit":["tunic", "bottom_of_the_well", "aaaa5", "mark", "", "unknown"],
	
	#West Garden
	"West Garden Exit after Boss":["tunic", "west_garden", "aaaa0", "mark", "", "unknown"],
	"West Garden Exit near Hero's Grave":["tunic", "west_garden", "aaaa1", "mark", "", "unknown"],	
	"West Garden Hero's Grave":["tunic", "west_garden", "grave", "mark", "", "unknown"],
	"West Garden Shop":["tunic", "west_garden", "aaaa3", "mark", "", "unknown"],
	"West Garden to Magic Dagger House":["tunic", "west_garden", "aaaa4", "mark", "", "unknown"],
	"West Garden to Far Shore":["tunic", "west_garden", "garden_portal", "mark", "", "unknown"],
	"West Garden Laurels Exit":["tunic", "west_garden", "aaaa6", "mark", "", "unknown"],
	"Magic Dagger House Exit":["tunic", "west_garden", "magic_dagger", "mark", "", "unknown"],

	#Beneath the earth	
	"Beneath the Earth to Fortress Interior":["tunic", "beneath_the_earth", "aaaa0", "mark", "", "unknown"],
	"Beneath the Earth to Fortress Courtyard":["tunic", "beneath_the_earth", "aaaa1", "mark", "", "unknown"],

	#Fortress
	"Fortress Courtyard to Overworld":["tunic", "fortress", "aaaa0", "mark", "", "unknown"],
	"Fortress Courtyard to Forest Belltower":["tunic", "fortress", "aaaa1", "mark", "", "unknown"],
	"Fortress Courtyard to Fortress Interior":["tunic", "fortress", "main_entry", "mark", "", "unknown"],
	"Fortress Courtyard to East Fortress":["tunic", "fortress", "aaaa3", "mark", "", "unknown"],
	"Fortress Courtyard to Fortress Grave Path Lower":["tunic", "fortress", "aaaa4", "mark", "", "unknown"],
	"Fortress Courtyard Shop":["tunic", "fortress", "aaaa5", "mark", "", "unknown"],
	"Fortress Courtyard to Beneath the Earth":["tunic", "fortress", "aaaa6", "mark", "", "unknown"],
	"Fortress Courtyard to Fortress Grave Path Upper":["tunic", "fortress", "aaaa7", "mark", "", "unknown"],
	"Fortress Grave Path Dusty Entrance":["tunic", "fortress", "aaaa8", "mark", "", "unknown"],
	"Fortress Hero's Grave":["tunic", "fortress", "aaaa9", "mark", "", "unknown"],
	"Fortress Grave Path Upper Exit":["tunic", "fortress", "aaaa10", "mark", "", "unknown"],
	"Fortress Grave Path Lower Exit":["tunic", "fortress", "aaaa11", "mark", "", "unknown"],
	"East Fortress to Courtyard":["tunic", "fortress", "aaaa12", "mark", "", "unknown"],
	"East Fortress to Interior Upper":["tunic", "fortress", "east_int_upper", "mark", "", "unknown"],
	"East Fortress to Interior Lower":["tunic", "fortress", "east_int_lower", "mark", "", "unknown"],
	"Fortress Interior to Beneath the Earth":["tunic", "fortress", "aaaa15", "mark", "", "unknown"],
	"Fortress Interior Main Exit":["tunic", "fortress", "arena_entry", "mark", "", "unknown"],
	"Fortress Interior Shop":["tunic", "fortress", "aaaa17", "mark", "", "unknown"],
	"Fortress Interior to Siege Engine Arena":["tunic", "fortress", "fortres_gold_door", "mark", "", "unknown"],
	"Fortress Interior to East Fortress Upper":["tunic", "fortress", "int_east_upper", "mark", "", "unknown"],
	"Fortress Interior to East Fortress Lower":["tunic", "fortress", "int_east_lower", "mark", "", "unknown"],
	"Dusty Exit":["tunic", "fortress", "dusty", "mark", "", "unknown"],
	"Fortress to Far Shore":["tunic", "fortress", "spidertank_portal", "mark", "", "unknown"],
	"Siege Engine Arena to Fortress":["tunic", "fortress", "spidertank_entry", "mark", "", "unknown"],

	#Atoll
	"Atoll to Far Shore":["tunic", "atoll", "portal", "mark", "", "unknown"],
	"Atoll to Far Shore":["tunic", "atoll", "portal", "mark", "", "unknown"],
	"Atoll Upper Exit":["tunic", "atoll", "upper_exit", "mark", "", "unknown"],
	"Atoll Lower Exit":["tunic", "atoll", "lower_exit", "mark", "", "unknown"],
	"Atoll Shop":["tunic", "atoll", "aaaa3", "mark", "", "unknown"],
	"Frog Stairs Mouth Entrance":["tunic", "atoll", "aaaa4", "mark", "", "unknown"],
	"Frog Stairs Eye Entrance":["tunic", "atoll", "aaaa5", "mark", "", "unknown"],
	"Atoll Statue Teleporter":["tunic", "atoll", "statue", "mark", "", "unknown"],
	
	#Frogs' Domain
	"Frog Stairs Eye Exit":["tunic", "frogs", "frog_eye", "mark", "", "unknown"],	
	"Frog Stairs Mouth Exit":["tunic", "frogs", "frog_mouth", "mark", "", "unknown"],
	"Frog Stairs to Frog's Domain's Entrance":["tunic", "frogs", "frog_ladder_top", "mark", "", "unknown"],
	"Frog Stairs to Frog's Domain's Exit":["tunic", "frogs", "frog_back_entry", "mark", "", "unknown"],
	"Frog's Domain Ladder Exit":["tunic", "frogs", "frog_ladder_bot", "mark", "", "unknown"],
	"Frog's Domain Orb Exit":["tunic", "frogs", "frog_exit", "mark", "", "unknown"],

	#Library
	"Library Exterior Tree":["tunic", "library", "aaaa0", "mark", "", "unknown"],
	"Library Exterior Ladder":["tunic", "library", "aaaa1", "mark", "", "unknown"],
	"Library Hall Bookshelf Exit":["tunic", "library", "aaaa2", "mark", "", "unknown"],
	"Library Hero's Grave":["tunic", "library", "aaaa3", "mark", "", "unknown"],
	"Library Hall to Rotunda":["tunic", "library", "aaaa4", "mark", "", "unknown"],
	"Library Rotunda Lower Exit":["tunic", "library", "aaaa5", "mark", "", "unknown"],
	"Library Rotunda Upper Exit":["tunic", "library", "aaaa6", "mark", "", "unknown"],
	"Library Lab to Rotunda":["tunic", "library", "aaaa7", "mark", "", "unknown"],
	"Library Lab to Librarian Arena":["tunic", "library", "aaaa8", "mark", "", "unknown"],
	"Library to Far Shore":["tunic", "library", "aaaa9", "mark", "", "unknown"],
	"Librarian Arena Exit":["tunic", "library", "aaaa10", "mark", "", "unknown"],
	
	#Quarry
	"Quarry to Monastery Front":["tunic", "quarry", "aaaa0", "mark", "", "unknown"],
	"Quarry to Mountain":["tunic", "quarry", "aaaa1", "mark", "", "unknown"],
	"Quarry to Overworld Exit":["tunic", "quarry", "aaaa2", "mark", "", "unknown"],
	"Quarry to Far Shore":["tunic", "quarry", "aaaa3", "mark", "", "unknown"],
	"Quarry Shop":["tunic", "quarry", "aaaa4", "mark", "", "unknown"],
	"Quarry to Ziggurat":["tunic", "quarry", "aaaa5", "mark", "", "unknown"],
	"Quarry to Monastery Back":["tunic", "quarry", "aaaa6", "mark", "", "unknown"],
	"Quarry Connector to Overworld":["tunic", "quarry", "aaaa7", "mark", "", "unknown"],
	"Quarry Connector to Quarry":["tunic", "quarry", "aaaa8", "mark", "", "unknown"],
	"Monastery Front Exit":["tunic", "quarry", "monastery_front", "mark", "", "unknown"],
	"Monastery Hero's Grave":["tunic", "quarry", "monastery_grave", "mark", "", "unknown"],
	"Monastery Rear Exit":["tunic", "quarry", "monastery_back", "mark", "", "unknown"],
	"Top of the Mountain Exit":["tunic", "quarry", "aaaa11", "mark", "", "unknown"],
	"Stairs to Top of the Mountain":["tunic", "quarry", "mountain_stairs", "mark", "", "unknown"],
	"Mountain to Quarry":["tunic", "quarry", "aaaa13", "mark", "", "unknown"],
	"Mountain to Overworld":["tunic", "quarry", "aaaa14", "mark", "", "unknown"],
	
	#Swamp/Cemetary
	"Swamp Upper Exit":["tunic", "swamp", "aaaa0", "mark", "", "unknown"],
	"Swamp Lower Exit":["tunic", "swamp", "aaaa1", "mark", "", "unknown"],
	"Swamp to Cathedral Main Entrance":["tunic", "swamp", "cathedral_door", "mark", "", "unknown"],
	"Swamp to Cathedral Secret Legend Room Entrance":["tunic", "swamp", "aaaa3", "mark", "", "unknown"],
	"Swamp Hero's Grave":["tunic", "swamp", "swamp_grave", "mark", "", "unknown"],
	"Swamp Shop":["tunic", "swamp", "aaaa5", "mark", "", "unknown"],
	"Swamp to Gauntlet":["tunic", "swamp", "gauntlet_entry", "mark", "", "unknown"],

	#Cathedral
	"Gauntlet Shop":["tunic", "cathedral", "aaaa0", "mark", "", "unknown"],
	"Gauntlet to Swamp":["tunic", "cathedral", "aaaa1", "mark", "", "unknown"],
	"Gauntlet Elevator":["tunic", "cathedral", "elev_bot", "mark", "", "unknown"],
	"Cathedral Secret Legend Room Exit":["tunic", "cathedral", "aaaa3", "mark", "", "unknown"],
	"Cathedral Main Exit":["tunic", "cathedral", "aaaa4", "mark", "", "unknown"],
	"Cathedral Elevator":["tunic", "cathedral", "elev_top", "mark", "", "unknown"],
	
	#Ziggurat
	"Ziggurat Entry Hallway to Quarry":["tunic", "ziggurat", "zig0_front", "mark", "", "unknown"],
	"Ziggurat Entry Hallway to Ziggurat Upper":["tunic", "ziggurat", "zig0_back", "mark", "", "unknown"],
	"Ziggurat Upper to Ziggurat Entry Hallway":["tunic", "ziggurat", "zig1_elev", "mark", "", "unknown"],
	"Ziggurat Upper to Ziggurat Tower":["tunic", "ziggurat", "zig1_back", "mark", "", "unknown"],
	"Ziggurat Tower to Ziggurat Upper":["tunic", "ziggurat", "zig2_top", "mark", "", "unknown"],
	"Ziggurat Tower to Ziggurat Lower":["tunic", "ziggurat", "zig2_bot", "mark", "", "unknown"],
	"Ziggurat Lower to Ziggurat Tower":["tunic", "ziggurat", "zig3_front", "mark", "", "unknown"],
	"Ziggurat Portal Room Entrance":["tunic", "ziggurat", "zig3_back", "mark", "", "unknown"],
	"Ziggurat Portal Room Exit":["tunic", "ziggurat", "zig_portal_door", "mark", "", "unknown"],
	"Ziggurat to Far Shore":["tunic", "ziggurat", "zig_portal_pad", "mark", "", "unknown"],
	
	#Farshore, Hero's Grave, Heir Fight
	"Far Shore to Heir":["tunic", "far_shore", "heir", "mark", "", "unknown"],
	"Far Shore to Quarry":["tunic", "far_shore", "quarry", "mark", "", "unknown"],
	"Far Shore to West Garden":["tunic", "far_shore", "west_garden", "mark", "", "unknown"],
	"Far Shore to Atoll":["tunic", "far_shore", "atoll", "mark", "", "unknown"],
	"Far Shore to Library":["tunic", "far_shore", "library", "mark", "", "unknown"],
	"Far Shore to Town":["tunic", "far_shore", "town", "mark", "", "unknown"],
	"Far Shore to Fortress":["tunic", "far_shore", "vault", "mark", "", "unknown"],
	"Far Shore to Ziggurat":["tunic", "far_shore", "zig", "mark", "", "unknown"],
	"Far Shore to Spawn":["tunic", "far_shore", "spawn", "mark", "", "unknown"],
	"Far Shore to East Forest":["tunic", "far_shore", "forest", "mark", "", "unknown"],
	"Hero's Grave to Library":["tunic", "far_shore", "library_grave", "mark", "", "unknown"],
	"Hero's Grave to West Garden":["tunic", "far_shore", "garden_grave", "mark", "", "unknown"],
	"Hero's Grave to Monastery":["tunic", "far_shore", "monastery_grave", "mark", "", "unknown"],
	"Hero's Grave to Fortress":["tunic", "far_shore", "fortress_grave", "mark", "", "unknown"],	
	"Hero's Grave to East Forest":["tunic", "far_shore", "forest_grave", "mark", "", "unknown"],
	"Hero's Grave to Swamp":["tunic", "far_shore", "swamp_grave", "mark", "", "unknown"],
	"Heir Arena Exit":["tunic", "far_shore", "heir_exit", "mark", "", "unknown"],
	
	
	
	
	
	

	

	

	

	

	
	

	
	
	



			

	
	
	

	
	
	
	




	
	
	

	
	







	
	
	

		


	
	
	
	
}

	



if __name__ == '__main__':
	main()