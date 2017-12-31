from PIL import Image
import glob, os, shutil, csv

# im = Image.open("test.jpg")
# im.rotate(45).show()

# tags = []

with open ('frameTimingAdjustments.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
    counter = 0
    for row in reader:
        # print(row[0])
        if counter != 0:
            # tags.append(row[0])
            tag = row[0]
            identifyTimeAdjustedVideos(r'./',r'*.jpg',tag)
            # if row[0] 
        counter ++


    # del tags[0]
    # print(tags)
        
    


def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir,pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename,
                  os.path.join(dir,titlePattern % title + ext))


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

def identifyTimeAdjustedVideos(dir, pattern, timeAdjustmentData):
    for pathAndFilename in glob.iglob(os.path.join(dir.pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        if tag in title:
                
            
        
        
    


# rename(r'./',r'*.jpg',r'new(%s)')

removeOver180Frames(r'./', r'*.jpg')
