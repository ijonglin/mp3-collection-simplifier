import re;
import os;
import sys;
import unicodedata;
from unidecode import unidecode;

fin=open("albums_list.out","r");
lines=fin.readlines();
fin.close();

original_fancy_lines=map(lambda x:x.replace("\n",""),lines);  # remove new lines

print original_fancy_lines;
for x in original_fancy_lines:
	albumName = x.split('/')[-1];
	artistName = x.split('/')[-2];
	cmd_song_dir =  '/'.join(map(lambda y : "\"" +y+"\"", x.split('/')));
	cmd_album_dir =  '/'.join(map(lambda y : "\"" +y+"\"", x.split('/')[:-1]));
	cmd = "mp3wrap  "+cmd_album_dir+"/\""+albumName+".album.mp3\" "+cmd_song_dir+"/*.mp3"
	song_title = "Album: "+ albumName
	tag_cmd = "id3v2 -a \""+artistName+"\" -A \""+song_title+"\" -t \""+song_title+"\" "+cmd_album_dir+"/\""+albumName+".album_MP3WRAP.mp3\""
	unwrap_cmd = "cd "+cmd_album_dir+";rm -f \"" + albumName+".album.mp3\""+";ffmpeg -i  \"" + albumName+".album_MP3WRAP.mp3\"  -ab 192k \"" + albumName+".album.mp3\""
	clean_cmd = "rm -rf  "+cmd_song_dir;
        if os.path.isdir(cmd_song_dir.replace("\"","")):
            print cmd;
	    os.system(cmd);
	    print clean_cmd;
	    os.system(clean_cmd);
        else:
            print "Skipped wrapping of songs-> "+cmd_song_dir+" doesn't exist"
        wrapped_filename = (cmd_album_dir+"/\""+albumName+".album_MP3WRAP.mp3\"").replace("\"","")
        if os.path.exists(wrapped_filename):
	    print tag_cmd;
	    os.system(tag_cmd);
	    print unwrap_cmd;
	    os.system(unwrap_cmd);
            os.remove(wrapped_filename);
        else:
            print "Skipped unwrap -> "+wrapped_filename+" doesn't exist"
