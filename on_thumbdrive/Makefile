all: list albumize

all_short: short_list albumize

list:
	find `pwd` -maxdepth 2 -mindepth 2 -type d> albums_list.out

list_cleaned:
	find `pwd` -maxdepth 2 -mindepth 2 -name "*.album_MP3WRAP.mp3" | sed -e "s/.album_MP3WRAP.mp3//" > albums_list.out

short_list:
	find `pwd` -maxdepth 2 -mindepth 2 -type d | grep "Nga"  > albums_list.out

short_list_cleaned:
	find `pwd` -maxdepth 2 -mindepth 2 -name "*.album_MP3WRAP.mp3" | sed -e "s/.album_MP3WRAP.mp3//" | grep "Tim Story" > albums_list.out

clean_empties:
	find . -maxdepth 1 -type d -exec rmdir {} \;

albumize:
	python albumize.py

order_by_date:
	find . -maxdepth 1 -type d | sort -r | while read i; do sleep 1; echo "$$i" ; touch "$$i" ; done

nissan_leaf_count:
	echo "NUMBER OF DIRS(<255):" `find . -type d | wc -l`
	echo "NUMBER OF FILES(<999)" `find . -type f | wc -l`
