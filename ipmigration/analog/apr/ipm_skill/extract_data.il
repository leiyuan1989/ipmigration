
procedure( bBoxToString( bBox)
  let( (x1 y1 x2 y2)
    ; Extract coordinates from the bounding box
    x1 = car(car(bBox))
    y1 = cadr(car(bBox))
    x2 = car(cadr(bBox))
    y2 = cadr(cadr(bBox))
    
    x1 = sprintf(nil "%f " x1)
    y1 = sprintf(nil "%f " y1)
    x2 = sprintf(nil "%f " x2)
    y2 = sprintf(nil "%f " y2)  
    s1 = strcat(x1 y1 x2 y2)

  )
)
procedure( transformToString(transform)
  let( (x1 y1 x2 y2)
    ; Extract coordinates from the bounding box
    loc=nth(0 transform)
    x1=car(loc)
    y1=cadr(loc)
    x1 = sprintf(nil "%f " x1)
    y1 = sprintf(nil "%f " y1)    
    rotate=nth(1 transform)
    s1 = strcat(x1 y1 rotate)
  )
)


;will gen this by python
lib="ipm_demo_amp2"
cell="OTA"
cell2="test2"

view_sch="schematic"
view_lay="layout"

data_dir="."

nmos="nmos3v"
pmos="pmos3v"
res1 = "rnhpoly"
cap1 = "mimcap"


data_file=strcat(data_dir "/layout_data.txt")
outHandle=outfile(data_file)
;sch=dbOpenCellViewByType(lib cell view_sch "" "r")
cv=dbOpenCellViewByType(lib cell view_lay "" "r")

;inst_sch=setof(x sch~>instances x~>libName==lib && x~>cellName==cell && x~>viewName==view_sch)

;simulator('spectre)
;design(lib cell view_sch "r")
;createNetlist(?display nil)
foreach(inst cv~>instances
    instName=inst->name    
    cellName=inst->cellName
    
    cond(
        ( cellName == pmos
    
            printf("\npmos: %s \n" instName)
            bBox = bBoxToString(inst->bBox)
            trans = transformToString(inst->transform)
            fprintf(outHandle "%s %s %s %s %s %s\n" instName cellName bBox trans inst->l inst->w )  
        )
    
        ( cellName == nmos
    
            printf("\nnmos: %s \n" instName)
            bBox = bBoxToString(inst->bBox)
            trans = transformToString(inst->transform)
            fprintf(outHandle "%s %s %s %s %s %s\n" instName cellName bBox trans inst->l inst->w )  
        )
        ( cellName == res1
    
            printf("\nnmos: %s \n" instName)
            bBox = bBoxToString(inst->bBox)
            trans = transformToString(inst->transform)
            fprintf(outHandle "%s %s %s %s %s %s %s\n" instName cellName bBox trans inst->l inst->w inst->segments)  
        )    
        ( cellName == cap1
    
            printf("\nnmos: %s \n" instName)
            bBox = bBoxToString(inst->bBox)
            trans = transformToString(inst->transform)
            fprintf(outHandle "%s %s %s %s %s %s\n" instName cellName bBox trans inst->l inst->w)  
        )         



       (t
    
          printf("no mos: %s %s\n" instName cellName)
        )

    

    );cond
);end foreach


foreach(via cv~>vias 
    viaType=via->viaHeader~>viaDefName
    bBox = bBoxToString(via->bBox)
    orient = via->orient
    rows = sprintf(nil "%d"  via->cutRows)
    cols = sprintf(nil "%d"  via->cutColumns)
    fprintf(outHandle "vias %s %s %s %s %s\n" viaType bBox orient rows cols)
);foreach  

foreach(shape cv~>shapes 
    objType = shape->objType
    cond(
        ( objType == "pathSeg"
            printf(shape->layerName)
            if(shape->layerName=="DIFF"
               s1 = shape
            )
          
            ;printf("\npmos: %s \n" instName)
            ;bBox = bBoxToString(inst->bBox)
            ;trans = transformToString(inst->transform)
            ;fprintf(outHandle "%s %s %s %s %s %s\n" instName cellName bBox trans inst->l inst->w )  
        )



       (t
    
          t
        )   
    );cond



);foreach  





close( outHandle )




















cv2=dbOpenCellViewByType(lib cell2 view_lay "" "w")

mastercv = dbOpenCellViewByType("tsmc18rf" pmos view_lay "" "r")

dbCreateParamInst(cv2 mastercv "inst1" list(0 0) "R0" 1 list( list("w" "string" "21u") list("l" "string" "2u") ) )

dbSave(cv2)
