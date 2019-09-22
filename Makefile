list:
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.mp4" > FANCYCAR.list.out
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.mp3" >> FANCYCAR.list.out
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.m4a" >> FANCYCAR.list.out

short_list:
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.mp4" | head -3 > FANCYCAR.list.out
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.mp3" | head -3 >> FANCYCAR.list.out
	find /home/ijonglin/BACKUP/D512/MP3s -name "*.m4a" | head -3 >> FANCYCAR.list.out

run: 
	python fancy2sad_listing.py

check:
	find /home/ijonglin/BACKUP/MP3_thumb -exec ls -l {} \;

clean:
	rm -rf /home/ijonglin/BACKUP/MP3_thumb/

install:
	sudo apt-get install python python-pip ffmpeg
	pip install Unidecode
