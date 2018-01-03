# Development Log for the Tootsie Project

_Development notes for the Tootsie project._

---

## 2018 1 2

### Naming Cleanup

We fixed up an error with the index numbers where for some reason 3 digit numbers were getting truncated. This probably had something to do with the fact that we weren't treating the index numbers as integers after parsing...

Ultimately got everything working and got the files properly named.

We also did the frame number adjustments.

### Image Pasting

We started looking into the way to paste the images all into the big final image.

Basically create a giant single image in the beginning. 

Then, for each image in the 39000 image directory, grab that image, and paste into the currently open big single image.

When you have finished that for all of the images, save the giant single image.

That's it.

We are already running up against potential limits in size for this image... pillow throws an error for a certain oversized image...

We got the basic structure working, and limited the number of images placed and the size of the global image, but realised that those images would not necessarily land inside the global image

---

## 2018 1 3

### Imaging Pasting and Writing

Ok we got a successful image paste working!

We spent a while trying to work out exactly what the maximum dimensions would be for the final image given the limitation of the image writing buffer.

See the pillow "limits" page for details:

http://pillow.readthedocs.io/en/4.0.x/reference/limits.html

This reference said that the maximum number of pixels was 0.5 Gpx (0.5 Gigapixels) which we think is 10^9 pixels?

Also, there was an error at some point which limited the dimensions of the image to 65500 I think? At this scaling, we got just under that.


We managed to get the global image construction to work at a factor of 4 times this.

This corresponds to:


scaleFactor: 0.15860849764526194

globalFinalImageWidth: 64864
globalFinalImageHeight: 30833

scaledWidth: 304
scaledHeight: 171

At this scale the computation finished!

#### Errors

There are still some issues with the final image:

1. We forgot to sort the videos by their length and start times...
2. There appear to be some missing images for some reason...
3. The dimensions of the global images are slightly wrong (this might have to do with some kind of rounding error accumulated?)
4. Do we want a black background? Is there a transparent background option in JPG export?
5. Do we want to consider a higher compression quality potentially?


