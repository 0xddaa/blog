# Init

1. pip install pelican markdown
1. git clone https://github.com/0xddaa/blog
1. cd blog && git submodule init && git submodule update

# Usage

1. write an article under `content/$YEAR/$ARTICLE`
    - put a exploit under `content/exp` and use `[text]({filename}/exp/$FILE)` to create a hyperlink to the exploit.
    - The same as above, put a picture upder `content/image` and usr `:![pic]({filename}/images/$IMAGE)` to display the picture.
2. `./develop_server.sh start`
    - access `http://$IP:8000` to view the website
    - or just execute `make publish` to generate the website without starting http server.
3. `./develop_server.sh stop`
    - stop http server
    - DO NOT start http server for a long time. It seems to exist memory leak issue...
4. `make github`
    - push the website to github page
