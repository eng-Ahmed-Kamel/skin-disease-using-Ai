#https://www.kaggle.com/code/ahmedkamel00/skin-cancer-prediction-randomforest-acc-96/edit
#https://www.kaggle.com/code/deepakbot/skin-cancer-prediction-randomforest-acc-96/output ##model skin cancer2.h5
#https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000/code    ##database 
#https://www.kaggle.com/code/mohamedkhaledidris/skin-cancer-classification-cnn-tensorflow/output ##model skincancer1.h5


from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QTextBrowser, QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import PIL
import numpy as np
import tensorflow as tf
import joblib
import matplotlib.pyplot as plt


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("mygui.ui", self)
        self.show()

        self.pushButton.clicked.connect(self.browse)
        self.pushButton_2.clicked.connect(self.check)
        self.image_path = None
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.textEdit = self.findChild(QTextBrowser, 'textEdit')

        # Load the model
        self.model = tf.keras.models.load_model('Skin Cancer1.h5')

    def browse(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp *.tif);;All Files (*)", options=options)

        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            item = QGraphicsPixmapItem(pixmap)
            self.scene.clear()
            self.scene.addItem(item)

    def check(self):
        if self.image_path:
            image = PIL.Image.open(self.image_path)
            image = image.resize((28, 28))
            img = np.array(image)

            # Reshape the array if needed
            img = img.reshape(-1, 28, 28, 3)  # Uncomment this line if needed

            result = self.model.predict(img)
            result = result.tolist()
            max_prob = max(result[0])
            class_ind = result[0].index(max_prob)
            classes = {
                0: ('akiec', 'actinic keratoses and intraepithelial carcinoma'),
                1: ('bcc', 'basal cell carcinoma '),#(cancer)
                2: ('bkl', 'benign keratosis-like lesions'),
                3: ('df', 'dermatofibroma'),
                4: ('nv', 'melanocytic nevi'),
                5: ('vasc', 'pyogenic granulomas and hemorrhage'),
                6: ('mel', 'melanoma '),#(cancer)
            }
            output_text = f"Predicted class: {classes[class_ind][0]} - {classes[class_ind][1]}\n"
            self.textEdit.setPlainText(output_text)


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()
