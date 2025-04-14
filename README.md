# Config Mapper
Last Updated On April 10th, 2025

Configuration Mapper that will take a local configuration and extract and replace with mapped configuration. 

## Test Environment
Tested on Python 3.9.6
Tested with configuration file of 2,741 lines

## Known Issues.
1. Overlapping Configuration Objects - Possible Duplication in Output of command lines if matches on multiple configuration objects in ```_output\output_config.cfg```

## Actions Performed

1. Search through Local Configurations located in ```input_directory``` for configuration objects found in [```config_object_mapping.txt```](config_object_mapping.txt)
1. Maps the configuration by replacing ```<local_config>``` with ```<mapped_config>``` within all files (*.cfg) defined in ```input_directory```
1. Uses the sub-folder of the filepath for ```TEMPLATE_VAR``` declared in ```config_object_mapping.txt```](config_object_mapping.txt)
1. Provides a File formatted for ingestion can be found in [```_output/```](_output/readme) in subdirectories similar to input

 
## Download Script
```
git clone https://github.com/jonhurtt/cfg-mapper.git
```

## Change permissions for script
```
chmod +x config_mapper.py
```

## Retrieving Local Configuration on PAN-OS Devices

SSH and Authenticate to the Device & Change to Set Output Format
```
set cli config-output-format set
```
Disable Pager to Off
```
set cli pager off
```
Navigate to Configuration
```
configure
```
Run Show Command to capture local configuration
```
show
```

All Commands to gather local configuration.
```
set cli config-output-format set
set cli pager off
configure
show
```
## Define Configuration Objects 

Make definitions in [```config_object_mapping.txt```](config_object_mapping.txt)

```
#=============================================================================
#Example List of Configuration Objects to Search for, a space will be appended at end of each command
#Syntax: <local_config>, <mapped_config>
#Use Variable of TEMPLATE_VAR for dynamic creation of variables based on folder structure.
#=============================================================================
#set deviceconfig, set template TEMPLATE_VAR config deviceconfig
#set address, set shared address
```

## Determining Local to Mapped

Using existing environments 

Getting Local Configuration 
```
set cli config-output-format set
configure
show zone
```

Example output of Local Config
```
show zone
set zone L3-100-NET-Lab network layer3 ethernet1/2
set zone L3-100-NET-Lab enable-user-identification yes
```

Getting Mapped Configuration
```
set cli config-output-format set
configure
show | match 'zone '
```
Note the trailing space will reduce the number matches, inspect configuration and find command.

Example output of Mapped Config
```
set template lab-template config vsys vsys1 zone L3-100-NET-Lab network layer3 ethernet1/2
set template lab-template config vsys vsys1 zone L3-100-NET-Lab enable-user-identification yes
```

Proper Local to Mapped Declaration in [```config_object_mapping.txt```](config_object_mapping.txt)
```
set zone, set template TEMPLATE_VAR config vsys vsys1 zone
```

## Execute Script
```
./config_mapper.py [ -input-dir <input_directory> -debug ]
```

### Example of execution of script. 
```
./config_mapper.py -input-dir _input
```

### Example Terminal Output (Recommended)
```
./config_mapper.py -input-dir _input > _terminal_output.txt    
```

```
================================================================================
15:02.30.080881 PM: Start of App - version 2.0
================================================================================
15:02.30.080899 PM: Start Time: Monday, April 14, 2025 @ 15:02.30
================================================================================
15:02.30.080902 PM: System Arguments
15:02.30.080905 PM: ['./config_mapper.py', '-input-dir', '_input']
================================================================================
15:02.30.080914 PM: input_dir defined via System Arguments:  _input
15:02.30.080918 PM: Input Directory: '_input'
================================================================================
15:02.30.080920 PM: Ingesting Config Objects
================================================================================
15:02.30.081166 PM: Displaying Configuration Object Mappings

'set network virtual-router' mapped to 'set template TEMPLATE_VAR config network virtual-router'
'set network interface' mapped to 'set template TEMPLATE_VAR config network interface'
'set zone' mapped to 'set template TEMPLATE_VAR config vsys vsys1 zone'
'set network dhcp interface' mapped to 'set template TEMPLATE_VAR config network dhcp interface'
================================================================================
15:02.30.081249 PM: Opening _input/template-001/device-config-02.cfg...
15:02.30.081252 PM: Searching _input/template-001/device-config-02.cfg...
================================================================================
15:02.30.089164 PM: set network virtual-router --> Found in 37 line(s)
15:02.30.097029 PM: set network interface --> Found in 89 line(s)
15:02.30.104371 PM: set zone --> Found in 40 line(s)
15:02.30.111739 PM: set network dhcp interface --> Found in 9 line(s)
================================================================================
15:02.30.111747 PM: Input File Line Count: 2,751 configuration lines.
15:02.30.111751 PM: Configurations Found: 175 line(s).
15:02.30.111754 PM: Completed Search of _input/template-001/device-config-02.cfg...
================================================================================
15:02.30.114386 PM: Writing Output File for Input File '_input/template-001/device-config-02.cfg'
15:02.30.114819 PM: File Write Complete '_output/template-001/formatted-device-config-02.cfg'
================================================================================
....
================================================================================
15:02.30.210727 PM: Total Config Lines Processed: 11,004 line(s).
15:02.30.210731 PM: Total Number of Configurations Found: 700 line(s).
================================================================================
15:02.30.210736 PM: End Time: Monday, April 14, 2025 @ 15:02.30
================================================================================
15:02.30.210744 PM: Time Elapsed: 0.129839 seconds
================================================================================
15:02.30.210747 PM: Output Configuration File(s) written to _output/
================================================================================
15:02.30.210749 PM: End of App
================================================================================
================================================================================

```


### Example To show Debug Commands
```
./config_mapper.py -input-dir _input -debug
```

### Send all output to debug file (Recommended for Troubleshooting)
```
./config_mapper.py -input-dir _input -debug > _debug_output.txt
```

```
================================================================================
15:03.58.320215 PM: Start of App - version 2.0
================================================================================
15:03.58.320244 PM: Start Time: Monday, April 14, 2025 @ 15:03.58
================================================================================
15:03.58.320247 PM: System Arguments
15:03.58.320250 PM: ['./config_mapper.py', '-input-dir', '_input', '-debug']
================================================================================
15:03.58.320254 PM: Debug Flag Enabled
================================================================================
15:03.58.320263 PM: input_dir defined via System Arguments:  _input
15:03.58.320266 PM: Input Directory: '_input'
================================================================================
15:03.58.320269 PM: Ingesting Config Objects
================================================================================
15:03.58.320475 PM: [*** debug ***][func_ingest_config_objects]set network virtual-router, set template TEMPLATE_VAR config network virtual-router
15:03.58.320481 PM: [*** debug ***][func_ingest_config_objects]set network interface, set template TEMPLATE_VAR config network interface
15:03.58.320485 PM: [*** debug ***][func_ingest_config_objects]set zone, set template TEMPLATE_VAR config vsys vsys1 zone
15:03.58.320491 PM: [*** debug ***][func_ingest_config_objects]set network dhcp interface, set template TEMPLATE_VAR config network dhcp interface
15:03.58.320512 PM: Displaying Configuration Object Mappings

'set network virtual-router' mapped to 'set template TEMPLATE_VAR config network virtual-router'
'set network interface' mapped to 'set template TEMPLATE_VAR config network interface'
'set zone' mapped to 'set template TEMPLATE_VAR config vsys vsys1 zone'
'set network dhcp interface' mapped to 'set template TEMPLATE_VAR config network dhcp interface'
================================================================================
15:03.58.320523 PM: [*** debug ***][process_directory]Processing Directory : _input
15:03.58.320571 PM: [*** debug ***][process_directory]dirpath: _input
15:03.58.320614 PM: [*** debug ***][process_directory]dirpath: _input/template-001
15:03.58.320618 PM: [*** debug ***][process_directory]filepath: _input/template-001/device-config-02.cfg
15:03.58.320622 PM: Opening _input/template-001/device-config-02.cfg...
15:03.58.320624 PM: Searching _input/template-001/device-config-02.cfg...
================================================================================
...
15:03.58.468464 PM: Writing Output File for Input File '_input/template-002/device-config-03.cfg'
15:03.58.468738 PM: File Write Complete '_output/template-002/formatted-device-config-03.cfg'
================================================================================
15:03.58.468748 PM: Total Config Lines Processed: 11,004 line(s).
15:03.58.468752 PM: Total Number of Configurations Found: 700 line(s).
================================================================================
15:03.58.468758 PM: End Time: Monday, April 14, 2025 @ 15:03.58
================================================================================
15:03.58.468767 PM: Time Elapsed: 0.148515 seconds
================================================================================
15:03.58.468770 PM: Output Configuration File(s) written to _output/
================================================================================
15:03.58.468772 PM: End of App
================================================================================
================================================================================

```


## Example Output 

Located at ```_output\<TEMPLATE_VAR>\formatted-<input_filename>.cfg```
```
#================================================================================
# Time Created: Monday, April 14, 2025 @ 15:03.58
# ./config_mapper.py - Formatted configuration from _input/template-001/device-config-01.cfg
# Template Variable template-001
# Command Mappings
#{'local': 'set network virtual-router', 'mapped': 'set template TEMPLATE_VAR config network virtual-router'}
#{'local': 'set network interface', 'mapped': 'set template TEMPLATE_VAR config network interface'}
#{'local': 'set zone', 'mapped': 'set template TEMPLATE_VAR config vsys vsys1 zone'}
#{'local': 'set network dhcp interface', 'mapped': 'set template TEMPLATE_VAR config network dhcp interface'}
#================================================================================
#================================================================================
#'set network virtual-router' mapped to 'set template TEMPLATE_VAR config network virtual-router'
#================================================================================

...

#================================================================================
# ./config_mapper.py  - Formatted configuration from _input/template-001/device-config-01.cfg
# Time Completed: Monday, April 14, 2025 @ 15:03.58
#================================================================================

```

##   Load Configuration

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