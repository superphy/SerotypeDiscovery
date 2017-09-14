from module import DownloadMetadata, FilterGenome, RetrieveGenome, BlastHelper, HeaderModifier, ResultParser
import os

# 1. Get a list of all genomes filename that has corresponding serotyped meta file
#   * Run FilterGenome.py
#   * filtered_genome_filenames.json now contains
# os.system("python FilterGenome.py")

# 2. copy all genome data in "filtered_genome" to data/fileter_genome with the following script:

def main():
    # 1. Get the metadata from enterobase.warwick.ac.uk
    DownloadMetadata.download_metadata()
    # 2. Get a list of all genomes filename that has corresponding serotyped meta file
    FilterGenome.filter_genome()
    # 3. copy all qualified genome data in from database
    RetrieveGenome.retrieve_genome()
    # 4. Add serotype and assembly barcode to header for easier mapping later on
    HeaderModifier.modify_header()
    # 5. Create blast database from extracted+modified genome files
    BlastHelper.makeBlastDB()
    # 6. Query the database with all the allele file we have
    BlastHelper.blastn()
    # 7. Create a json formatted serotype dictionary of all known/confident allele sequences
    ResultParser.parse_result()

if __name__ == '__main__':
    main()