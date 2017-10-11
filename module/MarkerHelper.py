'''
check the +/- of the 10 E. coli specific regions for each of the downloaded enterobase genomes,
and compile that as a table.

eg. `name` `marker 1` `marker 2` `marker N`
'''
import logging, sys, os
from collections import OrderedDict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from module import SubprocessHelper, LoggingHelper, JsonHelper

LOG = logging.getLogger(__name__)

def summarize_gene_presence(blast_result_file):
    '''
    Args:
        blast_result_file(str): genome output generated by blastn

    Returns:
        defaultdict: dict containing presence of gene in each genome in DB
    '''
    entry_tempalte = {
        "genome_name":'',
        "1436893830000|3159571":'',
        "1436893909000|3159808":'',
        "2873786891000|3159389":'',
        "2873787160000|3160196":'',
        "4310679577000|3158082":'',
        "4310679772000|3158667":'',
        "4310679831000|3158844":'',
        "4310680254000|3160113":'',
        "4310680315000|3160296":'',
        "4310680399000|3160548":''
    }
    summary = dict()

    for file in os.listdir('/home/sam/Projects/MoreSerotype/temp/genomes'):
        genome_name = os.path.splitext(os.path.basename(file))[0]
        summary[genome_name] = entry_tempalte.copy()
        summary[genome_name]['genome_name'] = genome_name
    
    count = 0

    with open(blast_result_file) as handle:
        for line in handle:
            fields = line.strip().split()
            blast_record = {
                'qseqid': fields[0],
                'qlen': fields[1],
                'sseqid': fields[2],
                'length': fields[3],
                'pident': fields[4],
                'sstart': fields[5],
                'send': fields[6],
                'sframe': fields[7]
            }
            genome_name = blast_record['sseqid'].split('|')[0]
            allele_name = '|'.join(blast_record['qseqid'].split('|')[1:])
            if summary[genome_name][allele_name] == '':
                count += 1
            summary[genome_name][allele_name] = 'Present'
    avg_count = count / len(summary.keys())
    LOG.info("Average marker count is %.2f / 10; total: %d", avg_count, count)
    return list(summary.values())


def find_gene_presence(marker_file):
    '''
    Summarize the presence of sequences in each genome in DB

    Args:
        marker_file (str): a genome file that contains multiple sequences

    Returns:
        (str): a tabular file that contains the presence of the given sequences
    '''
    blast_result_file = '/home/sam/Projects/MoreSerotype/output/marker.output'
    cmd = [
        'blastn',
        '-query', marker_file,
        '-db', '/home/sam/Projects/MoreSerotype/temp/blast_db/serotyped_blastdb',
        '-perc_identity', "97",
        '-qcov_hsp_perc', "90",
        '-max_target_seqs', '6000', # this number needs to be greater than number of genome
        '-max_hsps', '1', # we only want to know hit/no hit
        '-out', blast_result_file,
        '-outfmt', '6 qseqid qlen sseqid length pident sstart send sframe',
    ]
    SubprocessHelper.run_subprocess(cmd)
    presence_summary = summarize_gene_presence(blast_result_file)
    JsonHelper.write_to_json(presence_summary, '/home/sam/Projects/MoreSerotype/output/presence_summary.json')
    return presence_summary

def main():
    LoggingHelper.setup_logging()
    find_gene_presence('/home/sam/Projects/MoreSerotype/data/ecoli_specific_markers.fasta')

if __name__ == '__main__':
    main()