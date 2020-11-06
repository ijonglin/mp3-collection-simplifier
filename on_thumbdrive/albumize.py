import os
import re


def read_filename_list(filename):
    with open(filename, "r") as fin:
        lines = fin.readlines()
        return list(map(lambda x: x.replace("\n", ""), lines))


def wrap_into_albums_and_recode(lines, recode_bitrate):
    for x in lines:
        album_name = x.split('/')[-1]
        artist_name = x.split('/')[-2]
        cmd_song_dir = '/'.join(map(lambda y: "\"" + y + "\"", x.split('/')))
        cmd_album_dir = '/'.join(map(lambda y: "\"" + y + "\"", x.split('/')[:-1]))
        cmd = "mp3wrap  " + cmd_album_dir + "/\"" + album_name + ".album.mp3\" " + cmd_song_dir + "/*.mp3"
        song_title = "Album: " + album_name
        tag_cmd = "id3v2 -a \"" + artist_name + "\" -A \"" + song_title + "\" -t \"" + song_title + "\" " \
                  + cmd_album_dir + "/\"" + album_name + ".album_MP3WRAP.mp3\""
        unwrap_cmd = "cd " + cmd_album_dir + ";rm -f \"" + album_name + ".album.mp3\"" + ";ffmpeg -i  \"" \
                     + album_name + ".album_MP3WRAP.mp3\"  -ab "+recode_bitrate+" \"" + album_name + ".album.mp3\""
        clean_cmd = "rm -rf  " + cmd_song_dir
        if os.path.isdir(cmd_song_dir.replace("\"", "")):
            print(cmd)
            os.system(cmd)
            print(clean_cmd)
            os.system(clean_cmd)
        else:
            print("Skipped wrapping of songs-> " + cmd_song_dir + " doesn't exist")
        wrapped_filename = (cmd_album_dir + "/\"" + album_name + ".album_MP3WRAP.mp3\"").replace("\"", "")
        if os.path.exists(wrapped_filename):
            print(tag_cmd)
            os.system(tag_cmd)
            print(unwrap_cmd)
            os.system(unwrap_cmd)
            os.remove(wrapped_filename)
        else:
            print("Skipped unwrap -> " + wrapped_filename + " doesn't exist")


def consolidate_one_song_albums(lines, recode_bitrate, name_of_one_song_dir='one_off'):
    global fin
    fancy_sad_lines_mp3_only = []
    os.system('mkdir -p '+name_of_one_song_dir)
    for x in lines:
        os.system("ls \"" + x + "\" > count.out")
        fin = open("count.out")
        filenames = list(map(lambda y: y.replace("\n", ""), fin.readlines()))  # remove new lines
        if (len(filenames) == 1):
            print(x, filenames[0])
            album_name = x.split("/")[-1]
            fancy_sad_lines_mp3_only.append(
                [x + "/" + filenames[0], name_of_one_song_dir+ "/" + album_name + " - " + filenames[0]]
            )
    # print x, subprocess.check_output(["ls","\""+x+"\""])
    # print x, subprocess.check_output(["ls","\""+x+"\"","|","wc","-l"])
    # then go ahead and make all the copies.
    for x in range(0, len(fancy_sad_lines_mp3_only)):
        src = fancy_sad_lines_mp3_only[x][0]
        dest = fancy_sad_lines_mp3_only[x][1]
        is_mp3 = re.search("\.mp3$", dest) and False
        if is_mp3:
            cmd = "mv \"" + src + "\" \"" + dest + "\""
        else:
            dest_split = dest.split(".")
            dest_split[-1] = "mp3"
            dest = '.'.join(dest_split)
            cmd = "ffmpeg -i \"" + src + "\" -ab "+recode_bitrate+" \"" + dest + "\""

        print("[" + str(x) + "/" + str(len(fancy_sad_lines_mp3_only)) + "] " + cmd)
        os.system(cmd)


if __name__ == '__main__':
    original_fancy_lines = read_filename_list('albums_list.out')
    print(original_fancy_lines)
    # First remove the one song albums
    common_bitrate = '140k'
    consolidate_one_song_albums(original_fancy_lines, common_bitrate)
    wrap_into_albums_and_recode(original_fancy_lines, common_bitrate)

