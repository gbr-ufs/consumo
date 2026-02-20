# Commands Used for Generation

## `audio.mp3`

```
ffmpeg -f lavfi -i anullsrc=r=8000:cl=mono -t 1 -c:a libmp3lame -b:a 8k audio.mp3
```

## `video_no_duration.h264`

```
ffmpeg -f lavfi -i color=c=black:s=2x2:r=1 -t 1 -c:v libx264 -f h264 no_duration.h264
```

## `audio_no_extension`

```
ffmpeg -f lavfi -i anullsrc=channel_layout=mono:sample_rate=8000 -t 1 -c:a flac no_extension.flac
mv no_extension.flac no_extension
```

## `video.mkv`

```
ffmpeg -f lavfi -i color=c=black:s=2x2:r=1 -t 1 -c:v libx264 -crf 51 video.mkv
```

## `single_char.pdf`

```
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=single_char.pdf -c "/Helvetica findfont 12 scalefont setfont 50 750 moveto (a) show showpage"
```

## `empty.epub`

```
echo -N "" | pandoc -f markdown -t epub -o empty.epub
```

## `jumbled.mobi`

```
echo "Th3i1s 14214i1244is s4i24i14pposed t0 be 12 w0892415ords." | pandoc -f markdown -t epub -o jumbled.epub
ebook-convert jumbled.epub jumbled.mobi
rm jumbled.epub
```

This is supposed to be 12 words because `ebook-convert` automatically adds a Table of Contents to the file.

# Version Information

## `ffmpeg`

`fmpeg -version`

<details>

```
ffmpeg version 7.1.2 Copyright (c) 2000-2025 the FFmpeg developers
built with gcc 15 (GCC)
configuration: --prefix=/usr --bindir=/usr/bin --datadir=/usr/share/ffmpeg --docdir=/usr/share/doc/ffmpeg --incdir=/usr/include/ffmpeg --libdir=/usr/lib64 --mandir=/usr/share/man --arch=x86_64 --optflags='-O2 -flto=auto -ffat-lto-objects -fexceptions -g -grecord-gcc-switches -pipe -Wall -Wno-complain-wrong-lang -Werror=format-security -Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -fstack-protector-strong -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -march=x86-64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -mtls-dialect=gnu2 -fno-omit-frame-pointer -mno-omit-leaf-frame-pointer' --extra-ldflags='-Wl,-z,relro -Wl,--as-needed -Wl,-z,pack-relative-relocs -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -specs=/usr/lib/rpm/redhat/redhat-hardened-ld-errors -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -Wl,--build-id=sha1 -specs=/usr/lib/rpm/redhat/redhat-package-notes ' --extra-cflags=' -I/usr/include/rav1e' --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-version3 --enable-bzlib --enable-chromaprint --enable-fontconfig --enable-frei0r --enable-gcrypt --enable-gnutls --enable-ladspa --enable-lcms2 --enable-libaom --enable-libaribb24 --enable-libaribcaption --enable-libdav1d --enable-libass --enable-libbluray --enable-libbs2b --enable-libcodec2 --enable-libcdio --enable-libdrm --enable-libjack --enable-libjxl --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libharfbuzz --enable-libilbc --enable-liblc3 --enable-libmp3lame --enable-libmysofa --enable-nvenc --enable-openal --enable-opencl --enable-opengl --enable-libopenh264 --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-libplacebo --enable-librsvg --enable-librav1e --enable-librubberband --enable-libqrencode --enable-libsmbclient --enable-version3 --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libssh --enable-libsvtav1 --enable-libtesseract --enable-libtheora --enable-libtwolame --enable-libvorbis --enable-libv4l2 --enable-libvidstab --enable-libvmaf --enable-version3 --enable-vapoursynth --enable-libvpx --enable-libvvenc --enable-vulkan --enable-libshaderc --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid --enable-libxml2 --enable-libzimg --enable-libzmq --enable-libzvbi --enable-lv2 --enable-avfilter --enable-libmodplug --enable-postproc --enable-pthreads --disable-static --enable-shared --enable-gpl --disable-debug --disable-stripping --shlibdir=/usr/lib64 --enable-lto --enable-libvpl --enable-runtime-cpudetect
libavutil      59. 39.100 / 59. 39.100
libavcodec     61. 19.101 / 61. 19.101
libavformat    61.  7.100 / 61.  7.100
libavdevice    61.  3.100 / 61.  3.100
libavfilter    10.  4.100 / 10.  4.100
libswscale      8.  3.100 /  8.  3.100
libswresample   5.  3.100 /  5.  3.100
libpostproc    58.  3.100 / 58.  3.100
```

</details>

## `gs`

`gs --version`

<details>

```
10.05.1
```

</details>

## `pandoc`

`pandoc --version`

<details>

```
pandoc 3.6.4
Features: +server +lua
Scripting engine: Lua 5.4
User data directory: /home/gabriel/.local/share/pandoc
Copyright (C) 2006-2024 John MacFarlane. Web: https://pandoc.org
This is free software; see the source for copying conditions. There is no
warranty, not even for merchantability or fitness for a particular purpose.
```

</details>

## `ebook-convert`

`ebook-convert --version`

<details>

```
ebook-convert (calibre 8.14.0)
Created by: Kovid Goyal <kovid@kovidgoyal.net>
```

</details>
