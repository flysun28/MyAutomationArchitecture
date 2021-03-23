#!/usr/local/bin/python2.7
# encoding: utf-8
'''
@author:     80319739
@copyright:  2021 OPPO. All rights reserved.
'''

import sys
import os
import time
import pytest
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from lib.common.exception.intf_exception import CLIError

__all__ = []
__version__ = 1.0
__updated__ = time.strftime('%Y-%m-%d', time.localtime())

DEBUG = 0
TESTRUN = 0
PROFILE = 0
    

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s
  
  Copyright 2021 OPPO. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
e.g. python main_cli.py
e.g. python main_cli.py -i smoke -T interface -R inland -S http
e.g. python main_cli.py -T interface -R inland -S http -I simplepay
''' %program_shortdesc

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-i", "--include", dest="include", 
                            choices=['smoke', 'functional', 'positive', 'negative', 'inland', 'overseas'], 
                            help="only include tags to run, comma separated.")
        parser.add_argument("-e", "--exclude", dest="exclude", help="exclude tags not to run, comma separated.") #, metavar="RE" 
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-T', '--case-type', dest='case_type', choices=['interface', 'scenario'])        
        parser.add_argument('-R', '--region', dest='region', choices=['inland', 'overseas'])        
        parser.add_argument('-S', '--schema', dest='schema', choices=['http', 'dubbo'])
        parser.add_argument('-I', '--interface', dest='interface', help="the interface name, usually it's the last section of a URL")
        parser.add_argument('-f', '--instantfail', dest='instantfail', action='store_true', 
                            help='show failures and errors instantly as they occur, [default: %(default)s]')
        parser.add_argument('-x', '--exitonfail', action='store_true', help='exit instantly on first error or failed test.')
        # Process arguments
        args = parser.parse_args()
        inpat = args.include
        expat = args.exclude
        case_type = args.case_type
        region = args.region
        intf_name = args.interface
        schema = args.schema
        instantfail = args.instantfail
        exitonfail = args.exitonfail
        if inpat and expat and inpat == expat:
            raise CLIError("include and exclude pattern are equal! Nothing will be processed.")
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise e
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2
    else:
        pytest_opts = ['-vs', '--ff', '--cov='+os.getcwd(), '--cov-report=html', 
                       r'--html=%s\report\report_%s.html' %(os.getcwd(), __updated__),
                       '--timeout=300'] #'--lf'
        if instantfail:
            pytest_opts.append('-f')
        if exitonfail:
            pytest_opts.append('-x')
        markers = ''
        if inpat:
            markers += ' and '.join(inpat.split(','))
        if expat:
            markers += ' and not '.join(expat.split(','))
        if markers:
            pytest_opts += ['-m', markers]
        if intf_name:
            pytest_opts += ['-k', ' or '.join(intf_name.split(','))]
        path = os.getcwd()
        if case_type:
            path = os.path.join(path, case_type)
            if region:
                path = os.path.join(path, region)
                if schema:
                    path = os.path.join(path, schema)
        pytest_opts.append(path)
        print(pytest_opts)
        pytest.main(pytest_opts)
        return 0


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'case.main_cli_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "w")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())

