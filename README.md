# ipmigration
ASTRI IP Migration Platform


```
ipmigration
├─ configs
│  └─ README.md
├─ demo
│  └─ README.md
├─ docs
│  └─ README.md
├─ ipm
│  └─ README.md
├─ MANIFEST.in.py
├─ README.md
├─ resources
│  └─ README.md
├─ setup.cfg
├─ setup.py
├─ tests
│  └─ README.md
└─ tools
   └─ README.md

```
```
ipmigration
├─ MANIFEST.in
├─ README.md
├─ configs
│  └─ README.md
├─ demo
│  └─ README.md
├─ docs
│  └─ README.md
├─ ipmigration
│  ├─ README.md
│  ├─ analog
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  └─ __init__.cpython-311.pyc
│  │  ├─ apr
│  │  │  └─ __init__.py
│  │  └─ opt
│  │     ├─ README.md
│  │     ├─ __init__.py
│  │     ├─ __pycache__
│  │     │  ├─ __init__.cpython-311.pyc
│  │     │  ├─ calculator.cpython-311.pyc
│  │     │  ├─ figureplot.cpython-311.pyc
│  │     │  ├─ get_setting_for_release.cpython-311.pyc
│  │     │  ├─ gui_parser.cpython-311.pyc
│  │     │  ├─ logger.cpython-311.pyc
│  │     │  ├─ ml_predictor.cpython-311.pyc
│  │     │  ├─ moo_optimizer_hierarchy.cpython-311.pyc
│  │     │  ├─ ngl2.cpython-311.pyc
│  │     │  ├─ opt_setting.cpython-311.pyc
│  │     │  ├─ simulation_module.cpython-311.pyc
│  │     │  └─ utility.cpython-311.pyc
│  │     ├─ aop.py
│  │     ├─ apis
│  │     │  ├─ gpdk45_smic011.map
│  │     │  └─ ip_migration.il
│  │     ├─ calculator.py
│  │     ├─ data_loader.py
│  │     ├─ designlib
│  │     │  ├─ Opamp
│  │     │  │  ├─ .oalib
│  │     │  │  ├─ OpAmp
│  │     │  │  │  ├─ data.dm
│  │     │  │  │  ├─ maestro_basic
│  │     │  │  │  │  ├─ active.state
│  │     │  │  │  │  ├─ data.dm
│  │     │  │  │  │  ├─ documents
│  │     │  │  │  │  ├─ history
│  │     │  │  │  │  │  ├─ Interactive.0.zip
│  │     │  │  │  │  │  ├─ Interactive.1.zip
│  │     │  │  │  │  │  └─ history.sdb
│  │     │  │  │  │  ├─ maestro.sdb
│  │     │  │  │  │  ├─ maestro.sdb.cdslck
│  │     │  │  │  │  ├─ master.tag
│  │     │  │  │  │  ├─ plottingTemplates
│  │     │  │  │  │  │  └─ SwingFainUGF_PT
│  │     │  │  │  │  │     ├─ SwingFainUGF_PT.cmpt.group
│  │     │  │  │  │  │     ├─ SwingFainUGF_PT_0.cmpt
│  │     │  │  │  │  │     └─ SwingFainUGF_PT_1.cmpt
│  │     │  │  │  │  ├─ results
│  │     │  │  │  │  │  ├─ data
│  │     │  │  │  │  │  │  └─ MonteCarlo.17.log
│  │     │  │  │  │  │  └─ maestro
│  │     │  │  │  │  │     ├─ Interactive.0.log
│  │     │  │  │  │  │     ├─ Interactive.0.rdb
│  │     │  │  │  │  │     ├─ Interactive.1.log
│  │     │  │  │  │  │     └─ Interactive.1.rdb
│  │     │  │  │  │  └─ states
│  │     │  │  │  │     └─ ref_point_migrated.sdb
│  │     │  │  │  ├─ maestro_sweeps#2dcorners
│  │     │  │  │  │  ├─ active.state
│  │     │  │  │  │  ├─ data.dm
│  │     │  │  │  │  ├─ history
│  │     │  │  │  │  │  ├─ ForVerification.zip
│  │     │  │  │  │  │  ├─ FullCoverage.zip
│  │     │  │  │  │  │  ├─ Interactive.0.zip
│  │     │  │  │  │  │  └─ history.sdb
│  │     │  │  │  │  ├─ maestro.sdb
│  │     │  │  │  │  ├─ master.tag
│  │     │  │  │  │  ├─ results
│  │     │  │  │  │  │  ├─ data
│  │     │  │  │  │  │  │  └─ MonteCarlo.17.log
│  │     │  │  │  │  │  └─ maestro
│  │     │  │  │  │  │     ├─ ForVerification.log
│  │     │  │  │  │  │     ├─ ForVerification.rdb
│  │     │  │  │  │  │     ├─ FullCoverage.log
│  │     │  │  │  │  │     ├─ FullCoverage.rdb
│  │     │  │  │  │  │     ├─ Interactive.0.log
│  │     │  │  │  │  │     ├─ Interactive.0.rdb
│  │     │  │  │  │  │     └─ LoggingService.db
│  │     │  │  │  │  └─ states
│  │     │  │  │  │     └─ ref_point_migrated.sdb
│  │     │  │  │  ├─ schematic
│  │     │  │  │  │  ├─ data.dm
│  │     │  │  │  │  ├─ master.tag
│  │     │  │  │  │  ├─ sch.oa
│  │     │  │  │  │  ├─ thumbnail_1024x1024.png
│  │     │  │  │  │  └─ thumbnail_128x128.png
│  │     │  │  │  ├─ schematic2
│  │     │  │  │  │  ├─ data.dm
│  │     │  │  │  │  ├─ master.tag
│  │     │  │  │  │  ├─ sch.oa
│  │     │  │  │  │  ├─ thumbnail_1024x1024.png
│  │     │  │  │  │  └─ thumbnail_128x128.png
│  │     │  │  │  └─ symbol
│  │     │  │  │     ├─ master.tag
│  │     │  │  │     └─ symbol.oa
│  │     │  │  ├─ cdsinfo.tag
│  │     │  │  └─ data.dm
│  │     │  ├─ Opamp_TB
│  │     │  │  ├─ .oalib
│  │     │  │  ├─ OpAmp_AC_top
│  │     │  │  │  ├─ .sevSaveDir
│  │     │  │  │  ├─ config
│  │     │  │  │  │  ├─ data.dm
│  │     │  │  │  │  ├─ expand.cfg
│  │     │  │  │  │  └─ master.tag
│  │     │  │  │  ├─ data.dm
│  │     │  │  │  ├─ maestro_basic
│  │     │  │  │  │  ├─ active.state
│  │     │  │  │  │  ├─ data.dm
│  │     │  │  │  │  ├─ history
│  │     │  │  │  │  │  ├─ ExplorerRun.0.zip
│  │     │  │  │  │  │  └─ history.sdb
│  │     │  │  │  │  ├─ maestro.sdb
│  │     │  │  │  │  ├─ master.tag
│  │     │  │  │  │  └─ results
│  │     │  │  │  │     └─ maestro
│  │     │  │  │  │        ├─ ExplorerRun.0.log
│  │     │  │  │  │        └─ ExplorerRun.0.rdb
│  │     │  │  │  └─ schematic
│  │     │  │  │     ├─ data.dm
│  │     │  │  │     ├─ master.tag
│  │     │  │  │     ├─ sch.oa
│  │     │  │  │     └─ thumbnail_128x128.png
│  │     │  │  ├─ OpAmp_TRAN_top
│  │     │  │  │  ├─ config
│  │     │  │  │  │  ├─ data.dm
│  │     │  │  │  │  ├─ expand.cfg
│  │     │  │  │  │  └─ master.tag
│  │     │  │  │  ├─ config2
│  │     │  │  │  │  ├─ data.dm
│  │     │  │  │  │  ├─ expand.cfg
│  │     │  │  │  │  └─ master.tag
│  │     │  │  │  ├─ data.dm
│  │     │  │  │  ├─ maestro
│  │     │  │  │  │  ├─ active.state
│  │     │  │  │  │  ├─ data.dm
│  │     │  │  │  │  ├─ history
│  │     │  │  │  │  │  └─ history.sdb
│  │     │  │  │  │  ├─ maestro.sdb
│  │     │  │  │  │  └─ master.tag
│  │     │  │  │  └─ schematic
│  │     │  │  │     ├─ data.dm
│  │     │  │  │     ├─ master.tag
│  │     │  │  │     ├─ sch.oa
│  │     │  │  │     └─ thumbnail_128x128.png
│  │     │  │  ├─ cdsinfo.tag
│  │     │  │  ├─ data.dm
│  │     │  │  └─ opamp_dc_feedback
│  │     │  │     ├─ data.dm
│  │     │  │     ├─ schematic
│  │     │  │     │  ├─ data.dm
│  │     │  │     │  ├─ master.tag
│  │     │  │     │  ├─ sch.oa
│  │     │  │     │  └─ thumbnail_128x128.png
│  │     │  │     └─ symbol
│  │     │  │        ├─ master.tag
│  │     │  │        └─ symbol.oa
│  │     │  └─ Two_Stage_Opamp
│  │     │     ├─ .oalib
│  │     │     ├─ .sevSaveDir
│  │     │     ├─ Aux.Cat
│  │     │     ├─ Cells.Cat
│  │     │     ├─ Documentation.Cat
│  │     │     ├─ DualAmp
│  │     │     │  ├─ data.dm
│  │     │     │  ├─ schematic
│  │     │     │  │  ├─ data.dm
│  │     │     │  │  ├─ master.tag
│  │     │     │  │  ├─ sch.oa
│  │     │     │  │  ├─ sch.oa.cdslck
│  │     │     │  │  ├─ sch.oa.cdslck.RHEL30.noivl-sonals.31516
│  │     │     │  │  ├─ thumbnail_1024x1024.png
│  │     │     │  │  └─ thumbnail_128x128.png
│  │     │     │  └─ symbol
│  │     │     │     ├─ master.tag
│  │     │     │     ├─ symbol.oa
│  │     │     │     └─ thumbnail_128x128.png
│  │     │     ├─ Obsolete.Cat
│  │     │     ├─ OpAmp
│  │     │     │  ├─ data.dm
│  │     │     │  ├─ maestro_basic
│  │     │     │  │  ├─ active.state
│  │     │     │  │  ├─ data.dm
│  │     │     │  │  ├─ documents
│  │     │     │  │  ├─ history
│  │     │     │  │  │  ├─ Interactive.0.zip
│  │     │     │  │  │  ├─ Interactive.1.zip
│  │     │     │  │  │  └─ history.sdb
│  │     │     │  │  ├─ maestro.sdb
│  │     │     │  │  ├─ master.tag
│  │     │     │  │  ├─ plottingTemplates
│  │     │     │  │  │  └─ SwingFainUGF_PT
│  │     │     │  │  │     ├─ SwingFainUGF_PT.cmpt.group
│  │     │     │  │  │     ├─ SwingFainUGF_PT_0.cmpt
│  │     │     │  │  │     └─ SwingFainUGF_PT_1.cmpt
│  │     │     │  │  ├─ results
│  │     │     │  │  │  ├─ data
│  │     │     │  │  │  │  ├─ .rdb
│  │     │     │  │  │  │  ├─ MonteCarlo.17.log
│  │     │     │  │  │  │  └─ psf
│  │     │     │  │  │  │     ├─ AC
│  │     │     │  │  │  │     │  └─ psf
│  │     │     │  │  │  │     ├─ DC
│  │     │     │  │  │  │     │  └─ psf
│  │     │     │  │  │  │     └─ TRAN
│  │     │     │  │  │  │        └─ psf
│  │     │     │  │  │  └─ maestro
│  │     │     │  │  │     ├─ Interactive.0.log
│  │     │     │  │  │     ├─ Interactive.0.rdb
│  │     │     │  │  │     ├─ Interactive.1.log
│  │     │     │  │  │     └─ Interactive.1.rdb
│  │     │     │  │  ├─ states
│  │     │     │  │  │  └─ ref_point_migrated.sdb
│  │     │     │  │  └─ test_states
│  │     │     │  │     └─ Two_Stage_Opamp
│  │     │     │  │        ├─ .sevSaveDir
│  │     │     │  │        └─ OpAmp_AC_top
│  │     │     │  │           ├─ .sevSaveDir
│  │     │     │  │           └─ aps
│  │     │     │  ├─ maestro_sweeps#2dcorners
│  │     │     │  │  ├─ active.state
│  │     │     │  │  ├─ data.dm
│  │     │     │  │  ├─ documents
│  │     │     │  │  ├─ history
│  │     │     │  │  │  ├─ ForVerification.zip
│  │     │     │  │  │  ├─ FullCoverage.zip
│  │     │     │  │  │  ├─ Interactive.0.zip
│  │     │     │  │  │  └─ history.sdb
│  │     │     │  │  ├─ maestro.sdb
│  │     │     │  │  ├─ master.tag
│  │     │     │  │  ├─ results
│  │     │     │  │  │  ├─ data
│  │     │     │  │  │  │  ├─ .rdb
│  │     │     │  │  │  │  ├─ MonteCarlo.17.log
│  │     │     │  │  │  │  └─ psf
│  │     │     │  │  │  │     ├─ AC
│  │     │     │  │  │  │     │  └─ psf
│  │     │     │  │  │  │     ├─ DC
│  │     │     │  │  │  │     │  └─ psf
│  │     │     │  │  │  │     └─ TRAN
│  │     │     │  │  │  │        └─ psf
│  │     │     │  │  │  └─ maestro
│  │     │     │  │  │     ├─ ForVerification.log
│  │     │     │  │  │     ├─ ForVerification.rdb
│  │     │     │  │  │     ├─ FullCoverage.log
│  │     │     │  │  │     ├─ FullCoverage.rdb
│  │     │     │  │  │     ├─ Interactive.0.log
│  │     │     │  │  │     ├─ Interactive.0.rdb
│  │     │     │  │  │     └─ LoggingService.db
│  │     │     │  │  ├─ states
│  │     │     │  │  │  └─ ref_point_migrated.sdb
│  │     │     │  │  └─ test_states
│  │     │     │  │     └─ Two_Stage_Opamp
│  │     │     │  │        ├─ .sevSaveDir
│  │     │     │  │        ├─ OpAmp_AC_top
│  │     │     │  │        │  ├─ .sevSaveDir
│  │     │     │  │        │  ├─ aps
│  │     │     │  │        │  └─ spectre
│  │     │     │  │        └─ OpAmp_TRAN_top
│  │     │     │  │           └─ spectre
│  │     │     │  ├─ schematic
│  │     │     │  │  ├─ data.dm
│  │     │     │  │  ├─ master.tag
│  │     │     │  │  ├─ sch.oa
│  │     │     │  │  ├─ sch.oa-
│  │     │     │  │  ├─ thumbnail_1024x1024.png
│  │     │     │  │  └─ thumbnail_128x128.png
│  │     │     │  ├─ schematic2
│  │     │     │  │  ├─ data.dm
│  │     │     │  │  ├─ master.tag
│  │     │     │  │  ├─ sch.oa
│  │     │     │  │  ├─ thumbnail_1024x1024.png
│  │     │     │  │  └─ thumbnail_128x128.png
│  │     │     │  └─ symbol
│  │     │     │     ├─ master.tag
│  │     │     │     └─ symbol.oa
│  │     │     ├─ OpAmp_AC_top
│  │     │     │  ├─ .sevSaveDir
│  │     │     │  ├─ config
│  │     │     │  │  ├─ data.dm
│  │     │     │  │  ├─ expand.cfg
│  │     │     │  │  └─ master.tag
│  │     │     │  ├─ data.dm
│  │     │     │  ├─ maestro_basic
│  │     │     │  │  ├─ active.state
│  │     │     │  │  ├─ data.dm
│  │     │     │  │  ├─ documents
│  │     │     │  │  ├─ history
│  │     │     │  │  │  ├─ ExplorerRun.0.zip
│  │     │     │  │  │  └─ history.sdb
│  │     │     │  │  ├─ maestro.sdb
│  │     │     │  │  ├─ master.tag
│  │     │     │  │  ├─ results
│  │     │     │  │  │  └─ maestro
│  │     │     │  │  │     ├─ ExplorerRun.0.log
│  │     │     │  │  │     └─ ExplorerRun.0.rdb
│  │     │     │  │  └─ states
│  │     │     │  └─ schematic
│  │     │     │     ├─ data.dm
│  │     │     │     ├─ master.tag
│  │     │     │     ├─ sch.oa
│  │     │     │     ├─ sch.oa-
│  │     │     │     └─ thumbnail_128x128.png
│  │     │     ├─ OpAmp_TRAN_top
│  │     │     │  ├─ config
│  │     │     │  │  ├─ data.dm
│  │     │     │  │  ├─ expand.cfg
│  │     │     │  │  └─ master.tag
│  │     │     │  ├─ config2
│  │     │     │  │  ├─ data.dm
│  │     │     │  │  ├─ expand.cfg
│  │     │     │  │  ├─ expand.cfg%
│  │     │     │  │  └─ master.tag
│  │     │     │  ├─ data.dm
│  │     │     │  ├─ maestro
│  │     │     │  │  ├─ active.state
│  │     │     │  │  ├─ data.dm
│  │     │     │  │  ├─ documents
│  │     │     │  │  ├─ history
│  │     │     │  │  │  └─ history.sdb
│  │     │     │  │  ├─ maestro.sdb
│  │     │     │  │  ├─ master.tag
│  │     │     │  │  ├─ states
│  │     │     │  │  └─ test_states
│  │     │     │  │     └─ Two_Stage_Opamp
│  │     │     │  │        ├─ .sevSaveDir
│  │     │     │  │        └─ OpAmp_TRAN_top
│  │     │     │  │           ├─ .sevSaveDir
│  │     │     │  │           └─ spectre
│  │     │     │  │              ├─ .sevSaveDir
│  │     │     │  │              └─ tmpstate.614043148
│  │     │     │  │                 ├─ .sevSaveDir
│  │     │     │  │                 ├─ ADE_state.info
│  │     │     │  │                 ├─ analyses
│  │     │     │  │                 ├─ convergence
│  │     │     │  │                 ├─ cosimOptions
│  │     │     │  │                 ├─ devCheckingSetup
│  │     │     │  │                 ├─ environmentOptions
│  │     │     │  │                 ├─ graphicalStimuli
│  │     │     │  │                 ├─ mdlOptions
│  │     │     │  │                 ├─ modelSetup
│  │     │     │  │                 ├─ opPoints
│  │     │     │  │                 ├─ outputs
│  │     │     │  │                 ├─ outputsScripts
│  │     │     │  │                 ├─ paramSetup
│  │     │     │  │                 ├─ relxOptions
│  │     │     │  │                 ├─ rfstim
│  │     │     │  │                 ├─ simulationFiles
│  │     │     │  │                 ├─ simulatorOptions
│  │     │     │  │                 ├─ spList
│  │     │     │  │                 ├─ subckts
│  │     │     │  │                 ├─ turboOptions
│  │     │     │  │                 └─ variables
│  │     │     │  └─ schematic
│  │     │     │     ├─ data.dm
│  │     │     │     ├─ master.tag
│  │     │     │     ├─ sch.oa
│  │     │     │     ├─ sch.oa-
│  │     │     │     └─ thumbnail_128x128.png
│  │     │     ├─ Testbenches.Cat
│  │     │     ├─ Two_Stage_Opamp.TopCat
│  │     │     ├─ Verification.Cat
│  │     │     ├─ cdsinfo.tag
│  │     │     ├─ data.dm
│  │     │     └─ opamp_dc_feedback
│  │     │        ├─ data.dm
│  │     │        ├─ schematic
│  │     │        │  ├─ data.dm
│  │     │        │  ├─ master.tag
│  │     │        │  ├─ sch.oa
│  │     │        │  ├─ sch.oa-
│  │     │        │  └─ thumbnail_128x128.png
│  │     │        └─ symbol
│  │     │           ├─ master.tag
│  │     │           └─ symbol.oa
│  │     ├─ figureplot.py
│  │     ├─ get_setting_for_release.py
│  │     ├─ logger.py
│  │     ├─ ml_predictor.py
│  │     ├─ moo_optimizer_hierarchy.py
│  │     ├─ ngl2.py
│  │     ├─ operator_cust
│  │     │  ├─ __init__.py
│  │     │  ├─ __pycache__
│  │     │  │  ├─ __init__.cpython-311.pyc
│  │     │  │  ├─ pm_homemade.cpython-311.pyc
│  │     │  │  └─ sbx_homemade.cpython-311.pyc
│  │     │  ├─ lhs.py
│  │     │  ├─ pm.py
│  │     │  ├─ pm_homemade.py
│  │     │  ├─ sampling
│  │     │  │  ├─ __init__.py
│  │     │  │  ├─ __pycache__
│  │     │  │  │  ├─ __init__.cpython-311.pyc
│  │     │  │  │  ├─ lhs_homenade.cpython-311.pyc
│  │     │  │  │  └─ lhs_integer.cpython-311.pyc
│  │     │  │  ├─ lhs_homenade.py
│  │     │  │  └─ lhs_integer.py
│  │     │  ├─ sbx.py
│  │     │  └─ sbx_homemade.py
│  │     ├─ opt_setting.py
│  │     ├─ optimizer
│  │     │  └─ __init__.py
│  │     ├─ setting.csv
│  │     ├─ setting_csv
│  │     │  ├─ setting_Schmitt_trigger.csv
│  │     │  ├─ setting_class_ab.csv
│  │     │  ├─ setting_comparator.csv
│  │     │  ├─ setting_dynamic_comparator.csv
│  │     │  ├─ setting_level_shifter.csv
│  │     │  └─ setting_two_stage.csv
│  │     ├─ simulation_module.py
│  │     ├─ simulation_setup.py
│  │     ├─ simulator
│  │     ├─ smic011
│  │     │  ├─ ckt_netlist
│  │     │  │  ├─ FoldedCascodeOpamp.scs
│  │     │  │  ├─ FoldedCascodeOpamp2.scs
│  │     │  │  ├─ classabOpamp (copy).scs
│  │     │  │  ├─ classabOpamp.scs
│  │     │  │  ├─ classabOpamp2.scs
│  │     │  │  ├─ comparator1.scs
│  │     │  │  ├─ dynamicComparator.scs
│  │     │  │  ├─ level_shifter.scs
│  │     │  │  ├─ level_shifter_high_speed.scs
│  │     │  │  ├─ schmitt_trigger.scs
│  │     │  │  ├─ spectre
│  │     │  │  │  ├─ FoldedCascodeOpamp.scs
│  │     │  │  │  └─ twoStageOpamp2.scs
│  │     │  │  ├─ spice
│  │     │  │  │  ├─ FoldedCascodeOpamp.cir
│  │     │  │  │  └─ twoStageOpamp2.cir
│  │     │  │  └─ twoStageOpamp2.scs
│  │     │  ├─ models
│  │     │  │  ├─ hspice
│  │     │  │  │  ├─ ms011_ms013s_io33_diff_ind_3t_rf_pgs_n_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_diff_ind_3t_rf_pgs_psub_n_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_diff_ind_rf_pgs_n_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_diff_ind_rf_pgs_psub_n_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_ind_rf_pgs_n_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_ind_rf_pgs_psub_n_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_layer.map
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_3T_diff_ind_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_3Tdiff_1talpa_psub_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_3Tdiff_1talpa_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_TM2_res_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_diff_ind_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_interconnect_TM2_3um_ALPA_struct_1.txt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_interconnect_TM2_3um_ALPA_struct_2.txt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_mim_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_mom_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_mos_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_readme_v1p14.txt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_res_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_spir_ind_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_v1p14.lib
│  │     │  │  │  ├─ ms011_ms013s_io33_rf_var_v1p14.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_v1p24.lib
│  │     │  │  │  ├─ ms011_ms013s_io33_v1p24.mdl
│  │     │  │  │  ├─ ms011_ms013s_io33_v1p24_bjt.mdl
│  │     │  │  │  ├─ ms011_ms013s_io33_v1p24_dio.mdl
│  │     │  │  │  ├─ ms011_ms013s_io33_v1p24_interconnect_struct_1.txt
│  │     │  │  │  ├─ ms011_ms013s_io33_v1p24_interconnect_struct_2.txt
│  │     │  │  │  ├─ ms011_ms013s_io33_v1p24_mim.mdl
│  │     │  │  │  ├─ ms011_ms013s_io33_v1p24_mis.mdl
│  │     │  │  │  ├─ ms011_ms013s_io33_v1p24_readme.txt
│  │     │  │  │  ├─ ms011_ms013s_io33_v1p24_res.ckt
│  │     │  │  │  ├─ ms011_ms013s_io33_v1p24_res.mdl
│  │     │  │  │  └─ simulator_version.txt
│  │     │  │  └─ spectre
│  │     │  │     ├─ gc.va
│  │     │  │     ├─ gc_rf.va
│  │     │  │     ├─ ms011_ms013s_io33_diff_ind_3t_rf_pgs_n_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_diff_ind_3t_rf_pgs_psub_n_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_diff_ind_rf_pgs_n_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_diff_ind_rf_pgs_psub_n_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_ind_rf_pgs_n_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_ind_rf_pgs_psub_n_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_layer.map
│  │     │  │     ├─ ms011_ms013s_io33_rf_3T_diff_ind_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_rf_3Tdiff_1talpa_psub_spe_v1p14.ckt
│  │     │  │     ├─ ms011_ms013s_io33_rf_3Tdiff_1talpa_spe_v1p14.ckt
│  │     │  │     ├─ ms011_ms013s_io33_rf_TM2_res_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_rf_diff_ind_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_rf_interconnect_TM2_3um_ALPA_struct_1.txt
│  │     │  │     ├─ ms011_ms013s_io33_rf_interconnect_TM2_3um_ALPA_struct_2.txt
│  │     │  │     ├─ ms011_ms013s_io33_rf_mim_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_rf_mom_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_rf_mos_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_rf_readme_v1p14_spe.txt
│  │     │  │     ├─ ms011_ms013s_io33_rf_res_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_rf_spir_ind_spe_v1p14.ckt
│  │     │  │     ├─ ms011_ms013s_io33_rf_v1p14_spe.lib
│  │     │  │     ├─ ms011_ms013s_io33_rf_var_v1p14_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_v1p24_bjt_spe.mdl
│  │     │  │     ├─ ms011_ms013s_io33_v1p24_dio_spe.mdl
│  │     │  │     ├─ ms011_ms013s_io33_v1p24_interconnect_struct_1.txt
│  │     │  │     ├─ ms011_ms013s_io33_v1p24_interconnect_struct_2.txt
│  │     │  │     ├─ ms011_ms013s_io33_v1p24_mim_spe.mdl
│  │     │  │     ├─ ms011_ms013s_io33_v1p24_mis_spe.mdl
│  │     │  │     ├─ ms011_ms013s_io33_v1p24_readme_spe.txt
│  │     │  │     ├─ ms011_ms013s_io33_v1p24_res_spe.ckt
│  │     │  │     ├─ ms011_ms013s_io33_v1p24_res_spe.mdl
│  │     │  │     ├─ ms011_ms013s_io33_v1p24_spe.lib
│  │     │  │     ├─ ms011_ms013s_io33_v1p24_spe.mdl
│  │     │  │     ├─ res.va
│  │     │  │     ├─ res_rf.va
│  │     │  │     └─ simulator_version.txt
│  │     │  ├─ simResult
│  │     │  │  ├─ psf
│  │     │  │  │  ├─ logFile
│  │     │  │  │  ├─ logStatus
│  │     │  │  │  ├─ outac1.ac
│  │     │  │  │  ├─ outac1_spectre.out
│  │     │  │  │  ├─ outac2.ac
│  │     │  │  │  ├─ outac2_spectre.out
│  │     │  │  │  ├─ outac3.ac
│  │     │  │  │  ├─ outac3_spectre.out
│  │     │  │  │  ├─ outdc2.dc
│  │     │  │  │  ├─ outdc2_spectre.out
│  │     │  │  │  ├─ outtran1.tran.tran
│  │     │  │  │  ├─ outtran1_spectre.out
│  │     │  │  │  ├─ outtran2.tran.tran
│  │     │  │  │  └─ outtran2_spectre.out
│  │     │  │  ├─ test_comparator1_tran1.scs
│  │     │  │  ├─ test_comparator1_tran2.scs
│  │     │  │  ├─ test_comparator2_tran1.scs
│  │     │  │  ├─ test_comparator2_tran2.scs
│  │     │  │  ├─ test_diffamp1_ac1.scs
│  │     │  │  ├─ test_diffamp1_ac2.scs
│  │     │  │  ├─ test_diffamp1_ac3.scs
│  │     │  │  ├─ test_diffamp1_dc2.scs
│  │     │  │  ├─ test_diffamp1_tran1.scs
│  │     │  │  ├─ test_diffamp1_tran2.scs
│  │     │  │  ├─ test_ls1_tran1.scs
│  │     │  │  └─ test_st1_tran1.scs
│  │     │  └─ tb_template
│  │     │     ├─ Folded_Cascode
│  │     │     │  ├─ template_diffamp1_ac1.scs
│  │     │     │  ├─ template_diffamp1_ac2.scs
│  │     │     │  ├─ template_diffamp1_ac3.scs
│  │     │     │  ├─ template_diffamp1_dc1.scs
│  │     │     │  ├─ template_diffamp1_dc2.scs
│  │     │     │  ├─ template_diffamp1_op1.scs
│  │     │     │  ├─ template_diffamp1_tran1.scs
│  │     │     │  └─ template_diffamp1_tran2.scs
│  │     │     ├─ analog_comparator
│  │     │     │  ├─ template_comparator2_tran1.scs
│  │     │     │  └─ template_comparator2_tran2.scs
│  │     │     ├─ classAB
│  │     │     │  ├─ template_diffamp1_ac1.scs
│  │     │     │  ├─ template_diffamp1_ac2.scs
│  │     │     │  ├─ template_diffamp1_ac3.scs
│  │     │     │  ├─ template_diffamp1_dc1.scs
│  │     │     │  ├─ template_diffamp1_dc2.scs
│  │     │     │  ├─ template_diffamp1_op1.scs
│  │     │     │  ├─ template_diffamp1_tran1.scs
│  │     │     │  └─ template_diffamp1_tran2.scs
│  │     │     ├─ dynamic_comparator
│  │     │     │  ├─ template_comparator1_tran1.scs
│  │     │     │  └─ template_comparator1_tran2.scs
│  │     │     ├─ level_shifter
│  │     │     │  └─ template_ls1_tran1.scs
│  │     │     ├─ ls_higspeed
│  │     │     │  └─ template_ls1_tran1.scs
│  │     │     ├─ spectre
│  │     │     │  ├─ classab_old
│  │     │     │  │  ├─ template_diffamp1_ac1.scs
│  │     │     │  │  ├─ template_diffamp1_ac2.scs
│  │     │     │  │  ├─ template_diffamp1_ac3.scs
│  │     │     │  │  ├─ template_diffamp1_dc1.scs
│  │     │     │  │  ├─ template_diffamp1_dc2.scs
│  │     │     │  │  ├─ template_diffamp1_tran1.scs
│  │     │     │  │  └─ template_diffamp1_tran2.scs
│  │     │     │  ├─ template_diffamp1_ac1.scs
│  │     │     │  ├─ template_diffamp1_ac2.scs
│  │     │     │  ├─ template_diffamp1_ac3.scs
│  │     │     │  ├─ template_diffamp1_dc1.scs
│  │     │     │  ├─ template_diffamp1_dc2.scs
│  │     │     │  ├─ template_diffamp1_dc3.scs
│  │     │     │  ├─ template_diffamp1_tran1.scs
│  │     │     │  └─ template_diffamp1_tran2.scs
│  │     │     ├─ spice
│  │     │     │  ├─ template_diffamp1_ac1.sp
│  │     │     │  ├─ template_diffamp1_ac2.sp
│  │     │     │  ├─ template_diffamp1_ac3.sp
│  │     │     │  ├─ template_diffamp1_dc1.sp
│  │     │     │  ├─ template_diffamp1_dc2.sp
│  │     │     │  ├─ template_diffamp1_dc3.sp
│  │     │     │  ├─ template_diffamp1_op1.sp
│  │     │     │  ├─ template_diffamp1_tran1.sp
│  │     │     │  ├─ template_diffamp1_tran2.sp
│  │     │     │  ├─ template_diffamp2_ac1.sp
│  │     │     │  ├─ template_diffamp2_ac2.sp
│  │     │     │  ├─ template_diffamp2_ac3.sp
│  │     │     │  ├─ template_diffamp2_dc2.sp
│  │     │     │  ├─ template_diffamp2_tran1.sp
│  │     │     │  └─ template_diffamp2_tran2.sp
│  │     │     ├─ template_comparator1_tran1.scs
│  │     │     ├─ template_comparator1_tran2.scs
│  │     │     ├─ template_comparator2_tran1.scs
│  │     │     ├─ template_comparator2_tran2.scs
│  │     │     ├─ template_diffamp1_ac1.scs
│  │     │     ├─ template_diffamp1_ac2.scs
│  │     │     ├─ template_diffamp1_ac3.scs
│  │     │     ├─ template_diffamp1_dc1.scs
│  │     │     ├─ template_diffamp1_dc2.scs
│  │     │     ├─ template_diffamp1_op1.scs
│  │     │     ├─ template_diffamp1_tran1.scs
│  │     │     ├─ template_diffamp1_tran2.scs
│  │     │     ├─ template_ls1_tran1.scs
│  │     │     ├─ template_st1_tran1.scs
│  │     │     └─ two_stage_rc
│  │     │        ├─ template_diffamp1_ac1.scs
│  │     │        ├─ template_diffamp1_ac2.scs
│  │     │        ├─ template_diffamp1_ac3.scs
│  │     │        ├─ template_diffamp1_dc1.scs
│  │     │        ├─ template_diffamp1_dc2.scs
│  │     │        ├─ template_diffamp1_op1.scs
│  │     │        ├─ template_diffamp1_tran1.scs
│  │     │        ├─ template_diffamp1_tran2.scs
│  │     │        └─ two_stage
│  │     │           ├─ template_diffamp1_ac1.scs
│  │     │           ├─ template_diffamp1_ac2.scs
│  │     │           ├─ template_diffamp1_ac3.scs
│  │     │           ├─ template_diffamp1_dc1.scs
│  │     │           ├─ template_diffamp1_dc2.scs
│  │     │           ├─ template_diffamp1_op1.scs
│  │     │           ├─ template_diffamp1_tran1.scs
│  │     │           └─ template_diffamp1_tran2.scs
│  │     ├─ smic018
│  │     │  ├─ ckt_netlist
│  │     │  │  ├─ FoldedCascodeOpamp.scs
│  │     │  │  ├─ FoldedCascodeOpamp2.scs
│  │     │  │  ├─ classabOpamp (copy).scs
│  │     │  │  ├─ classabOpamp.scs
│  │     │  │  ├─ classabOpamp2.scs
│  │     │  │  ├─ comparator1.scs
│  │     │  │  ├─ dynamicComparator.scs
│  │     │  │  ├─ level_shifter.scs
│  │     │  │  ├─ level_shifter_high_speed.scs
│  │     │  │  ├─ schmitt_trigger.scs
│  │     │  │  ├─ spectre
│  │     │  │  │  ├─ FoldedCascodeOpamp.scs
│  │     │  │  │  └─ twoStageOpamp2.scs
│  │     │  │  ├─ spice
│  │     │  │  │  ├─ FoldedCascodeOpamp.cir
│  │     │  │  │  └─ twoStageOpamp2.cir
│  │     │  │  └─ twoStageOpamp2.scs
│  │     │  ├─ models
│  │     │  │  ├─ hspice
│  │     │  │  │  ├─ ms018_rf_v1p5.lib
│  │     │  │  │  ├─ ms018_rf_v1p5_diff_ind.ckt
│  │     │  │  │  ├─ ms018_rf_v1p5_mim.ckt
│  │     │  │  │  ├─ ms018_rf_v1p5_mos.ckt
│  │     │  │  │  ├─ ms018_rf_v1p5_readme.txt
│  │     │  │  │  ├─ ms018_rf_v1p5_res.ckt
│  │     │  │  │  ├─ ms018_rf_v1p5_spri_ind.ckt
│  │     │  │  │  ├─ ms018_rf_v1p5_var.ckt
│  │     │  │  │  ├─ ms018_v1p7.lib
│  │     │  │  │  ├─ ms018_v1p7.mdl
│  │     │  │  │  ├─ ms018_v1p7_bjt.mdl
│  │     │  │  │  ├─ ms018_v1p7_mim.mdl
│  │     │  │  │  ├─ ms018_v1p7_readme.txt
│  │     │  │  │  ├─ ms018_v1p7_res.ckt
│  │     │  │  │  ├─ ms018_v1p7_res.mdl
│  │     │  │  │  ├─ rf018_m6_res.lib
│  │     │  │  │  └─ rf018_m6_res.mdl
│  │     │  │  └─ spectre
│  │     │  │     ├─ #ms018_v1p7_spe_test.lib#
│  │     │  │     ├─ ms018_rf_v1p5_diff_ind_spe.ckt
│  │     │  │     ├─ ms018_rf_v1p5_mim_spe.ckt
│  │     │  │     ├─ ms018_rf_v1p5_mos_spe.ckt
│  │     │  │     ├─ ms018_rf_v1p5_readme_spe.txt
│  │     │  │     ├─ ms018_rf_v1p5_res_spe.ckt
│  │     │  │     ├─ ms018_rf_v1p5_spe.lib
│  │     │  │     ├─ ms018_rf_v1p5_spri_ind_spe.ckt
│  │     │  │     ├─ ms018_rf_v1p5_var_spe.ckt
│  │     │  │     ├─ ms018_v1p7_bjt_spe.mdl
│  │     │  │     ├─ ms018_v1p7_mim_spe.mdl
│  │     │  │     ├─ ms018_v1p7_readme_spe.txt
│  │     │  │     ├─ ms018_v1p7_res_spe.ckt
│  │     │  │     ├─ ms018_v1p7_res_spe.mdl
│  │     │  │     ├─ ms018_v1p7_spe.lib
│  │     │  │     ├─ ms018_v1p7_spe.mdl
│  │     │  │     ├─ ms018_v1p7_spe_test.lib
│  │     │  │     ├─ ms018_v1p7_spe_test.lib~
│  │     │  │     ├─ ms018_v1p7_spe_test.mdl
│  │     │  │     ├─ res.def
│  │     │  │     ├─ res_rf.def
│  │     │  │     ├─ rf018_m6_res_spe.lib
│  │     │  │     └─ rf018_m6_res_spe.mdl
│  │     │  ├─ simResult
│  │     │  │  ├─ psf
│  │     │  │  │  ├─ logFile
│  │     │  │  │  ├─ logStatus
│  │     │  │  │  ├─ outac1.ac
│  │     │  │  │  ├─ outac1_spectre.out
│  │     │  │  │  ├─ outac2.ac
│  │     │  │  │  ├─ outac2_spectre.out
│  │     │  │  │  ├─ outac3.ac
│  │     │  │  │  ├─ outac3_spectre.out
│  │     │  │  │  ├─ outdc2.dc
│  │     │  │  │  ├─ outdc2_spectre.out
│  │     │  │  │  ├─ outtran1.tran.tran
│  │     │  │  │  ├─ outtran1_spectre.out
│  │     │  │  │  ├─ outtran2.tran.tran
│  │     │  │  │  └─ outtran2_spectre.out
│  │     │  │  ├─ test_diffamp1_ac1.scs
│  │     │  │  ├─ test_diffamp1_ac2.scs
│  │     │  │  ├─ test_diffamp1_ac3.scs
│  │     │  │  ├─ test_diffamp1_dc2.scs
│  │     │  │  ├─ test_diffamp1_tran1.scs
│  │     │  │  └─ test_diffamp1_tran2.scs
│  │     │  └─ tb_template
│  │     │     ├─ Folded_Cascode
│  │     │     │  ├─ template_diffamp1_ac1.scs
│  │     │     │  ├─ template_diffamp1_ac2.scs
│  │     │     │  ├─ template_diffamp1_ac3.scs
│  │     │     │  ├─ template_diffamp1_dc1.scs
│  │     │     │  ├─ template_diffamp1_dc2.scs
│  │     │     │  ├─ template_diffamp1_op1.scs
│  │     │     │  ├─ template_diffamp1_tran1.scs
│  │     │     │  └─ template_diffamp1_tran2.scs
│  │     │     ├─ classAB
│  │     │     │  ├─ class_ab
│  │     │     │  │  ├─ template_diffamp1_ac1.scs
│  │     │     │  │  ├─ template_diffamp1_ac2.scs
│  │     │     │  │  ├─ template_diffamp1_ac3.scs
│  │     │     │  │  ├─ template_diffamp1_dc1.scs
│  │     │     │  │  ├─ template_diffamp1_dc2.scs
│  │     │     │  │  ├─ template_diffamp1_op1.scs
│  │     │     │  │  ├─ template_diffamp1_tran1.scs
│  │     │     │  │  └─ template_diffamp1_tran2.scs
│  │     │     │  ├─ template_diffamp1_ac1.scs
│  │     │     │  ├─ template_diffamp1_ac2.scs
│  │     │     │  ├─ template_diffamp1_ac3.scs
│  │     │     │  ├─ template_diffamp1_dc1.scs
│  │     │     │  ├─ template_diffamp1_dc2.scs
│  │     │     │  ├─ template_diffamp1_op1.scs
│  │     │     │  ├─ template_diffamp1_tran1.scs
│  │     │     │  └─ template_diffamp1_tran2.scs
│  │     │     ├─ high_speed_level_shifter
│  │     │     │  └─ template_ls1_tran1.scs
│  │     │     ├─ spectre
│  │     │     │  ├─ classab_old
│  │     │     │  │  ├─ template_diffamp1_ac1.scs
│  │     │     │  │  ├─ template_diffamp1_ac2.scs
│  │     │     │  │  ├─ template_diffamp1_ac3.scs
│  │     │     │  │  ├─ template_diffamp1_dc1.scs
│  │     │     │  │  ├─ template_diffamp1_dc2.scs
│  │     │     │  │  ├─ template_diffamp1_tran1.scs
│  │     │     │  │  └─ template_diffamp1_tran2.scs
│  │     │     │  ├─ template_diffamp1_ac1.scs
│  │     │     │  ├─ template_diffamp1_ac2.scs
│  │     │     │  ├─ template_diffamp1_ac3.scs
│  │     │     │  ├─ template_diffamp1_dc1.scs
│  │     │     │  ├─ template_diffamp1_dc2.scs
│  │     │     │  ├─ template_diffamp1_dc3.scs
│  │     │     │  ├─ template_diffamp1_tran1.scs
│  │     │     │  └─ template_diffamp1_tran2.scs
│  │     │     ├─ spice
│  │     │     │  ├─ template_diffamp1_ac1.sp
│  │     │     │  ├─ template_diffamp1_ac2.sp
│  │     │     │  ├─ template_diffamp1_ac3.sp
│  │     │     │  ├─ template_diffamp1_dc1.sp
│  │     │     │  ├─ template_diffamp1_dc2.sp
│  │     │     │  ├─ template_diffamp1_dc3.sp
│  │     │     │  ├─ template_diffamp1_op1.sp
│  │     │     │  ├─ template_diffamp1_tran1.sp
│  │     │     │  ├─ template_diffamp1_tran2.sp
│  │     │     │  ├─ template_diffamp2_ac1.sp
│  │     │     │  ├─ template_diffamp2_ac2.sp
│  │     │     │  ├─ template_diffamp2_ac3.sp
│  │     │     │  ├─ template_diffamp2_dc2.sp
│  │     │     │  ├─ template_diffamp2_tran1.sp
│  │     │     │  └─ template_diffamp2_tran2.sp
│  │     │     ├─ template_comparator1_tran1.scs
│  │     │     ├─ template_comparator1_tran2.scs
│  │     │     ├─ template_comparator2_tran1.scs
│  │     │     ├─ template_comparator2_tran2.scs
│  │     │     ├─ template_diffamp1_ac1.scs
│  │     │     ├─ template_diffamp1_ac2.scs
│  │     │     ├─ template_diffamp1_ac3.scs
│  │     │     ├─ template_diffamp1_dc1.scs
│  │     │     ├─ template_diffamp1_dc2.scs
│  │     │     ├─ template_diffamp1_op1.scs
│  │     │     ├─ template_diffamp1_tran1.scs
│  │     │     ├─ template_diffamp1_tran2.scs
│  │     │     ├─ template_ls1_tran1.scs
│  │     │     ├─ template_st1_tran1.scs
│  │     │     └─ two_stage_rc
│  │     │        ├─ template_diffamp1_ac1.scs
│  │     │        ├─ template_diffamp1_ac2.scs
│  │     │        ├─ template_diffamp1_ac3.scs
│  │     │        ├─ template_diffamp1_dc1.scs
│  │     │        ├─ template_diffamp1_dc2.scs
│  │     │        ├─ template_diffamp1_op1.scs
│  │     │        ├─ template_diffamp1_tran1.scs
│  │     │        └─ template_diffamp1_tran2.scs
│  │     ├─ smic40
│  │     │  ├─ ckt_netlist
│  │     │  │  ├─ FoldedCascodeOpamp.scs
│  │     │  │  ├─ FoldedCascodeOpamp2.scs
│  │     │  │  ├─ classabOpamp (copy).scs
│  │     │  │  ├─ classabOpamp.scs
│  │     │  │  ├─ classabOpamp2.scs
│  │     │  │  ├─ comparator1.scs
│  │     │  │  ├─ dynamicComparator.scs
│  │     │  │  ├─ level_shifter.scs
│  │     │  │  ├─ level_shifter_high_speed.scs
│  │     │  │  ├─ schmitt_trigger.scs
│  │     │  │  ├─ spectre
│  │     │  │  │  ├─ FoldedCascodeOpamp.scs
│  │     │  │  │  └─ twoStageOpamp2.scs
│  │     │  │  ├─ spice
│  │     │  │  │  ├─ FoldedCascodeOpamp.cir
│  │     │  │  │  └─ twoStageOpamp2.cir
│  │     │  │  └─ twoStageOpamp2.scs
│  │     │  ├─ models
│  │     │  │  ├─ simulator_version.txt
│  │     │  │  └─ spectre
│  │     │  │     ├─ bjt
│  │     │  │     │  ├─ npn11a100ll_sba_spe.mdl
│  │     │  │     │  ├─ npn11a100ll_spe.mdl
│  │     │  │     │  ├─ npn11a25ll_sba_spe.mdl
│  │     │  │     │  ├─ npn11a25ll_spe.mdl
│  │     │  │     │  ├─ npn11a4ll_sba_spe.mdl
│  │     │  │     │  ├─ npn11a4ll_spe.mdl
│  │     │  │     │  ├─ npn25a100ll_sba_spe.mdl
│  │     │  │     │  ├─ npn25a100ll_spe.mdl
│  │     │  │     │  ├─ npn25a25ll_sba_spe.mdl
│  │     │  │     │  ├─ npn25a25ll_spe.mdl
│  │     │  │     │  ├─ npn25a4ll_sba_spe.mdl
│  │     │  │     │  ├─ npn25a4ll_spe.mdl
│  │     │  │     │  ├─ pnp11a100ll_sba_spe.mdl
│  │     │  │     │  ├─ pnp11a100ll_spe.mdl
│  │     │  │     │  ├─ pnp11a25ll_sba_spe.mdl
│  │     │  │     │  ├─ pnp11a25ll_spe.mdl
│  │     │  │     │  ├─ pnp11a4ll_sba_spe.mdl
│  │     │  │     │  ├─ pnp11a4ll_spe.mdl
│  │     │  │     │  ├─ pnp25a100ll_sba_spe.mdl
│  │     │  │     │  ├─ pnp25a100ll_spe.mdl
│  │     │  │     │  ├─ pnp25a25ll_sba_spe.mdl
│  │     │  │     │  ├─ pnp25a25ll_spe.mdl
│  │     │  │     │  ├─ pnp25a4ll_sba_spe.mdl
│  │     │  │     │  └─ pnp25a4ll_spe.mdl
│  │     │  │     ├─ gc.va
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_n11ll_spe.mdl
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_n25ll_spe.mdl
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_nhvt11ll_spe.mdl
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_nlvt11ll_spe.mdl
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_nod33ll_spe.mdl
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_nud18ll_spe.mdl
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_p11ll_spe.mdl
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_p25ll_spe.mdl
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_phvt11ll_spe.mdl
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_plvt11ll_spe.mdl
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_pod33ll_spe.mdl
│  │     │  │     ├─ l0040ll_lpe_v1p4_1r_pud18ll_spe.mdl
│  │     │  │     ├─ l0040ll_v1p4_1r_dio_spe.mdl
│  │     │  │     ├─ l0040ll_v1p4_1r_ldmos_spe.ckt
│  │     │  │     ├─ l0040ll_v1p4_1r_mom_spe.ckt
│  │     │  │     ├─ l0040ll_v1p4_1r_readme_spe.txt
│  │     │  │     ├─ l0040ll_v1p4_1r_res_spe.ckt
│  │     │  │     ├─ l0040ll_v1p4_1r_spe.lib
│  │     │  │     ├─ l0040ll_v1p4_1r_spe.mdl
│  │     │  │     ├─ l0040ll_v1p4_1r_var_spe.ckt
│  │     │  │     └─ res.va
│  │     │  ├─ simResult
│  │     │  │  ├─ psf
│  │     │  │  │  ├─ logFile
│  │     │  │  │  ├─ logStatus
│  │     │  │  │  ├─ outac1.ac
│  │     │  │  │  ├─ outac1_spectre.out
│  │     │  │  │  ├─ outac2.ac
│  │     │  │  │  ├─ outac2_spectre.out
│  │     │  │  │  ├─ outac3.ac
│  │     │  │  │  ├─ outac3_spectre.out
│  │     │  │  │  ├─ outdc2.dc
│  │     │  │  │  ├─ outdc2_spectre.out
│  │     │  │  │  ├─ outtran1.tran.tran
│  │     │  │  │  ├─ outtran1_spectre.out
│  │     │  │  │  ├─ outtran2.tran.tran
│  │     │  │  │  └─ outtran2_spectre.out
│  │     │  │  ├─ test_diffamp1_ac1.scs
│  │     │  │  ├─ test_diffamp1_ac2.scs
│  │     │  │  ├─ test_diffamp1_ac3.scs
│  │     │  │  ├─ test_diffamp1_dc2.scs
│  │     │  │  ├─ test_diffamp1_tran1.scs
│  │     │  │  └─ test_diffamp1_tran2.scs
│  │     │  └─ tb_template
│  │     │     ├─ Folded_Cascode
│  │     │     │  ├─ template_diffamp1_ac1.scs
│  │     │     │  ├─ template_diffamp1_ac2.scs
│  │     │     │  ├─ template_diffamp1_ac3.scs
│  │     │     │  ├─ template_diffamp1_dc1.scs
│  │     │     │  ├─ template_diffamp1_dc2.scs
│  │     │     │  ├─ template_diffamp1_op1.scs
│  │     │     │  ├─ template_diffamp1_tran1.scs
│  │     │     │  └─ template_diffamp1_tran2.scs
│  │     │     ├─ classAB
│  │     │     │  ├─ class_ab
│  │     │     │  │  ├─ template_diffamp1_ac1.scs
│  │     │     │  │  ├─ template_diffamp1_ac2.scs
│  │     │     │  │  ├─ template_diffamp1_ac3.scs
│  │     │     │  │  ├─ template_diffamp1_dc1.scs
│  │     │     │  │  ├─ template_diffamp1_dc2.scs
│  │     │     │  │  ├─ template_diffamp1_op1.scs
│  │     │     │  │  ├─ template_diffamp1_tran1.scs
│  │     │     │  │  └─ template_diffamp1_tran2.scs
│  │     │     │  ├─ template_diffamp1_ac1.scs
│  │     │     │  ├─ template_diffamp1_ac2.scs
│  │     │     │  ├─ template_diffamp1_ac3.scs
│  │     │     │  ├─ template_diffamp1_dc1.scs
│  │     │     │  ├─ template_diffamp1_dc2.scs
│  │     │     │  ├─ template_diffamp1_op1.scs
│  │     │     │  ├─ template_diffamp1_tran1.scs
│  │     │     │  └─ template_diffamp1_tran2.scs
│  │     │     ├─ high_speed_level_shifter
│  │     │     │  └─ template_ls1_tran1.scs
│  │     │     ├─ spectre
│  │     │     │  ├─ classab_old
│  │     │     │  │  ├─ template_diffamp1_ac1.scs
│  │     │     │  │  ├─ template_diffamp1_ac2.scs
│  │     │     │  │  ├─ template_diffamp1_ac3.scs
│  │     │     │  │  ├─ template_diffamp1_dc1.scs
│  │     │     │  │  ├─ template_diffamp1_dc2.scs
│  │     │     │  │  ├─ template_diffamp1_tran1.scs
│  │     │     │  │  └─ template_diffamp1_tran2.scs
│  │     │     │  ├─ template_diffamp1_ac1.scs
│  │     │     │  ├─ template_diffamp1_ac2.scs
│  │     │     │  ├─ template_diffamp1_ac3.scs
│  │     │     │  ├─ template_diffamp1_dc1.scs
│  │     │     │  ├─ template_diffamp1_dc2.scs
│  │     │     │  ├─ template_diffamp1_dc3.scs
│  │     │     │  ├─ template_diffamp1_tran1.scs
│  │     │     │  └─ template_diffamp1_tran2.scs
│  │     │     ├─ spice
│  │     │     │  ├─ template_diffamp1_ac1.sp
│  │     │     │  ├─ template_diffamp1_ac2.sp
│  │     │     │  ├─ template_diffamp1_ac3.sp
│  │     │     │  ├─ template_diffamp1_dc1.sp
│  │     │     │  ├─ template_diffamp1_dc2.sp
│  │     │     │  ├─ template_diffamp1_dc3.sp
│  │     │     │  ├─ template_diffamp1_op1.sp
│  │     │     │  ├─ template_diffamp1_tran1.sp
│  │     │     │  ├─ template_diffamp1_tran2.sp
│  │     │     │  ├─ template_diffamp2_ac1.sp
│  │     │     │  ├─ template_diffamp2_ac2.sp
│  │     │     │  ├─ template_diffamp2_ac3.sp
│  │     │     │  ├─ template_diffamp2_dc2.sp
│  │     │     │  ├─ template_diffamp2_tran1.sp
│  │     │     │  └─ template_diffamp2_tran2.sp
│  │     │     ├─ template_comparator1_tran1.scs
│  │     │     ├─ template_comparator1_tran2.scs
│  │     │     ├─ template_comparator2_tran1.scs
│  │     │     ├─ template_comparator2_tran2.scs
│  │     │     ├─ template_diffamp1_ac1.scs
│  │     │     ├─ template_diffamp1_ac2.scs
│  │     │     ├─ template_diffamp1_ac3.scs
│  │     │     ├─ template_diffamp1_dc1.scs
│  │     │     ├─ template_diffamp1_dc2.scs
│  │     │     ├─ template_diffamp1_op1.scs
│  │     │     ├─ template_diffamp1_tran1.scs
│  │     │     ├─ template_diffamp1_tran2.scs
│  │     │     ├─ template_ls1_tran1.scs
│  │     │     ├─ template_st1_tran1.scs
│  │     │     └─ two_stage_rc
│  │     │        ├─ template_diffamp1_ac1.scs
│  │     │        ├─ template_diffamp1_ac2.scs
│  │     │        ├─ template_diffamp1_ac3.scs
│  │     │        ├─ template_diffamp1_dc1.scs
│  │     │        ├─ template_diffamp1_dc2.scs
│  │     │        ├─ template_diffamp1_op1.scs
│  │     │        ├─ template_diffamp1_tran1.scs
│  │     │        └─ template_diffamp1_tran2.scs
│  │     ├─ src
│  │     ├─ utility.py
│  │     └─ utils
│  │        ├─ __init__.py
│  │        ├─ __pycache__
│  │        │  ├─ __init__.cpython-311.pyc
│  │        │  ├─ gui.cpython-311.pyc
│  │        │  ├─ gui_parser.cpython-311.pyc
│  │        │  └─ log.cpython-311.pyc
│  │        ├─ gui.py
│  │        └─ log.py
│  ├─ cell
│  │  ├─ __init__.py
│  │  └─ apr
│  │     └─ __init__.py
│  ├─ ferry
│  │  └─ __init__.py
│  ├─ io
│  │  └─ __init__.py
│  └─ rule
│     └─ __init__.py
├─ output
│  └─ README.md
├─ resources
│  ├─ README.md
│  ├─ designlib
│  │  ├─ Opamp
│  │  │  ├─ .oalib
│  │  │  ├─ OpAmp
│  │  │  │  ├─ data.dm
│  │  │  │  ├─ maestro_basic
│  │  │  │  │  ├─ active.state
│  │  │  │  │  ├─ data.dm
│  │  │  │  │  ├─ documents
│  │  │  │  │  ├─ history
│  │  │  │  │  │  ├─ Interactive.0.zip
│  │  │  │  │  │  ├─ Interactive.1.zip
│  │  │  │  │  │  └─ history.sdb
│  │  │  │  │  ├─ maestro.sdb
│  │  │  │  │  ├─ maestro.sdb.cdslck
│  │  │  │  │  ├─ master.tag
│  │  │  │  │  ├─ plottingTemplates
│  │  │  │  │  │  └─ SwingFainUGF_PT
│  │  │  │  │  │     ├─ SwingFainUGF_PT.cmpt.group
│  │  │  │  │  │     ├─ SwingFainUGF_PT_0.cmpt
│  │  │  │  │  │     └─ SwingFainUGF_PT_1.cmpt
│  │  │  │  │  ├─ results
│  │  │  │  │  │  ├─ data
│  │  │  │  │  │  │  └─ MonteCarlo.17.log
│  │  │  │  │  │  └─ maestro
│  │  │  │  │  │     ├─ Interactive.0.log
│  │  │  │  │  │     ├─ Interactive.0.rdb
│  │  │  │  │  │     ├─ Interactive.1.log
│  │  │  │  │  │     └─ Interactive.1.rdb
│  │  │  │  │  └─ states
│  │  │  │  │     └─ ref_point_migrated.sdb
│  │  │  │  ├─ maestro_sweeps#2dcorners
│  │  │  │  │  ├─ active.state
│  │  │  │  │  ├─ data.dm
│  │  │  │  │  ├─ history
│  │  │  │  │  │  ├─ ForVerification.zip
│  │  │  │  │  │  ├─ FullCoverage.zip
│  │  │  │  │  │  ├─ Interactive.0.zip
│  │  │  │  │  │  └─ history.sdb
│  │  │  │  │  ├─ maestro.sdb
│  │  │  │  │  ├─ master.tag
│  │  │  │  │  ├─ results
│  │  │  │  │  │  ├─ data
│  │  │  │  │  │  │  └─ MonteCarlo.17.log
│  │  │  │  │  │  └─ maestro
│  │  │  │  │  │     ├─ ForVerification.log
│  │  │  │  │  │     ├─ ForVerification.rdb
│  │  │  │  │  │     ├─ FullCoverage.log
│  │  │  │  │  │     ├─ FullCoverage.rdb
│  │  │  │  │  │     ├─ Interactive.0.log
│  │  │  │  │  │     ├─ Interactive.0.rdb
│  │  │  │  │  │     └─ LoggingService.db
│  │  │  │  │  └─ states
│  │  │  │  │     └─ ref_point_migrated.sdb
│  │  │  │  ├─ schematic
│  │  │  │  │  ├─ data.dm
│  │  │  │  │  ├─ master.tag
│  │  │  │  │  ├─ sch.oa
│  │  │  │  │  ├─ thumbnail_1024x1024.png
│  │  │  │  │  └─ thumbnail_128x128.png
│  │  │  │  ├─ schematic2
│  │  │  │  │  ├─ data.dm
│  │  │  │  │  ├─ master.tag
│  │  │  │  │  ├─ sch.oa
│  │  │  │  │  ├─ thumbnail_1024x1024.png
│  │  │  │  │  └─ thumbnail_128x128.png
│  │  │  │  └─ symbol
│  │  │  │     ├─ master.tag
│  │  │  │     └─ symbol.oa
│  │  │  ├─ cdsinfo.tag
│  │  │  └─ data.dm
│  │  ├─ Opamp_TB
│  │  │  ├─ .oalib
│  │  │  ├─ OpAmp_AC_top
│  │  │  │  ├─ .sevSaveDir
│  │  │  │  ├─ config
│  │  │  │  │  ├─ data.dm
│  │  │  │  │  ├─ expand.cfg
│  │  │  │  │  └─ master.tag
│  │  │  │  ├─ data.dm
│  │  │  │  ├─ maestro_basic
│  │  │  │  │  ├─ active.state
│  │  │  │  │  ├─ data.dm
│  │  │  │  │  ├─ history
│  │  │  │  │  │  ├─ ExplorerRun.0.zip
│  │  │  │  │  │  └─ history.sdb
│  │  │  │  │  ├─ maestro.sdb
│  │  │  │  │  ├─ master.tag
│  │  │  │  │  └─ results
│  │  │  │  │     └─ maestro
│  │  │  │  │        ├─ ExplorerRun.0.log
│  │  │  │  │        └─ ExplorerRun.0.rdb
│  │  │  │  └─ schematic
│  │  │  │     ├─ data.dm
│  │  │  │     ├─ master.tag
│  │  │  │     ├─ sch.oa
│  │  │  │     └─ thumbnail_128x128.png
│  │  │  ├─ OpAmp_TRAN_top
│  │  │  │  ├─ config
│  │  │  │  │  ├─ data.dm
│  │  │  │  │  ├─ expand.cfg
│  │  │  │  │  └─ master.tag
│  │  │  │  ├─ config2
│  │  │  │  │  ├─ data.dm
│  │  │  │  │  ├─ expand.cfg
│  │  │  │  │  └─ master.tag
│  │  │  │  ├─ data.dm
│  │  │  │  ├─ maestro
│  │  │  │  │  ├─ active.state
│  │  │  │  │  ├─ data.dm
│  │  │  │  │  ├─ history
│  │  │  │  │  │  └─ history.sdb
│  │  │  │  │  ├─ maestro.sdb
│  │  │  │  │  └─ master.tag
│  │  │  │  └─ schematic
│  │  │  │     ├─ data.dm
│  │  │  │     ├─ master.tag
│  │  │  │     ├─ sch.oa
│  │  │  │     └─ thumbnail_128x128.png
│  │  │  ├─ cdsinfo.tag
│  │  │  ├─ data.dm
│  │  │  └─ opamp_dc_feedback
│  │  │     ├─ data.dm
│  │  │     ├─ schematic
│  │  │     │  ├─ data.dm
│  │  │     │  ├─ master.tag
│  │  │     │  ├─ sch.oa
│  │  │     │  └─ thumbnail_128x128.png
│  │  │     └─ symbol
│  │  │        ├─ master.tag
│  │  │        └─ symbol.oa
│  │  └─ Two_Stage_Opamp
│  │     ├─ .oalib
│  │     ├─ .sevSaveDir
│  │     ├─ Aux.Cat
│  │     ├─ Cells.Cat
│  │     ├─ Documentation.Cat
│  │     ├─ DualAmp
│  │     │  ├─ data.dm
│  │     │  ├─ schematic
│  │     │  │  ├─ data.dm
│  │     │  │  ├─ master.tag
│  │     │  │  ├─ sch.oa
│  │     │  │  ├─ sch.oa.cdslck
│  │     │  │  ├─ sch.oa.cdslck.RHEL30.noivl-sonals.31516
│  │     │  │  ├─ thumbnail_1024x1024.png
│  │     │  │  └─ thumbnail_128x128.png
│  │     │  └─ symbol
│  │     │     ├─ master.tag
│  │     │     ├─ symbol.oa
│  │     │     └─ thumbnail_128x128.png
│  │     ├─ Obsolete.Cat
│  │     ├─ OpAmp
│  │     │  ├─ data.dm
│  │     │  ├─ maestro_basic
│  │     │  │  ├─ active.state
│  │     │  │  ├─ data.dm
│  │     │  │  ├─ documents
│  │     │  │  ├─ history
│  │     │  │  │  ├─ Interactive.0.zip
│  │     │  │  │  ├─ Interactive.1.zip
│  │     │  │  │  └─ history.sdb
│  │     │  │  ├─ maestro.sdb
│  │     │  │  ├─ master.tag
│  │     │  │  ├─ plottingTemplates
│  │     │  │  │  └─ SwingFainUGF_PT
│  │     │  │  │     ├─ SwingFainUGF_PT.cmpt.group
│  │     │  │  │     ├─ SwingFainUGF_PT_0.cmpt
│  │     │  │  │     └─ SwingFainUGF_PT_1.cmpt
│  │     │  │  ├─ results
│  │     │  │  │  ├─ data
│  │     │  │  │  │  ├─ .rdb
│  │     │  │  │  │  ├─ MonteCarlo.17.log
│  │     │  │  │  │  └─ psf
│  │     │  │  │  │     ├─ AC
│  │     │  │  │  │     │  └─ psf
│  │     │  │  │  │     ├─ DC
│  │     │  │  │  │     │  └─ psf
│  │     │  │  │  │     └─ TRAN
│  │     │  │  │  │        └─ psf
│  │     │  │  │  └─ maestro
│  │     │  │  │     ├─ Interactive.0.log
│  │     │  │  │     ├─ Interactive.0.rdb
│  │     │  │  │     ├─ Interactive.1.log
│  │     │  │  │     └─ Interactive.1.rdb
│  │     │  │  ├─ states
│  │     │  │  │  └─ ref_point_migrated.sdb
│  │     │  │  └─ test_states
│  │     │  │     └─ Two_Stage_Opamp
│  │     │  │        ├─ .sevSaveDir
│  │     │  │        └─ OpAmp_AC_top
│  │     │  │           ├─ .sevSaveDir
│  │     │  │           └─ aps
│  │     │  ├─ maestro_sweeps#2dcorners
│  │     │  │  ├─ active.state
│  │     │  │  ├─ data.dm
│  │     │  │  ├─ documents
│  │     │  │  ├─ history
│  │     │  │  │  ├─ ForVerification.zip
│  │     │  │  │  ├─ FullCoverage.zip
│  │     │  │  │  ├─ Interactive.0.zip
│  │     │  │  │  └─ history.sdb
│  │     │  │  ├─ maestro.sdb
│  │     │  │  ├─ master.tag
│  │     │  │  ├─ results
│  │     │  │  │  ├─ data
│  │     │  │  │  │  ├─ .rdb
│  │     │  │  │  │  ├─ MonteCarlo.17.log
│  │     │  │  │  │  └─ psf
│  │     │  │  │  │     ├─ AC
│  │     │  │  │  │     │  └─ psf
│  │     │  │  │  │     ├─ DC
│  │     │  │  │  │     │  └─ psf
│  │     │  │  │  │     └─ TRAN
│  │     │  │  │  │        └─ psf
│  │     │  │  │  └─ maestro
│  │     │  │  │     ├─ ForVerification.log
│  │     │  │  │     ├─ ForVerification.rdb
│  │     │  │  │     ├─ FullCoverage.log
│  │     │  │  │     ├─ FullCoverage.rdb
│  │     │  │  │     ├─ Interactive.0.log
│  │     │  │  │     ├─ Interactive.0.rdb
│  │     │  │  │     └─ LoggingService.db
│  │     │  │  ├─ states
│  │     │  │  │  └─ ref_point_migrated.sdb
│  │     │  │  └─ test_states
│  │     │  │     └─ Two_Stage_Opamp
│  │     │  │        ├─ .sevSaveDir
│  │     │  │        ├─ OpAmp_AC_top
│  │     │  │        │  ├─ .sevSaveDir
│  │     │  │        │  ├─ aps
│  │     │  │        │  └─ spectre
│  │     │  │        └─ OpAmp_TRAN_top
│  │     │  │           └─ spectre
│  │     │  ├─ schematic
│  │     │  │  ├─ data.dm
│  │     │  │  ├─ master.tag
│  │     │  │  ├─ sch.oa
│  │     │  │  ├─ sch.oa-
│  │     │  │  ├─ thumbnail_1024x1024.png
│  │     │  │  └─ thumbnail_128x128.png
│  │     │  ├─ schematic2
│  │     │  │  ├─ data.dm
│  │     │  │  ├─ master.tag
│  │     │  │  ├─ sch.oa
│  │     │  │  ├─ thumbnail_1024x1024.png
│  │     │  │  └─ thumbnail_128x128.png
│  │     │  └─ symbol
│  │     │     ├─ master.tag
│  │     │     └─ symbol.oa
│  │     ├─ OpAmp_AC_top
│  │     │  ├─ .sevSaveDir
│  │     │  ├─ config
│  │     │  │  ├─ data.dm
│  │     │  │  ├─ expand.cfg
│  │     │  │  └─ master.tag
│  │     │  ├─ data.dm
│  │     │  ├─ maestro_basic
│  │     │  │  ├─ active.state
│  │     │  │  ├─ data.dm
│  │     │  │  ├─ documents
│  │     │  │  ├─ history
│  │     │  │  │  ├─ ExplorerRun.0.zip
│  │     │  │  │  └─ history.sdb
│  │     │  │  ├─ maestro.sdb
│  │     │  │  ├─ master.tag
│  │     │  │  ├─ results
│  │     │  │  │  └─ maestro
│  │     │  │  │     ├─ ExplorerRun.0.log
│  │     │  │  │     └─ ExplorerRun.0.rdb
│  │     │  │  └─ states
│  │     │  └─ schematic
│  │     │     ├─ data.dm
│  │     │     ├─ master.tag
│  │     │     ├─ sch.oa
│  │     │     ├─ sch.oa-
│  │     │     └─ thumbnail_128x128.png
│  │     ├─ OpAmp_TRAN_top
│  │     │  ├─ config
│  │     │  │  ├─ data.dm
│  │     │  │  ├─ expand.cfg
│  │     │  │  └─ master.tag
│  │     │  ├─ config2
│  │     │  │  ├─ data.dm
│  │     │  │  ├─ expand.cfg
│  │     │  │  ├─ expand.cfg%
│  │     │  │  └─ master.tag
│  │     │  ├─ data.dm
│  │     │  ├─ maestro
│  │     │  │  ├─ active.state
│  │     │  │  ├─ data.dm
│  │     │  │  ├─ documents
│  │     │  │  ├─ history
│  │     │  │  │  └─ history.sdb
│  │     │  │  ├─ maestro.sdb
│  │     │  │  ├─ master.tag
│  │     │  │  ├─ states
│  │     │  │  └─ test_states
│  │     │  │     └─ Two_Stage_Opamp
│  │     │  │        ├─ .sevSaveDir
│  │     │  │        └─ OpAmp_TRAN_top
│  │     │  │           ├─ .sevSaveDir
│  │     │  │           └─ spectre
│  │     │  │              ├─ .sevSaveDir
│  │     │  │              └─ tmpstate.614043148
│  │     │  │                 ├─ .sevSaveDir
│  │     │  │                 ├─ ADE_state.info
│  │     │  │                 ├─ analyses
│  │     │  │                 ├─ convergence
│  │     │  │                 ├─ cosimOptions
│  │     │  │                 ├─ devCheckingSetup
│  │     │  │                 ├─ environmentOptions
│  │     │  │                 ├─ graphicalStimuli
│  │     │  │                 ├─ mdlOptions
│  │     │  │                 ├─ modelSetup
│  │     │  │                 ├─ opPoints
│  │     │  │                 ├─ outputs
│  │     │  │                 ├─ outputsScripts
│  │     │  │                 ├─ paramSetup
│  │     │  │                 ├─ relxOptions
│  │     │  │                 ├─ rfstim
│  │     │  │                 ├─ simulationFiles
│  │     │  │                 ├─ simulatorOptions
│  │     │  │                 ├─ spList
│  │     │  │                 ├─ subckts
│  │     │  │                 ├─ turboOptions
│  │     │  │                 └─ variables
│  │     │  └─ schematic
│  │     │     ├─ data.dm
│  │     │     ├─ master.tag
│  │     │     ├─ sch.oa
│  │     │     ├─ sch.oa-
│  │     │     └─ thumbnail_128x128.png
│  │     ├─ Testbenches.Cat
│  │     ├─ Two_Stage_Opamp.TopCat
│  │     ├─ Verification.Cat
│  │     ├─ cdsinfo.tag
│  │     ├─ data.dm
│  │     └─ opamp_dc_feedback
│  │        ├─ data.dm
│  │        ├─ schematic
│  │        │  ├─ data.dm
│  │        │  ├─ master.tag
│  │        │  ├─ sch.oa
│  │        │  ├─ sch.oa-
│  │        │  └─ thumbnail_128x128.png
│  │        └─ symbol
│  │           ├─ master.tag
│  │           └─ symbol.oa
│  ├─ simulation_setup.txt
│  ├─ smic011
│  │  ├─ ckt_netlist
│  │  │  ├─ FoldedCascodeOpamp.scs
│  │  │  ├─ FoldedCascodeOpamp2.scs
│  │  │  ├─ classabOpamp (copy).scs
│  │  │  ├─ classabOpamp.scs
│  │  │  ├─ classabOpamp2.scs
│  │  │  ├─ comparator1.scs
│  │  │  ├─ dynamicComparator.scs
│  │  │  ├─ level_shifter.scs
│  │  │  ├─ level_shifter_high_speed.scs
│  │  │  ├─ schmitt_trigger.scs
│  │  │  ├─ spectre
│  │  │  │  ├─ FoldedCascodeOpamp.scs
│  │  │  │  └─ twoStageOpamp2.scs
│  │  │  ├─ spice
│  │  │  │  ├─ FoldedCascodeOpamp.cir
│  │  │  │  └─ twoStageOpamp2.cir
│  │  │  └─ twoStageOpamp2.scs
│  │  ├─ models
│  │  │  ├─ hspice
│  │  │  │  ├─ ms011_ms013s_io33_diff_ind_3t_rf_pgs_n_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_diff_ind_3t_rf_pgs_psub_n_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_diff_ind_rf_pgs_n_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_diff_ind_rf_pgs_psub_n_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_ind_rf_pgs_n_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_ind_rf_pgs_psub_n_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_layer.map
│  │  │  │  ├─ ms011_ms013s_io33_rf_3T_diff_ind_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_rf_3Tdiff_1talpa_psub_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_rf_3Tdiff_1talpa_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_rf_TM2_res_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_rf_diff_ind_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_rf_interconnect_TM2_3um_ALPA_struct_1.txt
│  │  │  │  ├─ ms011_ms013s_io33_rf_interconnect_TM2_3um_ALPA_struct_2.txt
│  │  │  │  ├─ ms011_ms013s_io33_rf_mim_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_rf_mom_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_rf_mos_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_rf_readme_v1p14.txt
│  │  │  │  ├─ ms011_ms013s_io33_rf_res_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_rf_spir_ind_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_rf_v1p14.lib
│  │  │  │  ├─ ms011_ms013s_io33_rf_var_v1p14.ckt
│  │  │  │  ├─ ms011_ms013s_io33_v1p24.lib
│  │  │  │  ├─ ms011_ms013s_io33_v1p24.mdl
│  │  │  │  ├─ ms011_ms013s_io33_v1p24_bjt.mdl
│  │  │  │  ├─ ms011_ms013s_io33_v1p24_dio.mdl
│  │  │  │  ├─ ms011_ms013s_io33_v1p24_interconnect_struct_1.txt
│  │  │  │  ├─ ms011_ms013s_io33_v1p24_interconnect_struct_2.txt
│  │  │  │  ├─ ms011_ms013s_io33_v1p24_mim.mdl
│  │  │  │  ├─ ms011_ms013s_io33_v1p24_mis.mdl
│  │  │  │  ├─ ms011_ms013s_io33_v1p24_readme.txt
│  │  │  │  ├─ ms011_ms013s_io33_v1p24_res.ckt
│  │  │  │  ├─ ms011_ms013s_io33_v1p24_res.mdl
│  │  │  │  └─ simulator_version.txt
│  │  │  └─ spectre
│  │  │     ├─ gc.va
│  │  │     ├─ gc_rf.va
│  │  │     ├─ ms011_ms013s_io33_diff_ind_3t_rf_pgs_n_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_diff_ind_3t_rf_pgs_psub_n_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_diff_ind_rf_pgs_n_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_diff_ind_rf_pgs_psub_n_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_ind_rf_pgs_n_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_ind_rf_pgs_psub_n_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_layer.map
│  │  │     ├─ ms011_ms013s_io33_rf_3T_diff_ind_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_rf_3Tdiff_1talpa_psub_spe_v1p14.ckt
│  │  │     ├─ ms011_ms013s_io33_rf_3Tdiff_1talpa_spe_v1p14.ckt
│  │  │     ├─ ms011_ms013s_io33_rf_TM2_res_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_rf_diff_ind_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_rf_interconnect_TM2_3um_ALPA_struct_1.txt
│  │  │     ├─ ms011_ms013s_io33_rf_interconnect_TM2_3um_ALPA_struct_2.txt
│  │  │     ├─ ms011_ms013s_io33_rf_mim_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_rf_mom_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_rf_mos_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_rf_readme_v1p14_spe.txt
│  │  │     ├─ ms011_ms013s_io33_rf_res_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_rf_spir_ind_spe_v1p14.ckt
│  │  │     ├─ ms011_ms013s_io33_rf_v1p14_spe.lib
│  │  │     ├─ ms011_ms013s_io33_rf_var_v1p14_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_v1p24_bjt_spe.mdl
│  │  │     ├─ ms011_ms013s_io33_v1p24_dio_spe.mdl
│  │  │     ├─ ms011_ms013s_io33_v1p24_interconnect_struct_1.txt
│  │  │     ├─ ms011_ms013s_io33_v1p24_interconnect_struct_2.txt
│  │  │     ├─ ms011_ms013s_io33_v1p24_mim_spe.mdl
│  │  │     ├─ ms011_ms013s_io33_v1p24_mis_spe.mdl
│  │  │     ├─ ms011_ms013s_io33_v1p24_readme_spe.txt
│  │  │     ├─ ms011_ms013s_io33_v1p24_res_spe.ckt
│  │  │     ├─ ms011_ms013s_io33_v1p24_res_spe.mdl
│  │  │     ├─ ms011_ms013s_io33_v1p24_spe.lib
│  │  │     ├─ ms011_ms013s_io33_v1p24_spe.mdl
│  │  │     ├─ res.va
│  │  │     ├─ res_rf.va
│  │  │     └─ simulator_version.txt
│  │  ├─ simResult
│  │  │  ├─ psf
│  │  │  │  ├─ logFile
│  │  │  │  ├─ logStatus
│  │  │  │  ├─ outac1.ac
│  │  │  │  ├─ outac1_spectre.out
│  │  │  │  ├─ outac2.ac
│  │  │  │  ├─ outac2_spectre.out
│  │  │  │  ├─ outac3.ac
│  │  │  │  ├─ outac3_spectre.out
│  │  │  │  ├─ outdc2.dc
│  │  │  │  ├─ outdc2_spectre.out
│  │  │  │  ├─ outtran1.tran.tran
│  │  │  │  ├─ outtran1_spectre.out
│  │  │  │  ├─ outtran2.tran.tran
│  │  │  │  └─ outtran2_spectre.out
│  │  │  ├─ test_comparator1_tran1.scs
│  │  │  ├─ test_comparator1_tran2.scs
│  │  │  ├─ test_comparator2_tran1.scs
│  │  │  ├─ test_comparator2_tran2.scs
│  │  │  ├─ test_diffamp1_ac1.scs
│  │  │  ├─ test_diffamp1_ac2.scs
│  │  │  ├─ test_diffamp1_ac3.scs
│  │  │  ├─ test_diffamp1_dc2.scs
│  │  │  ├─ test_diffamp1_tran1.scs
│  │  │  ├─ test_diffamp1_tran2.scs
│  │  │  ├─ test_ls1_tran1.scs
│  │  │  └─ test_st1_tran1.scs
│  │  └─ tb_template
│  │     ├─ Folded_Cascode
│  │     │  ├─ template_diffamp1_ac1.scs
│  │     │  ├─ template_diffamp1_ac2.scs
│  │     │  ├─ template_diffamp1_ac3.scs
│  │     │  ├─ template_diffamp1_dc1.scs
│  │     │  ├─ template_diffamp1_dc2.scs
│  │     │  ├─ template_diffamp1_op1.scs
│  │     │  ├─ template_diffamp1_tran1.scs
│  │     │  └─ template_diffamp1_tran2.scs
│  │     ├─ analog_comparator
│  │     │  ├─ template_comparator2_tran1.scs
│  │     │  └─ template_comparator2_tran2.scs
│  │     ├─ classAB
│  │     │  ├─ template_diffamp1_ac1.scs
│  │     │  ├─ template_diffamp1_ac2.scs
│  │     │  ├─ template_diffamp1_ac3.scs
│  │     │  ├─ template_diffamp1_dc1.scs
│  │     │  ├─ template_diffamp1_dc2.scs
│  │     │  ├─ template_diffamp1_op1.scs
│  │     │  ├─ template_diffamp1_tran1.scs
│  │     │  └─ template_diffamp1_tran2.scs
│  │     ├─ dynamic_comparator
│  │     │  ├─ template_comparator1_tran1.scs
│  │     │  └─ template_comparator1_tran2.scs
│  │     ├─ level_shifter
│  │     │  └─ template_ls1_tran1.scs
│  │     ├─ ls_higspeed
│  │     │  └─ template_ls1_tran1.scs
│  │     ├─ spectre
│  │     │  ├─ classab_old
│  │     │  │  ├─ template_diffamp1_ac1.scs
│  │     │  │  ├─ template_diffamp1_ac2.scs
│  │     │  │  ├─ template_diffamp1_ac3.scs
│  │     │  │  ├─ template_diffamp1_dc1.scs
│  │     │  │  ├─ template_diffamp1_dc2.scs
│  │     │  │  ├─ template_diffamp1_tran1.scs
│  │     │  │  └─ template_diffamp1_tran2.scs
│  │     │  ├─ template_diffamp1_ac1.scs
│  │     │  ├─ template_diffamp1_ac2.scs
│  │     │  ├─ template_diffamp1_ac3.scs
│  │     │  ├─ template_diffamp1_dc1.scs
│  │     │  ├─ template_diffamp1_dc2.scs
│  │     │  ├─ template_diffamp1_dc3.scs
│  │     │  ├─ template_diffamp1_tran1.scs
│  │     │  └─ template_diffamp1_tran2.scs
│  │     ├─ spice
│  │     │  ├─ template_diffamp1_ac1.sp
│  │     │  ├─ template_diffamp1_ac2.sp
│  │     │  ├─ template_diffamp1_ac3.sp
│  │     │  ├─ template_diffamp1_dc1.sp
│  │     │  ├─ template_diffamp1_dc2.sp
│  │     │  ├─ template_diffamp1_dc3.sp
│  │     │  ├─ template_diffamp1_op1.sp
│  │     │  ├─ template_diffamp1_tran1.sp
│  │     │  ├─ template_diffamp1_tran2.sp
│  │     │  ├─ template_diffamp2_ac1.sp
│  │     │  ├─ template_diffamp2_ac2.sp
│  │     │  ├─ template_diffamp2_ac3.sp
│  │     │  ├─ template_diffamp2_dc2.sp
│  │     │  ├─ template_diffamp2_tran1.sp
│  │     │  └─ template_diffamp2_tran2.sp
│  │     ├─ template_comparator1_tran1.scs
│  │     ├─ template_comparator1_tran2.scs
│  │     ├─ template_comparator2_tran1.scs
│  │     ├─ template_comparator2_tran2.scs
│  │     ├─ template_diffamp1_ac1.scs
│  │     ├─ template_diffamp1_ac2.scs
│  │     ├─ template_diffamp1_ac3.scs
│  │     ├─ template_diffamp1_dc1.scs
│  │     ├─ template_diffamp1_dc2.scs
│  │     ├─ template_diffamp1_op1.scs
│  │     ├─ template_diffamp1_tran1.scs
│  │     ├─ template_diffamp1_tran2.scs
│  │     ├─ template_ls1_tran1.scs
│  │     ├─ template_st1_tran1.scs
│  │     └─ two_stage_rc
│  │        ├─ template_diffamp1_ac1.scs
│  │        ├─ template_diffamp1_ac2.scs
│  │        ├─ template_diffamp1_ac3.scs
│  │        ├─ template_diffamp1_dc1.scs
│  │        ├─ template_diffamp1_dc2.scs
│  │        ├─ template_diffamp1_op1.scs
│  │        ├─ template_diffamp1_tran1.scs
│  │        ├─ template_diffamp1_tran2.scs
│  │        └─ two_stage
│  │           ├─ template_diffamp1_ac1.scs
│  │           ├─ template_diffamp1_ac2.scs
│  │           ├─ template_diffamp1_ac3.scs
│  │           ├─ template_diffamp1_dc1.scs
│  │           ├─ template_diffamp1_dc2.scs
│  │           ├─ template_diffamp1_op1.scs
│  │           ├─ template_diffamp1_tran1.scs
│  │           └─ template_diffamp1_tran2.scs
│  ├─ smic018
│  │  ├─ ckt_netlist
│  │  │  ├─ FoldedCascodeOpamp.scs
│  │  │  ├─ FoldedCascodeOpamp2.scs
│  │  │  ├─ classabOpamp (copy).scs
│  │  │  ├─ classabOpamp.scs
│  │  │  ├─ classabOpamp2.scs
│  │  │  ├─ comparator1.scs
│  │  │  ├─ dynamicComparator.scs
│  │  │  ├─ level_shifter.scs
│  │  │  ├─ level_shifter_high_speed.scs
│  │  │  ├─ schmitt_trigger.scs
│  │  │  ├─ spectre
│  │  │  │  ├─ FoldedCascodeOpamp.scs
│  │  │  │  └─ twoStageOpamp2.scs
│  │  │  ├─ spice
│  │  │  │  ├─ FoldedCascodeOpamp.cir
│  │  │  │  └─ twoStageOpamp2.cir
│  │  │  └─ twoStageOpamp2.scs
│  │  ├─ models
│  │  │  ├─ hspice
│  │  │  │  ├─ ms018_rf_v1p5.lib
│  │  │  │  ├─ ms018_rf_v1p5_diff_ind.ckt
│  │  │  │  ├─ ms018_rf_v1p5_mim.ckt
│  │  │  │  ├─ ms018_rf_v1p5_mos.ckt
│  │  │  │  ├─ ms018_rf_v1p5_readme.txt
│  │  │  │  ├─ ms018_rf_v1p5_res.ckt
│  │  │  │  ├─ ms018_rf_v1p5_spri_ind.ckt
│  │  │  │  ├─ ms018_rf_v1p5_var.ckt
│  │  │  │  ├─ ms018_v1p7.lib
│  │  │  │  ├─ ms018_v1p7.mdl
│  │  │  │  ├─ ms018_v1p7_bjt.mdl
│  │  │  │  ├─ ms018_v1p7_mim.mdl
│  │  │  │  ├─ ms018_v1p7_readme.txt
│  │  │  │  ├─ ms018_v1p7_res.ckt
│  │  │  │  ├─ ms018_v1p7_res.mdl
│  │  │  │  ├─ rf018_m6_res.lib
│  │  │  │  └─ rf018_m6_res.mdl
│  │  │  └─ spectre
│  │  │     ├─ #ms018_v1p7_spe_test.lib#
│  │  │     ├─ ms018_rf_v1p5_diff_ind_spe.ckt
│  │  │     ├─ ms018_rf_v1p5_mim_spe.ckt
│  │  │     ├─ ms018_rf_v1p5_mos_spe.ckt
│  │  │     ├─ ms018_rf_v1p5_readme_spe.txt
│  │  │     ├─ ms018_rf_v1p5_res_spe.ckt
│  │  │     ├─ ms018_rf_v1p5_spe.lib
│  │  │     ├─ ms018_rf_v1p5_spri_ind_spe.ckt
│  │  │     ├─ ms018_rf_v1p5_var_spe.ckt
│  │  │     ├─ ms018_v1p7_bjt_spe.mdl
│  │  │     ├─ ms018_v1p7_mim_spe.mdl
│  │  │     ├─ ms018_v1p7_readme_spe.txt
│  │  │     ├─ ms018_v1p7_res_spe.ckt
│  │  │     ├─ ms018_v1p7_res_spe.mdl
│  │  │     ├─ ms018_v1p7_spe.lib
│  │  │     ├─ ms018_v1p7_spe.mdl
│  │  │     ├─ ms018_v1p7_spe_test.lib
│  │  │     ├─ ms018_v1p7_spe_test.lib~
│  │  │     ├─ ms018_v1p7_spe_test.mdl
│  │  │     ├─ res.def
│  │  │     ├─ res_rf.def
│  │  │     ├─ rf018_m6_res_spe.lib
│  │  │     └─ rf018_m6_res_spe.mdl
│  │  ├─ simResult
│  │  │  ├─ psf
│  │  │  │  ├─ logFile
│  │  │  │  ├─ logStatus
│  │  │  │  ├─ outac1.ac
│  │  │  │  ├─ outac1_spectre.out
│  │  │  │  ├─ outac2.ac
│  │  │  │  ├─ outac2_spectre.out
│  │  │  │  ├─ outac3.ac
│  │  │  │  ├─ outac3_spectre.out
│  │  │  │  ├─ outdc2.dc
│  │  │  │  ├─ outdc2_spectre.out
│  │  │  │  ├─ outtran1.tran.tran
│  │  │  │  ├─ outtran1_spectre.out
│  │  │  │  ├─ outtran2.tran.tran
│  │  │  │  └─ outtran2_spectre.out
│  │  │  ├─ test_diffamp1_ac1.scs
│  │  │  ├─ test_diffamp1_ac2.scs
│  │  │  ├─ test_diffamp1_ac3.scs
│  │  │  ├─ test_diffamp1_dc2.scs
│  │  │  ├─ test_diffamp1_tran1.scs
│  │  │  └─ test_diffamp1_tran2.scs
│  │  └─ tb_template
│  │     ├─ Folded_Cascode
│  │     │  ├─ template_diffamp1_ac1.scs
│  │     │  ├─ template_diffamp1_ac2.scs
│  │     │  ├─ template_diffamp1_ac3.scs
│  │     │  ├─ template_diffamp1_dc1.scs
│  │     │  ├─ template_diffamp1_dc2.scs
│  │     │  ├─ template_diffamp1_op1.scs
│  │     │  ├─ template_diffamp1_tran1.scs
│  │     │  └─ template_diffamp1_tran2.scs
│  │     ├─ classAB
│  │     │  ├─ class_ab
│  │     │  │  ├─ template_diffamp1_ac1.scs
│  │     │  │  ├─ template_diffamp1_ac2.scs
│  │     │  │  ├─ template_diffamp1_ac3.scs
│  │     │  │  ├─ template_diffamp1_dc1.scs
│  │     │  │  ├─ template_diffamp1_dc2.scs
│  │     │  │  ├─ template_diffamp1_op1.scs
│  │     │  │  ├─ template_diffamp1_tran1.scs
│  │     │  │  └─ template_diffamp1_tran2.scs
│  │     │  ├─ template_diffamp1_ac1.scs
│  │     │  ├─ template_diffamp1_ac2.scs
│  │     │  ├─ template_diffamp1_ac3.scs
│  │     │  ├─ template_diffamp1_dc1.scs
│  │     │  ├─ template_diffamp1_dc2.scs
│  │     │  ├─ template_diffamp1_op1.scs
│  │     │  ├─ template_diffamp1_tran1.scs
│  │     │  └─ template_diffamp1_tran2.scs
│  │     ├─ high_speed_level_shifter
│  │     │  └─ template_ls1_tran1.scs
│  │     ├─ spectre
│  │     │  ├─ classab_old
│  │     │  │  ├─ template_diffamp1_ac1.scs
│  │     │  │  ├─ template_diffamp1_ac2.scs
│  │     │  │  ├─ template_diffamp1_ac3.scs
│  │     │  │  ├─ template_diffamp1_dc1.scs
│  │     │  │  ├─ template_diffamp1_dc2.scs
│  │     │  │  ├─ template_diffamp1_tran1.scs
│  │     │  │  └─ template_diffamp1_tran2.scs
│  │     │  ├─ template_diffamp1_ac1.scs
│  │     │  ├─ template_diffamp1_ac2.scs
│  │     │  ├─ template_diffamp1_ac3.scs
│  │     │  ├─ template_diffamp1_dc1.scs
│  │     │  ├─ template_diffamp1_dc2.scs
│  │     │  ├─ template_diffamp1_dc3.scs
│  │     │  ├─ template_diffamp1_tran1.scs
│  │     │  └─ template_diffamp1_tran2.scs
│  │     ├─ spice
│  │     │  ├─ template_diffamp1_ac1.sp
│  │     │  ├─ template_diffamp1_ac2.sp
│  │     │  ├─ template_diffamp1_ac3.sp
│  │     │  ├─ template_diffamp1_dc1.sp
│  │     │  ├─ template_diffamp1_dc2.sp
│  │     │  ├─ template_diffamp1_dc3.sp
│  │     │  ├─ template_diffamp1_op1.sp
│  │     │  ├─ template_diffamp1_tran1.sp
│  │     │  ├─ template_diffamp1_tran2.sp
│  │     │  ├─ template_diffamp2_ac1.sp
│  │     │  ├─ template_diffamp2_ac2.sp
│  │     │  ├─ template_diffamp2_ac3.sp
│  │     │  ├─ template_diffamp2_dc2.sp
│  │     │  ├─ template_diffamp2_tran1.sp
│  │     │  └─ template_diffamp2_tran2.sp
│  │     ├─ template_comparator1_tran1.scs
│  │     ├─ template_comparator1_tran2.scs
│  │     ├─ template_comparator2_tran1.scs
│  │     ├─ template_comparator2_tran2.scs
│  │     ├─ template_diffamp1_ac1.scs
│  │     ├─ template_diffamp1_ac2.scs
│  │     ├─ template_diffamp1_ac3.scs
│  │     ├─ template_diffamp1_dc1.scs
│  │     ├─ template_diffamp1_dc2.scs
│  │     ├─ template_diffamp1_op1.scs
│  │     ├─ template_diffamp1_tran1.scs
│  │     ├─ template_diffamp1_tran2.scs
│  │     ├─ template_ls1_tran1.scs
│  │     ├─ template_st1_tran1.scs
│  │     └─ two_stage_rc
│  │        ├─ template_diffamp1_ac1.scs
│  │        ├─ template_diffamp1_ac2.scs
│  │        ├─ template_diffamp1_ac3.scs
│  │        ├─ template_diffamp1_dc1.scs
│  │        ├─ template_diffamp1_dc2.scs
│  │        ├─ template_diffamp1_op1.scs
│  │        ├─ template_diffamp1_tran1.scs
│  │        └─ template_diffamp1_tran2.scs
│  └─ smic40
│     ├─ ckt_netlist
│     │  ├─ FoldedCascodeOpamp.scs
│     │  ├─ FoldedCascodeOpamp2.scs
│     │  ├─ classabOpamp (copy).scs
│     │  ├─ classabOpamp.scs
│     │  ├─ classabOpamp2.scs
│     │  ├─ comparator1.scs
│     │  ├─ dynamicComparator.scs
│     │  ├─ level_shifter.scs
│     │  ├─ level_shifter_high_speed.scs
│     │  ├─ schmitt_trigger.scs
│     │  ├─ spectre
│     │  │  ├─ FoldedCascodeOpamp.scs
│     │  │  └─ twoStageOpamp2.scs
│     │  ├─ spice
│     │  │  ├─ FoldedCascodeOpamp.cir
│     │  │  └─ twoStageOpamp2.cir
│     │  └─ twoStageOpamp2.scs
│     ├─ models
│     │  ├─ simulator_version.txt
│     │  └─ spectre
│     │     ├─ bjt
│     │     │  ├─ npn11a100ll_sba_spe.mdl
│     │     │  ├─ npn11a100ll_spe.mdl
│     │     │  ├─ npn11a25ll_sba_spe.mdl
│     │     │  ├─ npn11a25ll_spe.mdl
│     │     │  ├─ npn11a4ll_sba_spe.mdl
│     │     │  ├─ npn11a4ll_spe.mdl
│     │     │  ├─ npn25a100ll_sba_spe.mdl
│     │     │  ├─ npn25a100ll_spe.mdl
│     │     │  ├─ npn25a25ll_sba_spe.mdl
│     │     │  ├─ npn25a25ll_spe.mdl
│     │     │  ├─ npn25a4ll_sba_spe.mdl
│     │     │  ├─ npn25a4ll_spe.mdl
│     │     │  ├─ pnp11a100ll_sba_spe.mdl
│     │     │  ├─ pnp11a100ll_spe.mdl
│     │     │  ├─ pnp11a25ll_sba_spe.mdl
│     │     │  ├─ pnp11a25ll_spe.mdl
│     │     │  ├─ pnp11a4ll_sba_spe.mdl
│     │     │  ├─ pnp11a4ll_spe.mdl
│     │     │  ├─ pnp25a100ll_sba_spe.mdl
│     │     │  ├─ pnp25a100ll_spe.mdl
│     │     │  ├─ pnp25a25ll_sba_spe.mdl
│     │     │  ├─ pnp25a25ll_spe.mdl
│     │     │  ├─ pnp25a4ll_sba_spe.mdl
│     │     │  └─ pnp25a4ll_spe.mdl
│     │     ├─ gc.va
│     │     ├─ l0040ll_lpe_v1p4_1r_n11ll_spe.mdl
│     │     ├─ l0040ll_lpe_v1p4_1r_n25ll_spe.mdl
│     │     ├─ l0040ll_lpe_v1p4_1r_nhvt11ll_spe.mdl
│     │     ├─ l0040ll_lpe_v1p4_1r_nlvt11ll_spe.mdl
│     │     ├─ l0040ll_lpe_v1p4_1r_nod33ll_spe.mdl
│     │     ├─ l0040ll_lpe_v1p4_1r_nud18ll_spe.mdl
│     │     ├─ l0040ll_lpe_v1p4_1r_p11ll_spe.mdl
│     │     ├─ l0040ll_lpe_v1p4_1r_p25ll_spe.mdl
│     │     ├─ l0040ll_lpe_v1p4_1r_phvt11ll_spe.mdl
│     │     ├─ l0040ll_lpe_v1p4_1r_plvt11ll_spe.mdl
│     │     ├─ l0040ll_lpe_v1p4_1r_pod33ll_spe.mdl
│     │     ├─ l0040ll_lpe_v1p4_1r_pud18ll_spe.mdl
│     │     ├─ l0040ll_v1p4_1r_dio_spe.mdl
│     │     ├─ l0040ll_v1p4_1r_ldmos_spe.ckt
│     │     ├─ l0040ll_v1p4_1r_mom_spe.ckt
│     │     ├─ l0040ll_v1p4_1r_readme_spe.txt
│     │     ├─ l0040ll_v1p4_1r_res_spe.ckt
│     │     ├─ l0040ll_v1p4_1r_spe.lib
│     │     ├─ l0040ll_v1p4_1r_spe.mdl
│     │     ├─ l0040ll_v1p4_1r_var_spe.ckt
│     │     └─ res.va
│     ├─ simResult
│     │  ├─ psf
│     │  │  ├─ logFile
│     │  │  ├─ logStatus
│     │  │  ├─ outac1.ac
│     │  │  ├─ outac1_spectre.out
│     │  │  ├─ outac2.ac
│     │  │  ├─ outac2_spectre.out
│     │  │  ├─ outac3.ac
│     │  │  ├─ outac3_spectre.out
│     │  │  ├─ outdc2.dc
│     │  │  ├─ outdc2_spectre.out
│     │  │  ├─ outtran1.tran.tran
│     │  │  ├─ outtran1_spectre.out
│     │  │  ├─ outtran2.tran.tran
│     │  │  └─ outtran2_spectre.out
│     │  ├─ test_diffamp1_ac1.scs
│     │  ├─ test_diffamp1_ac2.scs
│     │  ├─ test_diffamp1_ac3.scs
│     │  ├─ test_diffamp1_dc2.scs
│     │  ├─ test_diffamp1_tran1.scs
│     │  └─ test_diffamp1_tran2.scs
│     └─ tb_template
│        ├─ Folded_Cascode
│        │  ├─ template_diffamp1_ac1.scs
│        │  ├─ template_diffamp1_ac2.scs
│        │  ├─ template_diffamp1_ac3.scs
│        │  ├─ template_diffamp1_dc1.scs
│        │  ├─ template_diffamp1_dc2.scs
│        │  ├─ template_diffamp1_op1.scs
│        │  ├─ template_diffamp1_tran1.scs
│        │  └─ template_diffamp1_tran2.scs
│        ├─ classAB
│        │  ├─ class_ab
│        │  │  ├─ template_diffamp1_ac1.scs
│        │  │  ├─ template_diffamp1_ac2.scs
│        │  │  ├─ template_diffamp1_ac3.scs
│        │  │  ├─ template_diffamp1_dc1.scs
│        │  │  ├─ template_diffamp1_dc2.scs
│        │  │  ├─ template_diffamp1_op1.scs
│        │  │  ├─ template_diffamp1_tran1.scs
│        │  │  └─ template_diffamp1_tran2.scs
│        │  ├─ template_diffamp1_ac1.scs
│        │  ├─ template_diffamp1_ac2.scs
│        │  ├─ template_diffamp1_ac3.scs
│        │  ├─ template_diffamp1_dc1.scs
│        │  ├─ template_diffamp1_dc2.scs
│        │  ├─ template_diffamp1_op1.scs
│        │  ├─ template_diffamp1_tran1.scs
│        │  └─ template_diffamp1_tran2.scs
│        ├─ high_speed_level_shifter
│        │  └─ template_ls1_tran1.scs
│        ├─ spectre
│        │  ├─ classab_old
│        │  │  ├─ template_diffamp1_ac1.scs
│        │  │  ├─ template_diffamp1_ac2.scs
│        │  │  ├─ template_diffamp1_ac3.scs
│        │  │  ├─ template_diffamp1_dc1.scs
│        │  │  ├─ template_diffamp1_dc2.scs
│        │  │  ├─ template_diffamp1_tran1.scs
│        │  │  └─ template_diffamp1_tran2.scs
│        │  ├─ template_diffamp1_ac1.scs
│        │  ├─ template_diffamp1_ac2.scs
│        │  ├─ template_diffamp1_ac3.scs
│        │  ├─ template_diffamp1_dc1.scs
│        │  ├─ template_diffamp1_dc2.scs
│        │  ├─ template_diffamp1_dc3.scs
│        │  ├─ template_diffamp1_tran1.scs
│        │  └─ template_diffamp1_tran2.scs
│        ├─ spice
│        │  ├─ template_diffamp1_ac1.sp
│        │  ├─ template_diffamp1_ac2.sp
│        │  ├─ template_diffamp1_ac3.sp
│        │  ├─ template_diffamp1_dc1.sp
│        │  ├─ template_diffamp1_dc2.sp
│        │  ├─ template_diffamp1_dc3.sp
│        │  ├─ template_diffamp1_op1.sp
│        │  ├─ template_diffamp1_tran1.sp
│        │  ├─ template_diffamp1_tran2.sp
│        │  ├─ template_diffamp2_ac1.sp
│        │  ├─ template_diffamp2_ac2.sp
│        │  ├─ template_diffamp2_ac3.sp
│        │  ├─ template_diffamp2_dc2.sp
│        │  ├─ template_diffamp2_tran1.sp
│        │  └─ template_diffamp2_tran2.sp
│        ├─ template_comparator1_tran1.scs
│        ├─ template_comparator1_tran2.scs
│        ├─ template_comparator2_tran1.scs
│        ├─ template_comparator2_tran2.scs
│        ├─ template_diffamp1_ac1.scs
│        ├─ template_diffamp1_ac2.scs
│        ├─ template_diffamp1_ac3.scs
│        ├─ template_diffamp1_dc1.scs
│        ├─ template_diffamp1_dc2.scs
│        ├─ template_diffamp1_op1.scs
│        ├─ template_diffamp1_tran1.scs
│        ├─ template_diffamp1_tran2.scs
│        ├─ template_ls1_tran1.scs
│        ├─ template_st1_tran1.scs
│        └─ two_stage_rc
│           ├─ template_diffamp1_ac1.scs
│           ├─ template_diffamp1_ac2.scs
│           ├─ template_diffamp1_ac3.scs
│           ├─ template_diffamp1_dc1.scs
│           ├─ template_diffamp1_dc2.scs
│           ├─ template_diffamp1_op1.scs
│           ├─ template_diffamp1_tran1.scs
│           └─ template_diffamp1_tran2.scs
├─ setup.cfg
├─ setup.py
├─ test.py
├─ tests
│  ├─ README.md
│  ├─ __pycache__
│  │  └─ test_1.cpython-311-pytest-7.4.0.pyc
│  └─ test_1.py
└─ tools
   └─ README.md

```