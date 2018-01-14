def max_temp(dict_lat):
	dict_max = {}
	dict_min = {}
	list_values = []
	for line in dict_lat:
		for line_lat in dict_lat[line]:
			list_values.append(line_lat)
			dict_max.update(dict([(line, max(list_values))]))
			dict_min.update(dict([(line, min(list_values))]))
		list_values = []
	return dict_max

def classi_hot_island (dict_ext):
	
	dict_hot_island = {}
	for line in dict_ext:
		#for line_dict_ext in dict_ext[line]:
		while ( cont <= len(dict_ext) ):
			if (abs(dict_ext[line] - dict_ext[cont]) <= 2 ):

				dict_hot_island.update(dict([(str(dict_ext[line]) + "/" + str(dict_ext[cont]), "fraca")]))

			elif (abs(dict_ext[line] - dict_ext[cont]) > 2 and abs(dict_ext[line] - dict_ext[cont]) <= 4  ):
			
				dict_hot_island.update(dict([(str(dict_ext[line]) + "/" + str(dict_ext[cont]), "moderada")]))

			elif (abs(dict_ext[line] - dict_ext[cont]) > 4 and abs(dict_ext[line] - dict_ext[cont]) <= 6  ):
	
				dict_hot_island.update(dict([(str(dict_ext[line]) + "/" + str(dict_ext[cont]), "forte")]))
			else:
		
				dict_hot_island.update(dict([(str(dict_ext[line]) + "/" + str(dict_ext[cont]), "muito forte")]))

	return dict_hot_island

		
		
			
				
			
			

def cartridge(tmp):
	from geopy.distance import vincenty
	list_temp = []
	dict_loc = {}
	dict_max = {}
	dict_min = {}
	list_values = []
	LOC_FOG = [-22.865690, -43.223827]
	RANGE_HOT_ISLAND = 10000
	for line in tmp:
		line_tmp = line.split(',')
		list_temp.append(line_tmp[4])
		if(dict_loc.has_key(str(line_tmp[1]) + "," + str(line_tmp[2])) == False):
			list_temp = []
			list_temp.append(line_tmp[4])
			dict_loc.update(dict([(str(line_tmp[1]) + "," + str(line_tmp[2]), list_temp)]))
			
		else:
			
			dict_loc[str(line_tmp[1]) + "," + str(line_tmp[2])] = list_temp
	#dict_max = max_temp(dict_lat)
	
	for line in dict_loc:
		line_split = line.split()
		line_loc = [line_split[0], line_split[1]]
		if (vicenty(line_loc, LOC_FOG) < RANGE_HOT_ISLAND):
			for line_loc in dict_loc[line]:
				list_values.append(line_lat)
				dict_max.update(dict([(line, max(list_values))]))
				dict_min.update(dict([(line, min(list_values))]))
			list_values = []

	dict_hot_island = classi_hot_island(dict_max)
	return dict_hot_island
			
	
	
