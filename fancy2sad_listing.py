import re
import os
import shutil
import sys
import time
import unicodedata
from unidecode import unidecode
from concurrent.futures import ThreadPoolExecutor
from slugify import slugify

# fin = open("FANCYCAR.list.out", "r", errors='replace')
fin = open("FANCYCAR.list.out", "r", encoding='ISO-8859-1', errors='replace')
lines = fin.readlines()
fin.close()
original_fancy_lines = map(lambda x: x.replace("\n", ""), lines);  # remove new lines
fancy_sad_lines = map(lambda x: [x, x], original_fancy_lines);  # make a mapping of these dirs


def map_to_sad_only(f_to_apply, combo_lines):
    return map(lambda x: [x[0], f_to_apply(x[1])], combo_lines)


def filter_to_sad_only(f_to_apply, combo_lines):
    return filter(lambda x: f_to_apply(x[1]), combo_lines)


# change root directory
fancy_sad_lines_pass1 = map_to_sad_only(lambda x: x.replace("D512/MP3s", "MP3_thumb"), fancy_sad_lines)


def clean_unicode(theString):
    theUString = unicodedata.normalize('NFKD', str(theString))
    return unidecode(theUString)


def valid_jvc_string(theString):
    # print "I'm trying to clean up:"+theString
    return '/'.join(map(lambda x: clean_unicode(x), theString.split('/')))


# remove unicode characters.
#fancy_sad_lines_pass2 = map_to_sad_only(lambda x: valid_jvc_string(x),
#                                        fancy_sad_lines_pass1);  # remove unicode characters
fancy_sad_lines_pass2 = fancy_sad_lines_pass1


def no_substring_over(theString, theMaxLength):
    fields = theString.split("/")
    if len(fields) == 7:
        fields = fields[0:4] + [(fields[4][0:12] + "-" + fields[5][0:12] + "-" + fields[6])]
        fields[-1] = fields[-1].replace("Compilations-", "")

    def local_slugify(substring):
        return slugify(substring, lowercase=False,
                       replacements=[
                           ['&', 'and'],
                           [';', '_'],
                           ['(', '_'],
                           [')', '_']
                       ])

    def chop_to_n(theString, theMaxLength):
        if theMaxLength > len(theString):
            theMaxLength = len(theString)
        is_mp3 = re.search("\.(mp3|mp4|m4a)$", theString)
        if is_mp3:
            return local_slugify(theString[0:(theMaxLength - 4)]) + is_mp3.group()
        else:
            return local_slugify(theString[0:theMaxLength])

    fields = map(lambda x: chop_to_n(x, theMaxLength), fields)
    return "/".join(fields)


# make sure each substring is less than 60 chars
fancy_sad_lines_pass3 = map_to_sad_only(lambda x: no_substring_over(x, 60), fancy_sad_lines_pass2)
# fancy_sad_lines_pass3.sort(key=lambda x:x[1])
# fancy_sad_lines_pass3 = fancy_sad_lines_pass2

# filter out only the things that you need to copy
fancy_sad_lines_mp3_only = filter_to_sad_only(lambda x: re.search("\/.*\.mp3$", x), fancy_sad_lines_pass3)
# print fancy_sad_lines_mp3_only[0:30]
fancy_sad_lines_mp3_only = list(fancy_sad_lines_pass3)

######
#  Need to organize these mp3 into a directory structure
#  where there are less than 255 directories
#  AND there are no more than 255 files in any one directory.
######

fancy_sad_dir_mapping = {}
for x in fancy_sad_lines_mp3_only:
    dir_name = '/'.join(x[1].split('/')[:-1])
    try:
        fancy_sad_dir_mapping[dir_name].append(x)
    except KeyError:
        # probably no key.
        fancy_sad_dir_mapping[dir_name] = [x]

# print fancy_sad_dir_mapping

print("Creating directory structure:")
for x in sorted(fancy_sad_dir_mapping.keys()):
    cmd = "mkdir -p " + x
    print("Running: " + cmd)
    os.system("mkdir -p \"" + x + "\"")

# then go ahead and make all the copies.
executor = ThreadPoolExecutor(24)


def task(cmd):
    os.system(cmd)


start = time.time()
future_list = []
fout = open('read_failures.log', "w")
for x in range(0, len(fancy_sad_lines_mp3_only)):
    src = fancy_sad_lines_mp3_only[x][0]
    dest = fancy_sad_lines_mp3_only[x][1]
    is_mp3 = re.search("\.mp3$", dest)

    def quote_closure(m):
        return "\""+m+"\""

    if is_mp3:
        cmd = "cp " + quote_closure(src) + " " + quote_closure(dest)
        try:
            shutil.copyfile(src, dest)
        except FileNotFoundError:
            print("Probably can't read the file: " + src)
            fout.write(src +"\n")
    else:
        dest_split = dest.split(".")
        dest_split[-1] = "mp3"
        dest = '.'.join(dest_split)
        cmd = "ffmpeg -loglevel warning -y -i " + quote_closure(src) + " -ab 192k " + quote_closure(dest)
        future_list.append(executor.submit(task, cmd))

    print("[" + str(x) + "/" + str(len(fancy_sad_lines_mp3_only)) + "] " + cmd)

print("All task submitted.  Waiting for the futures to finish")
fout.close()
while (len(future_list) > 0):
    print("*** Waiting for " + str(len(future_list)) + " to finish");
    future_list = list(filter(lambda x: not (x.done()), future_list))
    time.sleep(5)
end = time.time()
print("*** Finished after " + str(end - start) + "seconds.  Woot!")
