from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import matplotlib as mpl
mpl.use('Agg') # non-interactive
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
import os
import argparse
import sys
import datetime

class Logger(object):
    """
    Simple logger that can be used for saving plain print() statement output to
    an output file without performing full redirection. Pretty useful for
    testing. Install running:
        sys.stdout = Logger(my_path)
    """
    def __init__(self, path):
        self.console = sys.stdout
        self.log = open(path, "a")

    def write(self, message):
        self.console.write(message)
        self.log.write(message)  

    def flush(self):
        pass

    def close(self):
        self.log.close()

class AnalysisContext:
    """
    Simple analysis context manager for taking care of stuff like storing
    experiment output in a somewhat organized fashion. Because I hate ipython
    notebooks.

    Run like:
        with AnalysisContext("my_experiment") as experiment:
            # Log output will get saved even if your stuff crashes
            print("Doing some work")
            fig = plt.figure()
            # Do some plotting
            experiment.save_fig(fig, "My Figure")
    """
    def __init__(self, experiment_name, save_output=True):
        self.experiment_name = experiment_name
        self.save_output = save_output

        # Arg parsing
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--experiment_dir', default='./experiments')
        args = self.parser.parse_args()
        self.experiment_dir = args.experiment_dir

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        self.output_path = os.path.join(self.experiment_dir,
            experiment_name+"_"+timestamp)

        os.makedirs(self.output_path)

        # Output redirection
        if self.save_output:
            self.logger = Logger(os.path.join(self.output_path, "out.log"))

    def save_fig(self, fig, name, extension=".pdf"):
        fig.tight_layout()
        fname = str(name).replace(' ', '_')+extension
        fig.savefig(os.path.join(self.output_path, fname))

    def get_output_path(self):
        return self.output_path

    def get_experiment_path(self):
        return self.experiment_dir

    def get_parser(self):
        return self.parser

    def __enter__(self):
        print("----- Entering experiment context -----")

        # Style plots
        sns.set_style("whitegrid")

        # Wire up stdout
        if self.save_output:
            sys.stdout = self.logger

        return self

    def __exit__(self, type, value, traceback):
        # Undo stdout wiring
        if self.save_output:
            self.logger.close()
            sys.stdout = self.logger.console

        print("----- Leaving experiment context ------")
