# -*- coding: utf-8 -*-
""" Entry point for console fastproject script

This module parses arguments and places in the Global module

Then launches the main pipeline
"""

from __future__ import absolute_import, print_function, division;
from . import Global;
import argparse;


def parseFPArgs():
    """Defines the command-line arguments and parses the FastProject call

    Returns
    -------
    argparse.Namespace

    """
    parser = argparse.ArgumentParser(prog="FastProject", description='Analyze a set of expression data with FastProject.');

    parser.add_argument("data_file", help="Input expression data matrix");

    parser.add_argument("-k", "--housekeeping", metavar="FILE", default="",
                      help="Read list of housekeeping genes from FILE.  Uses default list if not specified");

    parser.add_argument("-s", "--signatures", metavar="FILE", nargs='*',
                      help="Loads signatures from FILE.");

    parser.add_argument("-p", "--precomputed", metavar="FILE", nargs='*',
                      help="Loads precomputed signature scores from FILE.");

    parser.add_argument("-o", "--output", metavar="DIRECTORY",
            help="Name of output directory.  Otherwise, output directory is auto-generated");

    parser.add_argument("--nofilter",   action="store_true",
            help="Project using all genes.");

    parser.add_argument("--nomodel",   action="store_true",
            help="No estimation of expression probability or false negative probability");

    parser.add_argument("--pca_filter", action="store_true",
            help="Filters PC principal components that correlate with a calculated QC metric for each sample");

    parser.add_argument("--qc",         action="store_true",
            help="Performs a quality check on samples, filtering samples that do not pass");

    parser.add_argument("--all_sigs",         action="store_true",
            help="Do not remove insignificant signatures from output.");

    parser.add_argument("--debug",         action="store_true",
            help="Run FastProject in Debug mode");

    parser.add_argument("--lean",         action="store_true",
            help="Run FastProject in Lean mode - subset of analyses to reduce runtime on large data sets");

    parser.add_argument("--subsample_size", type=int, metavar="N", default=1000,
            help="Planned Feature: Number of samples to use when sub_sampling");

    parser.add_argument("--min_signature_genes", type=int, metavar="N", default=5,
            help="Signatures that match less than N genes in the data are discarded");

    parser.add_argument("--projections", metavar="FILE", nargs='*',
                        help="Loads projection coordinates from FILE");

    parser.add_argument("--weights", metavar="FILE",
                        help="Loads weights from FILE. Use these weights instead of FastProject's FNR calculation");

    parser.add_argument("--threshold", metavar="N", type=int,
                        help="Removes transcripts detected in less than N samples. " +
                        "Default is 20%% of total sample count.")

    parser.add_argument("--sig_norm_method",
        choices=["none", "znorm_columns", "znorm_rows",
            "znorm_rows_then_columns", "rank_norm_columns"],
        default="znorm_rows",
        help="Pick a normalization method to be applied to data before evaluating signature scores");

    parser.add_argument("--sig_score_method",
        choices=["naive", "weighted_avg", "imputed", "only_nonzero"],
        default="weighted_avg",
        help="Pick a method to evaluate signature scores");

    args = parser.parse_args();

    return args;


def entry():
    """Entry point for the fastproject command-line script
    """
    args = parseFPArgs();
    Global.args = args;

    from . import Pipelines;
    try:
        Pipelines.FullOutput();
    except:
        import traceback;
        import sys;
        traceback.print_exc();

        tb_type, value, tb = sys.exc_info();

        if(args.debug):
            import pdb;
            pdb.post_mortem(tb);


if(__name__ == "__main__"):
    entry();
