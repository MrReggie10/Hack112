class Spell:
    def __init__(self):
        self.circle = [207, 100, 219, 103, 231, 107, 249, 112, 265, 117, 284, 130, 297, 142, 308, 157, 317, 171, 322, 185, 326, 201, 328, 214, 328, 228, 327, 243, 324, 256, 317, 269, 309, 279, 298, 287, 282, 294, 263, 299, 240, 302, 216, 302, 188, 302, 169, 302, 153, 297, 140, 289, 128, 277, 118, 264, 109, 252, 101, 240, 95, 227, 91, 215, 90, 204, 90, 192, 91, 180, 95, 171, 100, 160, 108, 149, 117, 139, 126, 131, 137, 122, 146, 117, 155, 111, 170, 106, 185, 100]
        self.figureEight = [199, 182, 201, 177, 223, 144, 239, 130, 252, 122, 268, 117, 285, 116, 300, 120, 315, 133, 327, 149, 334, 163, 337, 178, 337, 200, 331, 214, 322, 226, 310, 238, 298, 246, 284, 251, 266, 252, 247, 251, 229, 240, 206, 216, 196, 198, 184, 180, 175, 160, 166, 145, 156, 135, 148, 129, 137, 124, 119, 123, 104, 128, 90, 135, 78, 143, 69, 151, 61, 161, 56, 172, 53, 182, 53, 198, 56, 209, 66, 222, 79, 234, 93, 243, 106, 248, 118, 250, 132, 250, 148, 247, 163, 238, 174, 228, 184, 214, 192, 200, 197, 187, 198, 185, 199, 182, 199, 182, 199, 183]

    def getCircle(self):
        return self.circle

    def getFigureEight(self):
        return self.figureEight