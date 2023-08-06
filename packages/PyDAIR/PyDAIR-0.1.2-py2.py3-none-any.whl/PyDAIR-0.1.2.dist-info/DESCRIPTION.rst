|Build Status|

PyDAIR
======

PyDAIR is a Python package that aims to study immunoglobulin heavy (IGH)
chain diversity based on repertoire-sequencing (Rep-Seq) data using
high-throughput sequencing techonologies. PyDAIR identifies the germline
variable (V), diversity (D), and joining (J) genes that used by each IGH
sequence. BLAST is used for aligning sequences to a database of known
germline VDJ genes to assign VDJ. PyDAIR supports all features as long
as the two motifs that located at the end of V gene and the start of J
gene are know. PyDAIR is available under the terms of the GNU license.

INSTALLTION
-----------

PyDAIR requires Python 2.7 together with
`NumPy <http://www.numpy.org/>`__,
`Pandas <http://pandas.pydata.org/>`__,
`matplotlib <http://matplotlib.org/>`__, and
`BioPython <http://biopython.org/>`__ packages. Further, PyDAIR requires
`NCBI BLAST+ <https://www.ncbi.nlm.nih.gov/books/NBK279690/>`__ for
aligning IGH sequence to germline databases. PyDAIR is avaliable on the
`PyPI <https://pypi.python.org/pypi/PyDAIR>`__ repository, as well as
can be installed like any other Python package using ``pip`` command.

.. code:: bash

    pip install numpy --user
    pip install pandas --user
    pip install matplotlib --user
    pip install biopython --user
    pip install pydair --user

Installtion instructions for `NCBI
BLAST+ <https://www.ncbi.nlm.nih.gov/books/NBK279690/>`__ are available
on `NCBI website <https://www.ncbi.nlm.nih.gov/books/NBK279671/>`__.
User should follow the instruction to install `NCBI
BLAST+ <https://www.ncbi.nlm.nih.gov/books/NBK279690/>`__.

Usage
-----

PyDAIR has two main commands that are ``pydair-parseseq`` and
``pydair-analysis``.

+--------------------+-------------+
| Command            | Function    |
+====================+=============+
| pydair-parseseq    | Identificat |
|                    | ion         |
|                    | of V, D and |
|                    | J genes     |
|                    | that used   |
|                    | by each IGH |
|                    | sequence.   |
+--------------------+-------------+
| pydair-analysis    | Aggregation |
|                    | of the      |
|                    | frequencies |
|                    | of usage of |
|                    | V, D and J  |
|                    | genes, as   |
|                    | well as     |
|                    | extraction  |
|                    | of CDR-H3   |
|                    | sequences.  |
+--------------------+-------------+

``pydair-parseseq`` identifies V, D, and J genes from IGH each sequence
by aligning IGH sequence to germline (V, D, and J) database using NCBI
BLAST+. It requires IGH sequences, germline sequences, BLAST databases
of germiline sequences, and BLAST parameters. The sequences should be
given by FASTA format.

.. code:: bash

     pydair-parseseq -q input_igh_sequences.fa \
                     -v v.fa                   \
                     -d d.fa                   \
                     -j j.fa                   \
                     --v-blastdb blastdb_v     \
                     --d-blastdb blastdb_d     \
                     --j-blastdb blastdb_j     \
                     -o output1

PyDAIR generates several files to save the intermediate results, such as
BLAST results, region that cannot be aligned to V and J genes. The final
result is saved into ``output1.pydair`` file. If there several samples,
``pydair-parseseq`` should be run several times for each sample.

The statistical summaries are calculated by ``pydair-analysis`` command.

.. code:: bash

    pydair-analysis -i output1.pydair output2.pydair output3.pydair  \
                    -n Fugu1 Fugu2 Fugu3                             \
                    -o stats_result                                  \
                    --contain_ambiguous_D

.. |Build Status| image:: https://travis-ci.org/jqsunac/PyDAIR.svg?branch=master
   :target: https://travis-ci.org/jqsunac/PyDAIR


