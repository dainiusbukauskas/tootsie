from PIL import Image
import glob, os, shutil, csv, math, time, subprocess


standardCleanTitlePattern = r'index_%s_tag_%s_frameNumber_%s_incremented_%s'
sourceImageDirectory = r'./srcimg/'
destinationImageDirectory = r'./dstimg/'


def tryToExtractInfoFromRawImageName(title): # This function extracts the data from the original raw image file names.

    # Initialise these variables.
    index = -1 # -1 is a nonsense value so if index fails to get assigned we know something went wrong.
    tag = ''
    frameNumberInt = -1 # -1 is a nonsense value.

    index = int(title[:3]) # Extract the first 3 characters from the title. In the raw naming convention, this corresponds to the index value.

    frameNumberString = title[-3:] # Extract last 3 characters from title. This corresponds to the frame number and we will now to try to extract the integer value from this.

    try: # Try to extract an integer from the 3 characters we extracted.
        frameNumberInt = int(frameNumberString)
        tag = title[4:-3] # Used 4 index here because there is a dash at the beginning of all the tags for some reason.
    except ValueError: 
        print('This frameNumber only has 2 digits. Trying to extract number from 2 digits now:')
        try: # Try to extract an integer from the last 2 digits then.
            frameNumberInt = int(frameNumberString[1:])
            tag = title[3:-2]
        except ValueError:
            print('What? This frameNumber only has 1 digit??')
            frameNumberInt = int(frameNumberString[2:])
            tag = title[3:-1]

    print('index: ' + str(index) + ', tag: ' + tag + ', frameNumber: ' + str(frameNumberInt))
    return index, tag, frameNumberInt


def extractInfoFromFormattedImageName(title):

    # Extract all of the data from the formatted image name.

    incrementedText = title.split('incremented')
    incremented = incrementedText[1][1:]
    frameNumberText = incrementedText[0].split('frameNumber')
    frameNumber = int(frameNumberText[1][1:-1])
    tagText = frameNumberText[0].split('tag')
    tag = tagText[1][1:-1]
    indexText = tagText[0].split('index')
    index = int(indexText[1][1:-1])

    return index, tag, frameNumber, incremented

def cleanUpVideoNames(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))

        index, tag, frameNumber = tryToExtractInfoFromRawImageName(title)

        incremented = 'false'

        cleanRename(pathAndFilename, titlePattern, index, tag, frameNumber, incremented)


def extractInfoFromAllImages(dir, pattern):

    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        index, tag, frameNumber, incremented = extractInfoFromFormattedImageName(title)
        print('Extracting info from formatted image: index: ' + str(index) + ', tag: ' + tag + ', frameNumber: ' + str(frameNumber) + ', incremented: ' + incremented)
        

def cleanRename(pathAndFilename,titlePattern, index, tag, frameNumber, incremented):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    
    print ('Clean renaming from...')
    print (pathAndFilename)
    print ('...to...')
    print (os.path.dirname(pathAndFilename) + '/' + titlePattern % (index, tag, frameNumber, incremented) + ext)
    os.rename(pathAndFilename,
              os.path.dirname(pathAndFilename) + '/' + titlePattern % (index, tag, frameNumber, incremented) + ext)


def identifyAndAdjustTimeAdjustedVideos(dir, destinationImageDirectory, pattern, timeAdjustmentData):
    tag = timeAdjustmentData[0]
    startFrame = int(timeAdjustmentData[3])
    endFrame = int(timeAdjustmentData[4])
    print('Searching for ' + tag + '...')
    
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        if tag in title:
            print('Found a match for the tag: ' + tag + ' in ' + title)
            incrementFrameCounterForAGivenImage(pathAndFilename, destinationImageDirectory, startFrame)


def incrementFrameCounterForAGivenImage(pathAndFilename, destinationImageDirectory, counterIncrement):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    index, tag, frameNumber, incremented = extractInfoFromFormattedImageName(title)

    # print('frameNumber: ' + str(frameNumber))
    # print('counterIncrement: ' + str(counterIncrement))
    frameNumber += counterIncrement
    # print('frameNumber: ' + str(frameNumber))

    incremented = 'true'

    print(destinationImageDirectory)
    # Move the images to the destination directory.
    print('Moving image to be incremented to : ' + os.path.join(destinationImageDirectory,title + ext))
    shutil.move(pathAndFilename,os.path.join(destinationImageDirectory,title + ext))

    cleanRename(os.path.join(destinationImageDirectory,title + ext), standardCleanTitlePattern, index, tag, frameNumber, incremented)

                             
def incrementFrameCounterForAllVideosIdentifiedInTheCSVFile(csvFilePath,sourceImageDirectory,destinationImageDirectory):
    with open (csvFilePath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')  
        counter = 0
        for row in reader:
            # print(row[0])
            if counter != 0:
                if int(row[3]) > 0: # If we actually have a startFrame which is greater than 0, then go and adjust the timing.
                    # tags.append(row[0])
                    # tag = row[0]
                    identifyAndAdjustTimeAdjustedVideos(sourceImageDirectory, destinationImageDirectory,r'*.jpg',row)
                    # if row[0] 
            counter = counter + 1

        print('Finished incrementing.') 

    # del tags[0]
    # print(tags)
       

def moveRemainingUnincremementedVideosToTheDestinationImageDirectory(sourceImageDirectory, pattern, destinationImageDirectory):

    for pathAndFilename in glob.iglob(os.path.join(sourceImageDirectory,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))

        print(destinationImageDirectory)

        print('Moving image which will not be incremented to : ' + os.path.join(destinationImageDirectory,title + ext))
        shutil.move(pathAndFilename,os.path.join(destinationImageDirectory,title + ext))

    print('Finished moving unincremented images.')


def removeOver180Frames(dir, pattern):
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))

        index, tag, frameNumber, incremented = extractInfoFromFormattedImageName(title)
       
        if frameNumber > 179:
            print('This image has a frame number higher than 179: ' + os.path.join(dir,title+ext))
            print('Moving it to over180FramesFolder/')
            shutil.move(os.path.join(dir,title+ext),'./over180FramesFolder/' + title + ext)



def pasteImagesIntoGlobalFinalImage(dir, pattern):
    numberOfImagesToPaste = 35000
    
    width = 1920
    height = 1080

    numberOfImagesX = 213
    numberOfImagesY = 180

    maxPixelsAdjustmentFactor = 4

    maxPixels = 0.5 * math.pow(10,9) * maxPixelsAdjustmentFactor # 1 billion pixels (1 gigapixel)

    scaleFactor = computeScaleFactorForMaximumPixels(width,height,numberOfImagesX,numberOfImagesY,maxPixels)

    print('scaleFactor: ' + str(scaleFactor))
    # sys.stdout.write('scaleFactor: ' + str(scaleFactor))

    globalFinalImageWidth = math.floor(width * numberOfImagesX * scaleFactor)
    globalFinalImageHeight = math.floor(height * numberOfImagesY * scaleFactor)

    print('globalFinalImageWidth: ' + str(globalFinalImageWidth))
    print('globalFinalImageHeight: ' + str(globalFinalImageHeight))

    globalFinalImage = Image.new('RGB',(globalFinalImageWidth,globalFinalImageHeight),'black')

    scaledWidth = math.floor(width * scaleFactor)
    scaledHeight = math.floor(height * scaleFactor)

    print('scaledWidth: ' + str(scaledWidth))
    print('scaledHeight: ' + str(scaledHeight))

    cropBox = (0,0,width,height)

    # print('cropBox: ')
    # print(cropBox)

    counter = 0

    startTime = time.time()
    
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        imageManipulationStartTime = time.time()
        if counter < numberOfImagesToPaste:
            title, ext = os.path.splitext(pathAndFilename)

            index, tag, frameNumber, incremented = extractInfoFromFormattedImageName(title)

            # print('opening image')
            im = Image.open(pathAndFilename)

            region = im.crop(cropBox)
            # print('region: ')
            # print(region)

            resizedRegion = region.resize((scaledWidth, scaledHeight))
            # print('region after resizing: ')
            # print(resizedRegion)
    
            topLeftCornerX = 0 + (index * scaledWidth)
            topLeftCornerY = 0 + (frameNumber * scaledHeight)
            bottomRightCornerX = 0 + ((index + 1) * scaledWidth)
            bottomRightCornerY = 0 + ((frameNumber + 1) * scaledHeight)

            pasteBox = (topLeftCornerX, topLeftCornerY, bottomRightCornerX, bottomRightCornerY)
            
            # print('pasting image')
            globalFinalImage.paste(resizedRegion, pasteBox)

            percentComplete = counter / numberOfImagesToPaste

            # print(, end='\r')

            imageManipulationEndTime = time.time()

            imageManipulationTimeElapsed = imageManipulationEndTime - imageManipulationStartTime

            totalTimeEstimate = imageManipulationTimeElapsed * numberOfImagesToPaste

            totalTimeElapsed = time.time() - startTime

            totalRemainingTimeEstimate = totalTimeEstimate - totalTimeElapsed
            
            print('Pasting image ' + str(counter) + ' of ' + str(numberOfImagesToPaste) + '. ' + str(round(percentComplete,5)) + '% Completed. Time elapsed: ' + str(round(totalTimeElapsed/60,2)) + ' minutes. Estimated time remaining: ' + str(round(totalRemainingTimeEstimate/60,2)) + ' minutes.', end='\r')
            
            
        counter += 1

    timeAtEndOfPasting = time.time()
    timeTakenToPaste = timeAtEndOfPasting - startTime
    print('',end='\n')
    print('Pasting took ' + str(round(timeTakenToPaste/60,2)) + ' minutes in total. ')

    try:
        # print('',end='\n')
        print('Saving output image...')
        savingStartTime = time.time()
        globalFinalImage.save('./output.jpg')
        savingEndTime = time.time()
        print('Success! Saving completed in ' + str(round((savingEndTime - savingStartTime),4)) + ' seconds.')
    except IOError as error:
        print('IOError: ' + str(error))

    

def pasteImagesIntoTestImage(videosWhichStartAtZeroButEndBefore179, videosWhichStartAfterZeroButEndAt179, videosWhichStartAtZeroAndEndAt179):

    testImage = Image.new('RGB',(213,179),'black')

    x = 0


    for video in videosWhichStartAtZeroAndEndAt179:
        for imageFile in video.imageFiles:
            pasteImage = Image.new('RGB',(1,1),'white')
            pasteBox = (x,imageFile.frameNumber, x+1, imageFile.frameNumber+1)
            testImage.paste(pasteImage,pasteBox)

        x += 1 

    for video in videosWhichStartAfterZeroButEndAt179:
        for imageFile in video.imageFiles:
            pasteImage = Image.new('RGB',(1,1),'white')
            pasteBox = (x,imageFile.frameNumber, x+1, imageFile.frameNumber+1)
            testImage.paste(pasteImage,pasteBox)

        x += 1

    for video in videosWhichStartAtZeroButEndBefore179:
        for imageFile in video.imageFiles:
            pasteImage = Image.new('RGB',(1,1),'white')
            pasteBox = (x,imageFile.frameNumber, x+1, imageFile.frameNumber+1)
            testImage.paste(pasteImage,pasteBox)

        x += 1

    try:
        # print('',end='\n')
        print('Saving test output image...')
        savingStartTime = time.time()
        testImage.save('./position_test_output.jpg')
        savingEndTime = time.time()
        print('Success! Saving completed in ' + str(round((savingEndTime - savingStartTime),4)) + ' seconds.')
        print('Opening image now...')
        openTestImageCommand = "open position_test_output.jpg"
        # process = subprocess.Popen(openTestImageCommand.split(), stdout=subprocess.PIPE)
        # output, error = process.communicate()
    except IOError as error:
        print('IOError: ' + str(error))


def computeScaleFactorForMaximumPixels(width, height, numberX, numberY, maxPixels):

    # Ok so we need to find a choice of scaling factor such that the total number of pixels is less than maxPixels.

    scaleFactor = math.sqrt(maxPixels / (numberX * width * numberY * height))
    
    return scaleFactor


def returnSortedVideos(dir, pattern):

    videos = {}


    # Add ImageFiles to Videos
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))

        index, tag, frameNumber, incremented = extractInfoFromFormattedImageName(title)

        anImageFile = ImageFile(pathAndFilename, index, tag, frameNumber)

        if index in videos: # If the a video with the current index already exists in the Videos dictionary.
            # print('This video already exists. Adding the current ImageFile to it now...')
            videos[index].addImageFile(anImageFile) # Add an ImageFile to the video at the current index.
        else: 
            # print('This video does not exist yet. Creating a new Video and adding the current ImageFile to it now...')
            aVideo = Video(index) # Construct a new Video object.
            aVideo.addImageFile(anImageFile) # Add the current ImageFile to the newly created Video object.
            videos[index] = aVideo


    for index, video in videos.items():
        video.sortImageFilesInAscendingOrderByFrameNumber()
        if video.checkFrameContinuity() == False: 
            print('Video with index: ' + str(video.index) + ', tag: ' + video.imageFiles[0].tag + ', startFrame: ' + str(video.getStartFrame()) + ', endFrame: ' + str(video.getEndFrame()) + ' has a break in frameNumber continuity.')

    videosList = list(videos.values())

    videosWhichStartAtZeroButEndBefore179 = []

    videosWhichStartAtZeroAndEndAt179 = []

    videosWhichStartAfterZeroButEndAt179 = []

    for video in videosList:
        # print('Examining video with index ' + str(video.index))
        if video.getStartFrame() == 0:
            # print('video.getStartFrame() = 0.')
            if video.getEndFrame() < 179:
                # print('video.getEndFrame() < 179.')
                videosWhichStartAtZeroButEndBefore179.append(video)
            else: 
                # print('video.getEndFrame() = 179.')
                videosWhichStartAtZeroAndEndAt179.append(video)
        else:
            # print('video.getEndFrame() > 0.')
            videosWhichStartAfterZeroButEndAt179.append(video)


    videosWhichStartAtZeroButEndBefore179.sort(key = lambda x: x.getNumberOfFrames())
    videosWhichStartAfterZeroButEndAt179.sort(key = lambda x: x.getNumberOfFrames(), reverse = True)

    return videosWhichStartAtZeroButEndBefore179, videosWhichStartAtZeroAndEndAt179, videosWhichStartAfterZeroButEndAt179

class Video:
    def __init__(self, indexIn):
        self.index = indexIn
        #self.startFrame = startFrameIn
        #self.endFrame = endFrameIn
        self.imageFiles = []
        # self.startFrame = -1
        # self.endFrame = -1
        # self.numberOfFrames = -1

    def addImageFile(self, imageFile):
        self.imageFiles.append(imageFile)

    def sortImageFilesInAscendingOrderByFrameNumber(self):
        self.imageFiles.sort(key = lambda x: x.frameNumber)

    def getStartFrame(self): # This will only return the lowest frameNumber if the imageFiles have already been sorted.
        return self.imageFiles[0].frameNumber

    def getEndFrame(self):
        return self.imageFiles[-1].frameNumber

    def getNumberOfFrames(self):
        return self.getEndFrame() - self.getStartFrame()


    def checkFrameContinuity(self):
        frameContinuity = True
        frameNumber = -1
        counter = 0
        for imageFile in self.imageFiles:
            if counter == 0:
                frameNumber = imageFile.frameNumber
            else:
                if imageFile.frameNumber != frameNumber + 1:
                    frameContinuity = False
                frameNumber = imageFile.frameNumber
            counter += 1

        return frameContinuity

class ImageFile:
    def __init__(self, filePath, index, tag, frameNumber):
        self.filePath = filePath
        self.index = index
        self.tag = tag
        self.frameNumber = frameNumber
        
## Main Program Execution           

# 1. Clean Up Image File Names

# cleanUpVideoNames(sourceImageDirectory,r'*.jpg',standardCleanTitlePattern)

# 2. Adjust Frame Numbers to Correspond to Start Times Defined In CSV File

# Increment frame numbers and move them to the destination directory to prevent overwrites during the incrementing process.

# A Test function used to see that we are parsing data from the filenames correctly.
# extractInfoFromAllImages(sourceImageDirectory, r'*.jpg')

# incrementFrameCounterForAllVideosIdentifiedInTheCSVFile('frameTimingAdjustments.csv',sourceImageDirectory,destinationImageDirectory)

# Move the remaining unmodified videos to the destination directory as well.

# moveRemainingUnincremementedVideosToTheDestinationImageDirectory(sourceImageDirectory, r'*.jpg', destinationImageDirectory)

# 3. Remove all images with frameNumbers higher than 179.

removeOver180Frames(destinationImageDirectory, r'*.jpg')

# 5. Sort Videos




# anImageFile = ImageFile('someFilePath')

# aVideo = Video(5,9)

# aVideo.addImageFile(anImageFile)

# print(aVideo.imageFiles[0].path)

# videosWhichStartAtZeroButEndBefore179, videosWhichStartAtZeroAndEndAt179, videosWhichStartAfterZeroButEndAt179 = returnSortedVideos(r'./img/',r'*.jpg')


# for video in videosWhichStartAfterZeroButEndAt179:
#     print(video.getStartFrame())

# pasteImagesIntoTestImage(videosWhichStartAfterZeroButEndAt179, videosWhichStartAtZeroAndEndAt179, videosWhichStartAtZeroButEndBefore179)

# print('printing out all the imageFile paths in all the videos...')
# for index, video in videos.items():
#     for imageFile in video.imageFiles:
#         print (imageFile.filePath)

# 6. Start some image crep.

# pasteImagesIntoGlobalFinalImage(r'./img/',r'*.jpg')

