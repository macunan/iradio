for f in *\ *; do mv "$f" "${f// /_}"; done
playlist='topgun.m3u' ; if [ -f $playlist ]; then rm $playlist ; fi ; for f in *.mp3; do echo "$(pwd)/$f" >> "$playlist"; done
