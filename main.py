import textfsm, sys, argparse

inFileName = 'config.conf'
inFile=open(inFileName, 'r')
confFile=inFile.read()
inFile.close()

def writeToCSV(fileName,fsm_results,re_table):
    # the results are written to a CSV file
    file = "ConvertedFiles\\" + str(fileName)
    outfile_name = open(file, "w+")
    outfile = outfile_name

    # Display result as CSV and write it to the output file
    # First the column headers...
    print(re_table.header)
    for s in re_table.header:
        outfile.write("%s;" % s)
    outfile.write("\n")

    # ...now all row's which were parsed by TextFSM
    counter = 0
    for row in fsm_results:
        print(row)
        for s in row:
            outfile.write("%s;" % s)
        outfile.write("\n")
        counter += 1
    print("Write %d records" % counter)

def getAddressGroups(confFile):
    # open up the raw data from the config file and search through it using a textfsm template
    # this will then put the data in the below format using an array
    # name,members
    template = open("fsmTemplates\sonicwall_get_addressgroups.template")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(confFile)

    # Because this requires a different format then the normal csv format we will have to customize this a little bit
    # to be sure the format of the csv looks like the following (members seperated by commas)
    # GroupName;Member1,Member2,Member3;
    fileName = 'address-groups.csv'

    # the results are written to a CSV file
    file = "ConvertedFiles\\" + str(fileName)
    outfile_name = open(file, "w+")
    outfile = outfile_name

    # Display result as CSV and write it to the output file
    # First the column headers...
    for s in re_table.header:
        outfile.write("%s;" % s)
    outfile.write("\n")

    # ...now all row's which were parsed by TextFSM
    # this output takes all the members of the address grouo and
    # ouputs them eith a comma inbetween. when it gets to the last object
    # it writes the object without a comma.
    counter = 0
    for row in fsm_results:
        print(row)
        outfile.write(row[0] + ";")
        if len(row[1])>0:
            lastItemInList=row[1][-1]
        else:
            lastItemInList=''
        print(lastItemInList)
        for s in row[1]:
            if s == lastItemInList:
                outfile.write("%s" % s)
            else:
                outfile.write("%s," % s)

        outfile.write("\n")
        counter += 1
    print("Write %d records" % counter)

def getAddressObjects(confFile):
    # open up the raw data from the config file and search through it using a textfsm template
    # this will then put the data in the below format using an array
    # name,type,host_ip,netmask,start_IP,end_iP,zone

    template = open("fsmTemplates\sonicwall_get_addressobjects.template")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(confFile)

    for row in fsm_results:

        # convert the data before we write to CSV
        # data format is name,zone,type,network,netmask,start_ip,end_iP
        obj_type = row[2]
        name = row[0]
        quoteInName = "\""

        # replace any quotes in the name that might have come from the config output
        row[0] = row[0].replace('"','')

        if obj_type == "host":
            # PA does not suport host objects
            # we must convert this to a network object and place a /32 netmask
            # this will be the equivalant of a host object
            row[2] = "network"
            row[4] = "255.255.255.255"
        elif obj_type == "network":
            pass
        elif obj_type == "range":
            # move the startIP and endIP to the correct columns becuase the match statements
            # matched the same as the network
            row[5] = str(row[3])
            row[6] = str(row[4])
            row[3] = ""
            row[4] = ""
        else:
            pass

    writeToCSV('address-objects.csv', fsm_results, re_table)

def getInterfaces(confFile):
    # open up the raw data from the config file and search through it using a textfsm template
    # this will then put the data in the below format using an array
    # name,zone,ip,netmask,gateway,desc
    template = open("fsmTemplates\sonicwall_get_interfaces.template")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(confFile)

    fileName = 'interfaces.csv'

    # the results are written to a CSV file
    file = "ConvertedFiles\\" + str(fileName)
    outfile_name = open(file, "w+")
    outfile = outfile_name

    # Display result as CSV and write it to the output file
    # First the column headers...
    header = ['INTERFACE_NAME', 'ZONE', 'IP_ADDRESS', 'NETMASK', 'GATEWAY', 'DESCRIPTION','MEDIA']
    print(header)
    for s in header:
        outfile.write("%s;" % s)
    outfile.write("\n")

    # ...now all row's which were parsed by TextFSM
    counter = 0
    for row in fsm_results:
        row.append('ethernet')
        print(row)
        for s in row:
            outfile.write("%s;" % s)
        outfile.write("\n")
        counter += 1
    print("Write %d records" % counter)

def getZones(confFile):
    # open up the raw data from the config file and search through it using a textfsm template
    # this will then put the data in the below format using an array
    # zone
    template = open("fsmTemplates\sonicwall_get_zones.template")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(confFile)

    fileName = 'zones.csv'

    # the results are written to a CSV file
    file = "ConvertedFiles\\" + str(fileName)
    outfile_name = open(file, "w+")
    outfile = outfile_name

    # Display result as CSV and write it to the output file
    # First the column headers...
    header = ['ZONE','TYPE']
    print(header)
    for s in header:
        outfile.write("%s;" % s)
    outfile.write("\n")

    # ...now all row's which were parsed by TextFSM
    counter = 0
    for row in fsm_results:
        row.append('layer3')
        print(row)
        for s in row:
            outfile.write("%s;" % s)
        outfile.write("\n")
        counter += 1
    print("Write %d records" % counter)

def getAccessRules(confFile):
    # open up the raw data from the config file and search through it using a textfsm template
    # this will then put the data in the below format using an array
    # zone
    template = open("fsmTemplates\sonicwall_get_access_rules.template")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(confFile)

    writeToCSV('access-rules.csv',fsm_results,re_table)

def getNatPolicies(confFile):
    # open up the raw data from the config file and search through it using a textfsm template
    # this will then put the data in the below format using an array
    #
    template = open("fsmTemplates\sonicwall_get_nat_policies.template")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(confFile)

    writeToCSV('nat-policies.csv',fsm_results,re_table)

def getServiceGroups(confFile):
    # open up the raw data from the config file and search through it using a textfsm template
    # this will then put the data in the below format using an array
    # name,members
    template = open("fsmTemplates\sonicwall_get_servicegroups.template")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(confFile)


    # Because this requires a different format then the normal csv format we will have to customize this a little bit
    # to be sure the format of the csv looks like the following (members seperated by commas)
    # GroupName;Member1,Member2,Member3;
    fileName = 'service-groups.csv'

    # the results are written to a CSV file
    file = "ConvertedFiles\\" + str(fileName)
    outfile_name = open(file, "w+")
    outfile = outfile_name

    # Display result as CSV and write it to the output file
    # First the column headers...
    for s in re_table.header:
        outfile.write("%s;" % s)
    outfile.write("\n")

    # ...now all row's which were parsed by TextFSM
    # this output takes all the members of the service grouo and
    # ouputs them with a comma inbetween. when it gets to the last object
    # it writes the object without a comma.
    counter = 0
    for row in fsm_results:
        # remove all quotation marks in the objects name
        row[0] = row[0].replace('"','')

        # write the members to csv as comma seperated values
        print(row)
        outfile.write(row[0] + ";")
        if len(row[1])>0:
            lastItemInList=row[1][-1]
        else:
            lastItemInList=''
        for s in row[1]:
            # remove all the quotation marks from members
            s = s.replace('"','')

            if s == lastItemInList:
                outfile.write("%s" % s)
            else:
                outfile.write("%s," % s)

        outfile.write("\n")
        counter += 1
    print("Write %d records" % counter)

def getServiceObjects(confFile):
    # open up the raw data from the config file and search through it using a textfsm template
    # this will then put the data in the below format using an array
    # name,type,host_ip,netmask,start_IP,end_iP,zone

    template = open("fsmTemplates\sonicwall_get_serviceobjects.template")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(confFile)

    # now we need to transform the data before we write it to CSV
    # current data format is name,protocol,START_PROTO,END_PROTO,NONSTANDARD_PROTOCOL
    # we will start with migrating the start and end ports to the DESTINATION_PORT column in the correct range
    for row in fsm_results:
        if row[3] == '' or row[4] == '':
            pass
        elif row[3] == row[4]:
            row[2] = row[4]
        else:
            row[2] = str(row[3]) + '-' + str(row[4])

        # make the last two columns blank
        row.pop(4)
        row.pop(3)

    # set the filename
    fileName = 'service-objects.csv'

    # the results are written to a CSV file
    file = "ConvertedFiles\\" + str(fileName)
    outfile_name = open(file, "w+")
    outfile = outfile_name

    # print custom header because we cannot drop the re_table header like we would want:
    header = ['NAME', 'PROTOCOL', 'DESTINATION_PORT']

    # Display result as CSV and write it to the output file
    # First the column headers...
    print(header)
    for s in header:
        outfile.write("%s;" % s)
    outfile.write("\n")

    # ...now all row's which were parsed by TextFSM
    counter = 0
    for row in fsm_results:
        print(row)
        for s in row:
            outfile.write("%s;" % s)
        outfile.write("\n")
        counter += 1
    print("Write %d records" % counter)


def main():
    # run the address groups function to grab the address groups and members from the configurations
    # and export to csv
    getAddressGroups(confFile)

    # run the interface function to grab the interface configurations and export to csv
    getInterfaces(confFile)

    # run the zone function to grab the zone configurations and export them to csv
    getZones(confFile)

    # run the address object function to grab all the objects and export them to csv
    getAddressObjects(confFile)

    # run the access rules function to grab all the access policies and export them to csv
    getAccessRules(confFile)

    # run the nat policy function to grab all the nat rules and export them to CSV
    getNatPolicies(confFile)

    # run the service groups function to grab the service groups and export them to csv
    getServiceGroups(confFile)

    # run the service objects function to grab the service objects and expor thtme to csv
    getServiceObjects(confFile)

if __name__ == '__main__':
    main()
