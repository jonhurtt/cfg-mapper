# Config Mapper
Conifguration Mapper that will take a local configuration and extract and replace with mapped configuration. 

Last Updated On April 10th, 2025

## Test Enviornment
Tested on Python 3.9.6
Tested with configuration file of 2,741 lines

## Known Issues.
1. Possible Duplication in Output of command lines if matches on mutiple configuration objects in ```_output\output_config.cfg```

## Actions Performed

1. Will Search through Local Configurations for configuration objects found in [```config_object_mapping.txt```](config_object_mapping.txt)
1. Will Map the configuration by replacing ```<local_config>``` with ```<mapped_config>``` within all files (*.cfg) defined in ```input_directory```
1. Will use the sub-folder of the filepath for ```TEMPLATE_VAR``` declared in ```config_object_mapping.txt```](config_object_mapping.txt)
1. Will Provide a File formated for ingestion can be found in [```_output/```](_output/readme) in subdirecotries similar to input

 
## Download Script
```
git clone https://github.com/jonhurtt/eol-template-generator.git
```

## Change permissions for script
```
chmod +x config_mapper.py
```

## Retrieving Local Configuration on PAN-OS Devices
### SSH and Authenciate to the Device & Change to Set Output Format
```
set cli config-output-format set
```
### Disable Pager to Off
```
set cli pager off
```
### Navigate to Configuration
```
configure
```
### Run Show Command to capture local configuration
```
show
```

### All Commands to gather local configuration.
```
set cli config-output-format set
set cli pager off
configure
show
```
## Define Configuration Objects 

Make definitions in [```config_object_mapping.txt```](config_object_mapping.txt)

```
#Example List of Configuration Objects to Search for, a space will be appended at end of each command
#Synatx: <local_config>, <mapped_config>
```

## Execute Script
```
./config_mapper.py [ -input-dir <filename> -debug ]
```

### example of execution of script. 
```
./config_mapper.py -input-dir _input
```

### Example Terminal Output (Recommended)
```
./config_mapper.py -input-dir _input > _terminal_output.txt    
```

```
======================================================================================================================================================
11:50.38.125660 AM: Start of App - version 2.0
======================================================================================================================================================
11:50.38.125681 AM: Start Time: Thursday, April 10, 2025 @ 11:50.38
======================================================================================================================================================
11:50.38.125685 AM: System Arguments
11:50.38.125689 AM: ['./config_mapper.py', '-input-dir', '_input']
======================================================================================================================================================
11:50.38.125700 AM: input_dir defined via System Arguments:  _input
11:50.38.125705 AM: Input Directory: '_input'
======================================================================================================================================================
11:50.38.125709 AM: Ingesting Config Objects
======================================================================================================================================================
11:50.38.125960 AM: Displaying Configuration Object Mappings

'set network virtual-router' mapped to 'set template TEMPLATE_VAR config network virtual-router'
'set network interface' mapped to 'set template TEMPLATE_VAR config network interface'
'set zone' mapped to 'set template TEMPLATE_VAR config vsys vsys1 zone'
'set network dhcp interface' mapped to 'set template TEMPLATE_VAR config network dhcp interface'
======================================================================================================================================================
11:50.38.126076 AM: Opening _input/template-001/device-config-02.cfg...
11:50.38.126080 AM: Searching _input/template-001/device-config-02.cfg...
11:50.38.135862 AM: set network virtual-router --> Found in 37 line(s)
11:50.38.144968 AM: set network interface --> Found in 89 line(s)
11:50.38.153153 AM: set zone --> Found in 40 line(s)
11:50.38.160578 AM: set network dhcp interface --> Found in 9 line(s)
11:50.38.160581 AM: Completed Search of _input/template-001/device-config-02.cfg...
======================================================================================================================================================
11:50.38.163193 AM: Writing Output File (_output/template-001/device-config-02.cfg) for Input File (_input/template-001/device-config-02.cfg)
11:50.38.163821 AM: File Write Complete _output/template-001/device-config-02.cfg;
======================================================================================================================================================
....
======================================================================================================================================================
11:50.38.258622 AM: End Time: Thursday, April 10, 2025 @ 11:50.38
======================================================================================================================================================
11:50.38.258630 AM: Time Elapased: 0.132942 seconds
======================================================================================================================================================
11:50.38.258632 AM: Output Configuration File(s) written to _output/
======================================================================================================================================================
11:50.38.258635 AM: End of App
======================================================================================================================================================
======================================================================================================================================================

```


### example To show Debug Commands
```
./config_mapper.py -input-dir _input -debug
```

### Send all output to debug file (Recommended for Troublshooting)
```
./config_mapper.py -input-dir _input -debug > _debug_output.txt
```

```
======================================================================================================================================================
11:50.40.380145 AM: Start of App - version 2.0
======================================================================================================================================================
11:50.40.380166 AM: Start Time: Thursday, April 10, 2025 @ 11:50.40
======================================================================================================================================================
11:50.40.380171 AM: System Arguments
11:50.40.380175 AM: ['./config_mapper.py', '-input-dir', '_input', '-debug']
======================================================================================================================================================
11:50.40.380181 AM: Debug Flag Enabled
======================================================================================================================================================
11:50.40.380195 AM: input_dir defined via System Arguments:  _input
11:50.40.380200 AM: Input Directory: '_input'
======================================================================================================================================================
11:50.40.380204 AM: Ingesting Config Objects
======================================================================================================================================================
11:50.40.380260 AM: [*** debug ***][func_ingest_config_objects]set network virtual-router, set template TEMPLATE_VAR config network virtual-router
11:50.40.380269 AM: [*** debug ***][func_ingest_config_objects]set network interface, set template TEMPLATE_VAR config network interface
11:50.40.380275 AM: [*** debug ***][func_ingest_config_objects]set zone, set template TEMPLATE_VAR config vsys vsys1 zone
11:50.40.380283 AM: [*** debug ***][func_ingest_config_objects]set network dhcp interface, set template TEMPLATE_VAR config network dhcp interface
11:50.40.380309 AM: Displaying Configuration Object Mappings

'set network virtual-router' mapped to 'set template TEMPLATE_VAR config network virtual-router'
'set network interface' mapped to 'set template TEMPLATE_VAR config network interface'
'set zone' mapped to 'set template TEMPLATE_VAR config vsys vsys1 zone'
'set network dhcp interface' mapped to 'set template TEMPLATE_VAR config network dhcp interface'
======================================================================================================================================================
11:50.40.380318 AM: [*** debug ***][process_directory]Processing Directory : _input
11:50.40.380378 AM: [*** debug ***][process_directory]dirpath: _input
11:50.40.380429 AM: [*** debug ***][process_directory]dirpath: _input/template-001
11:50.40.380435 AM: [*** debug ***][process_directory]filepath: _input/template-001/device-config-02.cfg
11:50.40.380440 AM: Opening _input/template-001/device-config-02.cfg...
11:50.40.380444 AM: Searching _input/template-001/device-config-02.cfg...
11:50.40.380448 AM: [*** debug ***][func_find_config_objects][config_object search] set network virtual-router
11:50.40.380489 AM: [*** debug ***][func_find_config_objects][searching for set network virtual-router in 'set deviceconfig system ip-address 192.168.47.20']
11:50.40.380495 AM: [*** debug ***][func_find_config_objects][searching for set network virtual-router in 'set deviceconfig system netmask 255.255.255.0']
...
11:50.40.532243 AM: File Write Complete _output/template-002/device-config-03.cfg;
======================================================================================================================================================
11:50.40.532258 AM: End Time: Thursday, April 10, 2025 @ 11:50.40
======================================================================================================================================================
11:50.40.532267 AM: Time Elapased: 0.152095 seconds
======================================================================================================================================================
11:50.40.532270 AM: Output Configuration File(s) written to _output/
======================================================================================================================================================
11:50.40.532272 AM: End of App
======================================================================================================================================================
======================================================================================================================================================
```


## Example Output 
### Located at ```_output\output_config.cfg```
```
#======================================================================================================================================================
# Time Created: Thursday, April 10, 2025 @ 11:50.40
# ./config_mapper.py - Formatted configuration from _input/template-001/device-config-01.cfg
# Command Mappings
#{'local': 'set network virtual-router', 'mapped': 'set template TEMPLATE_VAR config network virtual-router'}
#{'local': 'set network interface', 'mapped': 'set template TEMPLATE_VAR config network interface'}
#{'local': 'set zone', 'mapped': 'set template TEMPLATE_VAR config vsys vsys1 zone'}
#{'local': 'set network dhcp interface', 'mapped': 'set template TEMPLATE_VAR config network dhcp interface'}
#======================================================================================================================================================
#======================================================================================================================================================
#'set network virtual-router' mapped to 'set template TEMPLATE_VAR config network virtual-router'
#======================================================================================================================================================

...

#======================================================================================================================================================
# ./config_mapper.py  - Formatted configuration from _input/template-001/device-config-01.cfg
# Time Completed: Thursday, April 10, 2025 @ 11:50.40
#======================================================================================================================================================
```

##  Load Configuratoin

### Via SSH on Panorama enable scripting mode
```
set cli scripting-mode on
```
### Paste Output into SSH Terminal to load configuration on to device

### Via SSH on Panorama enable scripting mode
```
commit
```

[/end]