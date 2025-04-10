# Config Mapper
Configuration Mapper that will take a local configuration and extract and replace with mapped configuration. 

Last Updated On April 10th, 2025

## Test Environment
Tested on Python 3.9.6
Tested with configuration file of 2,741 lines

## Known Issues.
1. Possible Duplication in Output of command lines if matches on multiple configuration objects in ```_output\output_config.cfg```

## Actions Performed

1. Will Search through Local Configurations for configuration objects found in [```config_object_mapping.txt```](config_object_mapping.txt)
1. Will Map the configuration by replacing ```<local_config>``` with ```<mapped_config>``` within all files (*.cfg) defined in ```input_directory```
1. Will use the sub-folder of the filepath for ```TEMPLATE_VAR``` declared in ```config_object_mapping.txt```](config_object_mapping.txt)
1. Will Provide a File formatted for ingestion can be found in [```_output/```](_output/readme) in subdirectories similar to input

 
## Download Script
```
git clone https://github.com/jonhurtt/cfg-mapper.git
```

## Change permissions for script
```
chmod +x config_mapper.py
```

## Retrieving Local Configuration on PAN-OS Devices
### SSH and Authenticate to the Device & Change to Set Output Format
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
#=============================================================================
#Example List of Configuration Objects to Search for, a space will be appended at end of each command
#Syntax: <local_config>, <mapped_config>
#Use Variable of TEMPLATE_VAR for dynamic creation of variables based on folder structure.
#=============================================================================
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
12:36.20.840682 PM: Start of App - version 2.0
======================================================================================================================================================
12:36.20.840703 PM: Start Time: Thursday, April 10, 2025 @ 12:36.20
======================================================================================================================================================
12:36.20.840708 PM: System Arguments
12:36.20.840712 PM: ['./config_mapper.py', '-input-dir', '_input']
======================================================================================================================================================
12:36.20.840724 PM: input_dir defined via System Arguments:  _input
12:36.20.840730 PM: Input Directory: '_input'
======================================================================================================================================================
12:36.20.840733 PM: Ingesting Config Objects
======================================================================================================================================================
12:36.20.841055 PM: Displaying Configuration Object Mappings

'set network virtual-router' mapped to 'set template TEMPLATE_VAR config network virtual-router'
'set network interface' mapped to 'set template TEMPLATE_VAR config network interface'
'set zone' mapped to 'set template TEMPLATE_VAR config vsys vsys1 zone'
'set network dhcp interface' mapped to 'set template TEMPLATE_VAR config network dhcp interface'
======================================================================================================================================================
12:36.20.841273 PM: Opening _input/template-001/device-config-02.cfg...
12:36.20.841277 PM: Searching _input/template-001/device-config-02.cfg...
12:36.20.851767 PM: set network virtual-router --> Found in 37 line(s)
12:36.20.861519 PM: set network interface --> Found in 89 line(s)
12:36.20.869994 PM: set zone --> Found in 40 line(s)
12:36.20.877630 PM: set network dhcp interface --> Found in 9 line(s)
12:36.20.877633 PM: Completed Search of _input/template-001/device-config-02.cfg...
======================================================================================================================================================
12:36.20.880329 PM: Writing Output File (_output/template-001/device-config-02.cfg) for Input File (_input/template-001/device-config-02.cfg)
12:36.20.881044 PM: File Write Complete '_output/template-001/device-config-02.cfg'
======================================================================================================================================================
....
======================================================================================================================================================
12:36.20.977313 PM: End Time: Thursday, April 10, 2025 @ 12:36.20
======================================================================================================================================================
12:36.20.977321 PM: Time Elapsed: 0.136613 seconds
======================================================================================================================================================
12:36.20.977323 PM: Output Configuration File(s) written to _output/
======================================================================================================================================================
12:36.20.977326 PM: End of App
======================================================================================================================================================
======================================================================================================================================================

```


### example To show Debug Commands
```
./config_mapper.py -input-dir _input -debug
```

### Send all output to debug file (Recommended for Troubleshooting)
```
./config_mapper.py -input-dir _input -debug > _debug_output.txt
```

```
======================================================================================================================================================
12:36.22.127618 PM: Start of App - version 2.0
======================================================================================================================================================
12:36.22.127639 PM: Start Time: Thursday, April 10, 2025 @ 12:36.22
======================================================================================================================================================
12:36.22.127644 PM: System Arguments
12:36.22.127648 PM: ['./config_mapper.py', '-input-dir', '_input', '-debug']
======================================================================================================================================================
12:36.22.127654 PM: Debug Flag Enabled
======================================================================================================================================================
12:36.22.127664 PM: input_dir defined via System Arguments:  _input
12:36.22.127669 PM: Input Directory: '_input'
======================================================================================================================================================
12:36.22.127673 PM: Ingesting Config Objects
======================================================================================================================================================
12:36.22.127723 PM: [*** debug ***][func_ingest_config_objects]set network virtual-router, set template TEMPLATE_VAR config network virtual-router
12:36.22.127732 PM: [*** debug ***][func_ingest_config_objects]set network interface, set template TEMPLATE_VAR config network interface
12:36.22.127738 PM: [*** debug ***][func_ingest_config_objects]set zone, set template TEMPLATE_VAR config vsys vsys1 zone
12:36.22.127746 PM: [*** debug ***][func_ingest_config_objects]set network dhcp interface, set template TEMPLATE_VAR config network dhcp interface
12:36.22.127770 PM: Displaying Configuration Object Mappings

'set network virtual-router' mapped to 'set template TEMPLATE_VAR config network virtual-router'
'set network interface' mapped to 'set template TEMPLATE_VAR config network interface'
'set zone' mapped to 'set template TEMPLATE_VAR config vsys vsys1 zone'
'set network dhcp interface' mapped to 'set template TEMPLATE_VAR config network dhcp interface'
======================================================================================================================================================
12:36.22.127779 PM: [*** debug ***][process_directory]Processing Directory : _input
12:36.22.127827 PM: [*** debug ***][process_directory]dirpath: _input
12:36.22.127878 PM: [*** debug ***][process_directory]dirpath: _input/template-001
12:36.22.127884 PM: [*** debug ***][process_directory]filepath: _input/template-001/device-config-02.cfg
12:36.22.127889 PM: Opening _input/template-001/device-config-02.cfg...
...
12:36.22.314632 PM: Writing Output File (_output/template-002/device-config-03.cfg) for Input File (_input/template-002/device-config-03.cfg)
12:36.22.314913 PM: File Write Complete '_output/template-002/device-config-03.cfg'
======================================================================================================================================================
12:36.22.314927 PM: End Time: Thursday, April 10, 2025 @ 12:36.22
======================================================================================================================================================
12:36.22.314935 PM: Time Elapsed: 0.187291 seconds
======================================================================================================================================================
12:36.22.314938 PM: Output Configuration File(s) written to _output/
======================================================================================================================================================
12:36.22.314941 PM: End of App
======================================================================================================================================================
======================================================================================================================================================
```


## Example Output 

Located at ```_output\<TEMPLATE_VAR>\<input_filename>.cfg```
```
#======================================================================================================================================================
# Time Created: Thursday, April 10, 2025 @ 12:36.22
# ./config_mapper.py - Formatted configuration from _input/template-001/device-config-01.cfg
# Template Variable template-001
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
# Time Completed: Thursday, April 10, 2025 @ 12:36.22
#======================================================================================================================================================
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