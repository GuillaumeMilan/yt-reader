
def verify(value):
    """ Verify that value is between 0 and 100 """ 
    if value >= 0 and value <= 100:
        return True 
    else :
        return False

class GraphicalObject():
    def __init__(self, obj, width = -1, height = -1, pos_x = 0, pos_y = 0, parent=None):
        """
            height and width are in procent of the parent window.
            if there is no parent, this is in pixel.
            object @type is QObject can be None 
            parent @type is GraphicalObject
            children @type is GraphicalObject
            width height @type are int (can be percent or real size depending if parent is None or not )
        """
        self.__object = obj
        self.__parent = parent
        self.__percent_pos_x = 0
        self.__percent_pos_y = 0
        self.__pos_x = 0
        self.__pos_y = 0
        self.__percent_height = -1
        self.__percent_width = -1
        self.__width = -1
        self.__height = -1
        self.__children = []
        if parent == None:
            self.__height = height
            self.__width = width
            self.__percent_height = -1
            self.__percent_width = -1
            self.__pos_x = pos_x
            self.__pos_y = pos_y
        else: 
            # Add this object to the parent children list 
            self.__parent.addChildren(self)
            # Verify percent size is correct (0-100)
            if (not verify(height)) or (not verify(width)):
                raise ValueError("The size given is not a percent size")
            self.__percent_height = height
            self.__percent_width = width
            self.__percent_pos_x = pos_x
            self.__percent_pos_y = pos_y
            self.__height = (parent.getRealHeight()*height) /100
            self.__width = (parent.getRealWidth()*width)    /100
            self.__pos_y = (parent.getRealHeight()*pos_y)   /100
            self.__pos_x = (parent.getRealWidth()*pos_x)    /100

    def getSize(self):
        if parent == None: 
            return (self.__width, self.__height)
        else :
            return parent.getSize()
    
    def getRealHeight(self):
        return self.__height
    
    def getRealWidth(self):
        return self.__width

    def getPercentHeight(self):
        return self.__percent_height

    def getPercentWidth(self):
        return self.__percent_width

    def getRealPosX(self):
        return self.__pos_x

    def getRealPosY(self):
        return self.__pos_y

    
    def getPercentPosX(self):
        return self.__percent_pos_x

    def getPercentPosY(self):
        return self.__percent_pos_y

    def resize(self, width, height):
        if self.__parent == None:
            self.__height = height
            self.__width = width
            self.__percent_height = -1
            self.__percent_width = -1
        else: 
            # Verify percent size is correct (0-100)
            if (not verify(height)) or (not verify(width)):
                raise ValueError("The size given is not a percent size")
            self.__percent_height = height
            self.__percent_width = width
            self.__height = (self.__parent.getRealHeight()*height) /100
            self.__width = (self.__parent.getRealWidth()*width)    /100
        if self.__object != None:
            self.__object.resize(self.__width, self.__height)
        for i in self.__children :
            i.updateObject()

    def updateObject(self):
        self.__width = ((self.__parent.getRealWidth() * self.__percent_width) 
                / 100)
        self.__height = ((self.__parent.getRealHeight() * self.__percent_height)
                / 100)
        if self.__object != None:
            self.__object.resize(self.__width, self.__height)
    
        self.__pos_x = ((self.__parent.getRealWidth() * self.__percent_pos_x) 
                / 100 + self.__parent.getRealPosX())
        self.__pos_y = ((self.__parent.getRealHeight() * self.__percent_pos_y) 
                /100 + self.__parent.getRealPosY())
        if self.__object != None:
            self.__object.move(self.__pos_x, self.__pos_y)

        for i in self.__children:
            i.updateObject()

    def move(self, pos_x, pos_y):
        if self.__parent == None:
            self.__pos_x = pos_x
            self.__pos_y = pos_y
            self.__percent_pos_x = 0
            self.__percent_pos_y = 0
        else:
            # Verify percent size is correct (0-100)
            if (not verify(pos_x)) or (not verify(pos_y)):
                raise ValueError("The position given is not a percent size")
            self.__percent_pos_x = pos_x
            self.__percent_pos_y = pos_y 
            self.__pos_x = (self.__parent.getRealWidth()*pos_x)    /100 + self.__parent.getRealPosX()
            self.__pos_y = (self.__parent.getRealHeight()*pos_y)   /100 + self.__parent.getRealPosY()
        if self.__object != None:
            self.__object.move(self.__pos_x, self.__pos_y)
    
    def addChildren(self, children):
        self.__children.append(children)


