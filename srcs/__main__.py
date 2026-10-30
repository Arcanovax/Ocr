
import cv2
import numpy as np
import questionary
import os



class Core:
    def __init__(self):
        self.image = self.get_input()
        
        self.matrice = self.get_matrice(self.image)
        self.matrice = self.align(self.matrice)
        
        self.matrice = self.crop(self.matrice)

        
        self.display_output(self.matrice)
        
    def find_strong_lines(self, matrice):
        h, w = matrice.shape
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (1, 25)
        )
        y = cv2.morphologyEx(
            matrice, cv2.MORPH_OPEN, kernel
        )
        kernel = cv2.getStructuringElement(
                    cv2.MORPH_RECT, (25, 1)
                )
        x = cv2.morphologyEx(
            matrice, cv2.MORPH_OPEN, kernel
        )
        return x + y    
        
    def crop(self, matrice):
        lines = self.find_strong_lines(matrice)
        ys, xs = np.where(lines != 0)
        
        x_min, x_max = xs.min(), xs.max()
        y_min, y_max = ys.min(), ys.max()

        matrice = matrice[y_min:y_max + 1, x_min:x_max + 1]
        
        return matrice
        

    def display_output(self, matrice):
        cv2.imshow("Ouput", matrice)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def align(self, matrice):
        lines = cv2.HoughLinesP(
            matrice,
            1,
            np.pi / 180,
            threshold=100,
            minLineLength=100,
            maxLineGap=15
        )
        angle = self.get_median_angle(lines)
        h, w = matrice.shape
        centre = (w // 2, h // 2)

        rotation_matrix = cv2.getRotationMatrix2D(
            centre, angle, 1.0
        )

        matrice = cv2.warpAffine(
            matrice, rotation_matrix, (w, h),
            flags=cv2.INTER_NEAREST,
            borderValue=0
        )
        return matrice
        
    def get_matrice(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        matrice = cv2.Canny(gray_image, 50, 150)
        return matrice
    
    def get_input(self):
        selected = questionary.select(
                "Choose an Img: ",
                choices=list(os.listdir("input"))
            ).ask()
        if selected is None:
            raise ValueError("Cancelled")
        image = cv2.imread(f'input/{selected}')
        return image
    
    def get_median_angle(self, lines):
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line

            angle = np.degrees(
                np.arctan2(y2 - y1, x2 - x1)
            )

            if abs(angle) < 20:
                angles.append(angle)
        return np.median(angles)
   
Core()
