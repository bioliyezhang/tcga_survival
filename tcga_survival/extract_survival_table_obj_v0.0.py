# -*- coding: cp936 -*-
"""
The main purpose of this script is to .

=============================
Usage: python extract_survival_table_obj_v0.0.py
-h help

-i files to processed                           *[No default value]

-p parameter file                               *[No default value]

-o prefix of output files                       [default:"output"]

-s suffix for the files to be processed         [default value "txt"]

-S output SUFFIX                                [default: "txt"]

-d sep_char within among columns                [default value '\t']

-j skip header lines                            [default value 1]
    if skip header lines = 0 indicates that there is no header line
    if skip header lines = n indicates that first n lines are header lines
    
-I input file path              [default: current folder]

-O output file path             [default: current folder]

-L unique_id length for the infile      [default value 2]

===================
input description:
input files:
1. TCGA firehose merged clinical data

======================
output files:
1. table with survival information

============================

Python & Module requirement:
Versions 2.x : 2.4 or above 
Module: No additional Python Module is required.

============================
Library file requirement:

Not Standalone version, few library file is required.

============================

External Tools requirement:

============================
command line example:

============================
versions update

"""

##Copyright
##By Liye Zhang
##Contact: bioliyezhang@gmail.com
##Compatible Python Version:2.4 or above

###Code Framework

### Specific Functions definiation
    
def specific_function(infiles):
    
    ##Section I: Generate the gene annotation dictionary
    
    cmd_records=record_command_line()  ##record the command line    
        
    for infile in infiles:
        print "Processing infile:", infile
        ##Set up infile object
        infile_obj=GeneralFile_class(infile)  ##create file obj(class)
        infile_obj.SKIP_HEADER=infile_skip    ##setup up the manual skip header if necessary
        infile_obj.SAMPLE_ID_LEN=unique_id_length  ##unique ID length
        infile_reader=infile_obj.reader_gen()  ##create the file reader to process infile
        anatomic_list = []
        
        
        ##Setup output file
        outfile_name=infile_obj.outputfilename_gen(prefix,OUTPUT_SUFFIX) ##create output file
        outfile_path=OUTPUT_PATH+"/"+outfile_name
        outfile_obj=GeneralFile_class(outfile_path)              ##create output obj
        outfile_obj.RECORD=cmd_records                           
        outfile_obj.output_handle_gen()    ##generate output handle       
        complete=0
        for row in infile_reader:    
            row_ID=row[0]
            if row_ID=="patient.clinical_cqcf.frozen_specimen_anatomic_site":
                anatomic_list=row
            if row_ID=="patient.bcr_patient_barcode":
                patient_barcode_list=row
                patient_count = len(patient_barcode_list)
                patient_survival_dict= dict()
                for index in range(patient_count):
                    patient_ID = patient_barcode_list[index]
                    patient_survival_dict[patient_ID]=["NA"]*3
                    ## number 1 will be status
                    ## number 2 will be days
            if row_ID=="patient.days_to_last_followup":
                follow_up_list=row
                complete+=1
            if row_ID=="patient.days_to_death":
                death_list=row
                complete+=1
            if row_ID=="patient.vital_status":
                status_list=row
                complete+=1
            if complete==3:
                for index in range(patient_count):
                    patient_ID = patient_barcode_list[index]
                    
                    
                    status=status_list[index]
                    if status=="alive":
                        day = follow_up_list[index]
                    elif status=="dead":
                        day= death_list[index]
                    else:
                        day="skipped"
                    if day=="NA":
                        print "incorrect paring found"
                        print "check sample", patient_ID
                        print "round0"
                        #sys.exit(0)
                    elif day=="skipped":
                        pass
                    else:
                        patient_survival_dict[patient_ID][0]=status
                        patient_survival_dict[patient_ID][1]=day
                        patient_survival_dict[patient_ID][2]="0"
                break

        ## round2
        infile_obj=GeneralFile_class(infile)  ##create file obj(class)
        infile_obj.SKIP_HEADER=infile_skip    ##setup up the manual skip header if necessary
        infile_obj.SAMPLE_ID_LEN=unique_id_length  ##unique ID length
        infile_reader=infile_obj.reader_gen() ##generate output handle       
        complete=0
        for row in infile_reader:    
            row_ID=row[0]
            if row_ID=="patient.follow_ups.follow_up.days_to_last_followup":
                follow_up_list=row
                complete+=1
            if row_ID=="patient.follow_ups.follow_up.days_to_death":
                death_list=row
                complete+=1
            if row_ID=="patient.follow_ups.follow_up.vital_status":
                status_list=row
                complete+=1
            if complete==3:
                for index in range(patient_count):
                    patient_ID = patient_barcode_list[index]
                    
                    
                    status=status_list[index]
                    if status=="alive":
                        day = follow_up_list[index]
                    elif status=="dead":
                        day= death_list[index]
                    else:
                        day="skipped"
                    
                    if day=="NA":
                        print "incorrect paring found"
                        print "check sample", patient_ID
                        print "round1"
                        #sys.exit(0)
                    elif day=="skipped":
                        pass
                    else:
                        patient_survival_dict[patient_ID][0]=status
                        patient_survival_dict[patient_ID][1]=day
                        patient_survival_dict[patient_ID][2]="1"
                break

        ## round3
        infile_obj=GeneralFile_class(infile)  ##create file obj(class)
        infile_obj.SKIP_HEADER=infile_skip    ##setup up the manual skip header if necessary
        infile_obj.SAMPLE_ID_LEN=unique_id_length  ##unique ID length
        infile_reader=infile_obj.reader_gen() ##generate output handle       
        complete=0
        for row in infile_reader:    
            row_ID=row[0]
            if row_ID=="patient.follow_ups.follow_up-2.days_to_last_followup":
                follow_up_list=row
                complete+=1
            if row_ID=="patient.follow_ups.follow_up-2.days_to_death":
                death_list=row
                complete+=1
            if row_ID=="patient.follow_ups.follow_up-2.vital_status":
                status_list=row
                complete+=1
            if complete==3:
                for index in range(patient_count):
                    patient_ID = patient_barcode_list[index]
                    status=status_list[index]
                    if status=="alive":
                        day = follow_up_list[index]
                    elif status=="dead":
                        day= death_list[index]
                    else:
                        day="skipped"
                    
                    if day=="NA":
                        print "incorrect paring found"
                        print "check sample", patient_ID
                        print "round2"
                        #sys.exit(0)
                    elif day=="skipped":
                        pass
                    else:
                        patient_survival_dict[patient_ID][0]=status
                        patient_survival_dict[patient_ID][1]=day
                        patient_survival_dict[patient_ID][2]="2"
                break


        ## round4
        infile_obj=GeneralFile_class(infile)  ##create file obj(class)
        infile_obj.SKIP_HEADER=infile_skip    ##setup up the manual skip header if necessary
        infile_obj.SAMPLE_ID_LEN=unique_id_length  ##unique ID length
        infile_reader=infile_obj.reader_gen() ##generate output handle       
        complete=0
        for row in infile_reader:    
            row_ID=row[0]
            if row_ID=="patient.follow_ups.follow_up-3.days_to_last_followup":
                follow_up_list=row
                complete+=1
            if row_ID=="patient.follow_ups.follow_up-3.days_to_death":
                death_list=row
                complete+=1
            if row_ID=="patient.follow_ups.follow_up-3.vital_status":
                status_list=row
                complete+=1
            if complete==3:
                for index in range(patient_count):
                    patient_ID = patient_barcode_list[index]
                    status=status_list[index]
                    if status=="alive":
                        day = follow_up_list[index]
                    elif status=="dead":
                        day= death_list[index]
                    else:
                        day="skipped"
                    
                    if day=="NA":
                        print "incorrect paring found"
                        print "check sample", patient_ID
                        print "round3"
                        #sys.exit(0)
                    elif day=="skipped":
                        pass
                    else:
                        patient_survival_dict[patient_ID][0]=status
                        patient_survival_dict[patient_ID][1]=day
                        patient_survival_dict[patient_ID][2]="3"
                break


        ## round5
        infile_obj=GeneralFile_class(infile)  ##create file obj(class)
        infile_obj.SKIP_HEADER=infile_skip    ##setup up the manual skip header if necessary
        infile_obj.SAMPLE_ID_LEN=unique_id_length  ##unique ID length
        infile_reader=infile_obj.reader_gen() ##generate output handle       
        complete=0
        for row in infile_reader:    
            row_ID=row[0]
            if row_ID=="patient.follow_ups.follow_up-4.days_to_last_followup":
                follow_up_list=row
                complete+=1
            if row_ID=="patient.follow_ups.follow_up-4.days_to_death":
                death_list=row
                complete+=1
            if row_ID=="patient.follow_ups.follow_up-4.vital_status":
                status_list=row
                complete+=1
            if complete==3:
                for index in range(patient_count):
                    patient_ID = patient_barcode_list[index]
                    status=status_list[index]
                    if status=="alive":
                        day = follow_up_list[index]
                    elif status=="dead":
                        day= death_list[index]
                    else:
                        day="skipped"
                    
                    if day=="NA":
                        print "incorrect paring found"
                        print "check sample", patient_ID
                        print "round4"
                        #sys.exit(0)
                    elif day=="skipped":
                        pass
                    else:
                        patient_survival_dict[patient_ID][0]=status
                        patient_survival_dict[patient_ID][1]=day
                        patient_survival_dict[patient_ID][2]="4"
                break

        ## round6
        infile_obj=GeneralFile_class(infile)  ##create file obj(class)
        infile_obj.SKIP_HEADER=infile_skip    ##setup up the manual skip header if necessary
        infile_obj.SAMPLE_ID_LEN=unique_id_length  ##unique ID length
        infile_reader=infile_obj.reader_gen() ##generate output handle       
        complete=0
        for row in infile_reader:    
            row_ID=row[0]
            if row_ID=="patient.follow_ups.follow_up-5.days_to_last_followup":
                follow_up_list=row
                complete+=1
            if row_ID=="patient.follow_ups.follow_up-5.days_to_death":
                death_list=row
                complete+=1
            if row_ID=="patient.follow_ups.follow_up-5.vital_status":
                status_list=row
                complete+=1
            if complete==3:
                for index in range(patient_count):
                    patient_ID = patient_barcode_list[index]
                    status=status_list[index]
                    if status=="alive":
                        day = follow_up_list[index]
                    elif status=="dead":
                        day= death_list[index]
                    else:
                        day="skipped"
                    
                    if day=="NA":
                        print "incorrect paring found"
                        print "check sample", patient_ID
                        print "round5"
                        #sys.exit(0)
                    elif day=="skipped":
                        pass
                    else:
                        patient_survival_dict[patient_ID][0]=status
                        patient_survival_dict[patient_ID][1]=day
                        patient_survival_dict[patient_ID][2]="5"
                break

        outfile_obj.handle.write("#patient_ID\tStatus\t")
        outfile_obj.handle.write("last_followup_days\tfollowup_No.\t")
        outfile_obj.handle.write("anatomic_site\n")
        for index in range(1,patient_count):
            patient_ID=patient_barcode_list[index]
            if len(anatomic_list)==0:
                patient_anatomic="NA"
            else:
                patient_anatomic=anatomic_list[index]
            patient_status=patient_survival_dict[patient_ID][0]
            patient_day = patient_survival_dict[patient_ID][1]
            if patient_day!="NA" and patient_status!="NA":
                patient_followup=patient_survival_dict[patient_ID][2]
                outfile_obj.handle.write(patient_ID.upper()+'\t'+patient_status+'\t')
                outfile_obj.handle.write(patient_day+'\t'+patient_followup+'\t')
                outfile_obj.handle.write(patient_anatomic+'\n')
        outfile_obj.handle.close()





if __name__ == "__main__":
    ###Python General Module Import 
    import sys, csv, getopt, re
    import os
    import math
    from itertools import ifilter
    
    ##Liye own common function,class loading
    from tcga_survival.constant import *
    from tcga_survival.general_functions import *
    from tcga_survival.general_class import *
    
    OUTPUT_SEP_CHAR='\t'
    
    
            
                 
    #exit if not enough arguments
    if len(sys.argv) < 3:
        print __doc__
        sys.exit(0)
    
    ###set default value
    suffix="txt"
    infile=None
    infile_skip=0
    sep_char='\t'
    sep_gene=','
    header_file=None
    unique_id_length=2
    parameter_file=None
    INPUT_PATH=os.getcwd()
    OUTPUT_PATH=os.getcwd()
    prefix="survival_table"
    OUTPUT_SUFFIX="txt"
    MAX_FOLLOWUP_COUNT=7
    
    ###get arguments(parameters)
    optlist, cmd_list = getopt.getopt(sys.argv[1:], 'hi:s:S:r:d:D:j:I:t:p:L:o:O:z',["test="])
    for opt in optlist:
        if opt[0] == '-h':
            print __doc__; sys.exit(0)
        elif opt[0] == '-i': infile = opt[1]
        elif opt[0] == '-I': INPUT_PATH = opt[1]
        elif opt[0] == '-O': OUTPUT_PATH = opt[1]
        elif opt[0] == '-S': OUTPUT_SUFFIX = opt[1]
        elif opt[0] == '-s': suffix = opt[1]
        elif opt[0] == '-d': sep_char =opt[1]
        elif opt[0] == '-D': sep_gene =opt[1]
        elif opt[0] == '-j': infile_skip= int(opt[1])
        elif opt[0] == '-r': reference = opt[1]
        elif opt[0] == '-o': prefix = opt[1]
        elif opt[0] == '-L': unique_id_length = int(opt[1])
        elif opt[0] == '--test': long_input = opt[1]
    
    #print "Test long input", long_input
    if infile==None:
        infiles=CurrentFolder_to_Infiles(INPUT_PATH, suffix)
    else:
        infiles=[infile]

    ##perform specific functions
    specific_function(infiles)
    
    
    
