from PIL import Image
import glob, os, shutil, csv

# im = Image.open("test.jpg")
# im.rotate(45).show()

# tags = []



def cleanUpVideoNames(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))

        index = title[:3]
        frameNumber = title[-3:]
        tag = title[4:-3]

        os.rename(pathAndFilename,
                  os.path.join(dir,titlePattern % index, tag, frameNumber)


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
            print('found a match: ' + title)
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
        
    
            


# rename(r'./img/',r'*.jpg',r'new(%s)')

# removeOver180Frames(r'./', r'*.jpg')

cleanUpVideoNames(r'./test',r'*.jpg',r'%s_%s_%s')

incrementFrameCounterForAllVideosIdentifiedInTheCSVFile('frameTimingAdjustments.csv',r'./test/')
