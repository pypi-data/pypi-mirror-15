#!/usr/bin/env python

import argparse
import logging
import sys

import sqlalchemy

from cdis_pipe_utils import pipe_util

import tools.bam_stats as bam_stats
import tools.picard_buildbamindex as picard_buildbamindex
import tools.picard_markduplicates as picard_markduplicates
import tools.picard_mergesamfiles as picard_mergesamfiles
import tools.picard_sortsam as picard_sortsam
import tools.picard_validatesamfile as picard_validatesamfile
from tools.picard_calculatehsmetrics_tcga import picard_calculatehsmetrics as picard_calculatehsmetrics_tcga
from tools.picard_calculatehsmetrics_target import picard_calculatehsmetrics as picard_calculatehsmetrics_target

def main():
    parser = argparse.ArgumentParser('picard docker tool')

    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)
    
    # Required flags.
    parser.add_argument('--tool_name',
                        required = True,
                        help = 'picard tool'
    )
    parser.add_argument('--uuid',
                        required = True,
                        help = 'uuid string',
    )
    parser.add_argument('--input_state',
                        required = True
    )
    
    # Tool flags
    parser.add_argument('--bam_path',
                        required = False,
                        action = 'append',
                        help = 'input bam path'
    )
    parser.add_argument('--reference_fasta_path',
                        required = False
    )
    parser.add_argument('--bait_intervals_path',
                        required = False
    )
    parser.add_argument('--target_intervals_path',
                        required = False
    )
    parser.add_argument('--outbam_name',
                        required = False
    )

    # optional flags
    parser.add_argument('--db_cred_s3url',
                        required = False
    )
    parser.add_argument('--s3cfg_path',
                        required = False
    )

    
    # setup required parameters
    args = parser.parse_args()
    tool_name = args.tool_name
    uuid = args.uuid
    input_state = args.input_state

    if args.db_cred_s3url:
        db_cred_s3url = args.db_cred_s3url
    else:
        db_cred_s3url = None
    if args.s3cfg_path:
        s3cfg_path = args.s3cfg_path

    logger = pipe_util.setup_logging('picard_' + tool_name, args, uuid)

    if db_cred_s3url is not None: #db server case
        conn_dict = pipe_util.get_connect_dict(db_cred_s3url, s3cfg_path, logger)
        engine = sqlalchemy.create_engine(sqlalchemy.engine.url.URL(**conn_dict))
    else: # local sqlite case
        sqlite_name = uuid + '.db'
        engine_path = 'sqlite:///' + sqlite_name
        engine = sqlalchemy.create_engine(engine_path, isolation_level='SERIALIZABLE')


    if tool_name == 'BuildBamIndex':
        bam_path = pipe_util.get_param(args, 'bam_path')[0]
        picard_buildbamindex.picard_buildbamindex(uuid, bam_path, input_state, engine, logger)
    elif tool_name == 'CalculateHsMetrics_target':
        bam_path = pipe_util.get_param(args, 'bam_path')[0]
        reference_fasta_path = pipe_util.get_param(args, 'reference_fasta_path')
        json_path = pipe_util.get_param(args, 'json_path')
        interval_dir = pipe_util.get_param(args, 'interval_dir')
        wxs_dict['bait_intervals_path'] = bait_intervals_path
        wxs_dict['target_intervals_path'] = target_intervals_path
        picard_calculatehsmetrics_target(uuid, bam_path, input_state, json_path, interval_dir, engine, logger, wxs_dict = wxs_dict)
    elif tool_name == 'CalculateHsMetrics_tcga':
        bam_path = pipe_util.get_param(args, 'bam_path')[0]
        reference_fasta_path = pipe_util.get_param(args, 'reference_fasta_path')
        json_path = pipe_util.get_param(args, 'json_path')
        interval_dir = pipe_util.get_param(args, 'interval_dir')
        wxs_dict['bait_intervals_path'] = bait_intervals_path
        wxs_dict['target_intervals_path'] = target_intervals_path
        picard_calculatehsmetrics_tcga(uuid, bam_path, input_state, json_path, interval_dir, engine, logger, wxs_dict = wxs_dict)
    elif tool_name == 'CollectAlignmentSummaryMetrics':
        bam_path = pipe_util.get_param(args, 'bam_path')[0]
        reference_fasta_path = pipe_util.get_param(args, 'reference_fasta_path')
        bam_stats.do_picard_metrics(uuid, bam_path, input_state, reference_fasta_path, engine, logger, 'CollectAlignmentSummaryMetrics')
    elif tool_name == 'CollectMultipleMetrics':
        bam_path = pipe_util.get_param(args, 'bam_path')[0]
        reference_fasta_path = pipe_util.get_param(args, 'reference_fasta_path')
        bam_stats.do_picard_metrics(uuid, bam_path, input_state, reference_fasta_path, engine, logger, 'CollectMultipleMetrics')
    elif tool_name == 'CollectWgsMetrics':
        bam_path = pipe_util.get_param(args, 'bam_path')[0]
        reference_fasta_path = pipe_util.get_param(args, 'reference_fasta_path')
        bam_stats.do_picard_metrics(uuid, bam_path, input_state, reference_fasta_path, engine, logger, 'CollectWgsMetrics')
    elif tool_name == 'MarkDuplicates':
        bam_path = pipe_util.get_param(args, 'bam_path')[0]
        picard_markduplicates.bam_markduplicates(uuid, bam_path, input_state, engine, logger)
    elif tool_name == 'MarkDuplicatesWithMateCigar':
        bam_path = pipe_util.get_param(args, 'bam_path')[0]
        picard_markduplicates.bam_markduplicateswithmatecigar(uuid, bam_path, input_state, engine, logger)
    elif tool_name == 'MergeSamFiles':
        bam_path = pipe_util.get_param(args, 'bam_path')
        outbam_name = pipe_util.get_param(args, 'outbam_name')
        picard_mergesamfiles.picard_mergesamfiles(uuid, bam_path, input_state, outbam_name, engine, logger)
    elif tool_name == 'SortSam':
        bam_path = pipe_util.get_param(args, 'bam_path')[0]
        picard_sortsam.picard_sortsam(uuid, bam_path, input_state, engine, logger)
    elif tool_name == 'ValidateSamFile':
        bam_path = pipe_util.get_param(args, 'bam_path')[0]
        picard_validatesamfile.picard_validatesamfile(uuid, bam_path, input_state, engine, logger)
    else:
        sys.exit('No recognized tool was selected')
        
    return


if __name__ == '__main__':
    main()
