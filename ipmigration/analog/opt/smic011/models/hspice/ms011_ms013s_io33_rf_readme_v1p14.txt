***0.11um Mixed Signal 1P8M with MIM Salicide 1.2V/3.3V Process***
*** For HSPICE only ***

1. Files:

      ms011_ms013s_io33_rf_readme_v1p14.txt     		.... This file!
      ms011_ms013s_io33_rf_v1p14.lib            		.... Corner values for RF mos, Resistors, MIM, MOM, Varactors and Inductors
      ms011_ms013s_io33_rf_mos_v1p14.ckt        		.... Subcircuit model of RF MOS
      ms011_ms013s_io33_rf_spir_ind_v1p14.ckt        	.... Subcircuit model of spiral inductor
      ms011_ms013s_io33_rf_diff_ind_v1p14.ckt           	.... Subcircuit model of differential inductor
      ms011_ms013s_io33_rf_3T_diff_ind_v1p14.ckt        	.... Subcircuit model of 3-terminal differential inductor formed from TM2 or ALPA
      ms011_ms013s_io33_rf_3Tdiff_1talpa_v1p14.ckt        .... Subcircuit model of 3-terminal differential inductor
      ms011_ms013s_io33_rf_3Tdiff_1talpa_psub_v1p14.ckt        .... Subcircuit model of 3-terminal differential inductor with psub
      ms011_ms013s_io33_ind_rf_pgs_psub_n_v1p14.ckt        	.... Subcircuit model of width scalable spiral inductor with pgs and psub
      ms011_ms013s_io33_ind_rf_pgs_n_v1p14.ckt        		.... Subcircuit model of width scalable spiral inductor with pgs 
      ms011_ms013s_io33_diff_ind_3t_rf_pgs_psub_n_v1p14.ckt     .... Subcircuit model of width scalable 3-terminal differential inductor with pgs and psub
      ms011_ms013s_io33_diff_ind_3t_rf_pgs_n_v1p14.ckt     	.... Subcircuit model of width scalable 3-terminal differential inductor with pgs 
      ms011_ms013s_io33_diff_ind_rf_pgs_psub_n_v1p14.ckt        .... Subcircuit model of width scalable differential inductor with pgs and psub
      ms011_ms013s_io33_diff_ind_rf_pgs_n_v1p14.ckt        	.... Subcircuit model of width scalable differential inductor with pgs 

      ms011_ms013s_io33_rf_mim_v1p14.ckt        		.... Subcircuit model of MIM 
      ms011_ms013s_io33_rf_mom_v1p14.ckt        		.... Subcircuit model of MOM 
      ms011_ms013s_io33_rf_var_v1p14.ckt        		.... Subcircuit model of varactor
      ms011_ms013s_io33_rf_res_v1p14.ckt        		.... Subcircuit model of SAB resistor
      ms011_ms013s_io33_rf_TM2_res_v1p14.ckt 		.... model card for TM2 resistor and ALPA resistor
      ms011_ms013s_io33_rf_interconnect_TM2_3um_ALPA_struct_1	.... Thick(TM2=3um) with ALPA layer interconnect tables for structure-1 (Parallel lines above a bottom plate)
      ms011_ms013s_io33_rf_interconnect_TM2_3um_ALPA_struct_2	.... Thick(TM2=3um) with ALPA layer interconnect tables for structure-2 (Parallel lines between two plates)
      ms011_ms013s_io33_rf_layer.map                   	.... GDSII layers definition file
      N12_W2d5Ld13N16.gds				.... GDSII file for 1.2V NMOS W/L/N=2.5/0.13/16
      N12_W2d5Ld13N16_WOGR.gds				.... GDSII file for 1.2V NMOS W/L/N=2.5/0.13/16 without guard ring
      DNW12_W2d5Ld13N16.gds				.... GDSII file for 1.2V Deep Nwell NMOS W/L/N=2.5/0.13/16
      DNW12_W2d5Ld13N16_WOGR.gds			.... GDSII file for 1.2V Deep Nwell NMOS W/L/N=2.5/0.13/16 without guard ring
      P12_W2d5Ld13N16.gds				.... GDSII file for 1.2V PMOS W/L/N=2.5/0.13/16
      P12_W2d5Ld13N16_WOGR.gds				.... GDSII file for 1.2V PMOS W/L/N=2.5/0.13/16 without guard ring
      N33_W2d5Ld35N16.gds                 		.... GDSII file for 3.3V NMOS W/L/N=2.5/0.35/16
      N33_W2d5Ld35N16_WOGR.gds                 		.... GDSII file for 3.3V NMOS W/L/N=2.5/0.35/16 without guard ring
      DNW33_W2d5Ld35N16.gds                  		.... GDSII file for 3.3V Deep Nwell NMOS W/L/N=2.5/0.35/16
      DNW33_W2d5Ld35N16_WOGR.gds               		.... GDSII file for 3.3V Deep Nwell NMOS W/L/N=2.5/0.35/16 without guard ring
      P33_W2d5Ld3N16.gds                 		.... GDSII file for 3.3V PMOS W/L/N=2.5/0.3/16
      P33_W2d5Ld3N16.gds                 		.... GDSII file for 3.3V PMOS W/L/N=2.5/0.3/16 without guard ring
      3T_DIFF_IND_ALPA_W8S4R30N5d5.gds			.... GDSII file for 3T differential Inductor formed from ALPA W/S/R/N=8/4/30/5.5
      VAR12_MOS_W2Ld5N4.gds				.... GDSII file for 1.2V MOS Varactor W/L/N=2/0.5/4
      VAR33_MOS_W2Ld5N4.gds				.... GDSII file for 3.3V MOS Varactor W/L/N=2/0.5/4
      MOM17_L18N20.gds					.... GDSII file for M1~M7 MOM with L=18um N=20 in NWELL with guard ring
      MOM17_L18N20_3T.gds				.... GDSII file for 3-terminal M1~M7 MOM with L=18um N=20 in NWELL with guard ring
      MOM17_L18N20_PWELL.gds				.... GDSII file for M1~M7 MOM with L=18um N=20 in PWELL with guard ring
      MOM17_L18N20_PWELL_3T.gds				.... GDSII file for 3-termianl M1~M7 MOM with L=18um N=20 in PWELL with guard ring
      MOM17_L18N20_PWELL_WOGR.gds			.... GDSII file for M1~M7 MOM with L=18um N=20 in PWELL without guard ring
      MOM17_L18N20_WOGR.gds				.... GDSII file for M1~M7 MOM with L=18um N=20 in NWELL without guard ring
      RNPOSAB_W1L5.gds					.... GDSII file for Non-silicide N+ Poly Resistor W/L=1/5 with guard ring
      RNPOSAB_W1L5_WOGR.gds				.... GDSII file for Non-silicide N+ Poly Resistor W/L=1/5 without guard ring
      RNPOSAB_W1L5_3T.gds				.... GDSII file for 3-terminal Non-silicide N+ Poly Resistor W/L=1/5 with guard ring
      RPPOSAB_W1L5.gds					.... GDSII file for Non-silicide P+ Poly Resistor W/L=1/5 with guard ring
      RPPOSAB_W1L5_WOGR.gds				.... GDSII file for Non-silicide P+ Poly Resistor W/L=1/5 without guard ring
      RPPOSAB_W1L5_3T.gds				.... GDSII file for 3-terminal Non-silicide P+ Poly Resistor W/L=1/5 with guard ring
      rhrpo_rf_w2l10.gds				.... GDSII file for Non-silicide HRP Resistor
      rhrpo_rf_3t_w2l10.gds				.... GDSII file for Non-silicide HRP Resistor (3-terminal)

      SUB_PP_100.gds                          	  	.... GDSII file for P+AA within floating P+ guard ring in Pwell for spacing=100um substrate coupling noise
      SUB_PP_FGR_100.gds                   		.... GDSII file for P+AA within floating P+ guard ring in Pwell for spacing=100um substrate coupling noise
      SUB_PDNWP_100.gds                    		.... GDSII file for P+AA in floating Deep Nwell to P+AA in Pwell with spacing=100um substrate coupling noise
      SUB_NNMOSDNW_100.gds           			.... GDSII file for NMOS in floating Deep Nwell to NMOS in floating Deep Nwell with spacing=100um substrate coupling noise
      SUB_NFGRP_100.gds                    		.... GDSII file for N+AA within P+ guard ring to P+AA in Pwell with spacing=100um substrate coupling noise
      streff.exe					.... Effective stress calculation tool
 
      mim1_rf_10x10.gds                        		.... GDSII file for 1fF/um2 MIM with Area=10*10
      mim1_rf_10x10_utm.gds                             .... GDSII file for 1fF/um2 MIM in UTM process, Area=10*10
      mim1_shield_rf_10x10.gds                       	.... GDSII file for 1fF/um2 MIM with metal shielding layer Area=10*10
      mim1_shield_rf_10x10_utm.gds                   	.... GDSII file for 1fF/um2 MIM with metal shielding layer in UTM process Area=10*10
      mim15_rf_10x10.gds                       		.... GDSII file for 1.5fF/um2 MIM with Area=10*10
      mim15_shield_rf_10x10.gds                      	.... GDSII file for 1.5fF/um2 MIM with metal shielding layer Area=10*10
      mim2_rf_2mask_10x10.gds                        		.... GDSII file for 2fF/um2 MIM with Area=10*10
      mim2_shield_rf_2mask_10x10.gds                     	.... GDSII file for 2fF/um2 MIM with shielding layer, Area=10*10
      mim3_rf_10x10.gds                                       .... GDSII file for 3fF/um2 MIM with Area=10*10
      MIM15_shield_rf_3t.gds					.... GDSII file for 3t 1.5fF/um2 MIM with shielding layer
      MIM15_rf_3t_Nwell.gds						.... GDSII file for  3t 1.5fF/um2 MIM on Nwell
      MIM15_rf_3t_Pwell.gds						.... GDSII file for  3t 1.5fF/um2 MIM on pwell
      mim1_shield_rf_3t_10x10.gds                       	.... GDSII file for 1fF/um2 MIM with metal shielding layer Area=10*10
      mim2_shield_rf_2mask_3t_10x10.gds                     	.... GDSII file for 2fF/um2 MIM with shielding layer, Area=10*10

      3T_diff_1talpa_n3r50_psub.gds				.... GDSII file for 3t ALPA differential inductor with psub, turns=3, radius=50u
      2T_diff_ind_rf_n2d5r60.gds					.... GDSII file for 2t differential inductor with half turns, turns=2.5, radius=60u
      2T_diff_ind_rf_n3r60.gds					.... GDSII file for 2t differential inductor with integer turns, turns=3, radius=60u
      2T_diff_ind_rf_pgs_n2d5r60.gds				.... GDSII file for 2t differential inductor with half turns and Pattern Ground Shielding
      2T_diff_ind_rf_pgs_n3r60.gds					.... GDSII file for 2t differential inductor with integer turns and Pattern Ground Shielding
      2T_diff_ind_rf_pgs_psub_n2d5r60.gds				.... GDSII file for 2t differential inductor with half turns and Pattern Ground Shielding and psub terminal
      2T_diff_ind_rf_pgs_psub_n3r60.gds				.... GDSII file for 2t differential inductor with integer turns and Pattern Ground Shielding and psub terminal
      2T_diff_ind_rf_psub_n2d5r60.gds				.... GDSII file for 2t differential inductor with half turns and psub terminal
      2T_diff_ind_rf_psub_n3r60.gds				.... GDSII file for 2t differential inductor with integer turns and psub terminal
      3T_diff_1talpa_n3r50.gds					.... GDSII file for 3t ALPA differential inductor with integer turns and psub terminal
      3T_DIFF_IND_ALPA_W8S4R30N5d5_psub.gds			.... GDSII file for 3t ALPA differential inductor with half turns and psub terminal
      3T_diff_ind_rf_n2d5r60.gds					.... GDSII file for 3t differential inductor with half turns
      3T_diff_ind_rf_n3r60.gds					.... GDSII file for 3t differential inductor with integer turns
      3T_diff_ind_rf_pgs_n2d5r60.gds				.... GDSII file for 3t differential inductor with half turns and Pattern Ground Shielding
      3T_diff_ind_rf_pgs_n3r60.gds					.... GDSII file for 3t differential inductor with integer turns and Pattern Ground Shielding
      3T_diff_ind_rf_pgs_psub_n2d5r60.gds				.... GDSII file for 3t differential inductor with half turns and Pattern Ground Shielding and psub terminal
      3T_diff_ind_rf_pgs_psub_n3r60.gds				.... GDSII file for 3t differential inductor with integer turns and Pattern Ground Shielding and psub terminal
      3T_diff_ind_rf_psub_n2d5r60.gds				.... GDSII file for 3t differential inductor with half turns and psub terminal
      3T_diff_ind_rf_psub_n3r60.gds				.... GDSII file for 3t differential inductor with integer turns and psub terminal
      ind_rf_n2d5r60.gds						.... GDSII file for single ended spiral inductor with half turns
      ind_rf_n3r60.gds						.... GDSII file for single ended spiral inductor with integer turns
      ind_rf_pgs_n2d5r60.gds					.... GDSII file for single ended spiral inductor with half turns and Pattern Ground Shielding
      ind_rf_pgs_n3r60.gds						.... GDSII file for single ended spiral inductor with integer turns and Pattern Ground Shielding
      ind_rf_pgs_psub_n2d5r60.gds					.... GDSII file for single ended spiral inductor with half turns and Pattern Ground Shielding and psub terminal
      ind_rf_pgs_psub_n3r60.gds					.... GDSII file for single ended spiral inductor with integer turns and Pattern Ground Shielding and psub terminal
      ind_rf_psub_n2d5r60.gds					.... GDSII file for single ended spiral inductor with half turns and psub terminal
      ind_rf_psub_n3r60.gds						.... GDSII file for single ended spiral inductor with integer turns and psub terminal
      ind_rf_pgs_psub_n.gds					.... GDSII file for single ended spiral inductor(width & radius scalable) with Pattern Ground Shielding and psub terminal
      ind_rf_pgs_n.gds						.... GDSII file for single ended spiral inductor(width & radius scalable) with Pattern Ground Shielding	
      diff_ind_rf_pgs_psub_n.gds				.... GDSII file for 2t differential inductor(width & radius scalable) with Pattern Ground Shielding and psub terminal
      diff_ind_rf_pgs_n.gds					.... GDSII file for 2t differential inductor(width & radius scalable) with Pattern Ground Shielding
      diff_ind_3t_rf_pgs_psub_n.gds				.... GDSII file for 3t differential inductor(width & radius scalable) with Pattern Ground Shielding and psub terminal
      diff_ind_3t_rf_pgs_n.gds					.... GDSII file for 3t differential inductor(width & radius scalable) with Pattern Ground Shielding



2. How to use SMIC SPICE models in HSPICE:

    ** Load model cards select corner
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' MOS_TT
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' MIM_TT
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' MOM_TT
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' RES_TT
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' TM2_RES_TT
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' VAR_TT
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' SPIRIND_TT
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' DIFFIND_TT
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' 3TDIFFIND_TT
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' ind_rf_pgs_psub_n_tt
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' ind_rf_pgs_n_tt
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' diff_ind_3t_rf_pgs_psub_n_tt
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' diff_ind_3t_rf_pgs_n_tt
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' diff_ind_rf_pgs_psub_n_tt
    .lib 'ms011_ms013s_io33_rf_v1p14.lib' diff_ind_rf_pgs_n_tt

    ** Load monte carlo models
    .lib 'ms013_io33_rf_v1p14.lib' MOS_MC
    .lib 'ms013_io33_rf_v1p14.lib' MIM_MC
    .lib 'ms013_io33_rf_v1p14.lib' MOM_MC
    .lib 'ms013_io33_rf_v1p14.lib' RES_MC
    .lib 'ms013_io33_rf_v1p14.lib' TM2_RES_MC
    .lib 'ms013_io33_rf_v1p14.lib' VAR_MC
    .lib 'ms013_io33_rf_v1p14.lib' SPIRIND_MC
    .lib 'ms013_io33_rf_v1p14.lib' DIFFIND_MC
    .lib 'ms013_io33_rf_v1p14.lib' 3TDIFFIND_MC
    .lib 'ms013_io33_rf_v1p14.lib' ind_rf_pgs_psub_n_mc
    .lib 'ms013_io33_rf_v1p14.lib' ind_rf_pgs_n_mc
    .lib 'ms013_io33_rf_v1p14.lib' diff_ind_3t_rf_pgs_psub_n_mc
    .lib 'ms013_io33_rf_v1p14.lib' diff_ind_3t_rf_pgs_n_mc
    .lib 'ms013_io33_rf_v1p14.lib' diff_ind_rf_pgs_psub_n_mc
    .lib 'ms013_io33_rf_v1p14.lib' diff_ind_rf_pgs_n_mc

    ** Call the models
     XM 1 2 0 0 n12_ckt_rf lr=0.13u wr=2.5u nf=16 sar=3.1523e-6 sbr=3.1523e-6 mr=1 mismod=0
     X1 1 2 mim1_rf lr=10u wr=10u mismod_mim_rf=0 xm=8 
     X2 1 2 mom_ckt_rf bm=1 tm=7 lr=18u nf=20   
     X3 1 2 rpposab_ckt_rf l=40u w=2u mismod_res_rf=0
     X4 1 2 0 rpposab_ckt_rf_3t l=40u w=2u mismod_res_rf=0
     X5 1 2 0 rtm2_rf l=500u w=2u
     X6 1 2 ind_rf r=60u n=3.5
     X7 1 2 diff_ind_rf r=60u n=3
     X8 1 2 T1 diff_ind_3t_rf R=30u N=5.5
     X9 1 2 T1 diff_ind_3t_alpa_rf R=30u N=5.5
     X10 1 2 0 ind_rf_pgs_psub_n R=60u W=8u n=2
     X11 1 2 ind_rf_pgs_n R=60u W=8u n=2
     X12 1 2 T1 0 diff_ind_3t_rf_pgs_psub_n R=60u W=8u n=2
     X13 1 2 T1 diff_ind_3t_rf_pgs_n R=60u W=8u n=2 
     X14 1 2 0 diff_ind_rf_pgs_psub_n R=60u W=8u n=2 
     X15 1 2 diff_ind_rf_pgs_n R=60u W=8u n=2   
     
3. The Capability of Model
        a. MOS Model 
	
        *----------------------------------------------------------------------------------------------* 
        |              MOSFET type             |  name        | Lmin   | Wmin  | minimum finger number |
        |==============================================================================================| 
        |   1.2V NMOS(With GR or Without GR)   | n12_ckt_rf   | 0.13um | 1um   |         1             |
        *----------------------------------------------------------------------------------------------*
        |   1.2V DNW MOS(With GR or Without GR)| dnw12_ckt_rf | 0.13um | 1um   |         1             |
        *----------------------------------------------------------------------------------------------*
        |   1.2V PMOS(With GR or Without GR)   | p12_ckt_rf   | 0.13um | 1um   |         1             |
        *----------------------------------------------------------------------------------------------*
        |   3.3V NMOS(With GR or Without GR)   | n33_ckt_rf   | 0.35um | 1um   |         1             |
        *----------------------------------------------------------------------------------------------*
        |   3.3V DNW MOS(With GR or Without GR)| dnw33_ckt_rf | 0.35um | 1um   |         1             |
        *----------------------------------------------------------------------------------------------*
        |   3.3V PMOS (With GR or Without GR)  | p33_ckt_rf   | 0.30um | 1um   |         1             |
        *----------------------------------------------------------------------------------------------*
         temperature range:-40C~125C

        For the detail RF MOS model capacity please refer to the section 7.3.1 of main document 
  
	b. Resistor Model

	*-----------------------------------------------------------------------------------------------------------------*
        |             Resistor Type               |       name         |     Lmin    |    Wmin    | minimum finger number |
        |=================================================================================================================|
        |  N+ poly SAB(With GR or Without GR      | rnposab_ckt_rf     |      0.5um  |    0.5um   |           0.5         |
        |-----------------------------------------------------------------------------------------------------------------|
        |  p+ poly SAB(With GR or Without GR      | rpposab_ckt_rf     |      0.5um  |    0.5um   |           0.5         |
        |-----------------------------------------------------------------------------------------------------------------|
        |  HR poly                                | rhrpo_ckt_rf       |      2um    |    2um     |           1           |
        |-----------------------------------------------------------------------------------------------------------------|   
        |  3T N+ poly SAB(With GR or Without GR)  | rnposab_ckt_rf_3t  |      0.5um  |    0.5um   |           0.5         |
        |-----------------------------------------------------------------------------------------------------------------|
        |  3T p+ poly SAB(With GR or Without GR)  | rpposab_ckt_rf_3t  |      0.5um  |    0.5um   |           0.5         |
        |-----------------------------------------------------------------------------------------------------------------|
        |  3T HR poly                             | rhrpo_ckt_rf_3t    |      2um    |    2um     |           1           |
        |-----------------------------------------------------------------------------------------------------------------|   
        |  Metal 8(TM2)                           | rtm2_rf            |      10um   |    2um     |           -           |
        |-----------------------------------------------------------------------------------------------------------------|
        |  ALPA                                   | ralpa_rf           |      10um   |    2um     |           -           |
        *-----------------------------------------------------------------------------------------------------------------*
        temperature range : -40C~125C
      
        For the detail RF Resistor model capacity please refer to the section 7.11.1 of main document 
       
     c. MIM capacitor Model
       
        *---------------------------------------------------------------------------------------*  
        |         capacitor Type                            |     name            | minimum area| 
        |=======================================================================================| 
        |   1fF/um^2 MIM capacitor                          |  mim1_rf            |   3x3 um^2  | 
        |---------------------------------------------------------------------------------------|  
        |   1.5fF/um^2 MIM capacitor                        |  mim15_rf           |   3x3 um^2  | 
        |---------------------------------------------------------------------------------------|  
        |   2fF/um^2 Two-Mask MIM capacitor                 |  mim2_rf_2mask      |   2x2 um^2  | 
        |---------------------------------------------------------------------------------------|
        |   3fF/um^2 MIM capacitor                          |  mim3_rf            |   3x3 um^2  | 
        |---------------------------------------------------------------------------------------|  
        |   1fF/um^2 MIM capacitor(with shielding)          |  mim1_shield_rf     |   3x3 um^2  | 
        |---------------------------------------------------------------------------------------|  
        |   1.5fF/um^2 MIM capacitor(with shielding)        |  mim15_shield_rf    |   3x3 um^2  | 
        |---------------------------------------------------------------------------------------|  
        |   2fF/um^2 Two-Mask MIM capacitor(with shielding) |mim2_shield_rf_2mask |   2x2 um^2  | 
        *---------------------------------------------------------------------------------------*
        temperature range : -40C~125C

        For the detail MIM model capacity please refer to the section 7.9.1 of main document 

           
        d. MOM capacitor Model

        *-------------------------------------------------------------------------------------------------------*  
        |  capacitor Type     |  Bottom Layer  |  Top Layer  |      name      | minimum length | minimum finger |
        |=======================================================================================================| 
        |                     |        1       |     3~7     |  mom_ckt_rf    |     12um       |        4       |
        |                     |---------------------------------------------------------------------------------|   
        |                     |        2       |     4~7     |  mom_ckt_rf    |     12um       |        4       |
        |                     |---------------------------------------------------------------------------------|  
        |  MOM capacitor      |        3       |     5~7     |  mom_ckt_rf    |     12um       |        4       |
        |                     |---------------------------------------------------------------------------------|  
        |                     |        4       |     6~7     |  mom_ckt_rf    |     12um       |        4       |
        |                     |---------------------------------------------------------------------------------|  
        |                     |        5       |     7       |  mom_ckt_rf    |     12um       |        4       |
        |-------------------------------------------------------------------------------------------------------|  
        |                     |        1       |     3~7     |  mom_ckt_rf_3t |     12um       |        4       |
        |                     |---------------------------------------------------------------------------------|   
        |                     |        2       |     4~7     |  mom_ckt_rf_3t |     12um       |        4       |
        |                     |---------------------------------------------------------------------------------|  
        |  3-T MOM capacitor  |        3       |     5~7     |  mom_ckt_rf_3t |     12um       |        4       |
        |                     |---------------------------------------------------------------------------------|  
        |                     |        4       |     6~7     |  mom_ckt_rf_3t |     12um       |        4       |
        |                     |---------------------------------------------------------------------------------|  
        |                     |        5       |     7       |  mom_ckt_rf_3t |     12um       |        4       | 
        *-------------------------------------------------------------------------------------------------------*
        temperature range : -40C~125C

        For the detail MOM model capacity please refer to the section 7.10.1 of main document 
  
        e. N+poly/NW MOS varactor model
        
        *--------------------------------------------------------------------------------------------------------------------*
        |       Varactor Type        |     name        |      poly length    |      poly width     | minimum finger number   |
        |====================================================================================================================|
        |    1.2V NMOS in NWELL      |  pvar12_ckt_rf  |       0.5~1.5um     |        2~10um       |           1             |
        |--------------------------------------------------------------------------------------------------------------------|
        |    3.3v NMOS in NWELL      |  pvar33_ckt_rf  |       0.5~1.5um     |        2~10um       |           1             |
        *--------------------------------------------------------------------------------------------------------------------*
        temperature range:-40C~125C

        For the detail N+poly/NW MOS Varactor model capacity please refer to the section 7.8.1 of main document 

      f.Spiral Inductor Model
       
        *-------------------------------------------------------------------------------------------------------------------------*  
        |        Inductor Type      |          model name        |  turn number  |  Radius range  |    Spacing     |  Width       |
        |=========================================================================================================================|  
        |       spiral inductor     |         ind_rf_1d5         |       1.5     |     60-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------* 
        |       spiral inductor     |         ind_rf_2           |       2       |     60-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |       spiral inductor     |         ind_rf_2d5         |       2.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |       spiral inductor     |         ind_rf_3           |       3       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |       spiral inductor     |         ind_rf_3d5         |       3.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |       spiral inductor     |         ind_rf_4           |       4       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |       spiral inductor     |         ind_rf_4d5         |       4.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |       spiral inductor     |         ind_rf_5           |       5       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |       spiral inductor     |         ind_rf_5d5         |       5.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |       spiral inductor     |         ind_rf_6           |       6       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |       spiral inductor     |         ind_rf_6d5         |       6.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with psub |        ind_rf_psub_1d5     |       1.5     |     60-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------* 
        | spiral inductor with psub |        ind_rf_psub_2       |       2       |     60-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with psub |        ind_rf_psub_2d5     |       2.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with psub |        ind_rf_psub_3       |       3       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with psub |        ind_rf_psub_3d5     |       3.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with psub |        ind_rf_psub_4       |       4       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with psub |        ind_rf_psub_4d5     |       4.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with psub |        ind_rf_psub_5       |       5       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with psub |        ind_rf_psub_5d5     |       5.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with psub |        ind_rf_psub_6       |       6       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with psub |        ind_rf_psub_6d5     |       6.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with pgs  |        ind_rf_pgs_1d5      |       1.5     |     60-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------* 
        | spiral inductor with pgs  |        ind_rf_pgs_2        |       2       |     60-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with pgs  |        ind_rf_pgs_2d5      |       2.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with pgs  |        ind_rf_pgs_3        |       3       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with pgs  |        ind_rf_pgs_3d5      |       3.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with pgs  |        ind_rf_pgs_4        |       4       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with pgs  |        ind_rf_pgs_4d5      |       4.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with pgs  |        ind_rf_pgs_5        |       5       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with pgs  |        ind_rf_pgs_5d5      |       5.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with pgs  |        ind_rf_pgs_6        |       6       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        | spiral inductor with pgs  |        ind_rf_pgs_6d5      |       6.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |spiral ind with pgs & psub |   ind_rf_pgs_psub_1d5      |       1.5     |     60-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------* 
        |spiral ind with pgs & psub |   ind_rf_pgs_psub_2        |       2       |     60-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |spiral ind with pgs & psub |   ind_rf_pgs_psub_2d5      |       2.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |spiral ind with pgs & psub |   ind_rf_pgs_psub_3        |       3       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |spiral ind with pgs & psub |   ind_rf_pgs_psub_3d5      |       3.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |spiral ind with pgs & psub |   ind_rf_pgs_psub_4        |       4       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |spiral ind with pgs & psub |   ind_rf_pgs_psub_4d5      |       4.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |spiral ind with pgs & psub |   ind_rf_pgs_psub_5        |       5       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |spiral ind with pgs & psub |   ind_rf_pgs_psub_5d5      |       5.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |spiral ind with pgs & psub |   ind_rf_pgs_psub_6        |       6       |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
        |spiral ind with pgs & psub |   ind_rf_pgs_psub_6d5      |       6.5     |     30-150um   | fixed at 1.5um | fixed at 8um |                    
        *-------------------------------------------------------------------------------------------------------------------------*
	
	Width scalable Spiral Inductor Model
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*
       |  Turn, Radius & Width  |    T=1~3 step 0.5, W=5~13.5um,R=1.7071*W+16.378~120um             |     T=3.5~5.0 step 0.5, W=5~8um,R=1.7071*W+16.378~120um           |
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*   
       |        Model Name      |                                                    ind_rf_pgs_psub_n    		                                        	|
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*
       |        Model Name      |                                                    ind_rf_pgs_n    		                                        		|
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*                                  

        temperature range:-40C~125C

        For the detail Spiral Inductor model capacity please refer to the section 7.4.1 of main document 

       g.Differential Inductor Model
       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        |         Inductor Type              |       model name         |     turn range   |  Radius range |    Spacing     |  Width       |
        |==================================================================================================================================|  
        |    differential inductor           |       diff_ind_rf        | 2 to 7 step 0.5  |    30-120um   | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------* 
        | differential inductor with psub    |     diff_ind_rf_psub     | 2 to 7 step 0.5  |    30-120um   | fixed at 1.5um | fixed at 8um |         
        *----------------------------------------------------------------------------------------------------------------------------------* 
        | differential inductor with pgs     |     diff_ind_rf_pgs      | 2 to 7 step 0.5  |    30-120um   | fixed at 1.5um | fixed at 8um |         
        *----------------------------------------------------------------------------------------------------------------------------------* 
        |differential inductor with pgs& psub|   diff_ind_rf_pgs_psub   | 2 to 7 step 0.5  |    30-120um   | fixed at 1.5um | fixed at 8um |         
        *----------------------------------------------------------------------------------------------------------------------------------* 

	Width scalable differential Inductor Model
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*
       |  Turn, Radius & Width  |    T=1~3 step 0.5, W=5~13.5um,R=1.7071*W+16.378~120um             |     T=3.5~5.0 step 0.5, W=5~8um,R=1.7071*W+16.378~120um           |
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*   
       |        Model Name      |                                                    diff_ind_rf_pgs_psub_n    		                                                |
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*
       |        Model Name      |                                                    diff_ind_rf_pgs_n    		                                                |
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*                                  
        temperature range:-40C~125C

        For the detail Differential Inductor model capacity please refer to the section 7.5.1 of main document 
      
       h.3-Terminal Differential Inductor Model
       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        |         Inductor Type              |       model name         |     turn range    | Radius range |    Spacing     |  Width       |
        |==================================================================================================================================|  
        |  3T differential inductor          |      diff_ind_3t_rf      |       1.5         |     60um     | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------* 
        |  3T differential inductor          |      diff_ind_3t_rf      |       2           |   60-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        |  3T differential inductor          |      diff_ind_3t_rf      |2.5 to 6.5 step 0.5|   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------* 
        | 3T differential inductor with psub |  diff_ind_3t_rf_psub     |       1.5         |     60um     | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------* 
        | 3T differential inductor with psub |  diff_ind_3t_rf_psub     |       2           |   60-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        | 3T differential inductor with psub |  diff_ind_3t_rf_psub     |2.5 to 6.5 step 0.5|   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------* 
        | 3T differential inductor with pgs  |  diff_ind_3t_rf_pgs_t1d5 |       1.5         |     60um     | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------* 
        | 3T differential inductor with pgs  |  diff_ind_3t_rf_pgs_t2   |       2           |   60-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        | 3T differential inductor with pgs  |  diff_ind_3t_rf_pgs_t2d5 |       2.5         |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*
        | 3T differential inductor with pgs  |  diff_ind_3t_rf_pgs_t3   |       3           |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        | 3T differential inductor with pgs  |  diff_ind_3t_rf_pgs_t3d5 |       3.5         |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*
        | 3T differential inductor with pgs  |  diff_ind_3t_rf_pgs_t4   |       4           |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        | 3T differential inductor with pgs  |  diff_ind_3t_rf_pgs_t4d5 |       4.5         |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*
        | 3T differential inductor with pgs  |  diff_ind_3t_rf_pgs_t5   |       5           |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        | 3T differential inductor with pgs  |  diff_ind_3t_rf_pgs_t5d5 |       5.5         |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*
        | 3T differential inductor with pgs  |  diff_ind_3t_rf_pgs_t6   |       6           |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        | 3T differential inductor with pgs  |  diff_ind_3t_rf_pgs_t6d5 |       6.5         |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*
        | 3T diff inductor with pgs & psub |diff_ind_3t_rf_pgs_psub_t1d5|       1.5         |     60um     | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------* 
        | 3T diff inductor with pgs & psub |diff_ind_3t_rf_pgs_psub_t2  |       2           |   60-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        | 3T diff inductor with pgs & psub |diff_ind_3t_rf_pgs_psub_t2d5|       2.5         |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*
        | 3T diff inductor with pgs & psub |diff_ind_3t_rf_pgs_psub_t3  |       3           |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        | 3T diff inductor with pgs & psub |diff_ind_3t_rf_pgs_psub_t3d5|       3.5         |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*
        | 3T diff inductor with pgs & psub |diff_ind_3t_rf_pgs_psub_t4  |       4           |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        | 3T diff inductor with pgs & psub |diff_ind_3t_rf_pgs_psub_t4d5|       4.5         |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*
        | 3T diff inductor with pgs & psub |diff_ind_3t_rf_pgs_psub_t5  |       5           |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        | 3T diff inductor with pgs & psub |diff_ind_3t_rf_pgs_psub_t5d5|       5.5         |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*
        | 3T diff inductor with pgs & psub |diff_ind_3t_rf_pgs_psub_t6  |       6           |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*  
        | 3T diff inductor with pgs & psub |diff_ind_3t_rf_pgs_psub_t6d5|       6.5         |   30-90um    | fixed at 1.5um | fixed at 8um |       
        *----------------------------------------------------------------------------------------------------------------------------------*

	Width scalable 3-termianl differential Inductor Model
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*
       |  Turn, Radius & Width  |    T=1~3 step 0.5, W=5~13.5um,R=1.7071*W+16.378~120um             |     T=3.5~5.0 step 0.5, W=5~8um,R=1.7071*W+16.378~120um           |
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*   
       |        Model Name      |                                                    diff_ind_3t_rf_pgs_psub_n    		                                        |
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*
       |        Model Name      |                                                    diff_ind_3t_rf_pgs_n    		                                        	|
       *------------------------*-------------------------------------------------------------------*-------------------------------------------------------------------*    
        temperature range:-40C~125C

        *--------------------------------------------------------------------------------------------------------------------------------------------*  
        |                Inductor Type              |       model name         |       turn range       | Radius range |   Spacing    |  Width       |
        |============================================================================================================================================|  
        |     3T differential ALPA inductor         |   diff_ind_3t_alpa_rf    | 2.5 to 7.5 with step 1 |    30-120um  | fixed at 4um | fixed at 8um |   
        *--------------------------------------------------------------------------------------------------------------------------------------------* 
        | 3T differential ALPA inductor with psub   | diff_ind_3t_alpa_rf_psub | 2.5 to 7.5 with step 1 |    30-120um  | fixed at 4um | fixed at 8um |    
        *--------------------------------------------------------------------------------------------------------------------------------------------*
        temperature range:-40C~125C

        *------------------------------------------------------------------------------------------------------------------------------------------*
        |        Inductor Type                                     |     name                 |turn| minimum Radius |     Spacing    |  Width      |
        |==========================================================================================================================================|
        | 3T Differential Inductor(TM2+ALPA; Width=15um)           | rf_3Tdiff_1talpa_t1      | 1  |    50um        | fixed at 2um   |fixed at 15um|
        *------------------------------------------------------------------------------------------------------------------------------------------*
        | 3T Differential Inductor(TM2+ALPA; Width=15um)           | rf_3Tdiff_1talpa_t2      | 2  |    50um        | fixed at 2um   |fixed at 15um|
        *------------------------------------------------------------------------------------------------------------------------------------------*
        | 3T Differential Inductor(TM2+ALPA; Width=15um)           | rf_3Tdiff_1talpa_t3      | 3  |    50um        | fixed at 2um   |fixed at 15um|
        *------------------------------------------------------------------------------------------------------------------------------------------*
        | 3T Differential Inductor(TM2+ALPA; Width=15um)           | rf_3Tdiff_1talpa_t4      | 4  |    50um        | fixed at 2um   |fixed at 15um|
        *------------------------------------------------------------------------------------------------------------------------------------------*
        | 3T Differential Inductor(TM2+ALPA; Width=15um)           | rf_3Tdiff_1talpa_t5      | 5  |    50um        | fixed at 2um   |fixed at 15um|
        *------------------------------------------------------------------------------------------------------------------------------------------*
        | 3T Differential Inductor(TM2+ALPA; Width=15um)           | rf_3Tdiff_1talpa_t6      | 6  |    50um        | fixed at 2um   |fixed at 15um|
        *------------------------------------------------------------------------------------------------------------------------------------------*
        | 3T Differential Inductor(TM2+ALPA; Width=15um)           | rf_3Tdiff_1talpa_t7      | 7  |    50um        | fixed at 2um   |fixed at 15um|
        *------------------------------------------------------------------------------------------------------------------------------------------*
        | 3T Differential Inductor(TM2+ALPA; Width=15um) with PSUB | rf_3Tdiff_1talpa_psub_t1 | 1  |    50um        | fixed at 2um   |fixed at 15um|
        *------------------------------------------------------------------------------------------------------------------------------------------*
        | 3T Differential Inductor(TM2+ALPA; Width=15um) with PSUB | rf_3Tdiff_1talpa_psub_t2 | 2  |    50um        | fixed at 2um   |fixed at 15um|
        *------------------------------------------------------------------------------------------------------------------------------------------*
        | 3T Differential Inductor(TM2+ALPA; Width=15um) with PSUB | rf_3Tdiff_1talpa_psub_t3 | 3  |    50um        | fixed at 2um   |fixed at 15um|
        *------------------------------------------------------------------------------------------------------------------------------------------*
        | 3T Differential Inductor(TM2+ALPA; Width=15um) with PSUB | rf_3Tdiff_1talpa_psub_t4 | 4  |    50um        | fixed at 2um   |fixed at 15um|          
        *------------------------------------------------------------------------------------------------------------------------------------------* 
        | 3T Differential Inductor(TM2+ALPA; Width=15um) with PSUB | rf_3Tdiff_1talpa_psub_t5 | 5  |    50um        | fixed at 2um   |fixed at 15um|         
        *------------------------------------------------------------------------------------------------------------------------------------------* 
        | 3T Differential Inductor(TM2+ALPA; Width=15um) with PSUB | rf_3Tdiff_1talpa_psub_t6 | 6  |    50um        | fixed at 2um   |fixed at 15um|          
        *------------------------------------------------------------------------------------------------------------------------------------------* 
        | 3T Differential Inductor(TM2+ALPA; Width=15um) with PSUB | rf_3Tdiff_1talpa_psub_t7 | 7  |    50um        | fixed at 2um   |fixed at 15um|          
        *------------------------------------------------------------------------------------------------------------------------------------------* 


        For the detail 3-Terminal Differential Inductor model capacity please refer to the section 7.6.1 and 7.7.1 of main document 


4.Corner Model: 
        
      ----------------------------------------------------
      MOS                      name : corner
      ----------------------------------------------------
                               MOS_TT : Typical case
                               MOS_FF : Fast case
                               MOS_SS : Slow case
                               MOS_FNSP : Fast N Slow P case    
                               MOS_SNFP : Slow N Fast P case    
      ----------------------------------------------------
      Resistor                 name : corner
      ----------------------------------------------------
                               RES_TT : Typical case
                               RES_FF : Fast case
                               RES_SS : Slow case 
      ----------------------------------------------------
      MIM                      name : corner
      ----------------------------------------------------
                               MIM_TT : Typical case
                               MIM_FF : Fast case
                               MIM_SS : Slow case 
      ----------------------------------------------------
      MOM                      name : corner
      ----------------------------------------------------
                               MOM_TT : Typical case
                               MOM_FF : Fast case
                               MOM_SS : Slow case 
      ----------------------------------------------------
      MOS Varactor             name : corner
      ----------------------------------------------------
                               VAR_TT : Typical case
                               VAR_FF : Fast case
                               VAR_SS : Slow case 
      ----------------------------------------------------
      Spiral Inductor          name : corner
      ----------------------------------------------------
                               SPIRIND_TT : Typical case
                               SPIRIND_FF : Fast case
                               SPIRIND_SS : Slow case 
      ----------------------------------------------------
      Differential Inductor    name : corner
      ----------------------------------------------------
                               DIFFIND_TT : Typical case
                               DIFFIND_FF : Fast case
                               DIFFIND_SS : Slow case 
      ----------------------------------------------------
      3T Differential Inductor name : corner
      ----------------------------------------------------
                               3TDIFFIND_TT : Typical case
                               3TDIFFIND_FF : Fast case
                               3TDIFFIND_SS : Slow case 
      ----------------------------------------------------
      Top Metal Resistor       name : corner
      ----------------------------------------------------
                               TM2_RES_TT : Typical case
                               TM2_RES_FF : Fast case
                               TM2_RES_SS : Slow case 
      ----------------------------------------------------
      ----------------------------------------------------
      Width scalable Spiral Inductor name : corner
      ----------------------------------------------------
                               ind_rf_pgs_psub_n_tt : Typical case
                               ind_rf_pgs_psub_n_ff : Fast case
                               ind_rf_pgs_psub_n_ss : Slow case 
                               ind_rf_pgs_n_tt : Typical case
                               ind_rf_pgs_n_ff : Fast case
                               ind_rf_pgs_n_ss : Slow case 
      ----------------------------------------------------
      Width scalable Differential Inductor name : corner
      ----------------------------------------------------
                               diff_ind_rf_pgs_psub_n_tt : Typical case
                               diff_ind_rf_pgs_psub_n_ff : Fast case
                               diff_ind_rf_pgs_psub_n_ss: Slow case 
                               diff_ind_rf_pgs_n_tt : Typical case
                               diff_ind_rf_pgs_n_ff : Fast case
                               diff_ind_rf_pgs_n_ss: Slow case 
      ----------------------------------------------------
      Width scalable 3T Differential Inductor name : corner
      ----------------------------------------------------
                               diff_ind_3t_rf_pgs_psub_n_tt : Typical case
                               diff_ind_3t_rf_pgs_psub_n_ff : Fast case
                               diff_ind_3t_rf_pgs_psub_n_ss : Slow case
                               diff_ind_3t_rf_pgs_n_tt : Typical case
                               diff_ind_3t_rf_pgs_n_ff : Fast case
                               diff_ind_3t_rf_pgs_n_ss : Slow case

      Note: Use 5*sigma of Cgg mapping data standard deviation for MOS Varactor corner

5.Statistical Model: 
        
      ----------------------------------------------------
      MOS                      name : statistical model
      ----------------------------------------------------
                               MOS_MC : Monte Carlo    
      ----------------------------------------------------
      Resistor                 name : statistical model
      ----------------------------------------------------
                               RES_MC : Monte Carlo    
      ----------------------------------------------------
      MIM                      name : statistical model
      ----------------------------------------------------
                               MIM_MC : Monte Carlo    
      ----------------------------------------------------
      MOM                      name : statistical model
      ----------------------------------------------------
                               MOM_MC : Monte Carlo    
      ----------------------------------------------------
      MOS/Junction Varactor    name : statistical model
      ----------------------------------------------------
                               VAR_MC : Monte Carlo    
      ----------------------------------------------------
      Spiral Inductor          name : statistical model
      ----------------------------------------------------
                               SPIRIND_MC : Monte Carlo    
      ----------------------------------------------------
      Differential Inductor    name : statistical model
      ----------------------------------------------------
                               DIFFIND_MC : Monte Carlo    
      ----------------------------------------------------
      3T Differential Inductor name : statistical model
      ----------------------------------------------------
                               3TDIFFIND_MC : Monte Carlo    
      ----------------------------------------------------
      Top Metal Resistor       name : statistical model
      ----------------------------------------------------
                               TM2_RES_MC : Monte Carlo    
      ----------------------------------------------------
      ----------------------------------------------------
      Width scalable Spiral Inductor name : statistical model
      ----------------------------------------------------
                               ind_rf_pgs_psub_n_mc : Monte Carlo 
                               ind_rf_pgs_n_mc : Monte Carlo   
      ----------------------------------------------------
      Width scalable Differential Inductor name : statistical model
      ----------------------------------------------------
                               diff_ind_rf_pgs_psub_n_mc : Monte Carlo  
                               diff_ind_rf_pgs_n_mc : Monte Carlo   
      ----------------------------------------------------
      Width scalable 3T Differential Inductor name : statistical model
      ----------------------------------------------------
                               diff_ind_3t_rf_pgs_psub_n_mc : Monte Carlo
                               diff_ind_3t_rf_pgs_n_mc : Monte Carlo    
      ----------------------------------------------------
