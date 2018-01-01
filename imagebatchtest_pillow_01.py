from PIL import Image
import glob, os, shutil, csv

# im = Image.open("test.jpg")
# im.rotate(45).show()

# tags = []



def checkFor3DigitFrameNumbers(dir, pattern):
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        frameNumber = tryToExtractFrameNumber(title)
        print(frameNumber)
        
def tryToExtractInfoFromRawImageName(title):

    index = ''
    tag = ''

    index = title[:3]
    frameNumberString = title[-3:] # Extract last 3 characters from title.

    try: # Try to extract an integer from the 3 characters we extracted.
        frameNumberInt = int(frameNumberString)
        tag = title[3:-3]
    except ValueError: 
        print('This frameNumber only has 2 digits. Trying to extract number from 2 digits now:')
        try: # Try to extract an integer from the last 2 digits then.
            frameNumberInt = int(frameNumberString[1:])
            tag = title[3:-2]
        except ValueError:
            print('What? This frameNumber only has 1 digit??')
            frameNumberInt = int(frameNumberString[2:])
            tag = title[3:-1]

    print('index: ' + index + ', tag: ' + tag + ', frameNumber: ' + str(frameNumberInt))
    return index, tag, frameNumberInt


def extractInfoFromFormattedImageName(title):

    splittedTitle = title.split('frameNumber')
    frameNumber = int(splittedTitle[1][1:])
    indexAndTag = splittedTitle[0].split('tag')
    tag = indexAndTag[1][1:-1]
    index = indexAndTag[0][-3:-1]
    print('index: ' + index + ', tag: ' + tag + ', frameNumber: ' + str(frameNumber))

    return index, tag, frameNumber

def cleanUpVideoNames(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))

        index, tag, frameNumber = tryToExtractInfoFromImageName(title)

        os.rename(pathAndFilename,
                  os.path.join(dir,titlePattern % (index, tag, frameNumber) + ext))

        # print(os.path.join(dir,titlePattern % (index, tag, frameNumber) + ext))


def extractInfoFromAllImages(dir, pattern):

    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        index, tag, frameNumber = extractInfoFromFormattedImageName(title)

def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
##        os.rename(pathAndFilename,
##                  os.path.join(dir,titlePattern % title + ext))

        # print(pathAndFilename)
        #print(os.path.basename(pathAndFilename))
        head, tail = os.path.split(pathAndFilename)
        print('head:' + head)
        print('tail:' + tail)

def removeOver180Frames(dir, pattern):
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        # print(title)
        lastThreeChars = title[-3:]
        # print(lastThreeChars)
        lastThreeCharsInt = int(lastThreeChars)
        # print(lastThreeCharsInt)
        if lastThreeCharsInt > 180:
            shutil.move(title+ext,'over180FramesFolder/' + title + ext)

def identifyAndAdjustTimeAdjustedVideos(dir, pattern, timeAdjustmentData):
    tag = timeAdjustmentData[0]
    startFrame = timeAdjustmentData[3]
    endFrame = timeAdjustmentData[4]
    print('searching for ' + tag)
    
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        if tag in title:
            # print('found a match: ' + title)
            incrementFrameCounterForAGivenImage(pathAndFilename, startFrame)


def incrementFrameCounterForAGivenImage(pathAndFilename,counterIncrement):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
    lastThreeChars = title[-3:]
    beforeLastThreeChars = title[:-3]
    # print(lastThreeChars)
    lastThreeCharsInt = int(lastThreeChars)
    lastThreeCharsInt += int(counterIncrement)

    # rename so that the last three characters of the title are replaced with the newly incremented frame numbers.
    
    os.rename(pathAndFilename,
              os.path.dirname(pathAndFilename) + '/' + beforeLastThreeChars + str(lastThreeCharsInt) + ext)

                             
def incrementFrameCounterForAllVideosIdentifiedInTheCSVFile(csvFilePath,imageDirectory):
    with open (csvFilePath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')  
        counter = 0
        for row in reader:
            # print(row[0])
            if counter != 0:
                # tags.append(row[0])
                # tag = row[0]
                identifyAndAdjustTimeAdjustedVideos(imageDirectory,r'*.jpg',row)
                # if row[0] 
            counter = counter + 1

        print('finished') 

    # del tags[0]
    # print(tags)
        

            

# removeOver180Frames(r'./', r'*.jpg')

# checkFor3DigitFrameNumbers(r'./img',r'*.jpg')

# cleanUpVideoNames(r'./img',r'*.jpg',r'index_%s_tag_%s_frameNumber_%s')

extractInfoFromAllImages(r'./img',r'*.jpg')

# incrementFrameCounterForAllVideosIdentifiedInTheCSVFile('frameTimingAdjustments.csv',r'./img/')
