import uuid
import time
import cv2
from db_helper import write_item
from cvzone.ClassificationModule import Classifier
import cvzone
import os
import newrelic.agent
newrelic.agent.initialize('./newrelic.ini')


if __name__ == "__main__":
    app = newrelic.agent.application("Trash_Sorting")
    cap = cv2.VideoCapture(0)
    classifier = Classifier('Resources/Model/keras_model.h5',
                            'Resources/Model/labels.txt')
    imgArrow = cv2.imread('Resources/arrow.png', cv2.IMREAD_UNCHANGED)
    classIDBin = 0
    # Import all the waste images
    imgWasteList = []
    pathFolderWaste = "Resources/Waste"
    pathList = os.listdir(pathFolderWaste)
    for path in pathList:
        imgWasteList.append(cv2.imread(os.path.join(
            pathFolderWaste, path), cv2.IMREAD_UNCHANGED))

    # Import all the waste images
    imgBinsList = []
    pathFolderBins = "Resources/Bins"
    pathList = os.listdir(pathFolderBins)
    for path in pathList:
        imgBinsList.append(cv2.imread(os.path.join(
            pathFolderBins, path), cv2.IMREAD_UNCHANGED))

    # 0 = Recyclable
    # 1 = Hazardous
    # 2 = Food
    # 3 = Residual
    classDicName = {0: 'Recyclable',
                    1: 'Hazardous',
                    2: 'Food',
                    3: 'Residual'
                    }

    classDic = {0: None,
                1: 0,
                2: 0,
                3: 3,
                4: 3,
                5: 1,
                6: 1,
                7: 2,
                8: 2}

    try:
        while True:
            _, img = cap.read()
            imgResize = cv2.resize(img, (454, 340))

            imgBackground = cv2.imread('Resources/background.png')

            predection = classifier.getPrediction(img)

            classID = predection[1]
            print(classID)
            if classID != 0:
                imgBackground = cvzone.overlayPNG(
                    imgBackground, imgWasteList[classID - 1], (909, 127))
                imgBackground = cvzone.overlayPNG(
                    imgBackground, imgArrow, (978, 320))

                @newrelic.agent.background_task()
                def write_to_db():
                    classIDBin = classDic[classID]
                    write_item(classDicName[classDic[classID]])
                    newrelic.agent.record_custom_event(
                        'trash_recorded', {str(uuid.uuid1()): str(classDicName[classDic[classID]])}, app)
                    return classIDBin
                classIDBin = write_to_db()

            imgBackground = cvzone.overlayPNG(
                imgBackground, imgBinsList[classIDBin], (895, 374))

            imgBackground[148:148 + 340, 159:159 + 454] = imgResize
            # Displays
            # cv2.imshow("Image", img)
            cv2.imshow("Output", imgBackground)
            cv2.waitKey(1)
            # wait a second before looking for new item
            time.sleep(1)
    except:
        pass
    finally:
        newrelic.agent.shutdown_agent(timeout=10)
