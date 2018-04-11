'''
This file is for upload the basic information locally.
'''

import PhytozomeDataProcessing

from ..classes.KBCDatabaseOperatorClass import KBCDatabaseOperatorClass

def main(data):
    db_admin_operator = KBCDatabaseOperatorClass("KBC_Admin")
    task_status_table_name = 'Admin_user_submitted_task'

    annotation_file = data['annotation']
    transcript_file = data['cdna']
    protein_file = data['protein']
    cds_file = data['cds']
    gff3_file = data['gff3']
    version = data['version']
    organism = data['organism']

    username = data['username']
    job_id = data['job_id']
    database_name = data['database_name']

    if 'path' in data:
        path = data['path']
        annotation_file = path + annotation_file
        transcript_file = path + transcript_file
        protein_file    = path + protein_file
        cds_file        = path + cds_file
        gff3_file       = path + gff3_file


    # Processing data
    dict_data = {'username':username, 'job_id':job_id, 'task_status':1, 'description':'Processing data'}
    db_admin_operator.insert_table(task_status_table_name, dict_data=dict_data)

    annotation_dict = PhytozomeDataProcessing.annotation_info_Phyto(annotation_file)
    transcript_dict = PhytozomeDataProcessing.transcript_fa_Phyto(transcript_file)
    protein_dict = PhytozomeDataProcessing.peptide_fa_Phyto(protein_file)
    cds_dict = PhytozomeDataProcessing.cds_fa_Phyto(cds_file)
    gff3_dict = PhytozomeDataProcessing.gene_gff3_Phyto(gff3_file)



    if annotation_dict['error'] is not None and transcript_dict['error'] is not None and protein_dict['error'] is not None and \
                    cds_dict['error'] is not None and gff3_dict['error'] is not None:
        return;


    job_dict = {}
    job_dict['cDNASequence']        = transcript_dict['cDNASequence']
    job_dict['PeptideSequence']     = protein_dict['PeptideSequence']
    job_dict['CDSSequence']         = cds_dict['CDSSequence']
    job_dict['ChromosomalPosition'] = gff3_dict['ChromosomalPosition']
    job_dict['SearchTableID']       = gff3_dict['SearchTableID']
    job_dict['ProteinAnnotation']   = annotation_dict['protein']
    job_dict['KOG']                 = annotation_dict['KOG']
    job_dict['Panther']             = annotation_dict['Panther']
    job_dict['Pfam']                = annotation_dict['Pfam']


    dict_data = {'task_status':2, 'description':'Importing data'}
    db_admin_operator.update_table_condition_two(task_status_table_name, 'username', username, 'job_id', job_id, dict_data=dict_data)

    db_operator = KBCDatabaseOperatorClass(database_name)
    db_operator.pipeline(job_dict, organism, version, string_size=500, no_version_table_list=['Pfam'], sequence_table_list=['cDNASequence', 'PeptideSequence', 'CDSSequence'])

    dict_data = {'task_status':99999, 'description':'Done.'}
    db_admin_operator.update_table_condition_two(task_status_table_name, 'username', username, 'job_id', job_id, dict_data=dict_data)
