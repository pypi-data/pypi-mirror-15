============
mkpassphrase
============

.. image:: https://travis-ci.org/eukaryote/mkpassphrase.svg?branch=master
    :target: https://travis-ci.org/eukaryote/mkpassphrase

`mkpassphrase` is a commandline script (and an associated package) for
generating passphrases by concatenating words chosen from a dictionary file
that contains one word per line (such as the standard `/usr/share/dict/words`
on *nix systems. It generates passphrases like
``flippant Attests Ivory mildly Roamers`` by default and is highly
configurable.

Installation
------------

To install or upgrade to the latest stable version of `mkpassphrase` from PyPI,
you can install it as your normal user by running:

.. code-block:: shell-session

    $ pip install --user --upgrade mkpassphrase

On Linux, that installs `mkpasphrase` to `~/.local/bin`, which you may need to
add to your `$PATH`.

Or you can install it globally by running:

.. code-block:: shell-session

    $ sudo pip install --upgrade mkpassphrase


Usage
-----

Generate a passphrase using the default settings:

.. code-block:: shell-session

    $ mkpassphrase
    Twelfth Ninja cubist Pepsin cattle

    60,298 unique candidate words
    79-bit security level

The security level reported is based only on the number of words in the
passphrase and the number of possible words (as well as whether
the ``--lowercase`` option is chosen), and does not include other factors
such as padding or a custom delimiter, which would increase the security
level.

Options
-------

Use the `--help` option to see the available options::

    $ mkpassphrase --help
    usage: mkpassphrase [-h] [-n NUM_WORDS] [--min MIN] [--max MAX] [-f WORD_FILE]
                        [--lowercase] [--non-ascii] [-p PAD] [-d DELIM] [-t TIMES]
                        [-V] [-q]

    Generate a passphrase.

    optional arguments:
      -h, --help            show this help message and exit
      -n NUM_WORDS, --num-words NUM_WORDS
                            Number of words in passphrase
      --min MIN             Minimum word length
      --max MAX             Maximum word length
      -f WORD_FILE, --word-file WORD_FILE
                            Word file path (one word per line)
      --lowercase           Make each word entirely lowercase, rather than the
                            default behavior of choosing Titlecase or lowercase
                            for each word (with probability 0.5)
      --non-ascii           Whether to allow words with non-ascii letters
      -p PAD, --pad PAD     Pad passphrase using PAD as prefix and suffix
      -d DELIM, --delimiter DELIM
                            Use DELIM to separate words in passphrase
      -t TIMES, --items TIMES
                            Generate TIMES different passphrases
      -V, --version         Show version
      -q, --quiet           Print just the passphrase


Supported Python Versions and Operating Systems
-----------------------------------------------

mkpassphrase is tested under py27, py32, py33, py34, pypy, and pypy3 on Linux,
but should work on any OS that supports those Python versions.


=======
Changes
=======

v0.9.0
------

 * much faster generation of multiple passphrases using `-t`
 * minor verbiage tweaks for non-quiet output

v0.8.0
------

 * use cryptographically secure pseudo-random number generator if available
 * added standard imports to help with python2/3 compatibility

v0.7.0
------

 * added -t|--times N to allow generating multiple passphrases w/ one command

v0.6.8
------

 * include CHANGES.rst and README.rst in sdist via MANIFEST.in

v0.6.7
------

 * cosmetic changes for better PyPI display


v0.6.6
------

 * cosmetic changes for better PyPI display


v0.6.4
-------

 * cosmetic changes for better PyPI display


v0.6.2
------

 * added -q option to omit extra information about how many unique candidate
   words were found and how many passphrases were possible
 * fix for --ascii option not being used, and improved encoding handling
 * start documenting changes in CHANGES.rst
 * use README and CHANGES as long_description for improved pypi info


