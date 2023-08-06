#!/usr/bin/env python

# Copyright (c) 2016. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Translate each non-synonymous coding variants into possible mutant protein
sequences using an RNAseq BAM from the same tissuie.
"""

from __future__ import print_function, division, absolute_import

import argparse

import varcode
from pysam import AlignmentFile

from isovar.args import add_somatic_vcf_args, add_rna_args
from isovar.translation import translate_variants_dataframe
from isovar.default_parameters import (
    MIN_TRANSCRIPT_PREFIX_LENGTH,
    MAX_REFERENCE_TRANSCRIPT_MISMATCHES,
    PROTEIN_SEQUENCE_LENGTH,
)


parser = argparse.ArgumentParser()
parser = add_somatic_vcf_args(parser)
parser = add_rna_args(parser)

parser.add_argument(
    "--protein-sequence-length",
    default=PROTEIN_SEQUENCE_LENGTH,
    type=int)

parser.add_argument(
    "--max-reference-transcript-mismatches",
    type=int,
    default=MAX_REFERENCE_TRANSCRIPT_MISMATCHES)

parser.add_argument(
    "--min-transcript-prefix-length",
    type=int,
    default=MIN_TRANSCRIPT_PREFIX_LENGTH,
    help=(
        "Number of nucleotides before the variant we try to match against "
        "a reference transcript. Values greater than zero exclude variants "
        "near the start codon of transcripts without 5' UTRs."))

parser.add_argument(
    "--output",
    default="isovar-translate-variants-results.csv",
    help="Name of CSV file which contains predicted sequences")

if __name__ == "__main__":
    args = parser.parse_args()

    print(args)

    variants = varcode.load_vcf(
        args.vcf,
        genome=args.genome)

    samfile = AlignmentFile(args.bam)
    df = translate_variants_dataframe(
        variants=variants,
        samfile=samfile,
        protein_sequence_length=args.protein_sequence_length,
        min_reads_supporting_rna_sequence=args.min_reads,
        min_transcript_prefix_length=args.min_transcript_prefix_length,
        max_transcript_mismatches=args.max_reference_transcript_mismatches)
    print(df)
    df.to_csv(args.output)
