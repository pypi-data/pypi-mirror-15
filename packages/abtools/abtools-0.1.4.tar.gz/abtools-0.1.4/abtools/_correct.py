#!/usr/bin/env python
# filename: _correct.py



###########################################################################
#
# Copyright (c) 2015 Bryan Briney.  All rights reserved.
#
# @version: 1.0.0
# @author: Bryan Briney
# @license: MIT (http://opensource.org/licenses/MIT)
#
###########################################################################



from __future__ import print_function

from collections import Counter
import json
import math
import multiprocessing as mp
import os
import shelve
import sqlite3
from StringIO import StringIO
import subprocess as sp
import sys
import tempfile
import time
import urllib
import uuid

import numpy as np

from pymongo import MongoClient

from Bio import SeqIO
from Bio import AlignIO
from Bio.Align import AlignInfo

from abtools import log, mongodb
from abtools.alignment import muscle
from abtools.pipeline import make_dir, list_files


def parse_args():
    import argparse
    parser = argparse.ArgumentParser("Clusters sequences using either an identity threshold or unique \
                                      antibody identifiers (UAIDs). \
                                      Calculates either the centroid or consensus sequence for each \
                                      identity/UAID cluster passing a cluster size threshold.")
    parser.add_argument('-d', '--database', dest='db', default=None,
                        help="Name of the MongoDB database to query. Required")
    parser.add_argument('-c', '--collection', dest='collection', default=None,
                        help="Name of the MongoDB collection to query. \
                        If not provided, all collections in the given database will be processed iteratively.")
    parser.add_argument('-j', '--json', dest='json', default=None,
                        help="Input JSON file or directory of JSON files.")
    parser.add_argument('-o', '--output', dest='output', required=True,
                        help="Output directory for the FASTA files. Required")
    parser.add_argument('-l', '--log', dest='log',
                        help="Location for the log file. \
                        If not provided, log will be written to <output>/abcorrect.log")
    parser.add_argument('-t', '--temp', dest='temp_dir', required=True,
                        help="Directory for temporary files, including the SQLite database. Required")
    parser.add_argument('-i', '--ip', dest='ip', default='localhost',
                        help="IP address for the MongoDB server.  Defaults to 'localhost'.")
    parser.add_argument('--port', dest='port', default=27017, type=int,
                        help="IP address for the MongoDB server.  Defaults to 'localhost'.")
    parser.add_argument('-u', '--user', dest='user', default=None,
                        help="Username for the MongoDB server. Not used if not provided.")
    parser.add_argument('-p', '--password', dest='password', default=None,
                        help="Password for the MongoDB server. Not used if not provided.")
    parser.add_argument('-m', '--min', dest='min_seqs', default=1, type=int,
                        help="Minimum number of sequences for finding centroids from a UAID group. \
                        Defaults to 1.")
    parser.add_argument('-U', '--no-uaid', dest='uaid', action='store_false', default=True,
                        help="Clusters sequences by identity rather than using universal antibody IDs (UAIDs).")
    parser.add_argument('-P', '--parse-uaids', dest='parse_uaids', type=int, default=0,
                        help="Length of the UAID to parse, if the UAID was not parsed during AbStar processing. \
                        If the '--no-uaid' flag is also used, this option will be ignored. \
                        For a UAID of length 20, option should be passed as '--parse-uaids 20'. \
                        Default is to not parse UAIDs.")
    parser.add_argument('-C', '--centroid', dest='consensus', action='store_false', default=True,
                        help="Generates consensus sequences for each UAID or homology cluster. \
                        Default is to identify cluster centroids.")
    parser.add_argument('-I', '--identity', dest='identity_threshold', default=0.975, type=float,
                        help="Identity threshold for sequence clustering. \
                        Not used for UAID-based correction. Default is 0.975.")
    parser.add_argument('--only-largest-cluster', default=False, action='store_true',
                        help="If set while calculating centroids using UAIDs, \
                        only the largest centroid for each UAID cluster is retained.")
    parser.add_argument('--non-redundant', dest='non_redundant', action='store_true', default=False,
                        help='If set, will make a non-redundant FASTA file using Unix sort. \
                        This is much faster than CD-HIT, but can only remove exact duplicates. \
                        Note that this is not exactly equivalent to clustering with a threshold of 1.0, \
                        because sequences of different length that align perfectly for the entirety \
                        of the shorter sequence will be collapsed when using CD-HIT but will not be \
                        collapsed by Unix sort.')
    parser.add_argument('-g', '--germs', dest='germs', default=None,
                        help="Path to a FASTA-formatted file of germline V gene sequences. \
                        Required if building consensus sequences, not required for centroids.")
    parser.add_argument('--aa', dest='aa', action='store_true', default=False,
                        help="If set, use amino acid sequences for identity-based clustering.")
    parser.add_argument('--field', dest='field', default='vdj_nt',
                        help="The MongoDB field to be used for clustering. \
                        If using UAIDs, this is the field that will be used to calculate \
                        consensus/centroid sequences. \
                        Default is 'vdj_nt'.")
    parser.add_argument('-D', '--debug', dest='debug', action='store_true', default=False,
                        help="If set, will run in debug mode.")
    parser.add_argument('-s', '--sleep', dest='sleep', type=int, default=0,
                        help="Delay, in minutes, until the script starts executing. Default is 0.")
    return parser


class Args(object):
    def __init__(self, db=None, collection=None, json=None,
                 output=None, log=None, temp=None,
                 ip='localhost', port=27017, user=None, password=None,
                 min_seqs=1, identity_threshold=0.975,
                 uaid=True, parse_uaids=0, non_redundant=False,
                 consensus=True, only_largest_cluster=False, germs=None,
                 aa=False, field='vdj_nt', debug=False, sleep=0):
        super(Args, self).__init__()
        if not all([db, output, temp]):
            print('\nERROR: Output and temp directories must be provided, \
                as well as a MongoDB database name.\n')
            sys.exit(1)
        self.db = db
        self.collection = collection
        self.json = json
        self.output = output
        self.log = log
        self.temp_dir = temp
        self.ip = ip
        self.port = int(port)
        self.user = user
        self.password = password
        self.min_seqs = int(min_seqs)
        self.uaid = False if non_redundant else uaid
        self.parse_uaids = int(parse_uaids)
        self.consensus = consensus
        self.identity_threshold = float(identity_threshold)
        self.only_largest_cluster = only_largest_cluster
        self.non_redundant = non_redundant
        self.germs = germs
        self.aa = aa
        self.field = field
        self.debug = debug
        self.sleep = int(sleep)



# =========================================
#
#        SEQUENCES AND DATABASES
#
# =========================================



def get_seqs(db, collection, args, make_seq_db=True):
    seqs = query(db, collection, args)
    if not make_seq_db:
        return seqs
    return build_seq_db(seqs, args)


def query(db, collection, args):
    seq_field = args.field
    # parse JSON file...
    if db is None:
        loger.info('Reading JSON file...')
        results = []
        with open(collection) as f:
            _results = json.load(f)
        for r in _results:
            try:
                d = {'seq_id': r['seq_id'],
                     seq_field: r[seq_field],
                     'raw_query': r['raw_query'],
                     'v_gene': {'full': f['v_gene']['full']}}
                if args.uaid is not None:
                    if 'uaid' in r:
                        d['uaid'] = r['uaid']
                    elif args.parse_uaids:
                        if args.parse_uaids > 0:
                            d['uaid'] = r['raw_query'][:args.parse_uaids]
                        else:
                            d['uaid'] = r['raw_query'][args.parse_uaids:]
                    else:
                        err = 'ERROR: UAID field was not found. '
                        err += 'Ensure that UAIDs were parsed by AbStar, '
                        err += 'use the -parse_uaids option to parse the UAIDs from the raw query input, '
                        err += 'or use the -u option for identity-based clustering.'
                        raise ValueError(err)
                results.append(d)
            except KeyError:
                continue
    # ...or get sequences from a MongoDB database
    else:
        logger.info('Getting sequences from MongoDB...')
        coll = db[collection]
        match = {'prod': 'yes'}
        project = {'_id': 0, 'seq_id': 1, seq_field: 1, 'raw_query': 1, 'v_gene.full': 1}
        if args.uaid is not None:
            project['uaid'] = 1
        # if args.consensus:
        #     project['v_gene.gene'] = 1
        results = coll.find(match, project)
        # results = coll.find({'prod': 'yes'}, {'_id': 0, 'v_gene.full': 1, 'seq_id': 1, 'uaid': 1, seq_field: 1, 'raw_query': 1})
    if args.non_redundant:
        return results
    elif args.uaid:
        seqs = []
        for r in results:
            if 'uaid' in r:
                seqs.append((r['seq_id'], r['uaid'], r[seq_field], r['raw_query'], r['v_gene']['full']))
            elif args.parse_uaids:
                if args.parse_uaids > 0:
                    seqs.append((r['seq_id'], r['raw_query'][:args.parse_uaids], r[seq_field], r['raw_query'], r['v_gene']['full']))
                else:
                    seqs.append((r['seq_id'], r['raw_query'][args.parse_uaids:], r[seq_field], r['raw_query'], r['v_gene']['full']))
            else:
                err = 'ERROR: UAID field was not found. '
                err += 'Ensure that UAIDs were parsed by AbStar, '
                err += 'use the -parse_uaids option to parse the UAIDs from the raw query input, '
                err += 'or use the -u option for identity-based clustering.'
                raise ValueError(err)
    else:
        seqs = [(r['seq_id'], r[seq_field], r['raw_query'], r['v_gene']['full']) for r in results]
    logger.info('Found {} sequences\n'.format(len(seqs)))
    return seqs


def build_seq_db(seqs, args):
    logger.info('Building a SQLite database of sequences...')
    db_path = os.path.join(args.temp_dir, 'seq_db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    create_cmd = get_seq_db_creation_cmd(args)
    insert_cmd = get_seq_db_insert_cmd(args)
    c.execute('DROP TABLE IF EXISTS seqs')
    c.execute(create_cmd)
    c.executemany(insert_cmd, seqs)
    c.execute('CREATE INDEX seq_index ON seqs (seq_id)')
    return c


def get_seq_db_creation_cmd(args):
    if args.uaid:
        return '''CREATE TABLE seqs (seq_id text, uaid text, seq text, raw text, v_gene text)'''
    return '''CREATE TABLE seqs (seq_id text, seq text, raw text, v_gene text)'''


def get_seq_db_insert_cmd(args):
    if args.uaid:
        return 'INSERT INTO seqs VALUES (?,?,?,?,?)'
    return 'INSERT INTO seqs VALUES (?,?,?,?)'


def remove_sqlite_db(args):
    db_path = os.path.join(args.temp_dir, 'seq_db')
    os.unlink(db_path)


def parse_germs(germ_file):
    germ_handle = open(germ_file, 'r')
    germs = {}
    for seq in SeqIO.parse(germ_handle, 'fasta'):
        germs[seq.id] = str(seq.seq).upper()
    return germs





# =========================================
#
#             NON-REDUNDANT
#
# =========================================


def unix_sort_unique(seqs, args):
    sort_file, input_count = make_sort_input(seqs, args)
    logger.info('Found {} sequences'.format(input_count))
    unique_file = tempfile.NamedTemporaryFile(dir=args.temp_dir, delete=False)
    sort_unique_cmd = 'sort -k2,2 -u -o {} {}'.format(unique_file.name, sort_file)
    logger.info('Running sort/uniq...')
    p = sp.Popen(sort_unique_cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    p.communicate()
    # fastas = parse_unique_file(unique_file.name)
    os.unlink(sort_file)
    # os.unlink(unique_file.name)
    # return fastas
    return unique_file.name



def make_sort_input(seqs, args):
    seq_field = args.field
    sort_file = tempfile.NamedTemporaryFile(dir=args.temp_dir, delete=False)
    sort_handle = open(sort_file.name, 'a')
    count = 0
    for s in seqs:
        sort_handle.write('{} {} {}\n'.format(s['seq_id'], s[seq_field], s['raw_query']))
        count += 1
    # seq_strings = [' '.join(s) for s in seqs]
    # sort_file.write('\n'.join(seq_strings))
    sort_handle.close()
    return sort_file.name, count


# def parse_unique_file(unique_file):
#     with open(unique_file) as f:
#         for line in f:
#             if len(line.strip().split()) < 3:
#                 continue
#             seq_id, vdj, raw = line.strip().split()
#             fastas.append('>{}\n{}'.format(seq_id, raw))
#     return fastas




# =========================================
#
#           CD-HIT CLUSTERING
#
# =========================================



def cdhit_clustering(seq_db, args, uaid=True, centroid=False):
    infile = make_cdhit_input(seq_db, args, uaid=uaid)
    outfile = os.path.join(args.temp_dir, 'clust')
    logfile = open(os.path.join(args.temp_dir, 'log'), 'a')
    threshold = 1.0 if uaid else args.identity_threshold
    do_cdhit(infile.name, outfile, logfile, threshold, args)
    if centroid:
        cent_handle = open(outfile, 'r')
        if not uaid:
            clust_handle = open('{}.clstr'.format(outfile), 'r')
            sizes = parse_cluster_sizes(clust_handle)
            seqs = parse_centroids(cent_handle, seq_db, sizes=sizes)
        else:
            seqs = parse_centroids(cent_handle, seq_db)
    else:
        clust_handle = open('{}.clstr'.format(outfile), 'r')
        seqs, sizes = parse_clusters(clust_handle, seq_db, args)
    if not args.debug:
        os.unlink(infile.name)
        os.unlink(os.path.join(args.temp_dir, 'log'))
        os.unlink(outfile)
        os.unlink(outfile + '.clstr')
    if uaid:
        return seqs
    return seqs, sizes


def make_cdhit_input(seq_db, args, uaid=True):
    infile = tempfile.NamedTemporaryFile(dir=args.temp_dir, delete=False)
    fastas = []
    if uaid:
        seqs = seq_db.execute('''SELECT seqs.seq_id, seqs.uaid FROM seqs''')
    else:
        seqs = seq_db.execute('''SELECT seqs.seq_id, seqs.seq FROM seqs''')
    for s in seqs:
        fastas.append('>{}\n{}'.format(s[0], s[1]))
    infile.write('\n'.join(fastas))
    infile.close()
    return infile


def do_cdhit(fasta, clust, log, threshold, args):
    seq_type = 'UAIDs' if args.uaid else 'sequences'
    logger.info('Clustering {} with CD-HIT...'.format(seq_type))
    start_time = time.time()
    cdhit_cmd = 'cd-hit -i {} -o {} -c {} -n 5 -d 0 -T 0 -M 35000'.format(fasta, clust, threshold)
    cluster = sp.Popen(cdhit_cmd, shell=True, stdout=log)
    cluster.communicate()
    logger.info('Clustering took {} seconds'.format(round(time.time() - start_time, 2)))
    logger.info('')


def parse_centroids(centroid_handle, sizes=None):
    cent_ids = []
    counter = 0
    for seq in SeqIO.parse(centroid_handle, 'fasta'):
        # seq_id = '{}_{}'.format(seq.id, sizes[counter]) if sizes is not None else seq.id
        seq_id = seq.id
        cent_ids.append(seq_id)
    return get_cluster_seqs(cent_ids, seq_db)
    # counter = 0
    # centroids = []
    # for seq in SeqIO.parse(centroid_handle, 'fasta'):
    #     if sizes:
    #         size = sizes[counter]
    #         centroids.append('>{}_{}\n{}'.format(seq.id, size, str(seq.seq)))
    #     else:
    #         centroids.append('>{}\n{}'.format(seq.id, str(seq.seq)))
    #     counter += 1
    # return centroids


def parse_clusters(cluster_handle, seq_db, args):
    logger.info('Parsing CD-HIT cluster file...')
    clusters = [c.split('\n') for c in cluster_handle.read().split('\n>')]
    logger.info('{} total clusters identified.\n'.format(len(clusters)))
    logger.info('Retrieving cluster sequences...')
    cluster_seqs = []
    start = time.time()
    lengths = []
    for cluster in clusters:
        lengths.append(len(cluster) - 1)
        if len(cluster) >= args.min_seqs + 1:
            cluster_ids = get_cluster_ids(cluster)
            cluster_seqs.append(get_cluster_seqs(cluster_ids, seq_db))
    logger.info('{} clusters meet the minimum size cutoff ({} sequences)'.format(len(cluster_seqs), args.min_seqs))
    logger.info('The average cluster contains {} sequences; the largest contains {} sequences.'.format(round(1. * sum(lengths) / len(lengths), 2), max(lengths)))
    logger.info('Cluster parsing and sequence retrieval took {} seconds\n'.format(round(time.time() - start, 2)))
    return cluster_seqs, lengths


def parse_cluster_sizes(cluster_handle):
    clusters = [c.split('\n') for c in cluster_handle.read().split('\n>')]
    lengths = []
    for cluster in clusters:
        lengths.append(len(cluster) - 1)
    return lengths


def get_cluster_ids(cluster):
    ids = []
    for c in cluster[1:]:
        if c:
            ids.append(c.split()[2][1:-3])
    return ids


def chunker(l, size=900):
    return (l[pos:pos + size] for pos in xrange(0, len(l), size))


def get_cluster_seqs(seq_ids, seq_db):
    seqs = []
    for chunk in chunker(seq_ids):
        seq_chunk = seq_db.execute('''SELECT seqs.seq_id, seqs.raw
                                   FROM seqs
                                   WHERE seqs.seq_id IN ({})'''.format(','.join('?' * len(chunk))), chunk)
        seqs.extend(seq_chunk)
    return ['>{}\n{}'.format(s[0], s[1]) for s in seqs]





# =========================================
#
#       UAID CENTROID CLUSTERING
#
# =========================================



def get_uaid_centroids(uaid_clusters, args):
    logger.info('Calculating centroid sequences with USEARCH:')
    start_time = time.time()
    centroids = []
    singletons = [c[0] for c in uaid_clusters if len(c) == 1]
    for s in singletons:
        seq_id = s.split('\n')[0].replace('>', '')
        seq = s.split('\n')[1]
        centroids.append('>{}\n{}'.format(seq_id, seq))
    sizes = [1] * len(centroids)
    clusters = [c for c in uaid_clusters if len(c) > 1]
    if args.debug:
        for cluster in clusters:
            centroid, size = do_usearch_centroid(cluster, args)
            centroids.extend(centroid)
            sizes.extend(size)
    else:
        p = mp.Pool(maxtasksperchild=100)
        async_results = []
        for c in clusters:
            async_results.append(p.apply_async(do_usearch_centroid, (c, args)))
        monitor_mp_jobs(async_results)
        for a in async_results:
            centroid, size = a.get()
            centroids.extend(centroid)
            sizes.extend(size)
        p.close()
        p.join()
        logger.info('Centroids were calculated in {} seconds.'.format(round(time.time() - start_time), 2))
    return centroids, sizes


def do_usearch_centroid(uaid_group_seqs, args):
    # '''
    # Clusters sequences at 90% identity using USEARCH.

    # Inputs
    # uaid_group_seqs: a list of fasta strings corresponding to sequences from a single UAID group.

    # Outputs
    # A list of fasta strings, containing centroid sequences for each cluster.
    # '''
    fasta = tempfile.NamedTemporaryFile(dir=args.temp_dir, prefix='cluster_input_', delete=False)
    results = tempfile.NamedTemporaryFile(dir=args.temp_dir, prefix='results_', delete=False)
    centroids = tempfile.NamedTemporaryFile(dir=args.temp_dir, prefix='centroids_', delete=False)
    fasta.write('\n'.join(uaid_group_seqs))
    fasta.close()
    usearch = ['usearch',
               '-cluster_fast',
               fasta.name,
               '-maxaccepts', '0',
               '-maxrejects', '0',
               '-id', '0.9',
               '-sizeout',
               '-uc', results.name,
               '-centroids', centroids.name]
    p = sp.Popen(usearch, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    centroid_seqs = []
    sizes = []
    for cent in SeqIO.parse(open(centroids.name, 'r'), 'fasta'):
        seq_id = cent.id.split(';')[0]
        size = int(cent.id.split(';')[1].replace('size=', ''))
        centroid_seqs.append('>{}\n{}'.format(seq_id, str(cent.seq)))
        sizes.append(size)
    if args.only_largest_cluster:
        cents_plus_sizes = sorted(zip(centroid_seqs, sizes), key=lambda x: x[1], reverse=True)
        centroid_seqs = [cents_plus_sizes[0][0], ]
        sizes = [cents_plus_sizes[0][1], ]
    os.unlink(fasta.name)
    os.unlink(results.name)
    os.unlink(centroids.name)
    return centroid_seqs, sizes





# =========================================
#
#          CONSENSUS SEQUENCES
#
# =========================================



def get_consensus(clusters, germs, args):
    logger.info('Building consensus sequences...')
    if args.debug:
        consensus_seqs = [calculate_consensus(cluster, germs, args) for cluster in clusters]
    else:
        p = mp.Pool()
        async_results = [p.apply_async(calculate_consensus, (cluster, germs, args)) for cluster in clusters]
        monitor_mp_jobs(async_results)
        results = [a.get() for a in async_results]
        p.close()
        p.join()
    fastas = []
    for r in results:
        seq = r[0]
        size = r[1]
        fastas.append('>{}\n{}'.format(uuid.uuid4(), seq))
    return fastas, [r[1] for r in results]


def calculate_consensus(cluster, germs, args):
    if len(cluster) == 1:
        return (cluster[0].split('\n')[1].upper(), 1)
    fasta_string = consensus_alignment_input(cluster, germs, args)

    if len(cluster) < 100:
        alignment = muscle(fasta_string)
    elif len(cluster) < 1000:
        alignment = muscle(fasta_string, maxiters=2)
    else:
        alignment = muscle(fasta_string, maxiters=1, diags=True)
    ambig = 'N' if 'nt' in args.field else 'X'
    summary_align = AlignInfo.SummaryInfo(alignment)
    consensus = summary_align.gap_consensus(threshold=0.51, ambiguous=ambig)
    consensus = str(consensus).replace('-', '')
    return (consensus.upper(), len(cluster))


def consensus_alignment_input(cluster, germs, args):
    if germs is not None:
        try:
            v_gene = vgene_lookup(cluster, args)
            germ = '>{}\n{}'.format(v_gene, germs[v_gene])
        except KeyError:
            germ = ''
    else:
        germ = ''
    cluster.append(germ)
    return '\n'.join(cluster)


def vgene_lookup(cluster, args):
    v_genes = []
    seq_ids = [seq.split('\n')[0].replace('>', '') for seq in cluster]
    db_path = os.path.join(args.temp_dir, 'seq_db')
    conn = sqlite3.connect(db_path)
    seq_db = conn.cursor()
    for chunk in chunker(seq_ids):
        v_chunk = seq_db.execute('''SELECT seqs.v_gene
                                    FROM seqs
                                    WHERE seqs.seq_id IN ({})'''.format(','.join('?' * len(chunk))), chunk)
        v_genes.extend(v_chunk)
    v_gene = Counter(v_genes).most_common()[0][0]
    conn.close()
    return v_gene





# =========================================
#
#         PROGRESS AND PRINTING
#
# =========================================



def _print_start_info(args):
    logger.info('')
    logger.info('')
    logger.info('')
    logger.info('-' * 25)
    logger.info('ERROR CORRECTION')
    logger.info('-' * 25)
    _log_params(args)


def _log_params(args):
    logger.info('')
    logger.info('INPUT DB: {}'.format(args.db))
    logger.info('OUTPUT DIR: {}'.format(args.output))
    logger.info('TEMP DIR: {}'.format(args.temp_dir))
    logger.info('UAIDs: {}'.format(args.uaid))
    logger.info('CLUSTERING TYPE: {}'.format('sort/uniq' if args.non_redundant else 'CD-HIT'))
    if args.non_redundant:
        logger.info('IDENTITY THRESHOLD: 1.0')
        logger.info('MIN SEQS: 1')
        return
    elif args.uaid == 0:
        logger.info('IDENTITY THRESHOLD: {}'.format(args.identity_threshold))
        logger.info('GERMLINES: {}'.format(args.germs))
    else:
        logger.info('PARSE UAIDS: {}'.format(args.parse_uaids))
    logger.info('MIN SEQS: {}'.format(args.min_seqs))
    logger.info('LARGEST CLUSTER ONLY: {}'.format(args.only_largest_cluster))



def monitor_mp_jobs(results):
    finished = 0
    jobs = len(results)
    while finished < jobs:
        time.sleep(1)
        ready = [ar for ar in results if ar.ready()]
        finished = len(ready)
        update_progress(finished, jobs, sys.stdout)
    sys.stdout.write('\n')


def update_progress(finished, jobs, log, failed=None):
    pct = int(100. * finished / jobs)
    ticks = pct / 2
    spaces = 50 - ticks
    if failed:
        prog_bar = '\r({}/{}) |{}{}|  {}% ({}, {})'.format(finished, jobs, '|' * ticks, ' ' * spaces, pct, finished - failed, failed)
    else:
        prog_bar = '\r({}/{}) |{}{}|  {}%'.format(finished, jobs, '|' * ticks, ' ' * spaces, pct)
    sys.stdout.write(prog_bar)


def write_output(collection, fastas, sizes, collection_start_time, args):
    seq_type = 'consensus' if args.consensus else 'centroid'
    logger.info('Writing {} sequences to output file...'.format(seq_type))
    write_fasta_output(collection, fastas, args)
    if sizes is not None:
        write_stats_output(collection, sizes, args)
    logger.info('{} {} sequences were identified.'.format(len(fastas), seq_type))
    logger.info('{} was processed in {} seconds.'.format(collection,
        round(time.time() - collection_start_time, 2)))
    logger.info('')


def write_nr_output(collection, unique_file, collection_start_time, args):
    logger.info('Writing non-redundant sequences to output file...')
    oname = collection
    if os.path.isfile(collection):
        oname = os.path.basename(collection).rstrip('.json')
    outfile = os.path.join(args.output, '{}_nr.fasta'.format(oname))
    open(outfile, 'w').write('')
    ohandle = open(outfile, 'a')
    count = 0
    with open(unique_file) as f:
        for line in f:
            if len(line.strip().split()) != 3:
                continue
            seq_id, vdj, raw = line.strip().split()
            ohandle.write('>{}\n{}\n'.format(seq_id, raw))
            count += 1
    logger.info('{} non-redundant sequences were identified.'.format(count))
    logger.info('{} was processed in {} seconds.'.format(collection,
        round(time.time() - collection_start_time, 2)))
    logger.info('')


def write_fasta_output(collection, fastas, args):
    seq_type = 'consensus' if args.consensus else 'centroids'
    oname = collection
    if os.path.isfile(collection):
        oname = os.path.basename(collection).rstrip('.json')
    outfile = os.path.join(args.output, '{}_{}.fasta'.format(oname, seq_type))
    out_handle = open(outfile, 'w')
    out_handle.write('\n'.join(fastas))
    out_handle.close()


def write_stats_output(collection, sizes, args):
    sizes = [int(s) for s in sizes]
    bin_counts = np.bincount(sizes)[1:]
    bins = range(1, len(bin_counts))
    binned_data = zip(bins, bin_counts)
    bin_string = 'Cluster Size\tCount\n'
    bin_string += '\n'.join(['{}\t{}'.format(b[0], b[1]) for b in binned_data])
    oname = collection
    if os.path.isfile(collection):
        oname = os.path.basename(collection).rstrip('.json')
    outfile = os.path.join(args.output, '{}_cluster_sizes.txt'.format(oname))
    out_handle = open(outfile, 'w')
    out_handle.write(bin_string)
    out_handle.close()



def print_collection_info(collection):
    logger.info('')
    logger.info('')
    logger.info(collection)
    logger.info('-' * len(collection))


def countdown(args):
    start = time.time()
    h = int(args.sleep / 60)
    m = int(args.sleep % 60)
    hz = '0' if len(str(h)) == 1 else ''
    mz = '0' if len(str(m)) == 1 else ''
    print('Countdown: {}{}:{}{}:{}'.format(hz, h, mz, m, '00'), end='')
    sys.stdout.flush()
    done = False
    while not done:
        time.sleep(0.25)
        elapsed = int(time.time() - start)
        if elapsed < args.sleep * 60:
            h = int((args.sleep - elapsed / 60.) / 60)
            m = int((args.sleep - elapsed / 60.) % 60)
            s = int((60 * args.sleep - elapsed) % 60)
            hz = '0' if len(str(h)) == 1 else ''
            mz = '0' if len(str(m)) == 1 else ''
            sz = '0' if len(str(s)) == 1 else ''
            print('\rCountdown: {}{}:{}{}:{}{}'.format(hz, h, mz, m, sz, s), end='')
            sys.stdout.flush()
        else:
            print('\rCountdown: 00:00:00')
            done = True


def run(**kwargs):
    '''
    Corrects antibody reads using UAIDs (molecular barcodes) or identity-based clustering.

    Either ``json`` or ``db`` is required.


    Args:

        db (str): Name of a MongoDB database to query.

        collection (str): Name of a MongoDB collection. If not provided, all
            collections in ``db`` will be iteratively processed.

        json: Can be one of two things:

            1. Path to a JSON file, containing sequence data annotated by AbStar.

            2. Path to a directory, containing one or more JSON files of
                AbStar-annotated data.

        output (str): Path to the output directory, into which corrected FASTA
            files will be deposited. If it does not exist, it will be created.

        log (str): Path to the log file. If the parent directory doesn't exist,
            it will be created.

        ip (str): IP address of the MongoDB server. Default is ``localhost``.

        port (int): Port of the MongoDB server. Default is ``27017``.

        user (str): Username with which to connect to the MongoDB database. If either
            of ``user`` or ``password`` is not provided, the connection to the MongoDB
            database will be attempted without authentication.

        password (str): Password with which to connect to the MongoDB database. If either
            of ``user`` or ``password`` is not provided, the connection to the MongoDB
            database will be attempted without authentication.

        min_seqs (int): Minimum number of sequences for a centroid/consensus sequence to be
            calculated. After clustering (either by identity or using UAIDs), clusters with
            at least ``min_seqs`` sequences will be retained for consensus/centroid calculation.
            Default is ``1``.

        uaid (bool): If ``True``, use Unique Antibody IDs (UAIDs) for error correction.
            Sequences will be binned by UAID and the sequences in each bin will be used to
            compute a centroid or consensus sequence. If ``False``, sequences will be clustered
            by identity and each cluster will be used for consensus/centroid determination.

        parse_uaids (int): If UAIDs haven't been pre-parsed by AbStar, indicate the length of the
            UAID sequence (in nucleotides) and the UAIDs will be parsed during correction. If
            ``parse_uaids`` is negative, the UAID will be parsed from the end of the sequence.
            Default is ``0``, which does not parse a UAID sequence.

        consensus (bool): If ``True``, consensus sequences are calculated. If ``False``, centroid
            sequences are calculated. Default is ``True``.

        identity_threshold (float): Identity threshold, if clustering by identity (not UAIDs).
            Must be a float between 0 and 1. Default is 0.975.

        only_largest_cluster (bool): When clustering using UAIDs, there is a some probability that
            different sequences get labeled with the same UAID. To limit incorrect consensus/centroid
            calculation, sequences in each UAID bin are clustered using ``identity_threshold`` before
            calculating consens/centroid sequences. By default, all UAID clusters that meet the
            ``min_seqs`` size threshold are used to generate consensus/centroid sequences. If that
            behavior is not desired, setting ``only_largest_cluster`` to ``True`` results in only
            the largest UAID cluster being used to generate centroid/consensus sequences.

        nr (bool): If ``True``, a non-redundant sequence dataset will be generated using ``sort | uniq``.
            This is much faster than normal sequence clustering with CD-HIT, but can only be performed at an
            identity threshold of 100%.

            .. note:

                Using ``nr`` may produce different results than clustering sequences with ``identity_threshold``
                set to ``1.0``. This is because sequences of different lengths that are otherwise identical
                will not be collapsed when using ``nr`` but will be collapsed using normal clustering.

        germs (str): Path to a file containing germline V-gene sequences. When clustering with ``min_seqs``
            equal to 2, the appropriate germline sequence will be added to the alignment to serve as a
            consensus tiebreaker.

        aa (bool): If ``True``, perform sequence clustering (either using ``identity_threshold`` or ``nr``)
            using amino acid sequences. Default is ``False``, which performs clustering using nucleotide
            sequences.

        debug (bool): If ``True``, logging is more verbose.
    '''
    args = Args(**kwargs)
    global logger
    logger = log.get_logger('abcorrect')
    main(args)


def run_standalone(args):
    logfile = args.log if args.log else os.path.join(args.output, 'abcorrect.log')
    log.setup_logging(logfile)
    global logger
    logger = log.get_logger('abcorrect')
    main(args)


def main(args):
    _print_start_info(args)
    if args.sleep:
        countdown(args)
    for d in [args.output, args.temp_dir]:
        make_dir(d)
    if args.consensus and args.germs:
        germs = parse_germs(args.germs)
    else:
        germs = args.germs
    # check whether JSON files have been passed
    if args.jsons is not None and all([args.db is None, args.collections is None]):
    	if os.path.isfile(args.jsons) and args.jsons.endswith('.json'):
    		collections = [args.jsons, ]
    	else:
        	collections = list_files(args.jsons, extension='json')
        db = None
    # otherwise, get sequences from MongoDB
    else:
        db = mongodb.get_db(args.db, args.ip, args.port, args.user, args.password)
        collections = mongodb.get_collections(db, collection=args.collection)
    for collection in collections:
        collection_start = time.time()
        print_collection_info(collection)
        if args.non_redundant:
            seqs = get_seqs(db, collection, args, make_seq_db=False)
            unique_file = unix_sort_unique(seqs, args)
            write_nr_output(collection, unique_file, collection_start, args)
        elif args.uaid:
            seq_db = get_seqs(db, collection, args)
            uaid_clusters = cdhit_clustering(seq_db, args)
            if args.consensus:
                sequences, sizes = get_consensus(uaid_clusters, germs, args)
            else:
                sequences, sizes = get_uaid_centroids(uaid_clusters, args)
        else:
            seq_db = get_seqs(db, collection, args)
            if args.consensus:
                seq_clusters, sizes = cdhit_clustering(seq_db, args, uaid=False)
                sequences, sizes = get_consensus(seq_clusters, germs, args)
            else:
                filtered_seqs = []
                filtered_sizes = []
                sequences, sizes = cdhit_clustering(seq_db, args, uaid=False, centroid=True)
                for seq, size in zip(sequences, sizes):
                    if size >= args.min_seqs:
                        filtered_seqs.append(seq)
                        filtered_sizes.append(size)
                sequences = filtered_seqs
                sizes = filtered_sizes
        if not args.non_redundant:
            write_output(collection, sequences, sizes, collection_start, args)
            remove_sqlite_db(args)


if __name__ == '__main__':
    parser = parse_args()
    args = parser.parse_args()
    logfile = args.log if args.log else os.path.join(args.output, 'abcorrect.log')
    log.setup_logging(logfile)
    logger = log.get_logger('abcorrect')
    main(args)
