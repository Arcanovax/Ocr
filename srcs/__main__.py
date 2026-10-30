
import cv2
import numpy as np
import questionary
import os



class Core:
    def __init__(self):
        self.image = self.get_input()
        
        self.matrice = self.get_matrice(self.image)
        self.matrice = self.align(self.matrice)
        
        h, w = self.matrice.shape
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (1, 15)
        )
        y = cv2.morphologyEx(
            self.matrice, cv2.MORPH_OPEN, kernel
        )
        kernel = cv2.getStructuringElement(
                    cv2.MORPH_RECT, (15, 1)
                )
        x = cv2.morphologyEx(
            self.matrice, cv2.MORPH_OPEN, kernel
        )
        self.matrice = x + y
        
        self.display_output(self.matrice)
        
        

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
    
# ys, xs = np.where(matrice != 0)

# x_min, x_max = xs.min(), xs.max()
# y_min, y_max = ys.min(), ys.max()

# crop = matrice[y_min:y_max + 1, x_min:x_max + 1]




# print(horizontal)
# cv2.imshow("Lignes horizontales", horizontal)


# cv2.imshow('Edges', crop)



# Redimensionner l'image
# resized_image = cv2.resize(image, (width, height))

# Faire pivoter l'image de 45 degrés
# rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), 45, 1)
# rotated_image = cv2.warpAffine(resized_image, rotation_matrix, (width, height))
