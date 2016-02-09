TCGA survival table extract
-----------------------
INSTALL:

python setup.py install

-----------------------

MANUAL: 
the input file(s) should be clinical files downloaded from TCGA by Firehose

to generate the overall survival data

python INSTALL_PATH/extract_survival_table_obj_v0.0.py -i BRCA.clin.merged.txt

to generate the disease free survival data

python INSTALL_PATH/extract_DiseaseFreesurvival_table_obj_v0.0.py -i -i BRCA.clin.merged.txt

for example the default INSTALL_PATH for linux is
/usr/local/lib/pythonX.X/dist-packages/


