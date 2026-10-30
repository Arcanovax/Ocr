
import cv2
import numpy as np

image = cv2.imread('input/IMG_4.png')


def get_median_angle(lines):
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line

        angle = np.degrees(
            np.arctan2(y2 - y1, x2 - x1)
        )

        if abs(angle) < 20:
            angles.append(angle)
    return np.median(angles)


gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

matrice = cv2.Canny(gray_image, 50, 150)


lines = cv2.HoughLinesP(
    matrice,
    1,
    np.pi / 180,
    threshold=100,
    minLineLength=100,
    maxLineGap=15
)


angle = get_median_angle(lines)

h, w = matrice.shape
centre = (w // 2, h // 2)

matrice = cv2.getRotationMatrix2D(
    centre, angle, 1.0
)

matrice = cv2.warpAffine(
    matrice, matrice, (w, h),
    flags=cv2.INTER_NEAREST,
    borderValue=0
)
cv2.imshow("Lignes horizontales", matrice)
for line in matrice:
    print(line)
# ys, xs = np.where(matrice != 0)

# x_min, x_max = xs.min(), xs.max()
# y_min, y_max = ys.min(), ys.max()

# crop = matrice[y_min:y_max + 1, x_min:x_max + 1]
# h, w = crop.shape


# kernel = cv2.getStructuringElement(
#     cv2.MORPH_RECT, (max(25, w // 25), 1)
# )
# horizontal = cv2.morphologyEx(
#     crop, cv2.MORPH_OPEN, kernel
# )
# print(horizontal)
# cv2.imshow("Lignes horizontales", horizontal)


# cv2.imshow('Edges', crop)
cv2.waitKey(0)
cv2.destroyAllWindows()



# Redimensionner l'image
# resized_image = cv2.resize(image, (width, height))

# Faire pivoter l'image de 45 degrés
# rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), 45, 1)
# rotated_image = cv2.warpAffine(resized_image, rotation_matrix, (width, height))
