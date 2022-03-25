from dataHandler.flashcard import *

initiateUserProgress()

if __name__ == "__main__":
    a = sys.argv[1]
    if a =='updateprogress':
        updateUserProgress()
    elif a == 'loadtext':
        loadTexts()
    elif a == 'initiateprogress':
        initiateUserProgress()
        
