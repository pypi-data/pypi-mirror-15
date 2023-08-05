"""Command line scripts"""
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import csv
import fnmatch
import os
import sys
import time

import appdirs

from . import __about__ as about
from . import Resolwe


ORGANISMS = {
    'HUMAN': 'Homo sapiens',
    'HOMO SAPIENS': 'Homo sapiens',
    'MOUSE': 'Mus musculus',
    'MUS MUSCULUS': 'Mus musculus',
    'DICTY': 'Dictyostelium discoideum',
    'DICTYOSTELIUM DISCOIDEUM': 'Dictyostelium discoideum',
}

EXPERIMENT_TYPE = {
    'RNA-SEQ': 'RNA-Seq',
    'MIRNA-SEQ': 'miRNA-Seq',
    'NCRNA-SEQ': 'ncRNA-Seq',
    'RNA-SEQ (CAGE)': 'RNA-Seq (CAGE)',
    'RNA-SEQ (RAGE)': 'RNA-Seq (RACE)',
    'CHIP-SEQ': 'ChIP-Seq',
    'MNASE-SEQ': 'MNase-Seq',
    'MBD-SEQ': 'MBD-Seq',
    'MRE-SEQ': 'MRE-Seq',
    'BISULFITE-SEQ': 'Bisulfite-Seq',
    'BISULFITE-SEQ (REDUCED REPRESENTATION)': 'Bisulfite-Seq (reduced representation)',
    'MEDIP-SEQ': 'MeDIP-Seq',
    'DNASE-HYPERSENSITIVITY': 'DNase-Hypersensitivity',
    'TN-SEQ': 'Tn-Seq',
    'FAIRE-SEQ': 'FAIRE-seq',
    'SELEX': 'SELEX',
    'RIP-SEQ': 'RIP-Seq',
    'CHIA-PET': 'ChIA-PET',
    'OTHER': 'OTHER',
}


def sequp():
    """Auto-upload NGS reads from directory to the Resolwe server.

    Script checks if there are new reads or annotation files in the
    target directory tree. If both: reads and corresponding annotation
    files are present, upload the reads and set the initial annotation
    based on the annotation file.

    We want to upload files which have not been uploaded yet. We need
    to know the most recent modification date of all uploaded files.
    Files modiffied later are upload candidates. The timestamp of last
    modification time is stored in config_file.

    """

    # XXX: Saving the config_file in user_data_dir is probably not the
    # right decision. We want multiple users to be able to upload data
    # to the same directory - therefore the config_file should be set
    # for the system and not user dependant.

    # Application data
    config_file = os.path.join(appdirs.user_data_dir(about.__title__, about.__author__), 'config')

    # XXX: Increase to 1h
    change_time_window = 5

    parser = argparse.ArgumentParser(description='Auto-upload NGS reads from '
                                     'directory to the Resolwe server.')

    parser.add_argument('-a', '--address', help='Resolwe server address')
    parser.add_argument('-e', '--email', help='User e-mail')
    parser.add_argument('-p', '--password', help='User password')
    parser.add_argument('-d', '--directory', help='Observed directory with reads')
    parser.add_argument('-f', '--force', action='store_true', help='Force upload of all files')

    args = parser.parse_args()

    genialis_url = args.address or os.getenv('GENIALIS_URL') or 'http://localhost:8000'
    genialis_email = args.email or os.getenv('GENIALIS_EMAIL') or 'admin'
    genialis_pass = args.password or os.getenv('GENIALIS_PASS') or 'admin'
    genialis_seq_dir = args.directory or os.getenv('GENIALIS_SEQ_DIR') or os.path.expanduser('~')

    print('Address:', genialis_url)
    print('User:', genialis_email)
    print('Pass:', genialis_pass)
    print('Directory:', genialis_seq_dir)

    if args.force and os.path.isfile(config_file):
        os.remove(config_file)

    def get_timestamp():
        """Get the timestamp for GENIALIS_SEQ_DIR"""
        data = {}
        # If file present
        if os.path.isfile(config_file):
            with open(config_file, 'r') as file_:
                for line in file_:
                    parts = line.strip().split('\t')
                    data[parts[0]] = float(parts[1])
            if genialis_seq_dir in data:
                return data[genialis_seq_dir]
            else:
                # File created, no entry, upload all files
                return 0

        # File not present, first iteration, upload all files
        else:
            return 0

    def set_timestamp(timestamp):
        """Set timestamp for GENIALIS_SEQ_DIR"""

        def write_timestamp(pairs):
            """Write the timestamp into appropriate file"""
            with open(config_file, 'w') as file_:
                for first, second in pairs.items():
                    file_.write(str(first) + '\t' + str(second) + '\n')

        # If file exists, rewrite
        if os.path.isfile(config_file):
            pairs = get_timestamp()
            pairs[genialis_seq_dir] = timestamp
            write_timestamp(pairs)

        # If file does not exist, create file and put in the data
        else:
            try:
                os.makedirs(os.path.dirname(config_file))
                write_timestamp({genialis_seq_dir: timestamp})
            except OSError:
                # Folder already exists, make the file
                write_timestamp({genialis_seq_dir: timestamp})

    # Get timestamp
    timestamp = get_timestamp()

    # Find new reads
    all_new_read_files = []
    read_file_extensions = ['*.fastq', '*.fastq.gz', '*.fq', '*.fq.gz']

    for root, _, filenames in os.walk(genialis_seq_dir):
        for extension in read_file_extensions:
            for filename in fnmatch.filter(filenames, extension):
                path = os.path.join(root, filename)
                if os.path.getmtime(path) > timestamp:
                    all_new_read_files.append(path)

    # Determnine if the candidate files are fully uploaded by the
    # sequencer. The idea is that the file size does not change in a
    # defined time window (change_time_window).
    sizes1 = {f: os.path.getsize(f) for f in all_new_read_files}
    time.sleep(change_time_window)
    sizes2 = {f: os.path.getsize(f) for f in all_new_read_files}

    all_new_read_files_uploaded = [f for f in all_new_read_files if sizes1[f] == sizes2[f]]

    # Find all annotation files
    all_annotation_files = []
    annotation_file_extensions = ['*.csv', '*.txt', '*.tsv']
    for root, _, filenames in os.walk(genialis_seq_dir):
        for extension in annotation_file_extensions:
            for filename in fnmatch.filter(filenames, extension):
                all_annotation_files.append(os.path.join(root, filename))

    def parse_annotation_file(annotation_file):
        """Parse annotation file to list of annotation objects"""

        anns = {}
        # We use 'rU' mode to be able to read also files with '\r' chars
        with open(annotation_file, 'rU') as file_:
            try:
                reader = csv.DictReader([row for row in file_ if row[0] != '#'],
                                        delimiter=str('\t'))

                # One line is one annotation (one reads file)
                for row in reader:
                    # Capitalize dict keys
                    row.update({k.upper(): v for k, v in row.items()})

                    if 'FASTQ_PATH' in row:
                        seqfile = os.path.normpath(os.path.join(genialis_seq_dir,
                                                                row['FASTQ_PATH']))

                        if os.path.isfile(seqfile):
                            row['FASTQ_PATH'] = seqfile
                            anns[seqfile] = row

            except csv.Error:
                print("File type not supported", file=sys.stderr)
                exit(1)
        return anns

    # Write all annotations to single dict with reads filenames as keys
    annotations = {}
    for ann_file in all_annotation_files:
        annotations.update(parse_annotation_file(ann_file))

    # Connect to Resolwe server
    resolwe = Resolwe(genialis_email, genialis_pass, genialis_url)

    read_schemas = resolwe.api.descriptorschema.get(slug='reads')
    read_schema = read_schemas[0] if len(read_schemas) > 0 else None

    # Upload all files in all_new_read_files_uploaded with annotations
    uploaded_files = []
    for fn in set(set(annotations.keys()) & set(all_new_read_files_uploaded)):
        kwargs = {
            'name': annotations[fn]['SAMPLE_NAME']
        }

        if read_schema:
            kwargs['descriptor_schema'] = read_schema['slug']
            kwargs['descriptor'] = {
                'barcode': annotations[fn].get('BARCODE', None),
                'barcode_removed': True if annotations[fn].get('BARCODE_REMOVED', 'N').upper() == 'Y' else False,
                'instrument_type': annotations[fn].get('INSTRUMENT', None),
                'seq_date': annotations[fn].get('SEQ_DATE', None),
            }

        # Paired-end reads
        if annotations[fn]['PAIRED_END'] == 'Y' and annotations[fn]['FASTQ_PATH_PAIR']:
            kwargs['process_name'] = 'Upload paired-end NGS reads'
            kwargs['src1'] = fn
            kwargs['src2'] = os.path.join(genialis_seq_dir, annotations[fn]['FASTQ_PATH_PAIR'])

        # Single-end reads
        else:
            kwargs['process_name'] = 'Upload NGS reads'
            kwargs['src'] = fn

        response = resolwe.upload(**kwargs)

        if response.ok:
            uploaded_files.append(fn)

            # XXX: Filter collections by sample descriptor schema
            # sample_schemas = resolwe.api.descriptorschema.get(slug='sample')
            # sample_schemas = sample_schemas[0] if len(sample_schemas) > 0 else None
            data_id = response.json()['id']
            sample = resolwe.api.collection.get(data=data_id, )[0]

            if 'geo' not in sample['descriptor']:
                sample['descriptor']['geo'] = {}

            organism = ORGANISMS.get(annotations[fn]['ORGANISM'].upper(), '')
            if organism:
                sample['descriptor']['geo']['organism'] = organism

            experiment_type = EXPERIMENT_TYPE.get(annotations[fn]['SEQ_TYPE'].upper(), '')
            if experiment_type:
                sample['descriptor']['geo']['experiment_type'] = experiment_type

            resolwe.api.collection(sample['id']).patch({'descriptor': sample['descriptor']})

        else:
            print("Error uploading {}".format(fn), file=sys.stderr)
            print(response.text, file=sys.stderr)

    # Set the modification timestamp
    modif_times = [os.path.getmtime(f) for f in uploaded_files]
    if len(modif_times) > 0:
        set_timestamp(sorted(modif_times)[-1])


def readsup():
    """Upload NGS reads to the Resolwe server."""
    parser = argparse.ArgumentParser(description='Upload NGS reads to the Resolwe server.')

    parser.add_argument('collection', help='Collection ID')
    parser.add_argument('-a', '--address', default='http://cloud.genialis.com', help='Resolwe server address')
    parser.add_argument('-e', '--email', default='anonymous@genialis.com', help='User e-mail')
    parser.add_argument('-p', '--password', default='anonymous', help='User password')
    parser.add_argument('-r', metavar='READS', help='NGS fastq file')
    parser.add_argument('-r1', metavar='READS-1', help='NGS fastq file (mate 1)')
    parser.add_argument('-r2', metavar='READS-2', help='NGS fastq file (mate 2)')

    args = parser.parse_args()

    if not (args.r or (args.r1 and args.r2)) or (args.r and (args.r1 or args.r2)):
        parser.print_help()
        print("\nERROR: define either -r or -r1 and -r2.\n")
        exit(1)

    resolwe = Resolwe(args.email, args.password, args.address)

    if args.r:
        resolwe.upload(process_name='import:upload:reads-fastq', collections=[args.collection], src=args.r)
    else:
        resolwe.upload(process_name='import:upload:reads-fastq-paired-end',
                       collections=[args.collection], src1=args.r1, src2=args.r2)


def readsup_batch():
    """Upload a batch NGS reads to the Resolwe server."""
    parser = argparse.ArgumentParser(description='Upload a batch NGS reads to the Resolwe server.')

    parser.add_argument('collection', help='Collection ID')
    parser.add_argument('-a', '--address', default='http://cloud.genialis.com', help='Resolwe server address')
    parser.add_argument('-e', '--email', default='anonymous@genialis.com', help='User e-mail')
    parser.add_argument('-p', '--password', default='anonymous', help='User password')
    parser.add_argument('-r', metavar='READS', nargs='*', help='List of NGS fastq files')
    parser.add_argument('-r1', metavar='READS-1', nargs='*', help='List of NGS fastq files (mate 1)')
    parser.add_argument('-r2', metavar='READS-2', nargs='*', help='List of NGS fastq files (mate 2)')

    args = parser.parse_args()

    if not (args.r or (args.r1 and args.r2)) or (args.r and (args.r1 or args.r2)):
        parser.print_help()
        print("\nERROR: define either -r or -r1 and -r2\n")
        exit(1)

    if not args.r and len(args.r1) != len(args.r2):
        parser.print_help()
        print("\nERROR: -r1 and -r2 file list length must match\n")
        exit(1)

    resolwe = Resolwe(args.email, args.password, args.address)

    if args.r:
        for read_file in args.r:
            resolwe.upload(process_name='import:upload:reads-fastq', collections=[args.collection], src=read_file)
    else:
        for read_file1, read_file2 in zip(args.r1, args.r2):
            resolwe.upload(process_name='import:upload:reads-fastq-paired-end',
                           collections=[args.collection], src1=read_file1, src2=read_file2)
