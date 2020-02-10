# GitHub Data

## Data Source

The data for GitHub repositories has been extracted from
`ghtorrent.org`, a project which persists regularly public
information about GitHub repositories.

The latest available dump (`mysql-2019-06-01.tar.gz`) has been
taken and the files `projects.csv` and `issues.csv` were
analyzed.

The original TAR file from `ghtorrent.org` is 100GB large, and the
two original files are 23GB and 5.5GB large.
Therefore in this repository only a sample of a few
lines is provided.

## Filtering and Merging in _R_

As a first step, the data was filtered and merged, using an _R_ script.
This script is called `transform.R`.

Only original repositories (not forked ones)
were taken into account, and only those which have
been forked more than 50 times (as a measure of _importance_)
were looked at.

Similarly the issues per repository were counted.
Only repositories with at least one issue are considered.

This script creates a combined file, `repos_issues.csv`.

The output of a similar script, `transforma_sample.R`,
which uses a reduced set of projects / issues only
is collected in `repos_isues_sample.csv` - for this subset
no minimum number of forks is required.

## Creation of RDF Files

To create the RDF version of the data, a small Python script,
`RDFize.py`, has been used.

