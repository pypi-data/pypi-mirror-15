# slide2pdf

slide2pdf is a command line tool to convert html slide presenation to portable 
document format (pdf).

### Installation

1. `git clone git@github.com:vengatlnx/slide2pdf.git`
2. `cd slide2pdf`
3. `python setup.py install`

or

```
  $ pip install slide2pdf
```

**Note**: Before installing this package please make sure that you have already 
installed **xdotool** _else_ install xdotool using `apt-get install xdotool`.

### Usage

```
  $ slide2pdf (-u <url>) (-n <num_of_slides>) [--height=<n>] [--width=<n>]

    Options:
      -h --help                show help
      -u --url URL             file-url path
      -n --num NO_OF_SLIDES    number of slides
      --height=<n>             window height [default: 1600]
      --width=<n>              window width [default: 1200]

  $ slide2pdf -u "file:///path/to/file.html" -n 10
```
