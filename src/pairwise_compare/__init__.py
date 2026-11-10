"""Compare groups of data specified in a tidy pandas dataframe."""

from importlib.metadata import PackageNotFoundError, version

from pairwise_compare.comparators.Comparator import Comparator
from pairwise_compare.comparators.PearsonsCorrelation import PearsonsCorrelation
from pairwise_compare.comparison_tools.PairwiseCompareManager import compare_pairs

try:
    __version__ = version("pairwise-compare")
except PackageNotFoundError:  # running from a source tree that is not installed
    __version__ = "unknown"

__all__ = ["Comparator", "PearsonsCorrelation", "compare_pairs"]
