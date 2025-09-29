#analog layout modules

'''

what do you want?


i1 = Instance(name,para,right(r1.inner_left, space))
i2 = Instance(name,para,abut(i1,'right'))
r1 = Ring(name,param,l(v),b(r),r(r),t(v))




ig1 = InstanceGroup()?




'''
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap

PARA_ATTR = {'mos':{'w':{'cdf_name':'w','cdf_unit':'u','cdf_type':'string'},
                    'l':{'cdf_name':'l','cdf_unit':'u','cdf_type':'string'},
                    'm':{'cdf_name':'m','cdf_unit':'','cdf_type':'string'}},
             'mimcap':{'w':{'cdf_name':'w','cdf_unit':'u','cdf_type':'string'},
                       'l':{'cdf_name':'l','cdf_unit':'u','cdf_type':'string'},
                       'm':{'cdf_name':'m','cdf_unit':'','cdf_type':'string'}},
             'respoly':{'w':{'cdf_name':'w','cdf_unit':'u','cdf_type':'string'},
                        'l':{'cdf_name':'l','cdf_unit':'u','cdf_type':'string'},
                        'm':{'cdf_name':'segments','cdf_unit':'','cdf_type':'string'}}
             }


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
        
    def set_value(self, value):
        if value:
            if isinstance(value, Box):
                #Creates an integer coordinate box from a box
                self.copy_from(value)
            elif isinstance(value, list):
                if value[-1] == 'c':
                    if len(value) == 3:
                        p, ext, _ = value
                        if isinstance(p, tuple):
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
                        if isinstance(p, tuple):
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
                            self.w_h  = 0.5*self.w 
                            self.h_h  = 0.5*self.h 
                            
                            self.c = (self.l+self.w_h, self.b+self.h_h)
                            self.area = self.w * self.h            
                        else:
                            raise ValueError('Box init error!')
                    elif len(value) == 3:
                        p,w,h = value
                        if isinstance(p, tuple):
                            self.w = w
                            self.h = h
                            self.w_h  = 0.5*self.w 
                            self.h_h  = 0.5*self.h 
                            
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
                        self.w_h  = 0.5*self.w 
                        self.h_h  = 0.5*self.h 
                        
                        self.c = (self.l+self.w_h, self.b+self.h_h)
                        self.area = self.w * self.h    
  
                    
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

    @staticmethod
    def merge(box1,box2):
        l = min(box1.l,box2.l)
        b = min(box1.b,box2.b)
        r = max(box1.r,box2.r)
        t = max(box1.t,box2.t)
        return Box([l,b,r,t])


    def stretch(self, ext_x, ext_y):
        new_lbrt = [self.l-ext_x,
                    self.b-ext_y,
                    self.r+ext_x, 
                    self.t+ext_y]
        self.set_value(new_lbrt)

    def __repr__(self):
        return 'name:%s, l:%.3f, b:%.3f, r:%.3f, t:%.3f'%(self.name,  self.l, self.b, self.r, self.t)





def rotate(box, transform, center_point):
    """
        transforms = ['R0', 'R90', 'R180', 'R270', 'MY', 'MY90', 'MX', 'MXR90']
    """
    left = box.l
    right = box.r
    top = box.t 
    bottom = box.b  
    center_x, center_y = center_point
    
    # 计算宽度和高度
    width = right - left
    height = bottom - top
    
    if transform == 'R0':
        new_left, new_right = left, right
        new_top, new_bottom = top, bottom
    
    elif transform == 'R90':
        # 围绕指定点顺时针旋转90度
        new_left = center_x - (bottom - center_y)
        new_right = center_x - (top - center_y)
        new_top = center_y + (left - center_x)
        new_bottom = center_y + (right - center_x)
    
    elif transform == 'R180':
        # 围绕指定点旋转180度
        new_left = 2 * center_x - right
        new_right = 2 * center_x - left
        new_top = 2 * center_y - bottom
        new_bottom = 2 * center_y - top
    
    elif transform == 'R270':
        # 围绕指定点顺时针旋转270度
        new_left = center_x + (top - center_y)
        new_right = center_x + (bottom - center_y)
        new_top = center_y - (right - center_x)
        new_bottom = center_y - (left - center_x)
    
    elif transform == 'MY':
        # 围绕指定点沿Y轴镜像
        new_left = 2 * center_x - right
        new_right = 2 * center_x - left
        new_top, new_bottom = top, bottom
    
    elif transform == 'MYR90':
        # 先沿Y轴镜像，再围绕指定点旋转90度
        temp_left = 2 * center_x - right
        temp_right = 2 * center_x - left
        temp_top, temp_bottom = top, bottom
        
        new_left = center_x - (temp_bottom - center_y)
        new_right = center_x - (temp_top - center_y)
        new_top = center_y + (temp_left - center_x)
        new_bottom = center_y + (temp_right - center_x)
    
    elif transform == 'MX':
        # 围绕指定点沿X轴镜像
        new_left, new_right = left, right
        new_top = 2 * center_y - bottom
        new_bottom = 2 * center_y - top
    
    elif transform == 'MXR90':
        # 先沿X轴镜像，再围绕指定点旋转90度
        temp_left, temp_right = left, right
        temp_top = 2 * center_y - bottom
        temp_bottom = 2 * center_y - top
        
        new_left = center_x - (temp_bottom - center_y)
        new_right = center_x - (temp_top - center_y)
        new_top = center_y + (temp_left - center_x)
        new_bottom = center_y + (temp_right - center_x)
    
    else:
        raise ValueError(transform)
    
    return Box([new_left,new_bottom,new_right,new_top])













# class Base:
#     def __init__(self,name,layer):
#         self.name = name
#     @property    
#     def coords(self):
#         coords = []
#         return coords        
#     @property   
#     def is_real(self):
#         for coord in self.coords:
#             if not(coord.is_real):
#                 return False
#         return True
    
#     def realize(self):
#         for coord in self.coords:
#             if not coord.is_real:
#                 try:
#                     ref_rect, ref_coord_name = coord.value
#                     ref_value = getattr(ref_rect, ref_coord_name)
#                     if ref_value.is_real:
#                         coord.value = ref_value.value
#                     else:
#                         return False
#                 except (TypeError, AttributeError):
#                     return False
        
#         return self.is_real

class Rect(Box):
    def __init__(self, layer, box, name=''):
        super().__init__([box.l, box.b, box.r, box.t], name=name)        
        self.layer = layer

    def __repr__(self):
        return  'name:%s, layer:%s, l:%d, b:%d, r:%d, t:%d'%(self.name, self.layer, self.l, self.b, self.r, self.t)

    def skill(self):
        return "dbCreateRect(cvid list(\"%s\" \"drawing\") list(%.2f:%.2f %.2f:%.2f)) \n"%(self.layer, self.l,self.b,self.r,self.t)
        


class Polygon:
    def __init__(self,layer,points):
        self.layer=layer
        self.points = points
    def skill(self):
        # dbCreatePolygon(cvid list("METAL3" "drawing") list(5:-10 0:-10 0:0))
        part1 = "dbCreatePolygon(cvid list(\"%s\" \"drawing\") "%(self.layer)
        part2=  "list("
        for x,y in self.points:
            part2 = part2 + "%.2f:%.2f "%(x,y)
        
        part3 = ")) \n"
        return part1 + part2[:-1] + part3
    


class Vias:
    def __init__(self, layer, size, space, rect1, rect2, enc):
        #TODO; consider enc1 and enc2,                 
        self.rect1 = rect1
        self.rect2 = rect2
        self.size = size
        self.space = space
        self.layer = layer
        self.margin = enc
        

        self.overlap_box = self._calculate_overlap()
        self.vias = []
        if self.overlap_box:
            self.vias = self._generate_squares()
    
    def _calculate_overlap(self):
        overlap_l = max(self.rect1.l, self.rect2.l)
        overlap_r = min(self.rect1.r, self.rect2.r)
        overlap_b = max(self.rect1.b, self.rect2.b)
        overlap_t = min(self.rect1.t, self.rect2.t)
    
        if overlap_l >= overlap_r or overlap_b >= overlap_t:
            return None  
        return Box([overlap_l, overlap_b, overlap_r, overlap_t])
    

    def _generate_squares(self):
        vias = []
        
        required_width = self.size + 2 * self.margin
        required_height = self.size + 2 * self.margin
        
        if (self.overlap_box.w < required_width or 
            self.overlap_box.h < required_height):
            return vias
        
        effective_l = self.overlap_box.l + self.margin
        effective_r = self.overlap_box.r - self.margin
        effective_b = self.overlap_box.b + self.margin
        effective_t = self.overlap_box.t - self.margin
        
        effective_width = effective_r - effective_l
        effective_height = effective_t - effective_b
        
        step_x = self.size + self.space
        step_y = self.size + self.space
        
        max_possible_x = int((effective_width - self.size) / step_x) + 1
        num_x = max_possible_x if max_possible_x % 2 == 1 else max_possible_x - 1
        if num_x < 1:
            return vias
        
        max_possible_y = int((effective_height - self.size) / step_y) + 1
        num_y = max_possible_y if max_possible_y % 2 == 1 else max_possible_y - 1
        if num_y < 1:
            return vias
        
        center_x = self.overlap_box.c[0] - self.size / 2
        center_y = self.overlap_box.c[1] - self.size / 2
        
        half_x = (num_x - 1) // 2
        half_y = (num_y - 1) // 2
        
 
        for i in range(-half_y, half_y + 1):
            for j in range(-half_x, half_x + 1):
                # 计算小正方形左下角坐标
                x = center_x + j * step_x
                y = center_y + i * step_y
                
                # 确保小正方形完全在有效区域内
                if (x >= effective_l and 
                    x + self.size <= effective_r and 
                    y >= effective_b and 
                    y + self.size <= effective_t):
                    
                    box = Box([(x, y), self.size, self.size])
                    via = Rect(self.layer,box)
                    vias.append(via)
        
        return vias
    
    def get_squares(self):
        """返回生成的小正方形列表"""
        return self.vias
    
    def skill(self):
        text = ''
        for via in self.vias:
            text += via.skill()

        return text

class GuardRing:
    def __init__(self, tech, ring_type, ct_num, box_in):
        #ring_type: 'PMOS'/'NMOS'/'RES'
        #TODO: condider box out
        self.tech =tech
        self.modules = []
        if ring_type == 'PMOS':
            ring_to_box = tech.RING_TO_MOS
            out_layer1 = tech.SN
            out_layer1_en = tech.RING_SN_EN_AA
            out_layer2 = tech.NW
            out_layer2_en = tech.RING_NW_EN_AA
            
        elif ring_type == 'NMOS':
            ring_to_box = tech.RING_TO_MOS
            out_layer1 = tech.SP
            out_layer1_en = tech.RING_SP_EN_AA
            out_layer2 = None
        elif ring_type == 'RES':
            #TODO: RES may have a ring of SP
            ring_to_box = tech.RING_TO_RES
            out_layer1 = tech.SN
            out_layer1_en = tech.RING_SN_EN_AA
            out_layer2 = tech.NW
            out_layer2_en = tech.RING_NW_EN_AA
            
        else:
            raise ValueError(ring_type)

        if ct_num == 1:
            ring_width = tech.RING_1CT
        elif ct_num == 2:
            ring_width = tech.RING_2CT
        else:
            raise ValueError()
        box = box_in.copy()
        box.stretch(ring_to_box, ring_to_box)
        self.box = box
    
        l = self.box.l 
        r = self.box.r 
        b = self.box.b 
        t = self.box.t
        
        self.box_out = Box([l-ring_width,b-ring_width,r+ring_width,t+ring_width])
        
        
        box_ll = Box([l-ring_width,b-ring_width,l,b])
        box_lr = Box([r,b-ring_width,r+ring_width,b])
        box_ul = Box([l-ring_width,t,l,t+ring_width])
        box_ur = Box([r,t,r+ring_width,t+ring_width])
        box_l = Box([l-ring_width,b,l,t])
        box_r = Box([r,b,r+ring_width,t])
        box_b = Box([l,b-ring_width,r,b])
        box_t = Box([l,t,r,t+ring_width])
        
        box_list = [box_ll,box_lr,box_ul,box_ur,box_l,box_b,box_r,box_t]
        self.box_ll = box_ll
        self.box_lr = box_lr
        self.box_ul = box_ul
        self.box_ur = box_ur
        self.box_l = box_l
        self.box_r = box_r
        self.box_b = box_b
        self.box_t = box_t        
        
        for box in box_list:
            r1 = Rect(tech.layer[tech.AA][0], box)
            r2 = Rect(tech.layer[tech.M1][0], box)
            self.modules.append(r1)
            self.modules.append(r2)
            self.modules.append(Vias(tech.layer[tech.CT][0], tech.CT_W, tech.CT_S, r1, r2, tech.CT_EN_AA))
            
            #TODO: M1 may not same with AA
            box1 = box.copy()
            box1.stretch(out_layer1_en,out_layer1_en)
            self.modules.append(Rect(tech.layer[out_layer1][0], box1))
            if out_layer2:
                box2 = box.copy()
                box2.stretch(out_layer2_en,out_layer2_en)    
                self.modules.append(Rect(tech.layer[out_layer2][0], box2))
        
        
    def skill(self):
        text = ''
        for module in self.modules:
            text += module.skill()
        return text
        
        
        


class Mos:
    def __init__(self,name,mos_type,tech,w,l,box):
        self.name = name
        self.type =mos_type
        self.tech = tech
        self.w = w
        self.l = l
        self.box=box
        
        self.x = 0 
        self.y = 0
        self.rotation = 'R0'
        self.set_pins()
        
        self.para_attr = PARA_ATTR['mos']
        
    def set_pins(self):
        t = self.tech
        if self.type == 'PMOS':
            self.mos_master='masterpmos'
            self.S_Box = Box([self.x - t.PMOS_GT_CT - t.CT_W-t.CT_EN_M1_MIN,
                              self.y,
                              self.x - t.PMOS_GT_CT + t.CT_EN_M1_MIN,
                              self.y+self.w]
                             )
            self.D_Box = Box([self.x + self.l + t.PMOS_GT_CT - t.CT_EN_M1_MIN,
                              self.y,
                              self.x + self.l + t.PMOS_GT_CT + t.CT_W + t.CT_EN_M1_MIN,
                              self.y+self.w]
                             )        
            self.GT_Box = Box([self.x,
                              self.y-t.PMOS_GT_EXT,
                              self.x+self.l,
                              self.y+self.w+t.PMOS_GT_EXT]
                              )
        
        elif self.type == 'NMOS':
            self.mos_master ='masternmos'
            self.S_Box = Box([self.x - t.NMOS_GT_CT - t.CT_W-t.CT_EN_M1_MIN,
                              self.y,
                              self.x - t.NMOS_GT_CT + t.CT_EN_M1_MIN,
                              self.y+self.w]
                             )
            self.D_Box = Box([self.x + self.l + t.NMOS_GT_CT - t.CT_EN_M1_MIN,
                              self.y,
                              self.x + self.l + t.NMOS_GT_CT + t.CT_W + t.CT_EN_M1_MIN,
                              self.y+self.w]
                             )        
            self.GT_Box = Box([self.x,
                              self.y-t.NMOS_GT_EXT,
                              self.x+self.l,
                              self.y+self.w+t.NMOS_GT_EXT]
                              )
        else:
            raise ValueError( self.type)
        # self.box_list = [self.Box,
        
    def copy(self,name):
        return Mos(name,self.type,self.tech,self.w,self.l,self.box.copy())
        
        
    def move(self,x,y,rotation='R0'):
        assert rotation in ['R0','MY']
        if rotation != 'R0':
            self.rotation=rotation
        
        self.x = x
        self.y = y
        self.box.move(x, y)
        self.S_Box.move(x, y)      
        self.D_Box.move(x, y)   
        self.GT_Box.move(x, y)
        
        if rotation in ['MY']:

            box = rotate(self.box,rotation,(self.x,self.y))
            GT_Box = rotate(self.GT_Box,rotation,(self.x,self.y))
            D_Box = rotate(self.S_Box,rotation,(self.x,self.y))
            S_Box = rotate(self.D_Box,rotation,(self.x,self.y))
            # print('test1',box,self.box)
            self.box = box
            self.GT_Box = GT_Box
            self.S_Box = S_Box
            self.D_Box = D_Box
               
    def abutment(self, target_mos, direction):
        assert direction in ['L','R']# L: self is on left of target mos
        if direction == 'L':
            c1 = target_mos.S_Box.c
            c2 = self.D_Box.c
        if direction == 'R':
            c1 = target_mos.D_Box.c
            c2 = self.S_Box.c
        x = c1[0] - c2[0]
        y = c1[1] - c2[1]
        self.move(x,y)
        
        
        
        
        
    def skill(self):
        w_cdf = self.para_attr['w']['cdf_name']
        l_cdf = self.para_attr['l']['cdf_name']
        w_type = self.para_attr['w']['cdf_type']
        l_type = self.para_attr['l']['cdf_type']
        
        part1 =  "dbCreateParamInst(cvid %s \"%s\" "%(self.mos_master,self.name)
        part2 = "list(%.3f %.3f) \"%s\" 1 "%(self.x, self.y, self.rotation)
        part3 = "list(list(\"%s\" \"%s\" \"%.2fu\") list(\"%s\" \"%s\" \"%.2fu\") ))\n"%(w_cdf,w_type,self.w,l_cdf,l_type,self.l)
        return part1 + part2 + part3


        

    

class Res:
    def __init__(self, tech, name, x, y,  w, l, rotation, segments):
        self.name = name
        self.tech = tech
        self.x = x
        self.y = y
        self.w = w
        self.l = l
        self.rotation = rotation
        self.segments = segments
        self.res_master = 'masterres'
        self.set_pins()
        self.para_attr = PARA_ATTR['respoly']
        
    def set_pins(self):
        t = self.tech
        
        box = Box([0 - t.RES_BOX_X, 
                   0 - t.RES_BOX_Y, 
                   0 + 2*t.RES_PO_EXT + self.l + t.RES_BOX_X,
                   0 + self.segments*self.w + (self.segments - 1)*t.RES_PO_S + t.RES_BOX_Y])
        
        box_a = Box([0,0,0+t.RES_PO_EXT,0+self.w])
        box_b = box_a.copy()
        box_b.move(0,(self.segments-1)*(t.RES_PO_S + self.w))
    
        box = rotate(box,self.rotation,(0,0))
        box_a = rotate(box_a,self.rotation,(0,0))
        box_b = rotate(box_b,self.rotation,(0,0))
        
        box.move(self.x,self.y)
        box_a.move(self.x,self.y)
        box_b.move(self.x,self.y)
        
        self.box  = Box([box.c,abs(box.w_h),abs(box.h_h),'c'])
        self.box_a = Box([box_a.c,abs(box_a.w_h),abs(box_a.h_h),'c'])
        self.box_b = Box([box_b.c,abs(box_b.w_h),abs(box_b.h_h),'c'])
        
    def skill(self):
        w_cdf = "\"%s\""%(self.para_attr['w']['cdf_name'])
        l_cdf = "\"%s\""%(self.para_attr['l']['cdf_name'])
        m_cdf = "\"%s\""%(self.para_attr['m']['cdf_name'])
        w_type = self.para_attr['w']['cdf_type']
        l_type = self.para_attr['l']['cdf_type']
        m_type = self.para_attr['m']['cdf_type']
        
        if w_type =='string':
            w_value = "\"%.2fu\""%(self.w)
        elif w_type == 'int':
            w_value = "%d"%(self.w)
        else:
            pass
        if l_type =='string':
            l_value = "\"%.2fu\""%(self.l)
        elif l_type == 'int':
            l_value = "%d"%(self.l)
        else:
            pass
        
        if m_type =='string':
            m_value = "\"%d\""%(self.segments)
        elif m_type == 'int':
            m_value = "%d"%(self.segments)
        else:
            pass    
            
        w_type = "\"%s\""%(w_type)
        l_type = "\"%s\""%(l_type)
        m_type = "\"%s\""%(m_type)
        
        part1 =  "dbCreateParamInst(cvid %s \"%s\" "%(self.res_master,self.name)
        part2 = "list(%.3f %.3f) \"%s\" 1 "%(self.x, self.y, self.rotation)
        part3 = "list(list(%s %s %s) list(%s %s %s) list(%s %s %s) ))\n"%(w_cdf,w_type,w_value,l_cdf,l_type,l_value,m_cdf,m_type,m_value)
        return part1 + part2 + part3


class MimCap:
    def __init__(self, tech, name, x, y,  w, l, rotation):
        self.name = name
        self.tech = tech
        self.x = x
        self.y = y
        self.w = w
        self.l = l
        self.rotation = rotation
        self.cap_master = 'mastercap'
        self.set_pins()
        
        self.para_attr = PARA_ATTR['mimcap']
        
    def set_pins(self):
        t = self.tech
        
        '''
        
        CAP_BOX_X,  CAP, 2.4, ''
        CAP_BOX_Y,  CAP, 2.4, ''
        CAP_BOX_M5, CAP, 2.4, ''
        CAP_BOX_M6, CAP, 2.0, ''
        '''
        
        box = Box([0 - t.CAP_BOX_X, 
                   0 - t.CAP_BOX_Y, #TODO: need test future
                   0 + t.CAP_BOX_X + self.w,
                   0 + t.CAP_BOX_Y + self.l])
    
        box = rotate(box,self.rotation,(0,0))
        box.move(self.x,self.y)        
        self.box  = box

        
    def skill(self):
        w_cdf = "\"%s\""%(self.para_attr['w']['cdf_name'])
        l_cdf = "\"%s\""%(self.para_attr['l']['cdf_name'])
        # m_cdf = "\"%s\""%(self.para_attr['m']['cdf_name'])
        w_type = self.para_attr['w']['cdf_type']
        l_type = self.para_attr['l']['cdf_type']
        # m_type = self.para_attr['m']['cdf_type']
        
        if w_type =='string':
            w_value = "\"%.2fu\""%(self.w)
        elif w_type == 'int':
            w_value = "%d"%(self.w)
        else:
            pass
        if l_type =='string':
            l_value = "\"%.2fu\""%(self.l)
        elif l_type == 'int':
            l_value = "%d"%(self.l)
        else:
            pass
        
        # if m_type =='string':
        #     m_value = "\"%.2fu\""%(self.segments)
        # elif m_type == 'int':
        #     m_value = "%d"%(self.segments)
        # else:
        #     pass    
            
        w_type = "\"%s\""%(w_type)
        l_type = "\"%s\""%(l_type)
        # m_type = "\"%s\""%(m_type)
        
        
        part1 =  "dbCreateParamInst(cvid %s \"%s\" "%(self.cap_master,self.name)
        part2 = "list(%.3f %.3f) \"%s\" 1 "%(self.x, self.y, self.rotation)
        part3 = "list(list(%s %s %s) list(%s %s %s) ))\n"%(w_cdf,w_type,w_value,l_cdf,l_type,l_value)
        return part1 + part2 + part3      

# R2 rnhpoly 82.870000 17.485000 85.560000 21.025000  83.090000 17.665000 MXR90 2.1u 1u 2
# R3 rnhpoly 56.005000 17.230000 58.695000 21.050000  58.475000 20.870000 MYR90 2.38u 1u 2
# C1.2 mimcap 28.215000 21.060000 61.015000 53.860000  30.615000 23.460000 R0 28u 28u
# C1.1 mimcap 61.015000 21.060000 93.815000 53.860000  63.415000 23.460000 R0 28u 28u

# RES_BOX_X, RES, 0.18, ''
# RES_BOX_Y, RES, 0.22, ''
# RES_PIN_X, RES, 0.22, ''
# RES_PIN_Y, RES, 0.315, ''
# RES_PIN_W, RES, 0.34, ''
# RES_PIN_H, RES, 0.81, ''
# CAP_BOX_X,  CAP, 2.4, ''
# CAP_BOX_Y,  CAP, 2.4, ''
# CAP_BOX_M5, CAP, 2.4, ''
# CAP_BOX_M6, CAP, 2.0, 






class Group:
    def __init__(self, tech, mos_type, master_mos, mos_data, group):
        self.tech = tech
        self.group = group
        # self.master_mos = master_mos
        self.mos = {}
        self.rotate = {}
        self.type = mos_type
        for mos_name in group:
             t,l,w,r = mos_data[mos_name] 
             master = master_mos[(t,w,l)]
             self.mos[mos_name] = master.copy(mos_name)
             self.rotate[mos_name] = r
    
        self.SD_pin = []
        self.GT_pin = []
        
    def draw(self, x, y, direction='LL'):
        #direction = 'LL' 'LR'  
        #TODO UL UR 
        box = [[],[],[],[]]
        if direction == 'LL':
            pass
        elif direction == 'LR':
            last_mos = None
            for i, mos_name in enumerate(self.group[::-1]):
                r = self.rotate[mos_name]
                mos = self.mos[mos_name]
                if i == 0:
                    mos.move(x,y,r)
                else:
                    mos.move(0,0,r)
                    mos.abutment(last_mos,'L')
                last_mos = mos                  
                box[0].append(mos.box.l)
                box[1].append(mos.box.b)                
                box[2].append(mos.box.r)                
                box[3].append(mos.box.t)        
            self.box = Box([min(box[0]),min(box[1]),max(box[2]),max(box[3])])
            
        else:
            pass
        
    def draw_SD_pin(self):

        for i, mos_name in enumerate(self.group):
            mos = self.mos[mos_name]
            if i == 0:
                box = Box( [mos.S_Box.c, 0.5*self.tech.MOS_SD_W,mos.S_Box.h_h,'c'])
                self.SD_pin.append(Rect(self.tech.layer[self.tech.M1][0],box))
            box = Box( [mos.D_Box.c, 0.5*self.tech.MOS_SD_W,mos.S_Box.h_h, 'c'])
            self.SD_pin.append(Rect(self.tech.layer[self.tech.M1][0],box))                
        
        self.SD_pin.sort(key=lambda x: x.l)
    
    def draw_GT_pin(self,loc='U'): 
        #loc: U or D
        tech = self.tech
        if loc == 'U':
            tops = []            
            for i, mos_name in enumerate(self.group):
                mos = self.mos[mos_name]
                top = mos.GT_Box.t + tech.MOS_GT_GT_PIN_H
                bottom = mos.GT_Box.t
                left = mos.GT_Box.l 
                right =  mos.GT_Box.r
                tops.append(top)
                
                box_gt = Box([left,bottom,right,top])
                rect_gt = Rect(tech.layer[tech.GT][0],box_gt)
                box_m1 = Box([left + tech.MOS_GT_M1_PIN_EN,bottom,right-tech.MOS_GT_M1_PIN_EN,top])
                rect_m1 = Rect(tech.layer[tech.M1][0],box_m1)
                vias = Vias(tech.layer[tech.CT][0], tech.CT_W, tech.CT_S, rect_gt, rect_m1, tech.CT_EN_M1_END)
                
                self.GT_pin.append([rect_gt,rect_m1,vias])
                # self.GT_pin .append(rect_m1)
                # self.GT_pin .append(vias)
            
            new_box = Box([self.box.l,self.box.b,self.box.r,max(tops)])
            self.box = new_box
            
        elif loc == 'D':
            bottoms = []            
            for i, mos_name in enumerate(self.group):
                mos = self.mos[mos_name]
                top = mos.GT_Box.b 
                bottom = mos.GT_Box.b - tech.MOS_GT_GT_PIN_H
                left = mos.GT_Box.l 
                right =  mos.GT_Box.r
                bottoms.append(bottom)
                
                box_gt = Box([left,bottom,right,top])
                rect_gt = Rect(tech.layer[tech.GT][0],box_gt)
                box_m1 = Box([left + tech.MOS_GT_M1_PIN_EN,bottom,right-tech.MOS_GT_M1_PIN_EN,top])
                rect_m1 = Rect(tech.layer[tech.M1][0],box_m1)
                vias = Vias(tech.layer[tech.CT][0], tech.CT_W, tech.CT_S, rect_gt, rect_m1, tech.CT_EN_M1_END)
                
                self.GT_pin.append([rect_gt,rect_m1,vias])
                # self.GT_pin .append(rect_m1)
                # self.GT_pin .append(vias)
            
            new_box = Box([self.box.l,min(bottoms) ,self.box.r,self.box.t])
            self.box = new_box
        
        else:
            pass
    
    
        self.GT_pin.sort(key=lambda x: x[0].l)
    
    
    
    
    
    def skill(self):
        text = ''
        for k,v in self.mos.items():
            text += v.skill()
        for v in self.SD_pin:
            text += v.skill()
        for v in self.GT_pin:
            for t in v:
                text += t.skill()
        return text
    
    
    
    






class Canvas:
    def __init__(self, tech, map_dict):
        # self.lib_name = lib_name
        # self.cell_name = cell_name
        self.tech = tech
        self.map_dict = map_dict
        self.modules = []



    def add(self,module):
        self.modules.append(module)
        

    def skill(self, skill_file):
        # map_dict = {'pmos':'pmos3v','nmos':'nmos3v','res':'rnhpoly','cap':'mimcap'}
        with open(skill_file,'w') as f:
            tech = self.tech.tech_name
            
            lib_name = 'ipm_demo_amp2'
            cell_name = 'ota_demo'
            
            # f.write("cvid = dbOpenCellViewByType(\"%s\" \"%s\" \"layout\" \"maskLayout\" \"w\")\n"%(lib_name,cell_name))
            f.write("masterpmos = dbOpenCellViewByType( \"%s\" \"%s\" \"layout\" \"maskLayout\" \"r\")\n"%(tech,self.map_dict['pmos']))
            f.write("masternmos = dbOpenCellViewByType( \"%s\" \"%s\" \"layout\" \"maskLayout\" \"r\")\n"%(tech,self.map_dict['nmos']))
            f.write("masterres = dbOpenCellViewByType( \"%s\" \"%s\" \"layout\" \"maskLayout\" \"r\")\n"%(tech,self.map_dict['res']))
            f.write("mastercap = dbOpenCellViewByType( \"%s\" \"%s\" \"layout\" \"maskLayout\" \"r\")\n"%(tech,self.map_dict['cap']))
            for module in self.modules:
                # print(module)
                f.write(module.skill())



def draw_boxes(boxes, title="Boxes Visualization", figsize=(10, 8)):
    """
    绘制Box对象列表
    
    参数:
        boxes: Box对象列表
        title: 图表标题
        figsize: 图表尺寸
    """
    if not boxes:
        print("没有Box对象可绘制")
        return
    
    # 创建自定义颜色映射
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F0E68C', '#DDA0DD']
    cmap = LinearSegmentedColormap.from_list("custom", colors, N=len(boxes))
    
    # 创建图形和坐标轴
    fig, ax = plt.subplots(figsize=figsize)
    
    # 计算坐标轴范围（留出适当边距）
    all_l = [box.l for box in boxes]
    all_r = [box.r for box in boxes]
    all_b = [box.b for box in boxes]
    all_t = [box.t for box in boxes]
    
    margin_x = (max(all_r) - min(all_l)) * 0.1
    margin_y = (max(all_t) - min(all_b)) * 0.1
    
    ax.set_xlim(min(all_l) - margin_x, max(all_r) + margin_x)
    ax.set_ylim(min(all_b) - margin_y, max(all_t) + margin_y)
    
    # 绘制每个Box
    for i, box in enumerate(boxes):
        # 创建矩形 patch
        rect = patches.Rectangle(
            (box.l, box.b),  # 左下角坐标
            box.w,           # 宽度
            box.h,           # 高度
            linewidth=2,
            edgecolor=cmap(i),
            facecolor=cmap(i),
            alpha=0.3,
            label=box.name if box.name else f"Box {i}"
        )
        ax.add_patch(rect)
        
        # 标记中心点
        ax.plot(box.c[0], box.c[1], 'ko', markersize=5)
        ax.text(box.c[0], box.c[1], 'C', fontsize=12, ha='center', va='center')
        
        # 标记左下角坐标
        ax.text(box.l, box.b, f"({box.l},{box.b})", 
                fontsize=8, ha='right', va='top')
    
    # 设置图表属性
    ax.set_title(title, fontsize=16)
    ax.set_xlabel("X", fontsize=14)
    ax.set_ylabel("Y", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax.legend(loc='best')
    
    # 确保坐标轴比例一致
    ax.set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    plt.show()

            
# b1 = Box([10,10,50,50],'b1')  
# b2 = Box([0,0,60,60],'b2') 
# r1 = Rect('Metal1', b1,'r1')           
# r2 = Rect('Metal2', b2,'r2')   


# v1 = Vias(r1, r2, 5, 5)


# draw_boxes([r1, r2] +v1.vias, "Test Boxes Visualization")
    
    

class Path:
    def __init__(self):
        pass




    







#test
if __name__ == "__main__" :
    
    pass
