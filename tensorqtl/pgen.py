# Functions for reading dosages from PLINK pgen files based on the Pgenlib Python API:
# https://github.com/chrchang/plink-ng/blob/master/2.0/Python/python_api.txt

import numpy as np
import pandas as pd
import pgenlib as pg


def read_pvar(pvar_path):
    """Read pvar file as pd.DataFrame"""
    return pd.read_csv(pvar_path, sep='\t', comment='#',
                       names=['chrom', 'pos', 'id', 'ref', 'alt', 'qual', 'filter', 'info'])


def read_psam(psam_path):
    """Read psam file as pd.DataFrame"""
    return pd.read_csv(psam_path, sep='\t', index_col=0)


def read_dosages(pgen_path, variant_idx, sample_subset=None, dtype=np.float32):
    """
    Get dosages for a variant.

    Parameters
    ----------
    pgen_path : str
        Path of PLINK 2 pgen file
    variant_idx : int
        Variant index
    sample_subset : array_like
        List of sample indexes to select. Must be sorted.
    dtype : np.float{32,64}
        Data type of the returned array.

    Returns
    -------
    dosages : ndarray
        Genotype dosages for the selected variant and samples.
    """
    if sample_subset is not None:
        sample_subset = np.array(sample_subset, dtype=np.uint32)
    with pg.PgenReader(pgen_path.encode(), sample_subset=sample_subset) as r:
        if sample_subset is None:
            num_samples = r.get_raw_sample_ct()
        else:
            num_samples = len(sample_subset)
        dosages = np.zeros(num_samples, dtype=dtype)
        r.read_dosages(np.array(variant_idx, dtype=np.uint32), dosages)
        return dosages


def read_alleles(pgen_path, variant_idx, sample_subset=None):
    """
    Get alleles for a variant.

    Parameters
    ----------
    pgen_path : str
        Path of PLINK 2 pgen file
    variant_idx : int
        Variant index
    sample_subset : array_like
        List of sample indexes to select. Must be sorted.

    Returns
    -------
    alleles: ndarray (2 * sample_ct)
        Alleles for the selected variant and samples.
        Elements 2n and 2n+1 correspond to sample n.
        Both elements are -9 for missing genotypes.
        If the genotype is unphased, the lower index appears first.
    """
    if sample_subset is not None:
        sample_subset = np.array(sample_subset, dtype=np.uint32)
    with pg.PgenReader(pgen_path.encode(), sample_subset=sample_subset) as r:
        if sample_subset is None:
            num_samples = r.get_raw_sample_ct()
        else:
            num_samples = len(sample_subset)
        alleles = np.zeros(2*num_samples, dtype=np.int32)
        r.read_alleles(np.array(variant_idx, dtype=np.uint32), alleles)
    return alleles


def read_dosages_list(pgen_path, variant_idxs, sample_subset=None, dtype=np.float32):
    """
    Get dosages for a list of variants.

    Parameters
    ----------
    pgen_path : str
        Path of PLINK 2 pgen file
    variant_idxs : array_like
        List of variant indexes
    sample_subset : array_like
        List of sample indexes to select. Must be sorted.
    dtype : np.float{32,64}
        Data type of the returned array.

    Returns
    -------
    dosages : ndarray
        Genotype dosages for the selected variants and samples.
    """
    if sample_subset is not None:
        sample_subset = np.array(sample_subset, dtype=np.uint32)
    with pg.PgenReader(pgen_path.encode(), sample_subset=sample_subset) as r:
        if sample_subset is None:
            num_samples = r.get_raw_sample_ct()
        else:
            num_samples = len(sample_subset)
        num_variants = len(variant_idxs)
        dosages = np.zeros([num_variants, num_samples], dtype=dtype)
        r.read_dosages_list(np.array(variant_idxs, dtype=np.uint32), dosages)
        return dosages


def read_alleles_list(pgen_path, variant_idxs, sample_subset=None):
    """
    Get alleles for a list of variants.

    Parameters
    ----------
    pgen_path : str
        Path of PLINK 2 pgen file
    variant_idxs : array_like
        List of variant indexes
    sample_subset : array_like
        List of sample indexes to select. Must be sorted.

    Returns
    -------
    alleles : ndarray
        Alleles for the selected variants and samples.
    """
    if sample_subset is not None:
        sample_subset = np.array(sample_subset, dtype=np.uint32)
    with pg.PgenReader(pgen_path.encode(), sample_subset=sample_subset) as r:
        if sample_subset is None:
            num_samples = r.get_raw_sample_ct()
        else:
            num_samples = len(sample_subset)
        num_variants = len(variant_idxs)
        alleles = np.zeros([num_variants, 2*num_samples], dtype=np.int32)
        r.read_alleles_list(np.array(variant_idxs, dtype=np.uint32), alleles)
        return alleles


def read_dosages_range(pgen_path, start_idx, end_idx, sample_subset=None, dtype=np.float32):
    """
    Get dosages for a range of variants.

    Parameters
    ----------
    pgen_path : str
        Path of PLINK 2 pgen file
    start_idx : int
        Start index of the range to query.
    end_idx : int
        End index of the range to query (inclusive).
    sample_subset : array_like
        List of sample indexes to select. Must be sorted.
    dtype : np.float{32,64}
        Data type of the returned array.

    Returns
    -------
    dosages : ndarray
        Genotype dosages for the selected variants and samples.
    """
    if sample_subset is not None:
        sample_subset = np.array(sample_subset, dtype=np.uint32)
    with pg.PgenReader(pgen_path.encode(), sample_subset=sample_subset) as r:
        if sample_subset is None:
            num_samples = r.get_raw_sample_ct()
        else:
            num_samples = len(sample_subset)
        num_variants = end_idx - start_idx + 1
        dosages = np.zeros([num_variants, num_samples], dtype=dtype)
        r.read_dosages_range(start_idx, end_idx+1, dosages)
        return dosages


def read_alleles_range(pgen_path, start_idx, end_idx, sample_subset=None):
    """
    Get alleles for a range of variants.

    Parameters
    ----------
    pgen_path : str
        Path of PLINK 2 pgen file
    start_idx : int
        Start index of the range to query.
    end_idx : int
        End index of the range to query (inclusive).
    sample_subset : array_like
        List of sample indexes to select. Must be sorted.

    Returns
    -------
    alleles : ndarray
        Alleles for the selected variants and samples.
    """
    if sample_subset is not None:
        sample_subset = np.array(sample_subset, dtype=np.uint32)
    with pg.PgenReader(pgen_path.encode(), sample_subset=sample_subset) as r:
        if sample_subset is None:
            num_samples = r.get_raw_sample_ct()
        else:
            num_samples = len(sample_subset)
        num_variants = end_idx - start_idx + 1
        alleles = np.zeros([num_variants, 2*num_samples], dtype=np.int32)
        r.read_alleles_range(start_idx, end_idx+1, alleles)
        return alleles


class Pgen(object):
    """

    To generate the pgen/psam/pvar files from a VCF, run
    plink2 --vcf ${vcf_file} 'dosage=DS' --output-chr chrM --out ${plink_prefix_path}
    """
    def __init__(self, plink_prefix_path, select_samples=None):

        self.pvar_df = read_pvar(f"{plink_prefix_path}.pvar")
        self.psam_df = read_psam(f"{plink_prefix_path}.psam")
        self.pgen_file = f"{plink_prefix_path}.pgen"

        self.num_variants = self.pvar_df.shape[0]
        self.variant_ids = self.pvar_df['id'].tolist()
        self.variant_idx_dict = {i:k for k,i in enumerate(self.variant_ids)}

        self.sample_id_list = self.psam_df.index.tolist()
        self.set_samples(select_samples)

    def set_samples(self, sample_ids=None, sort=True):
        """
        Set samples to load.

        Parameters
        ----------
        sample_ids : array_like
            List of samples to select.
        sort : bool
            Preserve sample order from pgen file.
        """
        if sample_ids is None:
            self.sample_ids = self.sample_id_list
            self.sample_idxs = None
        else:
            sample_idxs = [self.sample_id_list.index(i) for i in sample_ids]
            if sort:
                sidx = np.argsort(sample_idxs)
                sample_idxs = [sample_idxs[i] for i in sidx]
                sample_ids = [sample_ids[i] for i in sidx]
            self.sample_ids = sample_ids
            self.sample_idxs = sample_idxs

    def read_dosages_list(self, variant_ids, dtype=np.float32):
        variant_idxs = [self.variant_idx_dict[i] for i in variant_ids]
        dosages = read_dosages_list(self.pgen_file, variant_idxs, sample_subset=None, dtype=dtype)
        return pd.DataFrame(dosages, index=variant_ids, columns=self.sample_ids)

    def read_alleles_list(self, variant_ids):
        variant_idxs = [self.variant_idx_dict[i] for i in variant_ids]
        alleles = read_alleles_list(self.pgen_file, variant_idxs, sample_subset=self.sample_idxs)
        df1 = pd.DataFrame(alleles[:,::2], index=variant_ids, columns=self.sample_ids)
        df2 = pd.DataFrame(alleles[:,1::2], index=variant_ids, columns=self.sample_ids)
        return df1, df2

    def load_dosages_df(self):
        dosages = read_dosages_range(self.pgen_file, 0, self.num_variants-1, sample_subset=self.sample_idxs)
        return pd.DataFrame(dosages, index=self.pvar_df['id'], columns=self.sample_ids)


def load_dosages_df(plink_prefix_path, select_samples=None):
    """
    Load dosages for all variants and all/selected samples as a dataframe.

    Parameters
    ----------
    plink_prefix_path : str
        Prefix to .pgen/.psam/.pvar files
    select_samples : array_like
        List of sample IDs to select. Default: all samples.

    Returns
    -------
    dosages_df : pd.DataFrame (variants x samples)
        Genotype dosages for the selected samples.
    """
    p = Pgen(plink_prefix_path, select_samples=select_samples)
    return p.load_dosages_df()
