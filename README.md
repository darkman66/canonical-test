# canonical-test


The program should parse the file and output the statistics of the top 10 packages that have the most files associated with them.

An example output could be:

./package_statistics.py amd64

1. <package name 1> <number of files>
2. <package name 2> <number of files>
......
10. <package name 10> <number of files>

You can use the following Debian mirror

# Installation

To install locally you need to have

* Pyton 3.7
* pipenv

Once above is done install requirements:

    pipenv --python 3.7
    pipenv shell
    pipenv instal

When there are issues with using pipenv you can install with pip below packages

    nose = "==1.3.7"
    mock = "*"
    ipython = "*"
    requests = "*"
    nose-progressive = "*"

# Usage

To get help with script usage just do as follows:

    python package_statistics.py -h

    Usage: package_statistics.py [options]

    Options:
      -h, --help       show this help message and exit
      --mirror=MIRROR
      --arch=ARCH
      --level=LEVEL
      --cache          Use local cache

Example usage (downloading and analuzing amd64)

    python package_statistics.py --cache --arch arm64

Using option `cache` means that if you rerun script it will use donloaded file from mirron in local /var/tmp folder.

If you want to get more verbose output use `--level=debug`

# Testing

To test script just use nose, ie.

    nosetests tests

That is going to give you overview of number of tests performed and potential fails :)

# Tools

Basically I used barebone Python 3.7 with a bit of support of requets (to make my life easier).

# Sacrifices

1. Script does not use parallel processing to analyze and sort results.
2. Instead of lame and slow loop Regexp is being used:
    * getting only repeated package names in Contents file
    * counting occurrences of same package name in list
    * desc sorting number of repetitions

# Time spent

Total time spend on exercise ~ 2h

