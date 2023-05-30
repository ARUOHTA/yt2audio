init:
	poetry install
	mkdir yt2audio/downloaded
	touch yt2audio/archive.txt
	touch yt2audio/setting.json

run:
	poetry run python3 -m yt2audio
test:
	echo "未定義"