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
                ?value  "No"
                ?callback list("mapRadioButtonCB()")
            )        
        ;source cellView specification 
		mapSetLabel=hiCreateLabel( 
                ?name 'mapSetLabel
                ?labelText "Schematic Mapping Setting"
                ?justification 'left 
                ;?justification 'right 
            )
        sLibName=hiCreateStringField(
                ?name 'sLibName
                ?prompt "Source Library Name"
                ?callback "ddsUpdateSyncWithForm()"
                ?enabled nil ;or t
            )
        sCellName=hiCreateStringField(
                ?name 'sCellName
                ?prompt "Source Cell Name"
                ?callback "ddsUpdateSyncWithForm()"
                ?enabled nil ;or t
            )
        sViewName=hiCreateStringField(
                ?name 'sViewName
                ?prompt "Source View Name"
                ?callback "ddsUpdateSyncWithForm()"
                ?enabled nil ;or t
            )
        sBrowse=hiCreateButton(
                ?name 'sBrowse
                ?buttonText "Browse"
                ?callback "ipmSourceSyncBrowser()"
                ?enabled nil ;or t
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
                ?enabled nil ;or t
            ) ;hiCreateStringField   
        mapFileSel=hiCreateFormButton(
                ?name 'mapFileSel
                ?buttonText "Select"
                ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'mapFile  \"*.map\" 'anyFile \"mapping file select\")"
                ?enabled nil ;or t
            ) ;hiCreateFormButton        
        mapRun=hiCreateButton(
                ?name 'mapRun
                ?buttonText "Run Mapping"
                ?callback "mapRunButtonCB()"
                ?enabled nil ;or t
            )
        sep2=hiCreateSeparatorField(?name 'sep2)
        
        optLabel=hiCreateLabel( 
                ?name 'optLabel
                ?labelText "Circuit Optimization Setting"
                ?justification 'left 
            )
        genNetlist=hiCreateRadioField(
                ?name 'genNetlist
                ?prompt "Generate Netlist from Schematic"
                ?choices list("Yes" "No")
                ?value  "No"
                ?enabled nil
                ;?callback list("mapRadioButtonCB()")
            )   
        settingFile=hiCreateStringField(
                ?name  'settingFile
                ?prompt  "Setting File"
                ?enabled t 
                ?defValue "/data/icdesign/ams/ip_migration/users/leiyuan/ASMigration/ASOP/setting.csv"
            )    
        settingFileSel=hiCreateFormButton(
                ?name 'settingFileSel
                ?buttonText "Select"
                ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'settingFile  \"*.csv\" 'anyFile \"netlist file select\")"
                ?enabled t
            )    

        logFolder=hiCreateStringField(
                ?name  'logFolder
                ?prompt  "Log Direcotry"
                ?defValue simplifyFilename("./") 
                ?enabled t 
            )    
        logFolderSel=hiCreateFormButton(
                ?name 'logFolderSel
                ?buttonText "Select"
                ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'logFolder  \"*.*\" 'directoryOnly \"log folder select\")"
                ?enabled t
            )  
        
        genVarSet=hiCreateRadioField(
                ?name 'genVarSet
                ?prompt "Generate Variables Template"
                ?choices list("Yes" "No")
                ?value  "No"
                ?enabled nil
                ;?callback list("mapRadioButtonCB()")
            )  
        modelCardFile=hiCreateStringField(
                ?name  'modelCardFile
                ?prompt  "Model Card"
                ?enabled t 
                ?defValue "/data/icdesign/ams/ip_migration/users/leiyuan/ASMigration/ASOP/smic018/models/spectre/ms018_v1p7_spe.lib"
            )    
        modelCardFileSel=hiCreateFormButton(
                ?name 'modelCardFileSel
                ?buttonText "Select"
                ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'modelCardFile  \"*.*\" 'anyFile \"model card select\")"
                ?enabled t
            )   

        netlistFolder=hiCreateStringField(
                ?name  'netlistFolder
                ?prompt  "Netlist Folder"
                ?enabled t 
                ?defValue "/data/icdesign/ams/ip_migration/users/leiyuan/ASMigration/ASOP/smic018/tb_template"
            )    
        netlistFolderSel=hiCreateFormButton(
                ?name 'netlistFolderSel
                ?buttonText "Select"
                ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'netlistFolder  \"*.*\" 'directoryOnly \"netlist folder select\")"
                ?enabled t
            )  
        optNetlistFolder=hiCreateStringField(
                ?name  'optNetlistFolder
                ?prompt  "Optimized Netlist Folder"
                ?enabled t 
                ?defValue "/data/icdesign/ams/ip_migration/users/leiyuan/ASMigration/ASOP/smic011/simResult"
            )    
        optNetlistFolderSel=hiCreateFormButton(
                ?name 'optNetlistFolderSel
                ?buttonText "Select"
                ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'netlistFolder  \"*.*\" 'directoryOnly \"netlist folder select\")"
                ?enabled t
            )   
            
        generationField = hiCreateSpinBox(
                ?name 'generationField
                ?prompt "Generation:"
                ?arrowOrientation 'vertical
                ?range '(1 100)
                ?value 2
                ?defValue 2
                ?editable t
                ;?callback "callbackOne"
                ;?wrapAround nil
               )
        populationField = hiCreateSpinBox(
                ?name 'populationField
                ?prompt "Population:"
                ?arrowOrientation 'vertical
                ?range '(1 100)
                ?value 4
                ?defValue 4
                ?editable t
                ;?callback "callbackOne"
                ;?wrapAround nil
               )

        offspringField = hiCreateSpinBox(
                ?name 'offspringField
                ?prompt "Off Spring:"
                ?arrowOrientation 'vertical
                ?range '(1 100)
                ?value 4
                ?defValue 4
                ?editable t
                ;?callback "callbackOne"
                ;?wrapAround nil
               )

        optField = hiCreateCyclicField(
                ?name 'optField
                ?prompt "Optimizer:"
                ?defValue "USGA3" 
                ?choices list("USGA3" "NSGA2" "RVEA")
                ;?callback "callbackOne"

               )
	    optSelect=hiCreateRadioField(
            ?name 'optSelect
            ?prompt "Optimization:"
            ?choices list("From Scratch" "Fine-tune")
            ?defValue  "From Scratch"
            ?value  "From Scratch"
            ?enabled nil
            ;?callback list("oferRadioButtonCB()")
            )
        mlSelect=hiCreateRadioField(
                ?name 'mlSelect
                ?prompt "AI Accelerate:"
                ?choices list("Open" "Close")
                ?defValue  "Close"
                ?value  "Close"
                ?enabled nil
                ;?callback list("oferRadioButtonCB()")
                )
        
        stopLabel=hiCreateLabel( 
                ?name 'stopLabel
                ?labelText "Stop Criteria"
                ?justification 'left 
            )

        stop1Button=hiCreateBooleanButton(
                ?name 'stop1Button
                ?buttonText "All Specs Meet"
                ?defValue  t
                ?buttonLocation 'left
            )
        stop2Button=hiCreateBooleanButton(
                ?name 'stop2Button
                ?buttonText "Time Limit (min)"
                ?defValue  nil
                ?buttonLocation 'left
                ?enabled nil
            )
        stop3Button=hiCreateBooleanButton(
                ?name 'stop3Button
                ?buttonText "Time after All Specs Meet"
                ?defValue  nil
                ?buttonLocation 'left
                ?enabled nil
            )
        stop2String=hiCreateStringField(
                ?name  'stop2String
                ?prompt  ""
                ?enabled nil 
            )  
        stop3String=hiCreateStringField(
                ?name  'stop3String
                ?prompt  ""
                ?enabled nil                
            )  
        sep3=hiCreateSeparatorField(?name 'sep3)
        sep4=hiCreateSeparatorField(?name 'sep4) 
        pythonInterpreter = hiCreateStringField(
            ?name  'pythonInterpreter
            ?prompt  "Python Interpreter"
            ?enabled t 
            ?defValue "/data/icdesign/ams/ip_migration/tools/anaconda3/envs/sizing/bin/python3"
        )    
        pythonInterpreterSel=hiCreateFormButton(
            ?name 'pythonInterpreterSel
            ?buttonText "Select"
            ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'pythonInterpreter  \"*.*\" 'anyFile \"python interpreter select\")"
            ?enabled t
        )          
        ASOP=hiCreateStringField(
            ?name  'ASOP
            ?prompt  "ASTRI OP"
            ?enabled t 
            ?defValue "/data/icdesign/ams/ip_migration/users/leiyuan/ASMigration/ASOP/main.py"
        )    
        ASOPSel=hiCreateFormButton(
            ?name 'ASOPSel
            ?buttonText "Select"
            ?callback "ddsFileBrowseCB(hiGetCurrentForm() 'ASOP  \"*.py\" 'anyFile \"ASTRI OP select\")"
            ?enabled t
        )  

        hiCreateAppForm(
            ?name 'mainForm
            ?formTitle "ASTRI IP Migration"
            ?callback 'mainFormCB
            ?fields
                list(
                    list(tLibName 20:5 500:30 150)
                    list(tCellName 20:35 500:30 150)
                    list(tViewName 20:65 500:30 150)
                    list(tBrowse 520:65 60:30 150)
                    list(sep1 0:100 600:0)
                    list(mapSetLabel 0:105 500:30 )
                    list(mapSelect 20:135, 500:30 150)
                    list(sLibName    20:165 500:30 150)
                    list(sCellName   20:195 500:30 150)
                    list(sViewName   20:225 500:30 150)
                    list(sBrowse     520:225 60:30 150)
                    list(mapFile 20:265 500:30 150)
                    list(mapFileSel 520:265 60:30 150)
                    list(createInst 20:295, 500:30 150)
                    list(mapRun     170:330 200:25)
                    list(sep2 0:365 600:0)
                    list(optLabel 0:370 500:30 )
                    list(genNetlist 220:370, 200:30 100)
                    
                    list(logFolder 20:400 500:30 150)
                    list(logFolderSel 520:400 60:30 150)
                    list(modelCardFile 20:430 500:30 150)
                    list(modelCardFileSel 520:430 60:30 150)

                    list(settingFile 20:460 500:30 150)
                    list(settingFileSel 520:460 60:30 150)
                    
                    list(netlistFolder 20:490 500:30 150)
                    list(netlistFolderSel 520:490 60:30 150)  
                    list(optNetlistFolder 20:520 500:30 150)
                    list(optNetlistFolderSel 520:520 60:30 150)                  

                    
                    list(optField  20:560 60:30 130)
                    list(generationField 420:560 60:30 150)  
                    list(populationField 420:590 60:30 150) 
                    list(offspringField  420:620 60:30 150) 
                    
                    list(optSelect 20:590 60:30 130) 
                    list(mlSelect  20:620 60:30 130) 

                    list(sep3 0:655 620:0)
                    list(stopLabel 0:660 500:30 )
                    list(stop1Button 20:690 60:30 20)  
                    list(stop2Button 20:720 60:30 20) 
                    list(stop2String 200:720 50:30 10)
                    list(stop3Button 20:750 60:30 20) 
                    list(stop3String 200:750 50:30 10)
                    
                    list(sep4 0:785 620:0)
                    
                    list(pythonInterpreter 20:790 500:30 150)
                    list(pythonInterpreterSel 520:790 60:30 150)
                    list(ASOP     20:820 500:30 150)
                    list(ASOPSel 520:820 60:30 150)

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
*                      oferSaveTemplate()                      *
*                                                              *
*              Callback code to save the template              *
*                                                              *
***************************************************************/

procedure(oferSaveTemplate()
    let( (fileName fport)
        fileName=mainForm->templateFile->value
        when(fileName==""
            error("Must specify template filename")
            )
        fport=outfile(fileName)
        unless(fport
            error("Could not write to template file %s" fileName)
            )
        fprintf(fport "oferKeys='(nil\n")
        ; output all of the main form keys 
        foreach(key '(libName cellName viewName radio)
            fprintf(fport "  %s %L\n" key get(mainForm key)->value)
            )
        ; output all of the user data form keys 
        foreach(key '(userFilename userRadio)
            fprintf(fport "  %s %L\n" key get(oferUserDataForm key)->value)
            )
        ; end of the file
        fprintf(fport ")\n")
        close(fport)
        )
    )
        

/***************************************************************
*                                                              *
*                      oferLoadTemplate()                      *
*                                                              *
*              Callback code to load the template              *
*                                                              *
***************************************************************/

procedure(oferLoadTemplate()
    let( (fileName)
        fileName=mainForm->templateFile->value
        when(fileName==""
            error("Must specify template filename")
            )
        ; load it, and trap any errors. The file is just skill
        ; code, so can be loaded.
        errset(load(fileName) t)
        ; the keys are all in a disembodied property list called oferKeys
        ; input all of the main form keys 
        ; use get(), because oferKeys->key won't work, because the key variable
        ; needs to be evaluated.
        foreach(key '(libName cellName viewName radio)
            when(get(oferKeys key)
                get(mainForm key)->value=get(oferKeys key)
                )
            )
        ; output all of the user data form keys 
        foreach(key '(userFilename userRadio)
            when(get(oferKeys key)
                get(oferUserDataForm key)->value=get(oferKeys key)
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


/****************************************************************
*                                                               *
*                      oferRadioButtonCB()                      *
*                                                               *
*   Callback for the radio button on the form - this adds or    *
*       subtracts the dynamic fields. The dynamic fields        *
* are created at startup, and stored in a disembodied property  *
* list on the form, and the form positions are calculated based *
*        on the current positions of fields on the form.        *
*                                                               *
****************************************************************/

procedure(oferRadioButtonCB()
    let((radioVal newOffset newPosition oldPosition
            (currentOffset 0) (fieldHeight 30) newYcoord)
        ; determine the offset of the bottom fields at the moment
        when(mainForm->optionTwo
            currentOffset=currentOffset+fieldHeight
            )
        when(mainForm->optionThree
            currentOffset=currentOffset+fieldHeight
            )
        ; determine the offset that we want, based on the radio
        ; button value
        radioVal=mainForm->radio->value
        newOffset=case(radioVal
            ("Two" fieldHeight)
            ("Three" fieldHeight*2)
            (t 0)
            )
        ; shift the two bottom fields by the appropriate amount
        foreach(field '(sep3 userData)
            ; calculate the new position from the old, offset accordingly
            oldPosition=car(hiGetFieldInfo(mainForm field))
            newPosition=xCoord(oldPosition):yCoord(oldPosition)
                        +newOffset-currentOffset
            hiMoveField(
                mainForm
                field
                newPosition
                )
            )
        ; delete form fields if they're not needed
        when(radioVal=="One" && mainForm->optionTwo
            hiDeleteField(mainForm 'optionTwo))
        when(radioVal!="Three" && mainForm->optionThree
            hiDeleteField(mainForm 'optionThree))
        ; determine where the extra fields will be placed
        newYcoord=yCoord(car(hiGetFieldInfo(mainForm 'radio)))+
            if(dbGetDatabaseType()=="CDBA" 10 30)
        ; add the two fields if they're needed and not there already
        when(radioVal=="Two" || radioVal=="Three"
            unless(mainForm->optionTwo
                hiAddField(mainForm
                    list(mainForm->extraFields->optionTwo
                        0:newYcoord 600:30 200))
                )
            )
        when(radioVal=="Three"
            unless(mainForm->optionThree
                hiAddField(mainForm
                    list(mainForm->extraFields->optionThree
                        0:newYcoord+fieldHeight 600:30 200))
                )
            )
        ))
        



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
    oldLib oldView newLib newView backupOrg recreateInst
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

          ;printf("\n")
          ;println(oldTable[k])
          ;printf("\n")
          ;println(newTable[k])
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
            ;println(instList)
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
        fprintf(outHandle "%s\n" form->logFolder->value)
        fprintf(outHandle "%s\n" form->modelCardFile->value)
        fprintf(outHandle "%s\n" form->settingFile->value)
        fprintf(outHandle "%s\n" form->netlistFolder->value)
        fprintf(outHandle "%s\n" form->optNetlistFolder->value)
        fprintf(outHandle "%s\n" form->optField->value)
        fprintf(outHandle "%d\n" form->generationField->value)
        fprintf(outHandle "%d\n" form->populationField->value)
        fprintf(outHandle "%d\n" form->offspringField->value)  
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
        ;oferCreateUserDataForm()
		hiDisplayForm(mainForm)
)

