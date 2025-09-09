cvid = dbOpenCellViewByType("ipm_demo_amp2" "skill_test" "layout" "maskLayout" "w")
tech = techGetTechFile(cvid)


;dbCreateRect
dbCreateRect(cvid list(16 "drawing") list(0:0 20:10))
dbCreateRect(cvid list("METAL2" "drawing") list(30:20 40:30));ll and ur

;dbCreatePolygon
dbCreatePolygon(cvid list("METAL3" "drawing") list(5:-10 0:-10 0:0))


;dbCreatePath
dbCreatePath(cvid list("METAL2" "drawing") list(30:0 40:0 40:-3) 2 )
dbCreatePath(cvid list("METAL2" "drawing") list(30:-10 40:-10 40:-13) 2 )
dbCreatePath(cvid list("METAL2" "drawing") list(30:-20 40:-20 40:-23) 2 )

dbCreatePath(cvid list("METAL2" "drawing") list(50:0 60:0) 2)
;dbCreatePath(cvid list("METAL2" "drawing") list(50:-10 60:-10) 2 "extendExtend" 2 -2)?
dbCreatePath(cvid list("METAL2" "drawing") list(50:-20 60:-20) 2 "roundRound")
dbCreatePath(cvid list("METAL2" "drawing") list(50:-30 60:-30) 2 "extendExtend")
dbCreatePath(cvid list("METAL2" "drawing") list(50:-40 60:-40) 2 "varExtendExtend")
;"extendExtend"
;"roundRound"
;"truncateExtend" default
;"varExtendExtend"

;dbCreateLabel
dbCreateLabel(cvid list("METAL2" "pin") -10:-10 "myLabel" "centerLeft" "R0" "roman" 2)
;dbCreateTextDisplay?

;dbCreatePathSeg?

;dbCreateRoute？

;dbCreateVia
viaDefId = techFindViaDefByName(tech "M2_M1")
viaParams = list(list("cutRows" 3) list("cutColumns" 3))

;Place the via at the coordinate, and with orientation you want； must use calculation
newVia = dbCreateVia(cvid viaDefId list(-50 -50) "R0" viaParams) 

;dbCreateViaShapeArray

;dbCreateInst 
mastercv = dbOpenCellViewByType( "tsmc18rf" "pmos3v" "layout" "maskLayout" "r")
dbCreateParamInst(cvid mastercv "inst1" list(-10 -10) "R0" 1 list(list("w" "string" "21u") list("l" "string" "2u") ))


;dbCreateParamInst
;  (Tools -> CDF -> Edit) to see parameter



dbSave(cvid)