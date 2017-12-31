# Sips Resizing Learning

## Notes

http://osxdaily.com/2012/11/25/batch-resize-a-group-of-pictures-from-the-command-line-with-sips/

## Instructions:

* Currently at 1920 x 1080 --> 1.77 --> 16:9
* Crop to 18x10 --> 9:5    1066.666
* DPI = 3888 --> 72 / 3888 = 0.0851
* 

## Process

### 1. Crop image to full size but the correct aspect ratio.

`sips -c 1066.6666666 1920 <filename>`

### 2. Half Size

1920 / 2 = 960

1066 / 2 = 53

`sips --resampleHeightWidth 533 960 <filename>`

### 3. Change DPI to 3888

For some reason the DPI is refusing to change...

This fails to change the DPI:

`sips --setProperty dpiHeight 3888  test2_212-wb.blakeny-NEW2159.jpg` 




---


STANDARDIZED SPECS

Videos: 213
Images: 3970
Max image length: 180

Irregulars: 59
Pre: 28
Post: 31

Image dimensions: 
X: 18px  .25in
Y: 10px  .139in

Artboard dimensions:
X: 3834px
Y: 1800px


Full scale
1920px
1080px
72dpi

Small scale
18px
10px
3888dpi









