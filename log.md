# Development Log for the Simultania Project

_Development notes for the simultania project._

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

