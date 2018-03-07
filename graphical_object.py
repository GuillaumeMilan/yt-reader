def verify(value):
    """ 
################################################################################
# DESCRIPTION:
#   Verify that value is between 0 and 100 
################################################################################
    """
    if value >= 0 and value <= 100:
        return True 
    else :
        return False

class GraphicalObject():
    """
################################################################################
# DESCRIPTION:
#   This @class is used to create a hirearchy of PyQt object in order to scale
#   a window content to the window size
################################################################################
    """

    def __init__(self, obj, width = -1, height = -1, pos_x = 0, pos_y = 0, parent=None):
        """
################################################################################
# DESCRIPTION: 
#            height and width are in procent of the parent window.
#            if there is no parent, this is in pixel.
#            object @type is QObject can be None 
#            parent @type is GraphicalObject
#            children @type is GraphicalObject
#            width and height @type are int (can be percent or real size 
#               depending if parent is None or not )
################################################################################
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
            self.__parent.__add_children(self)
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
        """
################################################################################
# DESCRIPTION:
#   Return (@int,@int) the size of the main window in pixel
################################################################################
        """
        if parent == None: 
            return (self.__width, self.__height)
        else :
            return parent.getSize()
    
    def getRealHeight(self):
        """
################################################################################
# DESCRIPTION:
#   Return @int the height of the object in pixel 
################################################################################
        """
        return self.__height
    
    def getRealWidth(self):
        """
################################################################################
# DESCRIPTION:
#   Return @int the width of the object in pixel
################################################################################
        """
        return self.__width

    def getPercentHeight(self):
        """
################################################################################
# DESCRIPTION:
#  Return @int the height of the object in percentage of the parent object
################################################################################
        """
        return self.__percent_height

    def getPercentWidth(self):
        """
################################################################################
# DESCRIPTION:
#   Return @int the width of the object in percentage of the parent object
################################################################################
        """
        return self.__percent_width

    def getRealPosX(self):
        """
################################################################################
# DESCRIPTION:
#   Return @int the position (X) of the object in the main window in pixel
################################################################################
        """
        return self.__pos_x

    def getRealPosY(self):
        """
################################################################################
# DESCRIPTION:
#   Return @int the position (Y) of the object in the main window in pixel
################################################################################
        """
        return self.__pos_y

    
    def getPercentPosX(self):
        """
################################################################################
# DESCRIPTION:
#   Return @int the position (X) of the object in percentage of the width of the
#   parent object.
################################################################################
        """
        return self.__percent_pos_x

    def getPercentPosY(self):
        """
################################################################################
# DESCRIPTION:
#   Return @int the position (X) of the object in percentage of the width of the
#   parent object.
################################################################################
        """
        return self.__percent_pos_y

    def resize(self, width, height):
        """
################################################################################
# DESCRIPTION:
#   object.resize(@int,@int) resize the object to percent height and width of 
#   the parent.
#   If there is no parent then the object is resize exactly to this size in 
#   pixel.
################################################################################
        """
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
        """
################################################################################
# DESCRIPTION:
#   This method scale the size of the object and all his children to the size 
#   of his parent
#   TODO put in private ?
################################################################################
        """
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
        print("OBJECT: WIDTH = "+str(self.__width)+" HEIGHT = "+str(self.__height)+" POS X = "+str(self.__pos_x)+" POS Y = "+str(self.__pos_y))

    def move(self, pos_x, pos_y):
        """
################################################################################
# DESCRIPTION:
#   This method move the object in the parent. 
#   @arg pos_x is @int and is in percent of the parent width (absolute if no 
#   parent).
#   @arg pos_y is @int and is in percent of the parent height (absolute if no 
#   parent).
################################################################################
        """
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
    
    def __add_children(self, children):
        """
################################################################################
# DESCRIPTION:
#   Add a children to the current object.
################################################################################
        """
        self.__children.append(children)

    def delete_children(self, children):
        """
################################################################################
# DESCRIPTION:
#   Remove a children to the current object.
#   TODO put it in private
################################################################################
        """
        self.__children.remove(children)
        del children


