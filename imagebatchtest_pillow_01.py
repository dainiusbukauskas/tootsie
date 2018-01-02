from PIL import Image
import glob, os, shutil, csv


standardCleanTitlePattern = r'index_%s_tag_%s_frameNumber_%s'

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

    splittedTitle = title.split('frameNumber')
    frameNumber = int(splittedTitle[1][1:])
    indexAndTag = splittedTitle[0].split('tag')
    tag = indexAndTag[1][1:-1]
    index = int(indexAndTag[0].split('index')[1][1:-1])
    
    return index, tag, frameNumber

def cleanUpVideoNames(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))

        index, tag, frameNumber = tryToExtractInfoFromRawImageName(title)

        cleanRename(pathAndFileName, titlePattern, index, tag, frameNumber)


def extractInfoFromAllImages(dir, pattern):

    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        index, tag, frameNumber = extractInfoFromFormattedImageName(title)
        print('index: ' + str(index) + ', tag: ' + tag + ', frameNumber: ' + str(frameNumber))
        

def cleanRename(pathAndFilename,titlePattern, index, tag, frameNumber):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    
    print (pathAndFilename)
    print (os.path.dirname(pathAndFilename) + '/' + titlePattern % (index, tag, frameNumber) + ext)
    os.rename(pathAndFilename,
              os.path.dirname(pathAndFilename) + '/' + titlePattern % (index, tag, frameNumber) + ext)
    



def identifyAndAdjustTimeAdjustedVideos(dir, pattern, timeAdjustmentData):
    tag = timeAdjustmentData[0]
    startFrame = int(timeAdjustmentData[3])
    endFrame = int(timeAdjustmentData[4])
    print('searching for ' + tag)
    
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        if tag in title:
            # print('found a match: ' + title)
            incrementFrameCounterForAGivenImage(pathAndFilename, startFrame)


def incrementFrameCounterForAGivenImage(pathAndFilename,counterIncrement):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    index, tag, frameNumber = extractInfoFromFormattedImageName(title)

    print('frameNumber: ' + str(frameNumber))
    print('counterIncrement: ' + str(counterIncrement))
    frameNumber += counterIncrement
    # print('frameNumber: ' + str(frameNumber))

    cleanRename(pathAndFilename, standardCleanTitlePattern, index, tag, frameNumber)

                             
def incrementFrameCounterForAllVideosIdentifiedInTheCSVFile(csvFilePath,imageDirectory):
    with open (csvFilePath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')  
        counter = 0
        for row in reader:
            # print(row[0])
            if counter != 0:
                if int(row[3]) > 0: # If we actually have a startFrame which is greater than 0, then go and adjust the timing.
                    # tags.append(row[0])
                    # tag = row[0]
                    identifyAndAdjustTimeAdjustedVideos(imageDirectory,r'*.jpg',row)
                    # if row[0] 
            counter = counter + 1

        print('finished') 

    # del tags[0]
    # print(tags)
        

def removeOver180Frames(dir, pattern):
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))

        index, tag, frameNumber = extractInfoFromFormattedImageName(title)
       
        if frameNumber > 179:
            print('This image has a frame number higher than 179: ' + os.path.join(dir,title+ext))
            print('Moving it to over180FramesFolder/')
            shutil.move(os.path.join(dir,title+ext),'./over180FramesFolder/' + title + ext)


## Main Program Execution           


# cleanUpVideoNames(r'./img',r'*.jpg',standardCleanTitlePattern)

# extractInfoFromAllImages(r'./img',r'*.jpg')

# 3. Adjust Frame Numbers to Correspond to Start Times Defined In CSV File

# incrementFrameCounterForAllVideosIdentifiedInTheCSVFile('frameTimingAdjustments.csv',r'./img/')

# 4. Remove all images with frameNumbers higher than 179.

# removeOver180Frames(r'./img/', r'*.jpg')

# 5. Start some image crep.


