#!/usr/bin/env python3
# A black box that generates md5 strings for a given file

import argparse
import os
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument('--file', required=True)
parser.add_argument('--work_dir', required=True)
args = parser.parse_args()

output_filename = 'run_' + ''.join(random.choice(string.ascii_letters) for i in range(8))
print('Writing to ' + output_filename)
print(args.work_dir)
with open(os.path.join(args.work_dir, output_filename), 'w') as out:
    out.write(args.file + "\n")
    out.write(''.join(random.choice(string.hexdigits) for i in range(32)))
