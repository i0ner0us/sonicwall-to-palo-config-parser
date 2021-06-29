# sonicwall-to-palo-config-parser
######################################################################################
#################################### Instructions ####################################
######################################################################################


    To execute the script the following dir structure needs to be in palce
    Mode                LastWriteTime
    ----                -------------
    Directory           ConvertedFiles
    Directory           fsmTemplates
    --file              --fsmTemplates\sonicwall_get_access_rules.template
    --file              --fsmTemplates\sonicwall_get_addressgroups.template
    --file              --fsmTemplates\sonicwall_get_addressobjects.template
    --file              --fsmTemplates\sonicwall_get_interfaces.template
    --file              --fsmTemplates\sonicwall_get_nat_policies.template
    --file              --fsmTemplates\sonicwall_get_servicegroups.template
    --file              --fsmTemplates\sonicwall_get_serviceobjects.template
    --file              --fsmTemplates\sonicwall_get_zones.template
    -File              config.conf
    -File              main.py
    run the script from powershell by using the following structure:
        python.exe .\main.py --conf_file "c:\path\to\conf\file\config.conf"
    if you do not supply the --conf_file parameter it will default to use a file in the same folder as main.py
    with a name of "config.conf". When the program is ran it will output the following files into the ConvertedFiles folder:
        ConvertedFiles\access-rules.csv
        ConvertedFiles\address-groups.csv
        ConvertedFiles\address-objects.csv
        ConvertedFiles\interfaces.csv
        ConvertedFiles\nat-policies.csv
        ConvertedFiles\service-groups.csv
        ConvertedFiles\service-objects.csv
        ConvertedFiles\zones.csv
    These files can be used to import the config into Palo Alto expedition using the csv function.


######################################################################################
#################################### Requirements ####################################
######################################################################################

