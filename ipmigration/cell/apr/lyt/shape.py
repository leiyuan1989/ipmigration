# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:43:28 2024

@author: leiyuan
"""
import klayout.db as db

class Range:
    def __init__(self, a, b, set_t = 'cw'):
        #type ch bt
        self.set_value(a, b, set_t = set_t)
    
    def set_value(self, a, b, set_t = 'cw'):
        if set_t == 'cw':
            self.c = a
            self.w = b
            self.p1 = self.c - int(0.5*self.w)
            self.p2 = self.c + int(0.5*self.w)
        elif set_t == 'pp':
            self.p1 = min(a,b)
            self.p2 = max(a,b)
            self.w = self.p2 - self.p1
            self.c =  int(0.5*(self.p1 + self.p2))
            
        self.range = [self.p1,self.p2]    
    def in_track(self, p):
        return p in self.range

    def __repr__(self):
        return 'b:%d c:%d u:%d'%(self.p1,self.c,self.p2)

    def is_in(self, o_range):
        return (self.p1 >= o_range.p1) and (self.p2 <= o_range.p2) 
    def is_enclose(self, o_range):
        return (self.p1 <= o_range.p1) and (self.p2 >= o_range.p2)   
        
        
    def stretch(self, v):
        self.set_value(self.p1-v, self.p2+v, set_t = 'pp')
        assert self.p2>=self.p1
        
    def move(self, v):
        self.set_value(self.p1+v, self.p2+v, set_t = 'pp') 

    def copy(self):
        return Range(self.c,self.w)



class Box:
    def __init__(self, value=None, name =''):
        
        self.name = name
        self.ll = (0,0)
        self.lr = (0,0)
        self.ul = (0,0)
        self.ur = (0,0)
        self.l = 0
        self.r = 0
        self.t = 0
        self.b = 0
        self.c = (0,0)
        self.w = 0
        self.h = 0
        self.w_h  = 0
        self.h_h  = 0
        self.area = 0
        
        self.set_value(value)

    '''
    Public constructors
    new Box ptr new (const DBox dbox) 
    Creates an integer coordinate box from a box
    new Box ptr new 
    Creates an empty (invalid) box
    new Box ptr new (int w) 
    Creates a square with the given dimensions centered around the origin
    new Box ptr new (int w, int h)
    Creates a rectangle with given width and height, centered around the origin 
    new Box ptr new (int left, int bottom, int right, int top) Creates a box with four coordinates
    new Box ptr new (const Point lower_left, const Point upper_right)
    Creates a box from two points
    
    '''

        
    def set_value(self, value):
        if value:
            if isinstance(value, Box):
                #Creates an integer coordinate box from a box
                self.copy_from(value)
            elif isinstance(value, list):
                if value[-1] == 'c':
                    if len(value) == 3:
                        p, ext, _ = value
                        if isinstance(p, tuple) and isinstance(ext, int):
                            # Creates a square with the given dimensions centered around the point
                            self.c =  p
                            self.w_h  = ext
                            self.h_h  = ext
                            self.ll = (p[0]-ext,p[1]-ext)
                            self.lr = (p[0]+ext,p[1]-ext)
                            self.ul = (p[0]-ext,p[1]+ext)
                            self.ur = (p[0]+ext,p[1]+ext)
                            self.l =  p[0]-ext
                            self.r =  p[0]+ext
                            self.t =  p[1]+ext
                            self.b =  p[1]-ext
                            self.w =  2*ext
                            self.h =  2*ext                           
                            self.area = self.w * self.h     
                        else:
                            raise ValueError('Box init error!')
                    elif len(value) ==4:
                        p, ext_w, ext_h, _ = value
                        if isinstance(p, tuple) and isinstance(ext_h, int) and isinstance(ext_w, int):
                            # Creates a rectangle with given width and height, centered around the origin 
                            self.c =  p
                            self.w_h  = ext_w
                            self.h_h  = ext_h
                            self.ll = (p[0]-ext_w,p[1]-ext_h)
                            self.lr = (p[0]+ext_w,p[1]-ext_h)
                            self.ul = (p[0]-ext_w,p[1]+ext_h)
                            self.ur = (p[0]+ext_w,p[1]+ext_h)
                            self.l =  p[0]-ext_w
                            self.r =  p[0]+ext_w
                            self.t =  p[1]+ext_h
                            self.b =  p[1]-ext_h
                            self.w =  2*ext_w
                            self.h =  2*ext_h                           
                            self.area = self.w * self.h
                            
                        else:
                            raise ValueError('Box init error!')
                    else:
                        raise ValueError('Box init error!')
                else:
                    if len(value) == 2:
                        p1,p2 = value
                        if isinstance(p1, tuple) and isinstance(p2, tuple):
                            #Creates a box from two points ll&ur or lr&ul
                            self.l = min(p1[0],p2[0])
                            self.r = max(p1[0],p2[0])
                            self.b = min(p1[1],p2[1])
                            self.t = max(p1[1],p2[1])
                            
                            self.ll = (self.l,self.b)
                            self.lr = (self.r,self.b)
                            self.ul = (self.l,self.t)
                            self.ur = (self.r,self.t)
                            
                            self.w = self.r - self.l
                            self.h = self.t - self.b
                            self.w_h  = int(0.5*self.w )
                            self.h_h  = int(0.5*self.h )
                            
                            self.c = (self.l+self.w_h, self.b+self.h_h)
                            self.area = self.w * self.h            
                        else:
                            raise ValueError('Box init error!')
                    elif len(value) == 3:
                        p,w,h = value
                        if isinstance(p, tuple) and isinstance(w, int) and isinstance(h, int):
                            self.w = w
                            self.h = h
                            self.w_h  = int(0.5*self.w )
                            self.h_h  = int(0.5*self.h )
                            
                            self.l = p[0]
                            self.r = p[0] + w
                            self.b = p[1]
                            self.t = p[1] + h
                            
                            self.ll = p
                            self.lr = (self.r,self.b)
                            self.ul = (self.l,self.t)
                            self.ur = (self.r,self.t)
                            
                            self.c = (self.l+self.w_h, self.b+self.h_h)
                            self.area = self.w * self.h                            
                        else:
                            raise ValueError('Box init error!')
                        
                    elif len(value) == 4:
                        l,b,r,t = value
                        if isinstance(l, int) and isinstance(r, int) and isinstance(b, int) and isinstance(t, int):
                            #(int left, int bottom, int right, int top) Creates a box with four coordinates
                            self.l = l
                            self.r = r
                            self.b = b
                            self.t = t
                            
                            self.ll = (self.l,self.b)
                            self.lr = (self.r,self.b)
                            self.ul = (self.l,self.t)
                            self.ur = (self.r,self.t)
                            
                            self.w = self.r - self.l
                            self.h = self.t - self.b
                            self.w_h  = int(0.5*self.w )
                            self.h_h  = int(0.5*self.h )
                            
                            self.c = (self.l+self.w_h, self.b+self.h_h)
                            self.area = self.w * self.h    
                        else:
                            raise ValueError('Box init error!')
                    
                    else:
                        raise ValueError('Box init error!')                                 
                
            
        else:
            #Creates an empty (invalid) box
            pass
        
        
        
    def copy_from(self, box):
        self.name = box.name
        self.ll = box.ll
        self.lr = box.lr
        self.ul = box.ul
        self.ur = box.ur
        self.l =  box.l
        self.r =  box.r
        self.t =  box.t
        self.b =  box.b
        self.c =  box.c
        self.w =  box.w
        self.h =  box.h
        self.w_h  = box.w_h
        self.h_h  = box.h_h
        self.area = box.area       
    
    def copy(self):
        new_box = Box()
        new_box.name = self.name
        new_box.ll = self.ll
        new_box.lr = self.lr
        new_box.ul = self.ul
        new_box.ur = self.ur
        new_box.l =  self.l
        new_box.r =  self.r
        new_box.t =  self.t
        new_box.b =  self.b
        new_box.c =  self.c
        new_box.w =  self.w
        new_box.h =  self.h
        new_box.w_h  = self.w_h
        new_box.h_h  = self.h_h
        new_box.area = self.area       
        return new_box      
        
        
    def move(self, x, y):
        new_ll = (self.l+x, self.b+y)
        self.set_value([new_ll, self.w, self.h])

    def stretch(self, ext_x, ext_y):
        new_lbrt = [self.l-ext_x,
                    self.b-ext_y,
                    self.r+ext_x, 
                    self.t+ext_y]
        self.set_value(new_lbrt)

    def to_dbBox(self):
        return db.Box(db.Point(self.l, self.b),
                      db.Point(self.r, self.t))

    def __repr__(self):
        return 'name:%s, l:%d, b:%d, r:%d, t:%d'%(self.name, self.l, self.b, self.r, self.t)


'''
Test 

p1 = (1,1)
p2 = (6,7)
w = 5
h = 6

b1 = Box(name='b1') 
b2 = Box([p1,w,h],name='b2')
b3 = Box([p1,p2],name='b3')
b4 = Box([1,1,6,7],name='b4')
b5 = Box(b2,name='b5')

b6 = Box([p1,w,'c'],name='b6')
b7 = Box([p1,w,h,'c'],name='b7')
print(b1)
print(b2)
print(b3)
print(b4)
print(b5)
print(b6)
print(b7)

'''

class Text:
    def __init__(self):
        pass

class Shapes:
    #A shapes collection is a collection of geometrical objects, such as polygons, boxes, paths, edges, edge pairs or text objects.
    #Shapes objects are the basic containers for geometrical objects of a cell. Inside a cell, there is one Shapes object per layer.
    def __init__(self):
        self.shapes = []
    def add(self,shape):
        self.shapes.append(shape)
    def add_from(self,shapes):
        #add shapes from list
        self.shapes = self.shapes + shapes
    def __repr__(self):
        return self.shapes





    
    



