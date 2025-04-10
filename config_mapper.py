#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from datetime import timedelta
from timeit import default_timer as timer
#=================================================================================
#=================================================================================
#Global Variables
#=================================================================================
#=================================================================================
version = '2.0'
spacer_length = 150
char_limit = 80
new_line = "\n"
tab_char = "\t"
space = " "
config_object_file = "config_object_mapping.txt"
output_config = []
input_dir = ""
output_dir = "_output/"
debug_flag = False
date_format = '%A, %B %d, %Y @ %H:%M.%S'
template_variable_placeholder = "TEMPLATE_VAR"


#=================================================================================
#=================================================================================
#General Functions
#=================================================================================
#=================================================================================

#*****************************************************
#Spacer Function
#*****************************************************
def func_spacer(length=spacer_length):
	spacer_str = ""
	for i in range(length):
		spacer_str = spacer_str+"="
	return spacer_str

#*****************************************************
#Log Event in uniform manner
#*****************************************************
def log_event(event, spacer_flag=True, ts_flag=True, debug_command=False):
	event_output = ""
	


	if ts_flag:
		timestamp = datetime.strftime(datetime.today(), '%H:%M.%S.%f %p')
		event_output += str(timestamp) + ": "
	
	if debug_command:
		event_output += "[*** debug ***]"

	event_output += str(event)

	if debug_command and debug_flag:	
		print(event_output)
	elif not debug_command:
		print(event_output)
	
	if(spacer_flag):
		print(spacer)
	
#*****************************************************
#Log Debug Event in uniform manner
#*****************************************************	
def log_debug_event(event, function):
 	log_event("["+function+"]"+event, False, True, True)


#*****************************************************
#Ingest Config Objects
#*****************************************************
def func_ingest_config_objects(config_object_file):
	config_objects_idx = 0
	config_objects = {}

	for line in open(config_object_file):
		config_line=line.strip()
		if (not config_line == ""):
			if (not config_line.startswith("#")):			
				log_debug_event(config_line.strip(), "func_ingest_config_objects")
				config_object = config_line.split(',')
				if len(config_object) != 2:
					log_event("Error with config_object_mapping.txt", False, False)
					log_event(str(config_object), False, False)
					sys.exit("Ensure all entries have a mappings '"+str(config_object)+"'"+new_line+spacer)
				config_objects.update({config_objects_idx : { "local" : config_object[0].strip(), "mapped" : config_object[1].strip() }})
				config_objects_idx += 1
	
	if config_objects_idx < 1:
		log_event("Error with config_object_mapping.txt", False, False)
		sys.exit("Detected Zero (0) configuration mappings"+new_line+spacer)
	return config_objects 


#*****************************************************
#Get Configuration Objects 
#*****************************************************
def get_config_objects(config_object):
	return "'"+config_object['local']+"' mapped to '"+config_object['mapped']+"'"

#*****************************************************
#Get Configuration Objects Mapping
#*****************************************************
def get_config_objects_mapping(config_object_mapping):
	config_object_mappings_str = ""
	new_line_flag = False
	for config_objects in config_object_mapping.values():
		if(new_line_flag):
			config_object_mappings_str += new_line
		new_line_flag = True	 
		config_object_mappings_str += (get_config_objects(config_objects))
	return config_object_mappings_str

#*****************************************************
#Display the Configuration Objects
#*****************************************************
def show_config_objects_mapping(config_object_mapping):
	log_event("Displaying Configuration Object Mappings"+new_line, False)
	print(get_config_objects_mapping(config_object_mapping))
	print(spacer)

#*****************************************************
#Dynamically Check of String has open 'double quote'
#*****************************************************
def check_multi_line(line):
	if line.count('"') == 1:
		log_debug_event("Line Check Fail: [" + line + "]", "check_multi_line")
		return True
	else:
		log_debug_event("Line Check Success : [" + line + "]", "check_multi_line")
		return False

#*****************************************************
#Check if the raw command is already in the list.
#*****************************************************
def check_for_duplication(input_config_command,raw_config_commands ):
	log_debug_event("Checking '"+ input_config_command + "'", "check_for_duplication")
	for raw_commands in raw_config_commands:
		if input_config_command == raw_commands:
			log_debug_event("[Duplicate Found] '"+ input_config_command + "'", "check_for_duplication")
			return False
	return True

#*****************************************************
#Find Config Ojbects in File
#*****************************************************
def func_find_config_objects(input_filename, config_object_mapping):
	first_pass_flag = True
	end_of_line_flag = False
	raw_config_commands = []
	
	
	log_event("Opening " + input_filename + "...", False) 
	log_event("Searching " + input_filename + "...", False) 	

	#Iterate through configurations
	for config_object_map in config_object_mapping.values():
		config_object_search_count = 0
		config_object = config_object_map['local']
		log_debug_event("[config_object search] "+config_object, "func_find_config_objects")
		
		#Iterate though each line in the input file
		with open(input_filename) as input_file:
			for line in input_file:

				input_config_command = line.strip()
				log_debug_event("[searching for "+config_object+" in '"+input_config_command+"']", "func_find_config_objects")
				
				#Ignore Commented (#) lines
				if not input_config_command.startswith("#"): #Ignore Commented lines in the Input
					#Compare if Config object is in the Input Config Command	
					if config_object+space in input_config_command: #add space at end of each config object
						
						#Additional Output for Troubleshooting
						if len(input_config_command) > int(char_limit+3):
							log_debug_event("[MATCH] "+config_object+" --> Found in ["+input_config_command.strip()[:char_limit]+"...]", "func_find_config_objects")
						else:
							log_debug_event("[MATCH] "+config_object+" --> Found in ["+input_config_command.strip()+"]", "func_find_config_objects")

						if check_multi_line(input_config_command):
							log_debug_event("Multi-Line Detected: " + input_config_command.strip()[:char_limit], "func_find_config_objects")
							while(not end_of_line_flag):
								next_line = input_file.readline()
								log_debug_event("Next Line: [" + next_line+"]", "func_find_config_objects")
								input_config_command += next_line
								if("\"" in next_line):
									#log_event("6a: Found" + next_line)
									end_of_line_flag = True
							
							config_object_search_count += 1
							end_of_line_flag = False
							
							if check_multi_line(input_config_command):
								log_event("[ERROR - func_find_config_objects] with dynamic multi-line ["+input_config_command+"]")
								sys.exit()
							else:
								log_debug_event("Multi-Line Capture Complete", "func_find_config_objects")
								if check_for_duplication(input_config_command.strip(), raw_config_commands):
									raw_config_commands.append(input_config_command.strip())
							
						else:
							log_debug_event("Multi-Line False - Adding to Commands", "func_find_config_objects")
							config_object_search_count += 1
							if check_for_duplication(input_config_command.strip(), raw_config_commands):
								raw_config_commands.append(input_config_command.strip())
	
		#Summarize after each config object			
		log_event(config_object+" --> Found in " +str(config_object_search_count)+ " line(s)", False)
		
		#set first past flag to false
		first_pass_flag =False	
	
	log_event("Completed Search of " + input_filename + "...") 		
	return raw_config_commands


#*****************************************************
# Get Output File Header
#*****************************************************
def get_output_file_header(input_filepath, config_object_mapping):
	header = []
	header.append("#"+str(func_spacer()))
	header.append("# Time Created: " + str(datetime.strftime(datetime.today(), date_format)))
	header.append("# "+str(sys.argv[0])+" - Formatted configuration from "+input_filepath)
	header.append("# Command Mappings")
	for config_object in config_object_mapping.values():
		header.append("#"+str(config_object))
	header.append("#"+str(func_spacer()))
	return header

#*****************************************************
# Get Output File Footer
#*****************************************************
def get_output_file_footer(input_filepath):
	footer = []
	footer.append("#"+str(func_spacer()))
	footer.append("# "+str(sys.argv[0])+"  - Formatted configuration from "+input_filepath)
	footer.append("# Time Completed: " + str(datetime.strftime(datetime.today(), date_format)))
	footer.append("#"+str(func_spacer()))
	return footer


#*****************************************************
# Get Command Header
#*****************************************************
def get_command_header(config_object):
	command_header = []
	command_header.append("#"+str(func_spacer()))
	command_header.append("#"+str(get_config_objects(config_object)))
	command_header.append("#"+str(func_spacer()))
	return command_header

#*****************************************************
#Check for Valid Directory
#*****************************************************
def check_dir(dir):
	if os.path.exists(dir):
		return True
	else:
		return False
			  
#*****************************************************
#Prompt for Input Directory
#*****************************************************
def prompt_for_input_dir():
    while True:
        dir = input("Please define input_dir [eg '_input/'] : ")
        if check_dir(dir):
             return dir
        log_event("[ERROR] '"+dir +"' does not exist!. Please Try Again", False)

#*****************************************************
#Format Config Commands
#*****************************************************
def format_output(input_filepath, raw_config_commands, config_object_mapping):
	formatted_config_commands = []
	template_variable = get_template_subdir(input_filepath)
	log_debug_event("Setting Template Variable to : "+template_variable+" ","format_output")

	#Insert Header
	formatted_config_commands += get_output_file_header(input_filepath, config_object_mapping)
	log_debug_event("Begin Formating with Mappings","format_output")
	for config_object_map in config_object_mapping.values():
		config_object = config_object_map['local']
		log_debug_event("Start mapping from Local: "+config_object+" ","format_output")
		formatted_config_commands += get_command_header(config_object_map)
		
		for raw_config_command in raw_config_commands:
			log_debug_event("Local: "+config_object+" - rawconfig: "+raw_config_command+" ","format_output")
			if config_object+space in raw_config_command: #add space at end of each config object
				log_debug_event("Match","format_output")
				formatted_config_command = raw_config_command.replace(str(config_object), config_object_map['mapped'])
				formatted_config_command = formatted_config_command.replace(template_variable_placeholder, template_variable)
				log_debug_event("Formatted Config Command: "+formatted_config_command,"format_output")
				formatted_config_commands.append(formatted_config_command)
	formatted_config_commands += get_output_file_footer(input_filepath)
	return formatted_config_commands

#*****************************************************
#Generate Output Filepath
#*****************************************************
def get_template_subdir(input_filepath):
	return input_filepath.split("/")[-2].strip()

#*****************************************************
#Generate Output Filepath
#*****************************************************
def generate_output_filepath(input_filepath):
	return output_dir+get_template_subdir(input_filepath)+"/"+os.path.basename(input_filepath)

#*****************************************************
#Write Output to file
#*****************************************************
def func_write_to_file(input_filepath, formatted_output):
	output_filepath = generate_output_filepath(input_filepath)
	log_event("Writing Output File ("+output_filepath+") for Input File ("+input_filepath+")", False)
	os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
	
	try:
		with open(output_filepath, "w") as output_file:
			for command_line in formatted_output:
				output_file.write(command_line+new_line)
	except Exception as e:
		log_event("An error occurred: {"+str(e)+"}")

	log_event("File Write Complete '"+output_filepath+"'")


#*****************************************************
#Process Input Config File and Create Output Config File
#*****************************************************
def process_input_cfg(input_filepath, config_object_mapping):
	#Search, Format and Write
	raw_output = func_find_config_objects(input_filepath, config_object_mapping)
	formatted_output = format_output(input_filepath, raw_output, config_object_mapping)
	func_write_to_file(input_filepath, formatted_output)


#*****************************************************
#Process Input Directory
#*****************************************************
def process_directory(directory_path, config_object_mapping):
	try:
		log_debug_event("Processing Directory : " + directory_path,'process_directory')
		for dirpath, dirnames, filenames in os.walk(directory_path):
			log_debug_event("dirpath: "+ str(dirpath), 'process_directory')
			for filename in filenames:
				if filename.endswith(".cfg"):
					log_debug_event("filepath: "+str(dirpath)+"/"+str(filename), 'process_directory')
					filepath = str(dirpath)+"/"+str(filename)
					process_input_cfg(filepath, config_object_mapping)
	except FileNotFoundError:
		log_event("Error: Directory not found: '"+directory_path+"'")
	except Exception as e:
		log_event("An error occurred: {"+str(e)+"}")
				
				

#=================================================================================
#=================================================================================
#Start of Main Program
#=================================================================================
#=================================================================================
spacer = func_spacer()
print(spacer)

log_event("Start of App - version "+version)
start = timer()
start_time = datetime.strftime(datetime.today(), date_format)
log_event("Start Time: " + start_time)

log_event("System Arguments", False)
log_event(sys.argv)

#Check to see if Debug flagged
if(len(sys.argv) > 3):
	if(sys.argv[3] == "-debug"):
		log_event("Debug Flag Enabled")
		debug_flag = True

#Retrieve Input File Name via Sys Argv or User Input
if(len(sys.argv) > 1):
	if(sys.argv[1] == "-input-dir"):
		if (check_dir(sys.argv[2])):
			input_dir = sys.argv[2]
		else:
			log_event("[Error] input_dir defined via System Arguments not found:  "+sys.argv[2], False)
			input_dir = prompt_for_input_dir()
		log_event("input_dir defined via System Arguments:  "+input_dir, False)
else:
	input_dir = prompt_for_input_dir()
	log_event("input_dir defined via User Input:  "+input_dir, False)

#Define Input Directory
log_event("Input Directory: '" + input_dir+"'")

#Ingest Configuration Objects & Show to screen
log_event("Ingesting Config Objects")
config_object_mapping = func_ingest_config_objects(config_object_file)
show_config_objects_mapping(config_object_mapping)

#Process Directory
process_directory(input_dir, config_object_mapping)

#Finish and End App
end = timer()
end_time = datetime.strftime(datetime.today(), date_format)
log_event("End Time: " + end_time)
log_event("Time Elapased: " + str(timedelta(seconds=end-start).total_seconds()) + " seconds")
log_event("Output Configuration File(s) written to "+output_dir)
log_event("End of App")
print(spacer)