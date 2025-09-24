/* ip_migration.il

Author     LEI Yuan
Group      Hong Kong Applied Science and Technology Research Institute (ASTRI) 
Language   SKILL
Date Created    Dec 24, 2024 
Last Modified   Jan 02, 2025 
By         LEI Yuan

Skill code of ip migration project
Cadence Version: IC 6.1.8
***************************************************

*/

/***************************************************************
*                                                              *
*                       ipmCreateForm()                       *
*                                                              *
*                     Create the main form                     *
*                                                              *
***************************************************************/

procedure(ipmCreateForm()
    let((libName cellName viewName mapSelect tLibName tCellName tViewName tBrowse
        mapSetLabel sLibName sCellName sViewName sBrowse mapFile mapFileSel createInst mapRun
        sep1 sep2 sep3 sep4 sep5 sep6
       )
   
        ;target cellView specification

        tLibName=hiCreateStringField(
                ?name 'tLibName
                ?prompt "Target Library Name"
                ?callback "ddsUpdateSyncWithForm()"
            )
        tCellName=hiCreateStringField(
                ?name 'tCellName
                ?prompt "Target Cell Name"
                ?callback "ddsUpdateSyncWithForm()"
            )
        tViewName=hiCreateStringField(
                ?name 'tViewName
                ?prompt "Target View Name"
                ?callback "ddsUpdateSyncWithForm()"
            )
        tBrowse=hiCreateButton(
                ?name 'tBrowse
                ?buttonText "Browse"
                ?callback "ipmTargetSyncBrowser()"
            )
        
        sep1=hiCreateSeparatorField(?name 'sep1)           
        
        mapSelect=hiCreateRadioField(
                ?name 'mapSelect
                ?prompt "Schematic Mapping"
                ?choices list("Yes" "No")
                ?value  "Yes"
                ?callback list("mapRadioButtonCB()")
            )        
        ;source cellView specification 
		mapSetLabel=hiCreateLabel( 
                ?name 'mapSetLabel
                ?labelText "Schematic Porting"
                ?justification 'left 
                ;?justification 'right 
            )
        sLibName=hiCreateStringField(
                ?name 'sLibName
                ?prompt "Source Library Name"
                ?callback "ddsUpdateSyncWithForm()"
                ;?enabled nil ;or t
            )
        sCellName=hiCreateStringField(
                ?name 'sCellName
                ?prompt "Source Cell Name"
                ?callback "ddsUpdateSyncWithForm()"
                ;?enabled nil ;or t
            )
        sViewName=hiCreateStringField(
                ?name 'sViewName
                ?prompt "Source View Name"
                ?callback "ddsUpdateSyncWithForm()"
                ;?enabled nil ;or t
            )
        sBrowse=hiCreateButton(
                ?name 'sBrowse
                ?buttonText "Browse"
                ?callback "ipmSourceSyncBrowser()"
                ;?enabled nil ;or t
            )
        createInst=hiCreateRadioField(
                ?name 'createInst
                ?prompt "Recreate Instance"
                ?choices list("Yes" "No")
                ?value  "No"
                ?enabled nil
                ;?callback list("mapRadioButtonCB()")
            )          
        mapFile=hiCreateStringField(
                ?name  'mapFile
                ?prompt  "Mapping File"
                ;?enabled nil ;or t
            ) ;hiCreateStringField   
        mapFileSel=hiCreateFormButton(
                ?name 'mapFileSel
                ?buttonText "Select"
                ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'mapFile  \"*.map\" 'anyFile \"mapping file select\")"
                ;?enabled nil ;or t
            ) ;hiCreateFormButton        
        mapRun=hiCreateButton(
                ?name 'mapRun
                ?buttonText "Run Schematic Porting"
                ?callback "mapRunButtonCB()"
                ;?enabled nil ;or t
            )
        sep2=hiCreateSeparatorField(?name 'sep2)
        
        optLabel=hiCreateLabel( 
                ?name 'optLabel
                ?labelText "Circuit Optimization Setting"
                ?justification 'left 
            )

        exportLabel=hiCreateLabel( 
                ?name 'exportLabel
                ?labelText "1. Exprot Schematic Data"
                ?justification 'left 
            )

        importLabel=hiCreateLabel( 
                ?name 'importLabel
                ?labelText "2. Improt Sized Schematic Data"
                ?justification 'left 
            )

        settingFile=hiCreateStringField(
                ?name  'settingFile
                ?prompt  "Sized Schematic Data"
                ?enabled t 
                ?defValue ""
            )    
        settingFileSel=hiCreateFormButton(
                ?name 'settingFileSel
                ?buttonText "Select"
                ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'settingFile  \"*.il\" 'anyFile \"sized schematic data select\")"
                ?enabled t
            )    

        logFolder=hiCreateStringField(
                ?name  'logFolder
                ?prompt  "Export Direcotry"
                ?defValue simplifyFilename("./") 
                ?enabled t 
            )    
        logFolderSel=hiCreateFormButton(
                ?name 'logFolderSel
                ?buttonText "Select"
                ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'logFolder  \"*.*\" 'directoryOnly \"export direcotry select\")"
                ?enabled t
            )  
         

        optField = hiCreateCyclicField(
                ?name 'optField
                ?prompt "Simulator:"
                ?defValue "Spectre" 
                ?choices list("Spectre" "Hspice" "NGspice")
                ;?callback "callbackOne"
               )

        
        exportRun=hiCreateButton(
                ?name 'exportRun
                ?buttonText "Export Schematic Data"
                ?callback "exportRunButtonCB()"
                ;?enabled nil ;or t
            )

        importRun=hiCreateButton(
                ?name 'importRun
                ?buttonText "Import Schematic Data"
                ;?callback "exportRunButtonCB()"
                ;?enabled nil ;or t
            )



        layoutLabel=hiCreateLabel( 
                ?name 'layoutLabel
                ?labelText "Layout Porting"
                ?justification 'left 
            )

        layoutFile=hiCreateStringField(
                ?name  'layoutFile
                ?prompt  "Layout Skill File"
                ?enabled t 
                ?defValue ""
            )    
        layoutFileSel=hiCreateFormButton(
                ?name 'layoutFileSel
                ?buttonText "Select"
                ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'layoutFile  \"*.il\" 'anyFile \"layout data select\")"
                ?enabled t
            )  
        layoutRun=hiCreateButton(
                ?name 'layoutRun
                ?buttonText "Import Layout Data"
                ?callback "layoutRunButtonCB()"
                ;?enabled nil ;or t
            )


        sep3=hiCreateSeparatorField(?name 'sep3)
        sep4=hiCreateSeparatorField(?name 'sep4) 
        pythonInterpreter = hiCreateStringField(
            ?name  'pythonInterpreter
            ?prompt  "Python Interpreter"
            ?enabled nil 
            ?defValue "/data/icdesign/ams/ip_migration/tools/anaconda3/envs/sizing/bin/python3"
        )    
        pythonInterpreterSel=hiCreateFormButton(
            ?name 'pythonInterpreterSel
            ?buttonText "Select"
            ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'pythonInterpreter  \"*.*\" 'anyFile \"python interpreter select\")"
            ?enabled nil
        )          
        ASOP=hiCreateStringField(
            ?name  'ASOP
            ?prompt  "ASTRI OP"
            ?enabled nil 
            ?defValue "/data/icdesign/ams/ip_migration/users/leiyuan/ASMigration/ASOP/main.py"
        )    
        ASOPSel=hiCreateFormButton(
            ?name 'ASOPSel
            ?buttonText "Select"
            ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'ASOP  \"*.py\" 'anyFile \"ASTRI OP select\")"
            ?enabled nil
        )  


        hiCreateAppForm(
            ?name 'mainForm
            ?formTitle "ASTRI IP Migration"
            ?callback 'mainFormCB
            ?fields
                list(
                    list(mapSetLabel 0  :5    500:30 )
                    list(mapSelect   20 :35   500:30 150)
                    list(sLibName    20 :65   500:30 120)
                    list(sCellName   20 :95   500:30 120)
                    list(sViewName   20 :125  500:30 120) 
                    list(sBrowse     520:125  60 :30 150)
                    list(sep1        0  :160  600:0)
                    list(tLibName    20 :165 500:30 120)
                    list(tCellName   20 :195 500:30 120)
                    list(tViewName   20 :225 500:30 120)
                    list(tBrowse     520:225 60 :30 150)

                    list(mapFile 20:265 500:30 120)
                    list(mapFileSel 520:265 60:30 150)
                    list(createInst 20:295, 500:30 150)
                    list(mapRun     400:330 200:25)
                    list(sep2 0:365 600:0)

                    list(optLabel 0:370 500:30 )
                    list(exportLabel 0:400 500:30 )
                    list(optField  20:430 60:30 130)
                    list(logFolder 20:460 500:30 120)
                    list(logFolderSel 520:460 60:30 150)
                    list(exportRun     400:500 200:25)
                    list(importLabel 0:530 500:30 )
                    list(settingFile 20:560 500:30 150)
                    list(settingFileSel 520:560 60:30 150)
                    list(importRun     400:590 200:25)
                    list(sep3 0:625 620:0)

                    list(layoutLabel 0:630 500:30 )
                    list(layoutFile 20:660 500:30 150)
                    list(layoutFileSel 520:660 60:30 150)
                    list(layoutRun     400:690 200:25)
                    
                    list(sep4 0:735 620:0)
                    
                    list(pythonInterpreter 20:740 500:30 150)
                    list(pythonInterpreterSel 520:740 60:30 150)
                    list(ASOP     20:770 500:30 150)
                    list(ASOPSel 520:770 60:30 150)

                    )
            ?initialSize list(900 1400)
            )
        

            ; store the extra fields on the form, ready for later

        mainForm
        )
    )





procedure(mapRadioButtonCB()
    let((radioVal )
        radioVal=mainForm->mapSelect->value
        when(radioVal=="Yes"
            mainForm->sLibName->enabled = t
            mainForm->sCellName->enabled = t
            mainForm->sViewName->enabled = t
            mainForm->sBrowse->enabled = t
            mainForm->mapFile->enabled = t
            mainForm->mapFileSel->enabled = t
            mainForm->mapRun->enabled = t
        )
        when(radioVal=="No"
            mainForm->sLibName->enabled = nil
            mainForm->sCellName->enabled = nil
            mainForm->sViewName->enabled = nil
            mainForm->sBrowse->enabled = nil
            mainForm->mapFile->enabled = nil
            mainForm->mapFileSel->enabled = nil
            mainForm->mapRun->enabled = nil
        )       
    ))





procedure(mapRunButtonCB()
    let((addDestructor )
        prog((a)
        
        hiDisplayProgressBox(
            ?name        'pb
            ?banner      "Mapping Progress"
            ?text        "Running..."
            ?totalSteps  100
        )
        ;hiSetProgress(pb 0)
        schematicMapping(hiGetCurrentForm())
        ;hiSetProgress(pb 100)
     
        a = 0
        while(a <= 100
            hiSetProgress(pb a)
            if(a==100 then    hiSetProgressText(pb "Complete !!"))
            a++
            )
        )      
    )
)
procedure(exportRunButtonCB()
    let((addDestructor )
        prog((a)
        
        hiDisplayProgressBox(
            ?name        'pb2
            ?banner      "Mapping Progress"
            ?text        "Running..."
            ?totalSteps  100
        )
        exportSchematicData(hiGetCurrentForm())
        a = 0
        while(a <= 100
            hiSetProgress(pb2 a)
            if(a==100 then    hiSetProgressText(pb2 "Complete !!"))
            a++
            )
        )      
    );let
)
;exportRunButtonCB

procedure(layoutRunButtonCB()
    let((addDestructor )
        prog((a)
        
        hiDisplayProgressBox(
            ?name        'pb4
            ?banner      "Mapping Progress"
            ?text        "Running..."
            ?totalSteps  100
        )
        importLayoutData(hiGetCurrentForm())
        a = 0
        while(a <= 100
            hiSetProgress(pb4 a)
            if(a==100 then    hiSetProgressText(pb4 "Complete !!"))
            a++
            )
        )      
    );let
)
;layoutRunButtonCB



/***************************************************************
*                                                              *
*                   oferCreateUserDataForm()                   *
*                                                              *
*                  Creates the user data form                  *
*                                                              *
***************************************************************/

procedure(oferCreateUserDataForm()
    let((userFilename userRadio)
        userFilename=hiCreateStringField(
                ?name 'userFilename
                ?prompt "Filename"
                )
        userRadio=hiCreateRadioField(
                ?name 'userRadio
                ?choices list("a" "b" "c" "d")
                ?value "a"
                ?prompt "Another Radio"
                )
        ; example - don't bother filling 
        hiCreateAppForm(
            ?name 'oferUserDataForm
            ?formTitle "Ofer's User Data"
            ?fields list(
                userFilename
                userRadio
                )
            )
        )
    )





/***************************************************************
*                                                              *
*                      ipmSyncBrowser()                       *
*                                                              *
*                 Synchronise with the browser                 *
*                                                              *
***************************************************************/

procedure(ipmTargetSyncBrowser()
    ddsSyncWithForm(
        mainForm
        'tBrowse
        'tLibName
        'tCellName
        'tViewName
        )
    )
procedure(ipmSourceSyncBrowser()
    ddsSyncWithForm(
        mainForm
        'sBrowse
        'sLibName
        'sCellName
        'sViewName
        )
    )





/***************************************************************
*                                                              *
*                     get cdf parameters                       *
*                                                              *
***************************************************************/
procedure( getSchematicCDF(lib cell instName)
   let( (cv inst instCdf para)
    cv=dbOpenCellViewByType(lib cell "schematic" "" "r")
    
    
    foreach(inst cv->instances
        printf("name: %s;libName: %s; cellName: %s; viewName: %s\n" inst->name inst->libName inst->cellName inst->viewName )
        if(inst->name==instName then
            printf("-------------------------------------------------------\n")
            instCdf=cdfGetInstCDF(inst)
            foreach(para instCdf->parameters
                printf("Show: ")
                printf(para->prompt)
                printf(" | Name: ")
                printf(para->name)
                printf(" | Value: ")
                println(para->value)
                ;printf("  \n")               

            );foreach
            printf("-------------------------------------------------------\n")
            ;println(instCdf)
        );if
 
        
    );foreach
    t
   );let
);procedure





/***************************************************************
*                                                              *
*                     schematic mapping                        *
*                                                              *
***************************************************************/



procedure( schematicMapping(mainForm)
   let( (startTime endTime totalTime s_lib s_cell s_view t_lib t_cell t_view mapFile inPort oldTable newTable k badLines
        ;cv_s cv_t
    cv_s_temp s_cell_temp
    oldCell newCell cv viewType inLine inLineList 
    oldLib oldView newLib newView backupOrg recreateInst inst
	instList totalLibs libCount totalViews viewCount libList targetLibCellList targetLibList targetCellList
	paramTable j instCdf paramId instMaster instName instPt instOrient)
    
    startTime=getCurrentTime()
    printf(strcat("Schematic Mapping @ ", startTime))
    
    s_lib=mainForm->sLibName->value
    s_cell=mainForm->sCellName->value
    s_view=mainForm->sViewName->value

    t_lib=mainForm->tLibName->value
    t_cell=mainForm->tCellName->value
    t_view=mainForm->tViewName->value

    mapFile=mainForm->mapFile->value 
    unless( isFile(mapFile) error("File %s cannot be found\n" mapFile))
    
    printf(strcat("\nSource  : ", s_lib, " " ,s_cell, " " ,s_view))
    printf(strcat("\nTarget  : ", t_lib, " " ,t_cell, " " ,t_view))
    printf(strcat("\nMapFile : ", mapFile))  
    printf("\n")

    inPort=infile(mapFile)
    
    oldTable=makeTable("oldTable" nil)
    newTable=makeTable("newTable" nil)
    k=0
    badLines=list()
    while( gets(inLine inPort)
       inLineList=parseString(inLine "#\n")
       when( !pcreMatchp("^(\\s*|\\t*);" inLine) && length(inLineList)>=2
          oldTable[k]=parseString(car(inLineList) " \t")
          newTable[k]=parseString(cadr(inLineList) " \t")

          printf("\n")
          println(oldTable[k])
          printf("\n")
          println(newTable[k])
          unless( length(oldTable[k])==length(newTable[k])
             badLines=cons(inLine badLines)
          ) ;unless
          k++
       ) ;when
    ) ;while
    close(inPort)
    
    ;println(oldTable)
    ;println(newTable)    


    when( length(badLines)>0
       printf("The following lines in mapping file needs to be corrected:\n")
       foreach(line badLines
          printf("%s\n" line)
       ) ;foreach
       printf("=== Format of mapping file ===\n")
       printf("oldLib oldCell oldView # newLib newCell newView\n")
       error("")
    ) ;when


    paramTable=makeTable("paramTable" nil)
        
    ;create a temp cellview 
    s_cell_temp=strcat(s_cell "_temp_for_mapping")
    cv_s=dbOpenCellViewByType(s_lib s_cell s_view "" "r")
    cv_s_temp=dbCopyCellView(cv_s s_lib s_cell_temp s_view nil nil t) ;last t means overwirte existing

    ;cvid = ddGetObj("libName" "cellName" "viewName")
    ;cv_t=dbOpenCellViewByType(t_lib t_cell t_view "" "a")

    if(cv_s_temp then
        for(i 0 length(oldTable)-1
            ; oldTable[i]=list(oldLib oldCell oldView oldParam1 oldParam2 ...)
            ; newTable[i]=list(newLib newCell newView newParam1 newParam2 ...)
            oldLib=nth(0 oldTable[i]) 
            oldCell=nth(1 oldTable[i])
            oldView=nth(2 oldTable[i])
            newLib=nth(0 newTable[i])
            newCell=nth(1 newTable[i])
            newView=nth(2 newTable[i])
 
            instList=setof(x cv_s_temp~>instances x~>libName==oldLib && x~>cellName==oldCell && x~>viewName==oldView)
            ;printf("test0\n")
            ;println(cv_s_temp~>instances)

            foreach( inst instList

                j=0
                instCdf=cdfGetInstCDF(inst)
                ;prop is different with cdf inst prop
                foreach(param cdddr(oldTable[i])
                    paramTable[j]=cdfFindParamByName(instCdf param)~>value
                    ;printf("test1\n")
                    ;printf(param)
                    ;println(paramTable[j])
                    j++
                ) ;foreach

                if( recreateInst=="Yes" then
                    instMaster=dbOpenCellViewByType(newLib newCell newView)
                    instName=inst~>name
                    instPt=inst~>xy
                    instOrient=inst~>orient
                    dbDeleteObject(inst)
                    inst=dbCreateInst(cv instMaster instName instPt instOrient)
                else
                     leReplaceAnyInstMaster(inst newLib newCell newView)
                ) ;if recreateInst=="Yes"

                j=0
                ;printf("test2\n")
                instCdf=cdfGetInstCDF(inst)
                foreach(param cdddr(newTable[i])
                    paramId=cdfFindParamByName(instCdf param)
                    if( paramId~>paramType=="string" && !stringp(paramTable[j]) then
                        paramId~>value=sprintf(nil "\"%s\"" paramTable[j])
                    else
                        paramId~>value=paramTable[j]
                    ) ;if
                    j++
                ) ;foreach

                foreach( prop inst~>prop
                    unless( setof(x instCdf->parameters x->name==prop~>name)
                    dbDeleteObject(prop)
                    ) ;unless
                ) ;foreach
            ) ;foreach
        ) ;for

        when( cv_s_temp~>modifiedButNotSaved
            when(viewType=="schematic" schCheck(cv_s_temp))
            dbSave(cv_s_temp)
        ) ;when
        ;cv_t=dbCopyCellView(cv_s_temp t_lib t_cell t_view t nil t) ;last t means overwirte existing 
        cv_t=dbOpenCellViewByType(t_lib t_cell t_view "" "w")
        ;printf("test3\n")
        ;println(inst)
        foreach(inst cv_s_temp->instances 
            dstFig = dbCopyFig(inst cv_t)    
        
        );foreach
        foreach(inst cv_s_temp->shapes 
            if( inst->layerName == "wire" then
                dstFig = dbCopyFig(inst cv_t)    
            );if
        
        ); foreach  
        foreach(inst cv_s_temp->shapes 
            if( inst->layerName == "annotate" then
                dstFig = dbCopyFig(inst cv_t)    
            );if
        
        ); foreach  
        foreach(inst cv_s_temp->shapes 
            if( inst->layerName == "text" then
                dstFig = dbCopyFig(inst cv_t)    
            );if
        
        ); foreach 
        when( cv_t~>modifiedButNotSaved
            when(viewType=="schematic" schCheck(cv_t))
            dbSave(cv_s_temp)
        ) ;when
        dbClose(cv_t)

        dbClose(cv_s_temp)
        cv_s_temp = ddGetObj(s_lib s_cell_temp s_view)
        ddDeleteObj(cv_s_temp)

    else
        printf(" Cellview %s/%s/%s not processed\n" t_lib t_cell t_view)
    ) ;if cv_t


    endTime=getCurrentTime()
    printf("\n")
    printf("Migration start time : %s\n" startTime)
    printf("Migration end time   : %s\n" endTime)
    totalTime=(stringToTime(endTime)-stringToTime(startTime))/3600.0
    printf("Total time           : %.1f mins\n" totalTime)

   );let
);schematicMapping



procedure( exportSchematicData(mainForm)
   let( (t_lib t_cell t_view file1 file2 file)

        t_lib=mainForm->tLibName->value
        t_cell=mainForm->tCellName->value
        t_view=mainForm->tViewName->value
        t_cell="test1"
        simulator('spectre)
    
        design(t_lib t_cell t_view "r")
        file1=createNetlist(?display nil)
        file2=strcat(mainForm->logFolder->value "/schematic_data.scs" )

        file = strcat("cp " file1 " " file2)
        system(file)

        printf(file)
        printf("\n")

    );
   )






   procedure( importLayoutData(mainForm)
   let( ()
        load(mainForm->layoutFile->value)
        printf(mainForm->layoutFile->value)
        printf("\n")

    );
   )

/****************************************************************
*                                                               *
*                    mainFormCB(form)                           *
*                                                               *
*                 The main form callback -                      *
*                                                               *
****************************************************************/

procedure(mainFormCB(form)
    let((outHandle)
        printf(form->logFolder->value)
        printf("\n") 
        simFile=strcat(form->logFolder->value "/simulation_setup.txt" )
        outHandle = outfile( simFile)
        ;fprintf(outHandle "%s\n" form->logFolder->value)
        ;fprintf(outHandle "%s\n" form->modelCardFile->value)
        ;fprintf(outHandle "%s\n" form->settingFile->value)
        ;fprintf(outHandle "%s\n" form->netlistFolder->value)
        ;fprintf(outHandle "%s\n" form->optNetlistFolder->value)
        ;fprintf(outHandle "%s\n" form->optField->value)
        ;fprintf(outHandle "%d\n" form->generationField->value)
        ;fprintf(outHandle "%d\n" form->populationField->value)
        ;fprintf(outHandle "%d\n" form->offspringField->value)  
        close( outHandle )
        ;/data/icdesign/ams/ip_migration/tools/anaconda3/envs/sizing/bin/python3


        prog((a)
        
        hiDisplayProgressBox(
            ?name        'python
            ?banner      "Optimization Progress"
            ?text        "Running..."
            ?totalSteps  10000
        )
        cmd = strcat(form->pythonInterpreter->value " " form->ASOP->value " --data_file " simFile )
        printf(cmd )
        system(cmd)     
        a = 0
        while(a <= 10000
            hiSetProgress(python a)
            if(a==10000 then    hiSetProgressText(python "Complete !!"))
            a++
            )
        ) 

    );let
);procedure


/***************************************************************
*                                                              *
*                       Main entry point                       *
*                                                              *
***************************************************************/

procedure(main()
        ipmCreateForm()
        oferCreateUserDataForm()
		hiDisplayForm(mainForm)
)

