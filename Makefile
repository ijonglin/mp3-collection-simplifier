all: clean list run

list:
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.mp4" > FANCYCAR.list.out
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.mp3" >> FANCYCAR.list.out
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.m4a" >> FANCYCAR.list.out

short_list:
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.mp4" | head -3 > FANCYCAR.list.out
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.mp3" | head -3 >> FANCYCAR.list.out
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.m4a" | head -3 >> FANCYCAR.list.out

run:
	python3.7 fancy2sad_listing.py

check:
	find /home/ijonglin/BACKUP/MP3_thumb -exec ls -l {} \;

clean:
	rm -rf /home/ijonglin/BACKUP/MP3_thumb/

do_setup:
	cp -rp /home/ijonglin/BACKUP/MP3-thumb /home/ijonglin/BACKUP/MP3-thumb-albums
	cp albumize.py one_offs.py Makefile /home/ijonglin/BACKUP/MP3-thumb-albums
	cd /home/ijonglin/MP3-thumb-albums; make

install:
	sudo apt-get install python python-pip ffmpeg
	pip install Unidecode
