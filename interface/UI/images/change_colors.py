import cv2
import numpy as np


imagem = cv2.imread("light/users.png",cv2.IMREAD_UNCHANGED)
altura, largura, _ = imagem.shape

imagem_2 = np.zeros((altura, largura, 4), dtype=np.uint8)
change_colors = 1
invert = 0
for y in range(altura):
    for x in range(largura):
        # Acessar cada pixel
        pixel = imagem[y, x]
        if change_colors:
            # Faça algo com o pixel (por exemplo, acessar seus valores de canal)
            if pixel[-1] == 255:
                pixel=[0,0,0,255]
            else:
                pixel=[0,0,0,0]
            imagem_2[y,x] = pixel
            
        if invert:
            imagem_2[y,-(x+1)] = pixel

cv2.imwrite('dark/users.png', imagem_2)




