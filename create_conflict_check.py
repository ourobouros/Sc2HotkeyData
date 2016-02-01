from _operator import length_hint
filepaths = ['data\HotkeyData LotV Multiplayer.txt',
			 'data\HotkeyData Coop.txt',
			 'data\HotkeyData LotV Campaign.txt',
			 'data\HotkeyData LotV Prologue.txt',
			 'data\HotkeyData HotS Campaign.txt',
			 'data\HotkeyData WoL Campaign.txt',
			 'data\HotkeyData HotS Multiplayer.txt',
			 'data\HotkeyData WoL Multiplayer.txt',
			 'data\HotkeyData Left2Die.txt']

def read_KeyData(filename):
	# Reads the format of HotkeyData files to produce a hotkey dictionary containing command cards
	key_dict = {}
	key = []
	key_str_save = ''
	with open(filename, 'r') as file:
			data = file.readlines()
	
	for line in data:
		sline = line.strip(' \t\n\r')
		if sline:
			if not '=' in line and not 'UnitCommands' in line:
				key = key[:line.count('\t')]
				key.append(sline)
				key_str = filename.replace('data\HotkeyData ', '').replace('.txt', '') + '/' + '/'.join(key)
				if key_str in key_dict:
					print('ERROR:\nRepeated key in ', filename, ' at\n', key_str)
					return
			else:
				key_str = filename.replace('data\HotkeyData ', '').replace('.txt', '') + '/' + '/'.join(key)
				if key_str == key_str_save:
					print('ERROR:\nRepeated key in ', filename, ' at\n', key_str)
				if not key_str in key_dict:
					key_dict[key_str] = []
				ssline = sline.split('=')
				key_dict[key_str].append(ssline[0])
		else:
			new_key = 1
			key_str_save = key_str
	return key_dict


def key_cull(key_dict1, key_dict2):
	# removes command cards in key_dict2 which are already represented in key_dict1
	temp_keys = key_dict2.copy()
	for key1 in key_dict1:
		for key2 in key_dict2:
			if (key2 in temp_keys and
			   key1 != key2 and
			   all(keys in key_dict1[key1] for keys in key_dict2[key2])):
				# print (key2+'\t<=\n'+key1+'\n')
				temp_keys.pop(key2, None)
	return temp_keys


# Create a trimmed dictionary of unique command cards from filepaths
key_dict = []
for file in filepaths:
	key_dict.append(read_KeyData(file))

for i in range(len(key_dict)):
	for j in range(len(key_dict)):
		key_dict[j] = key_cull(key_dict[i], key_dict[j])


# Generate CONFLICT_CHECKS list
CONFLICT_CHECKS_NEW = []		
with open('CONFLICT_CHECKS.txt', 'w') as file:
	jlength = len(key_dict)
	j = 1
	for key_dict_group in key_dict:
		llength = len(key_dict_group)
		l = 1
		for key in sorted(key_dict_group):
			isfirst = j == 1 and l == 1
			if isfirst:
				prefix = 'CONFLICT_CHECKS = {'
			else:
				prefix = '                   '
				
			if 'BasicUnitCommands' in key_dict_group[key]:
				i = key_dict_group[key].index('BasicUnitCommands')
				key_dict_group[key] = key_dict_group[key][:i] + ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack'] + key_dict_group[key][i + 1:]
			elif 'PacifistUnitCommands' in key_dict_group[key]:
				i = key_dict_group[key].index('PacifistUnitCommands')
				key_dict_group[key] = key_dict_group[key][:i] + ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol'] + key_dict_group[key][i + 1:]
			updated_key = key.replace("\'", "\\\'")
			
			islast = j == jlength and l == llength
			if islast:
				suffix = '}'
			else:
				suffix = ',\n'
			file.write(prefix + "\'" + updated_key + "\' : " + str(key_dict_group[key]) + suffix)
			l = l + 1
		j = j + 1