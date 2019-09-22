import os
import re

fin=open("ALBUM_DIRS.list.out","r");
lines=fin.readlines();
fin.close();
original_oneoff_lines=map(lambda x:x.replace("\n",""),lines);  # remove new lines

# print original_oneoff_lines

fancy_sad_lines_mp3_only = [];

for x in original_oneoff_lines:
	os.system("ls \""+x+"\" > count.out")
	fin = open("count.out");
	filenames = map(lambda x:x.replace("\n",""), fin.readlines());  # remove new lines
	if(len(filenames) == 1):
		print x, filenames[0]
		album_name = x.split("/")[-1];
		fancy_sad_lines_mp3_only.append(
			[x+"/"+filenames[0], "one_off/"+album_name+" - "+filenames[0]]
			)
	#print x, subprocess.check_output(["ls","\""+x+"\""])

	# print x, subprocess.check_output(["ls","\""+x+"\"","|","wc","-l"])
		
	
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
