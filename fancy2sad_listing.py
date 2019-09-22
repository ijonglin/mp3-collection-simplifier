import re;
import os;
import sys;
import unicodedata;
from unidecode import unidecode;

fin=open("FANCYCAR.list.out","r");
lines=fin.readlines();
fin.close();
original_fancy_lines=map(lambda x:x.replace("\n",""),lines);  # remove new lines
fancy_sad_lines=map(lambda x:[x,x],original_fancy_lines);  # make a mapping of these dirs

def map_to_sad_only(f_to_apply,combo_lines):
	return map(lambda x: [x[0], f_to_apply(x[1])] ,combo_lines);

def filter_to_sad_only(f_to_apply,combo_lines):
	return filter(lambda x: f_to_apply(x[1]) ,combo_lines);

# change root directory
fancy_sad_lines_pass1=map_to_sad_only(lambda x:x.replace("D512/MP3s","MP3_thumb"),fancy_sad_lines);

def clean_unicode(theString):
	theUString = unicodedata.normalize('NFKD',unicode(theString,errors='replace'));
	return unidecode(theUString);

def valid_jvc_string(theString):
	# print "I'm trying to clean up:"+theString;
	return '/'.join(map(lambda x:clean_unicode(x), theString.split('/')));

# remove unicode characters.
fancy_sad_lines_pass2=map_to_sad_only(lambda x:valid_jvc_string(x),fancy_sad_lines_pass1);  # remove unicode characters

def no_substring_over(theString,theMaxLength):
	theString=theString.replace(" ","_");
	theString=theString.replace("?","_");
	fields=theString.split("/");
	if len(fields)==7:
		fields= fields[0:4]+[(fields[4][0:12]+"-"+fields[5][0:12]+"-"+fields[6])];
		fields[-1]=fields[-1].replace("Compilations-","");

	def chop_to_n(theString,theMaxLength):
		if(len(theString)>theMaxLength):
			is_mp3=re.search("\.mp3$",theString);
			if is_mp3:
				return theString[0:(theMaxLength-4)]+".mp3"
			else:
				return theString[0:theMaxLength];
		else:
			return theString;
	fields=map(lambda x:chop_to_n(x,theMaxLength), fields);
	return "/".join(fields);

# make sure each substring is less than 60 chars
#fancy_sad_lines_pass3=map_to_sad_only(lambda x:no_substring_over(x,60),fancy_sad_lines_pass2);
#fancy_sad_lines_pass3.sort(key=lambda x:x[1]);
fancy_sad_lines_pass3 = fancy_sad_lines_pass2

# filter out only the things that you need to copy
fancy_sad_lines_mp3_only=filter_to_sad_only(lambda x:re.search("\/.*\.mp3$",x), fancy_sad_lines_pass3);
#print fancy_sad_lines_mp3_only[0:30];
fancy_sad_lines_mp3_only=fancy_sad_lines_pass3

######
#  Need to organize these mp3 into a directory structure
#  where there are less than 255 directories
#  AND there are no more than 255 files in any one directory.
######

fancy_sad_dir_mapping={};
for x in fancy_sad_lines_mp3_only:
	dir_name='/'.join(x[1].split('/')[:-1])
	try:
		fancy_sad_dir_mapping[dir_name].append(x);
	except KeyError:
		# probably no key.
		fancy_sad_dir_mapping[dir_name]=[x];

#print fancy_sad_dir_mapping;

print "Creating directory structure:"
for x in sorted(fancy_sad_dir_mapping.keys()):
	cmd="mkdir -p "+x;
	print "Running: "+cmd;
	os.system("mkdir -p \""+x+"\"");

# then go ahead and make all the copies.
for x in range(0,len(fancy_sad_lines_mp3_only)):
	src=fancy_sad_lines_mp3_only[x][0];
	dest=fancy_sad_lines_mp3_only[x][1];
	is_mp3=re.search("\.mp3$",dest);
	if is_mp3:
		cmd="cp \""+src+"\" \""+dest+"\"";
	else:
		dest_split = dest.split(".");
		dest_split[-1] = "mp3";
		dest = '.'.join(dest_split)
		cmd="ffmpeg -i \""+src+"\" -ab 192k \""+dest+"\"";

	print "["+str(x)+"/"+str(len(fancy_sad_lines_mp3_only))+"] "+cmd;
	os.system(cmd);
