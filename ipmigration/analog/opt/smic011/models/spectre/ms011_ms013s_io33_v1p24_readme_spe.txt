*** SMIC SPICE model for 0.11um mixed signal 1.2V/3.3V 1P8M process ***
*** For Spectre only ***


1. Update History:

      v2.0: Initiate
      v2.1: Main document change description:
              a. Updated P12 corner table in section 7.2.2.
              b. Added BJT model in section 7.3.
              b. Added resistor model card description in section 7.6.4.
              d. Added MIM capacitance model in section 7.7.
              e. Added N+poly/NW MOS varactor model in section 7.8.
              f. Added model fitting and plotting results in section 7.9.
              g. Updated the list of attachment files in section 8.
            Attachment files change description:
              a. Added gds and layer definition files of diode and BJT.
              b. Added fitting plots files 'ms011_ms013s_io33_fitA~F'. 
              c. Updated P12 corner model, added BJT, MIM and varactor corner model in files 'ms011_ms013s_io33_v2p1.lib', 'ms011_ms013s_io33_v2p1_spe.lib' and 'ms011_ms013s_io33_v2p1_eldo.lib'.
              d. Updated P12 temperature parameters and N33 noise parameters in model files 'ms011_ms013s_io33_v2p1.mdl', 'ms011_ms013s_io33_v2p1_spe.mdl' and 'ms011_ms013s_io33_v2p1_eldo.mdl'.
              e. Added BJT model card files 'ms011_ms013s_io33_v2p1_bjt.mdl', 'ms011_ms013s_io33_v2p1_bjt_spe.mdl' and 'ms011_ms013s_io33_v2p1_bjt_eldo.mdl'.
              f. Added MIM model card files 'ms011_ms013s_io33_v2p1_mim.mdl', 'ms011_ms013s_io33_v2p1_mim_spe.mdl' and 'ms011_ms013s_io33_v2p1_mim_eldo.mdl'. 
              g. Revised the parameter definition of 'temper' to direct expression to avoid the limitation of simulator, added MIM and varactor macro model
                 in files 'ms011_ms013s_io33_v2p1_res.ckt', 'ms011_ms013s_io33_v2p1_res_spe.ckt' and 'ms011_ms013s_io33_v2p1_res_eldo.ckt'.
              h. Updated resistor module file for spectre model and renamed 'res.def' to 'res.va'.   
              i. Updated readme files 'ms011_ms013s_io33_v2p1_readme.txt', 'ms011_ms013s_io33_v2p1_readme_spe.txt' and 'ms011_ms013s_io33_v2p1_readme_eldo.txt'. 
              j. Updated model version from v2.0 to v2.1.     
      v2.2: Main document change description:
              1.Revised mos ioff model and corner model with gidl parameter and added dagidl parameter in section 7.2.2
              2.Added Gate Current model description in section 7.2.3
              3.Revised mos fnsp/snfp corner model with dtox, dxl and dxw=0 and cgdo, cgso=0 and updated in section 7.2.2 and simulation result in section 7.2.8 and in section 7.2.9
              4.Added STI stress effect model description in section 7.2.10
              5.Modified bjt corner for IS and NF parameter and updated in section 7.3.2
              6.Added DNW/Pwell and BPW/DNW diode model in section 7.4 and updated capability of model in section 7.4.1 and corner model table of diode in section 7.4.2
              7.Revised interconnect variation and redefine the methodology of corner model simulation in section 7.5;
              8.Revised Resistance Table and description and plot in senction 7.6.1, 7.6.2, 7.6.3 and updated Resistance corner model table in 7.6.4 
              9.Added MIM cap model for MIM Cspec=2fF/um^2 and MIM Cspec=4fF/um^2 and updated in section 7.7
              10.Revised MOS varactor model and modified the valid range and Cg-Vg plot in section 7.8
              11.Added MOM model in section 7.9
              12.Add BP1095 (SAB) in 7.10.
            Attachment files change description:
              1.Revised mos fnsp/snfp corner model 
              2.Revised mos ioff model
              3.Added Gate Current model for hvt/lvt core device
              4.Added ".option gmindc=1e-14" in corner model files 
              5.Modified bjt corner model
              6.Added DNW/Pwell and BPW/DNW diode model
              7.Updated interconnect model
              8.Updated Resistance model card to center to PCM spec and revised SAB related ú¿except hrpú¨resistance with 2-terminal structure to extract dl
              9.Added MIM cap model for Cspec=2fF/um^2, 4fF/um^2
              10.Updated MOS varactor model
              11.Added MOM model
              12.Added Monte Carlo Statistical model
             Above changes have done modification in following attached file:"ms011_ms013s_io33_interconnect_struct_1.txt","ms011_ms013s_io33_interconnect_struct_2.txt","ms011_ms013s_io33_v2p3_res_spe.ckt","ms011_ms013s_io33_v2p3_mim_spe.mdl", "ms011_ms013s_io33_v2p3_spe.mdl", "ms011_ms013s_io33_v2p3_spe.lib", 'res.va',"ms011_ms013s_io33_v2p3_dio_spe.mdl", "ms011_ms013s_io33_fit_C.pdf""ms011_ms013s_io33_fit_D.pdf", "ms011_ms013s_io33_fit_E.pdf" and "ms011_ms013s_io33_fit_F.pdf"
              13.Changed model version from 2.1 to 2.2
              14.Zipped all ASCII files in Attachment
              PS. All model changes not related process change

	v2.3: Main document change description:
               1. Add 0.13um Logic 1P8M Salicide 1.2/3.3V PCM SPEC (TD-LO13-PC-2002) in section 5 "Reference" and revised the organization name of SMIC SPICE model team group description in section 6 "Responsibility"
	       2. Revised the shrinkage formulae of 3.3V device in section 7.0 "Technology Information" and removed the copy description since it is not directly copied from 0.13um model document file. Revised correlative lot/wafer/die site information in section 7.1 "Wafer Information"
               3. Add correlative NMOSFET in Deep Nwell content description and schematic layout/ cross-section plots in section 7.2.1 "Capability of Model" and change corresponding device corner model parameters in section 7.2.2 "Corner Model Table".
               4. Removed correlative content description for ELDO format in section 7.2.1 "Capability of Model", section 7.2.3 "Gate Current model", section 8 "Attachment", since ELDO model format is no longer the default support model format in SMIC. 
               5. Add Monte Carlo Statistical model description content in section 7.2.4 "Monte Carlo Statistical model", and removed the ring oscillator verification content by aligning the document content with other technology nodes
               6. Change correlative simulation and measurement results in section 7.2.5 "1/f Noise Model", section 7.2.7 "Comparison Between MOSFET Model Simulation and Measurement Results", section 7.2.8 "Comparison Between MOSFET Model Simulation and PCM spec"
               7. Add six small size NPN BJT devices (NPN12A100, NPN12A25, NPN12A4, NPN33A100, NPN33A25 and NPN33A4) and update correlative content in section 7.3.1 "Validity of Model " and section 7.3.2  "Corner Model Table of BJT"	
               8. Modified filename list in section 7.10 "Model fitting and Plotting results" by following the correlative attachment file
               9. Change stress parameters "sa0"/"sb0" to "saref"/"sbref" in section 7.2.6 "MOSFET Model Parameters Description for HSPICE Level 49 (BSIM3V3.24)" and section 7.2.9 "STI Stress Effect Model"
               10. Add two new MIM devices for 1fF/um2 and 1.5fF/um2 (MIM1_TM, MIM15_TM), and add two correlative section 7.7.5 "Two masks MIM Cspec=1(fF/um2)" and section 7.7.6 "Two masks MIM Cspec= 1.5(fF/um2)". Revise sections names of other MIM devices with declaration of MIM process options (one mask, two masks or stacked).
	      Attachment files change description:	     
	       1. Revised all mos models from new 0.13um process fitting models including svt/hvt/lvt/io33/nt12/nt33 devices
	       2. Update noise models based on silicon data of 0.13um model wafers and only minute change of corner parameters
	       3. Reseving stress related parameters of n12/p12/n33/p33, changing sa0/sb0 to saref/sbref to match Bsim4 param definition
	       4. Change one parameter "sigma" in monte-calo to sperate corresponding model parameters as "sigma_mos", "sigma_res", "sigma_mom", "sigma_mim" in .lib file for solving naming conflict issue
	       5. Add scale multiple factor 0.9 by replacing "lr" to "lr*0.9" or "ldraw" to "ldraw*0.9" in resistor macro model for parameters ("vc1","vc2") in "res.va" file
	       6. Change parmaters "l" to "lr" and "w" to "wr" in MOS Varactor macro model (pvar12_ckt/pvar33_ckt) in "ms011_ms013s_io33_v2p3_res_spe.ckt" file for LVS naming correlation of both SPECTRE and HSPICE format model
	       7. Add area scale divison factor 0.81 in MOM macro model for parameter ("cj") in "ms011_ms013s_io33_v2p3_res_spe.ckt" file and add scale option syntax in .lib file "ms011_ms013s_io33_v2p3_spe.lib"
	       8. Add width shift of "-0.003*0.9um=-2.7e-9m" by mask sizing LOTA rules in all poly related resistor macro model by revising parameter "dw" in "ms011_ms013s_io33_v2p3_res_spe.ckt" file
               9. No changes for other devices including bjt/diode/MIM and BEOL interconnect models
	      10. Keep model card format and device names as previous 2.2 version including scale factor syntax in models
              11. Remove ELDO format model card files and Changed model version from 2.2 to 2.3
              12. Zipped all ASCII and GDSII files seperately in Attachment files "ASCII.7z" and "GDSII.7z" 

         v1.24:Main document files change description:
               1.Extend Lmax to 20u, and update in section 7.2.1(extend poly length range to cover more design structures)                                                                                                                                                                                                                
               2.Change nt12, nt33 Wmin from 0.15u to 0.28u, and update in section 7.2.1(accuracy improvement)                                                                                                                                                                                                                            
               3.Modify dnw mos model: dnw12_ckt / dnwhvt12_ckt / dnwlvt12_ckt / dnw33_ckt, and remove dnw description in document, and update in section 7.2.1(accuracy improvement)                                                                                                                                                     
               4.Add SA,SB calculation method description, and update in section 7.2.10(new content added)                                                                                                                                                                                                                                
               5.Modify interconnection information, and update in section 7.5.2(align with PIE)                                                                                                                                                                                                                                          
               6.Modify resistor model width range, and update in section 7.6.1(align with PDK)                                                                                                                                                                                                                                           
               7.Add ALPA resistor model, and update in section 7.6.2 and 7.6.4(new option added)                                                                                                                                                                                                                                         
               8.Delete one mask 2fF/um2, 4fF/um2, and two masks 1fF/um2 and 1.5fF/um2 model, and delete their description in section 7.7.3~7.7.6(process improvement)                                                                                                                                                                    
               9.Add two mask 2fF/um2 and one mask stacked 3fF/um2 mim model, add all mim mismatch model, and update in section 7.7.3~7.7.4(new option added)                                                                                                                                                                             
               10.Update varactor model, extend length range to 1.5um, and update in section 7.8.1~7.8.2(extend poly length range to cover more design structures)                                                                                                                                                                        
               11.Modify spectre mom model to pure subckt format, and update in section 8.1(accuracy improvement)                                                                                                                                                                                                                         
               12.Add mom model: mom15_ckt / mom14_ckt / mom13_ckt / mom25_ckt / mom24_ckt / mom35_ckt, and update in section 7.9.1~7.9.2(new option added)                                                                                                                                                                               
               13.Change macro resistor voltage coefficient limit boundary, and update in section 8.1(accuracy improvement)                                                                                                                                                                                                               
               14.Modify mom corner format, no impact on model content, and update in section 8.1(model format improvement)                                                                                                                                                                                                               
               15.Add diode model: parasitic_nwd / parasitic_rwd / parasitic_dnwd, and update in section 8.1(new option added)                                                                                                                                                                                                            
               16.Modify diode model rs parameter, and update in section 8.1(accuracy improvement)                                                                                                                                                                                                                                        
               17.Improve gate leakage model of  nt12, nhvt12, p12, plvt12, phvt12, and update in section 8.1(accuracy improvement)                                                                                                                                                                                                                      
               18.Add mos mismatch model in n12_mis_ckt  / p12_mis_ckt / n33_mis_ckt / p33_mis_ckt, and update in section 8.1(new option added)                                                                                                                                                                                           
               19.Add 4t dnw mos model: dnw12_4t_ckt / dnwhvt12_4t_ckt / dnwlvt12_4t_ckt / dnw33_4t_ckt, and update in section 8.1(new option added)                                                                                                                                                                                      
               20.Interchange varactor ff and ss corner, and update in section 8.1(accuracy improvement)                                                                                                                                                                                                                                  
               21.Add bjt and varactor monte carlo corner (bjt_mc, var_mc), and update in section 8.1(new option added)                                                                                                                                                                                                                   
               22.Add mim subckt model in spectre model, and update in section 8.1(new option added)                                                                                                                                                                                                                                      
               23.Improve some mos model: (1)n12 change "cdscb=-1e-4" to 0 (2)nt12, add "ngate=1.176E+21", and open gate leakage mode "igcmod=1 , igbmod=1"  (3)plvt12, change noia=3.639E+21 to 2.00E+19,noib=-8.8204E+05 to 1 (4)nt33 change noib=-1.0817E+03 to 1, and update in section 8.1(accuracy improvement)
               24.Add resistor mismatch model in rndifsab_ckt, rpdifsab_ckt, rnposab_ckt, rnposab_3t_ckt, rpposab_ckt, rpposab_3t_ckt, rhrpo_ckt, rhrpo_3t_ckt, and update in section 8.1(new option added)                                                                                                                               
               25.Add width shift of "-0.003*0.9um=-2.7e-9m" by mask sizing LOTA rules in all poly related resistor compact model by revising parameter "dw", and update in section 8.1(accuracy improvement)                                                                                                                             
               26.Add mim 1.5fF/um2 3 terminal model, and update in section 8.1(new option added)                                                                                                                                                                                                                                         
               27.Add BJT NPN12A100, NPN12A25, NPN12A4, NPN33A100, NPN33A25 and NPN33A4 fitting plots in í—ms011_ms013s_io33_fit_B.docí˜, and update in section 7.10 ,8.3(new option added)                                                                                                                                               
               28.Improve nlvt12, modify diode parameter jsw=1.6e-8 to 1.2e-013,and set agidl=0 , and update in section 8.1(accuracy improvement)                                                                                                                                                                                         
               29.Add mos subckt instance sa/sb/as/ad/ps/pd/nrd/nrs calculate formula as default value in library file, and update in section 8.1(improve model format )                                                                                                                                                                  
               30.Modify the subckt model to inline subckt format in file " ms011_ms013s_io33_v1p24_spe.lib"(new option added)                                                                                                                                                                                                          
               31.Modify model file name in attachment due to version up, and update the model name and title name in main document(new version name consistency)                                                                                                                                                                         
               32.Update gds sample , and update in section 8.2 and GDSII.7z(align with PDK)                                                                                                                                                                                                                                              
               33.Due to main document title change, also change all fitting plot file document, and update in section 8.3(new version name consistency)                                                                                                                                                                                  
               34.Updated n33, p33 model to PCM target, and update in section 7.2.8
               35.Updated n33, p33, nt33 corner model to PCM SPEC, and update in section 7.2.2 and 7.2.8
               36.Changed n33, p33 dlc parameter to match ring oscillator speed, and update in section 7.2.9
               37.Improve some diode capacitance temperature parameter: pdio12, ndio33, ntdio12, ntdio33, plvtdio12, nwdio, rwdio33, dnwdio33, parasitic_nwd, parasitic_rwd, parasitic_dnwd. and update the related MOSFET/BJT/varactor,and update in section 7.2.9, 7.3.2

2. Files:

      ms011_ms013s_io33_v1p24_readme_spe.txt               .... This file!
      ms011_ms013s_io33_v1p24_spe.lib                      .... Corner values for MOSFETs, diode, BJT, resistors, MIM, MOM and varactor
      ms011_ms013s_io33_v1p24_spe.mdl                      .... Model parameters file for MOSFETs
      ms011_ms013s_io33_v1p24_mis_spe.mdl                  .... Model parameters file for MOSFETs
      ms011_ms013s_io33_v1p24_dio_spe.mdl                  .... Model parameters file for diode
      ms011_ms013s_io33_v1p24_bjt_spe.mdl                  .... Model parameters file for BJT
      ms011_ms013s_io33_v1p24_mim_spe.mdl                  .... Model parameters file for MIM
      ms011_ms013s_io33_v1p24_res_spe.mdl                  .... Model parameters file for resistors
      ms011_ms013s_io33_v1p24_res_spe.ckt                  .... Resistor, MOM capacitance, MIM capacitance and varactor macro model 
      res.va                                                 .... Resistor modules
      gc.va                                                  .... MOS varactor modules
      ms011_ms013s_io33_v1p24_interconnect_struct_1.txt    .... Interconnect tables for structure-1 (Parallel lines above a bottom plate)
      ms011_ms013s_io33_v1p24_interconnect_struct_2.txt    .... Interconnect tables for structure-2 (Parallel lines between two plates)      
      ms011_ms013s_io33_fit_A.doc                            .... Section A of the fitting plots for 0.11um mixed signal model
      ms011_ms013s_io33_fit_B.doc                            .... Section B of the fitting plots for 0.11um mixed signal model
      ms011_ms013s_io33_fit_C.doc                            .... Section C of the fitting plots for 0.11um mixed signal model
      ms011_ms013s_io33_fit_D.doc                            .... Section D of the fitting plots for 0.11um mixed signal model
      ms011_ms013s_io33_fit_E.doc                            .... Section E of the fitting plots for 0.11um mixed signal model
      ms011_ms013s_io33_fit_F.doc                            .... Section F of the fitting plots for 0.11um mixed signal model
      ms011_ms013s_io33_fit_G.doc                            .... Section G of the fitting plots for 0.11um mixed signal model
      PNP12A100.gds                                          .... GDSII file for 1.2V BJT PNP 10X10
      PNP12A25.gds                                           .... GDSII file for 1.2V BJT PNP 5X5
      PNP12A4.gds                                            .... GDSII file for 1.2V BJT PNP 2X2
      PNP33A100.gds                                          .... GDSII file for 3.3V BJT PNP 10X10
      PNP33A25.gds                                           .... GDSII file for 3.3V BJT PNP 5X5
      PNP33A4.gds                                            .... GDSII file for 3.3V BJT PNP 2X2
      NPN12A400.gds                                          .... GDSII file for 1.2V BJT NPN 20X20
      NPN12A225.gds                                          .... GDSII file for 1.2V BJT NPN 15X15
      NPN12A100.gds                                          .... GDSII file for 1.2V BJT NPN 10X10
      NPN12A25.gds                                           .... GDSII file for 1.2V BJT NPN 5X5
      NPN12A4.gds                                            .... GDSII file for 1.2V BJT NPN 2X2
      NPN33A100.gds                                          .... GDSII file for 3.3V BJT NPN 10X10
      NPN33A25.gds                                           .... GDSII file for 3.3V BJT NPN 5X5
      NPN33A4.gds                                            .... GDSII file for 3.3V BJT NPN 2X2
      DIO_NPW12.gds                                          .... GDSII file for 1.2V Diode N+/Pwell
      DIO_PNW12.gds                                          .... GDSII file for 1.2V Diode P+/Nwell
      DIO_NPW33.gds                                          .... GDSII file for 3.3V Diode N+/Pwell
      DIO_PNW33.gds                                          .... GDSII file for 3.3V Diode P+/Nwell
      DIO_NTPW12.gds                                         .... GDSII file for 1.2V Native Diode N+/Pwell
      DIO_NTPW33.gds                                         .... GDSII file for 3.3V Native Diode N+/Pwell
      DIO_NHVT12.gds                                         .... GDSII file for 1.2V HVT Diode N+/Pwell
      DIO_PHVT12.gds                                         .... GDSII file for 1.2V HVT Diode P+/Nwell
      DIO_NWPS.gds                                           .... GDSII file for Diode Nwell/Pwell
      DIO_NLVT12.gds                                         .... GDSII file for 1.2V LVT Diode N+/Pwell
      DIO_PLVT12.gds                                         .... GDSII file for 1.2V LVT Diode P+/Nwell
      DIO_DNWD33.gds                                         .... GDSII file for 3.3V Diode DNW/Pwell
      DIO_RWDNW33.gds                                        .... GDSII file for 3.3V Diode RW/DNW
      MOM17_L12N20.gds                                       .... GDSII file for Metal 1 stacked to Metal 7(Mlayer=7) MOM
      MOM27_L18N20.gds                                       .... GDSII file for Metal 2 stacked to Metal 7(Mlayer=6) MOM
      MOM16_L18N20.gds                                       .... GDSII file for Metal 1 stacked to Metal 6(Mlayer=6) MOM
      MOM26_L18N20.gds                                       .... GDSII file for Metal 2 stacked to Metal 6(Mlayer=5) MOM
      MOM46_L12N50.gds                                       .... GDSII file for Metal 4 stacked to Metal 6(Mlayer=3) MOM
      MOM13_L18N20.gds                                       .... GDSII file for Metal 1 stacked to Metal 3(Mlayer=3) MOM
      MOM14_L18N20.gds                                       .... GDSII file for Metal 1 stacked to Metal 4(Mlayer=4) MOM
      MOM15_L12N12.gds                                       .... GDSII file for Metal 1 stacked to Metal 5(Mlayer=5) MOM
      MOM24_L18N20.gds                                       .... GDSII file for Metal 2 stacked to Metal 4(Mlayer=3) MOM
      MOM25_L18N20.gds                                       .... GDSII file for Metal 2 stacked to Metal 5(Mlayer=4) MOM
      MOM35_L12N50.gds                                       .... GDSII file for Metal 3 stacked to Metal 5(Mlayer=3) MOM
      simulator_version.txt                                  .... Recommend simulator version list
      

3. How to use SMIC SPICE models in SPECTRE:


      Add the following statements to SPECTRE netlist.
      
      a. Specify MOS, diode and BJT model corner by the 'include' statement;

         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=tt
                                                               ^^ mos model corner
         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=dio_tt
                                                               ^^ diode model corner
         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=bjt_tt
                                                               ^^ bjt model corner   

      b. Include MOS, diode, BJT, resistor and mim model parameters by the 'include' statement;
         
         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.mdl"

         include "/xxx/xxx/ms011_ms013_io33_v1p24_dio_spe.mdl"

         include "/xxx/xxx/ms011_ms013_io33_v1p24_bjt_spe.mdl"        

         include "/xxx/xxx/ms011_ms013_io33_v1p24_res_spe.mdl"
         
         include "/xxx/xxx/ms011_ms013_io33_v1p24_mim_spe.mdl"
 
    c. Call resistor, MIM , MOM, Varactor macro model subcircuit by the following statement;

         include "/xxx/xxx/ms011_ms013_io33_v1p24_res_spe.ckt"
         
         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=dio_tt
                                                                ^^ diode model corner

         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=res_tt
                                                                ^^ resistor model corner

         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=mim_tt
                                                                ^^ mim model corner

         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=mom_tt
                                                                ^^ mom model corner

         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=var_tt
                                                                ^^ varactor model corner

         then add the following statement in your netlist to define subcircuit condition
         you want to simulate. 
         e.g. 
             * nwell resistor under STI        
               X1  1 2 3 rnwsti_ckt w=1u l=1u
             * mim capacitor
               X2  1 2 mim1_ckt w=30u l=30u

         Where /xxx/xxx is the directory where mdl and lib files are located.

      d. Call N+poly/NW MOS varactor model by the following statement;

         include "/xxx/xxx/ms011_ms013_io33_v1p24_res_spe.ckt"

         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=var_tt
                                                                ^^ varactor model corner
         
         then add the following statement in your netlist to define subcircuit condition
         you want to simulate.
         
         e.g. XCKT 1 2 pvar33_ckt lr=1u wr=10u nf=16 
      e. Call mom macro model subcircuit by the following statement;
         
         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=mom_tt
                                                              ^^ mom model corner
         .include '/xxx/xxx/ms011_ms013_io33_v1p24_res_spe.ckt'
          
         then add the following statement in your netlist to define  
	 subcircuit condition you want to simulate. 

         e.g. mom17
        
         X1 2 0 mom17_ckt l=20u n=100     
            
         Where '/xxx/xxx/' is the directory where mdl and lib files are located.
      f. Specify mos, resistor, mom, mim, varactor and BJT model corner by the '.lib' statement;

         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=mos_mc
                                                              ^^ mos monte carlo model corner
         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=res_mc
                                                              ^^ mos monte carlo model corner
         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=mom_mc
                                                              ^^ mos monte carlo model corner
         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=mim_mc
                                                              ^^ mos monte carlo model corner
         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=var_mc
                                                              ^^ varactor monte carlo model corner
         include "/xxx/xxx/ms011_ms013_io33_v1p24_spe.lib" section=bjt_mc
                                                              ^^ bjt monte carlo model corner
  
  
4. The Capability of Model

	a. MOS Model 
        *--------------------------------------------------------------------*
        |     MOSFET type              |     name            | Lmin  | Wmin  |
        |====================================================================| 
        |   1.2V NMOS                  |   n12               |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V PMOS                  |   p12               |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V Native NMOS           |   nt12              |0.3um  |0.28um |
        *--------------------------------------------------------------------*
        |   3.3V NMOS                  |   n33               |0.35um |0.15um |
        *--------------------------------------------------------------------*
        |   3.3V PMOS                  |   p33               |0.30um |0.15um |
        *--------------------------------------------------------------------*
        |   3.3V Native NMOS           |   nt33              |1.0um  |0.28um |
        *--------------------------------------------------------------------*
        |   1.2V HVT NMOS              |   nhvt12            |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V HVT PMOS              |   phvt12            |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V LVT NMOS              |   nlvt12            |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V LVT PMOS              |   plvt12            |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V NMOS                  |  n12_mis_ckt        |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V PMOS                  |  p12_mis_ckt        |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   3.3V NMOS                  |  n33_mis_ckt        |0.35um |0.15um |
        *--------------------------------------------------------------------*
        |   3.3V PMOS                  |  p33_mis_ckt        |0.30um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V NMOS(6 terminals)     |  dnw12_ckt          |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   3.3V NMOS(6 terminals)     |  dnw33_ckt          |0.35um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V HVT NMOS(6 terminals) | dnwhvt12_ckt        |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V LVT NMOS(6 terminals) | dnwlvt12_ckt        |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V NMOS(4 terminals)     |  dnw12_4t_ckt       |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   3.3V NMOS(4 terminals)     |  dnw33_4t_ckt       |0.35um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V HVT NMOS(4 terminals) | dnwhvt12_4t_ckt     |0.13um |0.15um |
        *--------------------------------------------------------------------*
        |   1.2V LVT NMOS(4 terminals) | dnwlvt12_4t_ckt     |0.13um |0.15um |
        *--------------------------------------------------------------------*
        Notice: Before 90% shrink for lmin and wmin 
        temperature range:-40C~125C
   
	b. BJT Model

        *---------------------------------------------------* 
        |      BJT type     |     name      |  Emitter Area |
        |===================================================|
        |   1.2V PNP_10X10  |   pnp12a100   |   10*10 um^2  |
        *---------------------------------------------------*  
        |   1.2V PNP_5X5    |   pnp12a25    |   5*5 um^2    |
        *---------------------------------------------------* 
        |   1.2V PNP_2X2    |   pnp12a4     |   2*2 um^2    |
        *---------------------------------------------------* 
        |   3.3V PNP_10X10  |   pnp33a100   |   10*10 um^2  |
        *---------------------------------------------------*  
        |   3.3V PNP_5X5    |   pnp33a25    |   5*5 um^2    |
        *---------------------------------------------------* 
        |   3.3V PNP_2X2    |   pnp33a4     |   2*2 um^2    |
        *---------------------------------------------------* 
        |   1.2V NPN_20X20  |   npn12a400   |   20*20 um^2  |
        *---------------------------------------------------* 
        |   1.2V NPN_15X15  |   npn12a225   |   15*15 um^2  |
        *---------------------------------------------------* 
        |   1.2V NPN_10X10  |   npn12a100   |   10*10 um^2  |
        *---------------------------------------------------* 
        |   1.2V NPN_5X5    |   npn12a25    |   5*5 um^2    |
        *---------------------------------------------------* 
        |   1.2V NPN_2X2    |   npn12a4     |   2*2 um^2    |
        *---------------------------------------------------* 
        |   3.3V NPN_10X10  |   npn33a100   |   10*10 um^2  |
        *---------------------------------------------------* 
        |   3.3V NPN_5X5    |   npn33a25    |   5*5 um^2    |
        *---------------------------------------------------* 
        |   3.3V NPN_2X2    |   npn33a4     |   2*2 um^2    |
        *---------------------------------------------------* 
        Notice: After 90% shrink
        temperature range:-40C~125C
         
	c. Diode Model               
	
        *------------------------------------------------* 
        |      Diode type         |  name   |    Area    |
        |================================================| 
        |    1.2V N+/PWELL        | ndio12  | 60*60 um^2 |
        *------------------------------------------------*
        |    1.2V P+/NWELL        | pdio12  | 60*60 um^2 |
        *------------------------------------------------*
        |   1.2V Native N+/PWELL  | ntdio12 | 60*60 um^2 |
        *------------------------------------------------*
        |    3.3V N+/PWELL        | ndio33  | 60*60 um^2 |
        *------------------------------------------------*
        |    3.3V P+/NWELL        | pdio33  | 60*60 um^2 |
        *------------------------------------------------*
        |   3.3V Native N+/PWELL  | ntdio33 | 60*60 um^2 |	
	*------------------------------------------------*
        |      NWELL/PSUB         |  nwdio  | 60*60 um^2 |	
	*------------------------------------------------*	
        |  1.2V HVT N+/PWELL      |nhvtdio12| 60*60 um^2 |
        *------------------------------------------------*
        |  1.2V HVT P+/NWELL      |phvtdio12| 60*60 um^2 |
        *------------------------------------------------*
	|  1.2V LVT N+/PWELL      |nlvtdio12| 60*60 um^2 |
        *------------------------------------------------*
        |  1.2V LVT P+/NWELL      |plvtdio12| 60*60 um^2 |
        *------------------------------------------------*
        |  3.3V BPW/DNWELL        |rwdio33  | 24*298 um^2|
        *------------------------------------------------*
        |  3.3V DNWELL/PWELL      |dnwdio33 | 30*300 um^2|
        *------------------------------------------------*
        | parasitic nwell/psub    |   parasitic_nwd      |
        *------------------------------------------------*
        | parasitic rwell/dnwell  |   parasitic_rwd      | 
        *------------------------------------------------*
        | parasitic dnwell/psub   |   parasitic_dnwd     | 
        *------------------------------------------------*
        Notice: Before 90% shrink 
	temperature range:-40C~125C

	d. Resistor Model

	*----------------------------------------------------*  
        |          Resistor Type                | 1.2V/3.3V  | 
        |====================================================|  
        | Silicide N+ Diffusion                 |   rndif    | 
        |----------------------------------------------------|  
        | Silicide P+ Diffusion                 |   rpdif    | 
        |----------------------------------------------------|  
        | Silicide N+ Poly                      |   rnpo     | 
        |----------------------------------------------------| 
        | Silicide N+ Poly (three terminal)     |  rnpo_3t   | 
        |----------------------------------------------------|    
        | Silicide P+ Poly                      |   rppo     | 
        |----------------------------------------------------| 
        | Silicide P+ Poly (three terminal)     |  rppo_3t   | 
        |----------------------------------------------------| 
        | NWell under STI                       |  rnwsti    | 
        |----------------------------------------------------| 
        | NWell under AA                        |  rnwaa     |      
        |----------------------------------------------------| 
        | Non-silicide N+ Diffusion             | rndifsab   | 
        |----------------------------------------------------|  
        | Non-silicide P+ Diffusion             | rpdifsab   | 
        |----------------------------------------------------| 
        | Non-silicide N+ Poly                  |  rnposab   | 
        |----------------------------------------------------|
        | Non-silicide N+ Poly (three terminal) | rnposab_3t | 
        |----------------------------------------------------|  
        | Non-silicide P+ Poly                  |  rpposab   | 
        |----------------------------------------------------| 
        | Non-silicide P+ Poly (three terminal) | rpposab_3t | 
        |----------------------------------------------------|
        | High Resistance Poly                  |   rhrpo    |
        |----------------------------------------------------|
        | High Resistance Poly (three terminal) |  rhrpo_3t  |
        |----------------------------------------------------| 
        |          Metal 1                      |    rm1     | 
        |----------------------------------------------------|  
        |          Metal 2                      |    rm2     |
        |----------------------------------------------------|  
        |          Metal 3                      |    rm3     | 
        |----------------------------------------------------|  
        |          Metal 4                      |    rm4     | 
        |----------------------------------------------------|  
        |          Metal 5                      |    rm5     | 
        |----------------------------------------------------|  
        |          Metal 6                      |    rm6     | 
        |----------------------------------------------------|  
        |          Metal 7                      |    rm7     |
        |----------------------------------------------------|  
        |          Metal 8                      |    rm8     | 
        |----------------------------------------------------| 
        |           ALPA                        |   ralpa    | 
        *----------------------------------------------------*  
         subckt model:
	*--------------------------------------------------------*  
        |          Resistor Type                |  1.2V/3.3V     | 
        |========================================================|  
        | Silicide N+ Diffusion                 |   rndif_ckt    | 
        |--------------------------------------------------------|   
        | Silicide P+ Diffusion                 |   rpdif_ckt    | 
        |--------------------------------------------------------|   
        | Silicide N+ Poly                      |   rnpo_ckt     | 
        |--------------------------------------------------------|  
        | Silicide N+ Poly (three terminal)     |  rnpo_3t_ckt   | 
        |--------------------------------------------------------|     
        | Silicide P+ Poly                      |   rppo_ckt     | 
        |--------------------------------------------------------|  
        | Silicide P+ Poly (three terminal)     |  rppo_3t_ckt   | 
        |--------------------------------------------------------|  
        | NWell under STI                       |  rnwsti_ckt    | 
        |--------------------------------------------------------|  
        | NWell under AA                        |  rnwaa_ckt     |      
        |--------------------------------------------------------|  
        | Non-silicide N+ Diffusion             | rndifsab_ckt   | 
        |--------------------------------------------------------|   
        | Non-silicide P+ Diffusion             | rpdifsab_ckt   | 
        |--------------------------------------------------------|  
        | Non-silicide N+ Poly                  |  rnposab_ckt   | 
        |--------------------------------------------------------| 
        | Non-silicide N+ Poly (three terminal) | rnposab_3t_ckt | 
        |--------------------------------------------------------|   
        | Non-silicide P+ Poly                  |  rpposab_ckt   | 
        |--------------------------------------------------------|  
        | Non-silicide P+ Poly (three terminal) | rpposab_3t_ckt | 
        |--------------------------------------------------------| 
        | High Resistance Poly                  |   rhrpo_ckt    |
        |--------------------------------------------------------| 
        | High Resistance Poly (three terminal) |  rhrpo_3t_ckt  |
        |--------------------------------------------------------|  
        |          Metal 1                      |    rm1_ckt     | 
        |--------------------------------------------------------|   
        |          Metal 2                      |    rm2_ckt     |
        |--------------------------------------------------------|   
        |          Metal 3                      |    rm3_ckt     | 
        |--------------------------------------------------------|   
        |          Metal 4                      |    rm4_ckt     | 
        |--------------------------------------------------------|   
        |          Metal 5                      |    rm5_ckt     | 
        |--------------------------------------------------------|   
        |          Metal 6                      |    rm6_ckt     | 
        |--------------------------------------------------------|   
        |          Metal 7                      |    rm7_ckt     |
        |--------------------------------------------------------|   
        |          Metal 8                      |    rm8_ckt     | 
        |--------------------------------------------------------| 
        |           ALPA                        |   ralpa_ckt    | 
        *--------------------------------------------------------*  
        temperature range:-40C~125C
      
       e. MIM capacitor Model
           capacitor name    : mim 

        *---------------------------------------------------------------------------------------------------------* 
        |  mim cap type           |  cspec = 1ff/um^2  | cspec = 1.5ff/um^2 | cspec = 2ff/um^2 | cspec = 3ff/um^2 |
        |=========================================================================================================| 
        |  mim model(one mask)    |     mim1           |   mim15            |    NA            |    mim3          |
        |---------------------------------------------------------------------------------------------------------|
        |  mim model(two mask)    |       NA           |      NA            |  mim2_tm         |    NA            |
        |---------------------------------------------------------------------------------------------------------|

         subckt model:
        *-----------------------------------------------------------------------------------------------------------------* 
        |  mim cap type           |  cspec = 1ff/um^2      | cspec = 1.5ff/um^2     | cspec = 2ff/um^2 | cspec = 3ff/um^2 |
        |=================================================================================================================| 
        |  mim model(one mask)    |     mim1_ckt           |   mim15_ckt            |    NA            |    mim3_ckt      |
        |-----------------------------------------------------------------------------------------------------------------|
        |  mim model(two mask)    |       NA               |      NA                |  mim2_tm_ckt     |       NA         |
        |-----------------------------------------------------------------------------------------------------------------|
        |  3t mim model(one mask) |       NA               |      mim15_3t_ckt      |     NA           |       NA         |
        |-----------------------------------------------------------------------------------------------------------------|
        temperature range : -40C~125C

       f. Thin oxide N+poly/NW MOS varactor model
        *------------------------------------------------*  
        |          Varactor Type          |     name     | 
        |================================================|  
        |    1.2V Thin Oxide Varactor     |  pvar12_ckt  | 
        |------------------------------------------------|  
        |    3.3V Thick Oxied Varactor    |  pvar33_ckt  | 
        *------------------------------------------------*
        temperature range:-40C~125C
        
       g. MOM Capacitor Model
       *-------------------------------------------------------------------------------------------------------------------------*
       |   MIM type   |     name      |      width        |       space       |  Mlayer | minimum length | minimum finger number |
       |=========================================================================================================================|
       |   M1~M6      |   mom16_ckt   | fixed at 0.20 um  |  fixed at 0.20um  |    6    |       18       |         20            |
       *-------------------------------------------------------------------------------------------------------------------------|
       |   M1~M7      |   mom17_ckt   | fixed at 0.20 um  |  fixed at 0.20um  |    7    |       12       |         12            |
       *-------------------------------------------------------------------------------------------------------------------------|
       |   M2~M6      |   mom26_ckt   | fixed at 0.20 um  |  fixed at 0.20um  |    5    |       18       |         20            |
       *-------------------------------------------------------------------------------------------------------------------------|
       |   M2~M7      |   mom27_ckt   | fixed at 0.20 um  |  fixed at 0.20um  |    6    |       18       |         20            |
       *-------------------------------------------------------------------------------------------------------------------------|
       |   M4~M6      |   mom46_ckt   | fixed at 0.20 um  |  fixed at 0.20um  |    3    |       12       |         50            |
       *-------------------------------------------------------------------------------------------------------------------------|
       |   M1~M5      |   mom15_ckt   | fixed at 0.20 um  |  fixed at 0.20um  |    5    |       12       |         12            |
       *-------------------------------------------------------------------------------------------------------------------------|
       |   M1~M4      |   mom14_ckt   | fixed at 0.20 um  |  fixed at 0.20um  |    4    |       18       |         20            |
       *-------------------------------------------------------------------------------------------------------------------------|
       |   M1~M3      |   mom13_ckt   | fixed at 0.20 um  |  fixed at 0.20um  |    3    |       18       |         20            |
       *-------------------------------------------------------------------------------------------------------------------------|
       |   M2~M5      |   mom25_ckt   | fixed at 0.20 um  |  fixed at 0.20um  |    4    |       18       |         20            |
       *-------------------------------------------------------------------------------------------------------------------------|
       |   M2~M4      |   mom24_ckt   | fixed at 0.20 um  |  fixed at 0.20um  |    3    |       18       |         20            |
       *-------------------------------------------------------------------------------------------------------------------------|
       |   M3~M5      |   mom35_ckt   | fixed at 0.20 um  |  fixed at 0.20um  |    6    |       12       |         50            |
       *-------------------------------------------------------------------------------------------------------------------------|
        Notice: After 90% shrink
        temperature range:-40C~125C
        For more detailed information, please refer to the main document in section 7.9


5. Corner Model 

   Five model corners are provided for MOSFETs, 
   three model corners are provided for diode,
   three model corners are provided for BJT,
   three model corners are provided for resistors,
   three model corners are provided for MIM,
   three model corners are provided for varactor.
   three model corners are provided for MOM.

   They are
        
   ----------------------------------------------------
   MOS      name : corner
   ----------------------------------------------------
            TT   : Typical case
            SS   : Slow case
            FF   : Fast case
            SNFP : Slow N Fast P case    
            FNSP : Fast N Slow P case    
   ----------------------------------------------------
   Diode    name : corner
   ----------------------------------------------------
            DIO_TT : Typical case
            DIO_SS : Slow case
            DIO_FF : Fast case 
   ----------------------------------------------------
   BJT      name : corner
   ----------------------------------------------------
            BJT_TT : Typical case
            BJT_SS : Slow case
            BJT_FF : Fast case 
   ----------------------------------------------------
   Resistor name : corner
   ----------------------------------------------------
            RES_TT : Typical case
            RES_SS : Slow case
            RES_FF : Fast case 
   ----------------------------------------------------
   MIM      name : corner
   ----------------------------------------------------
            MIM_TT : Typical case
            MIM_SS : Slow case
            MIM_FF : Fast case
   ----------------------------------------------------
   Varactor name : corner
   ----------------------------------------------------
            VAR_TT : Typical case
            VAR_SS : Slow case
            VAR_FF : Fast case
   ----------------------------------------------------
   ----------------------------------------------------
   MOM        name : corner
   ----------------------------------------------------
            MOM_TT : Typical case
            MOM_SS : Slow case
            MOM_FF : Fast case 
   ----------------------------------------------------

6. Monte Carlo Statistical model

   The model is given in Spectre format. Running Monte Carlo by using this model, user can get the distribution of the simulation target.
Please notice that, Gaussian distribution calculation method is different in the three simulators.  
The results generated from three simulators cannot be exactly match given the exactly same input conditions due to the different internal engines.  
Moreover, the number of occurrences in Monte Carlo simulation also has a great influence on the result; hence we recommend user to use no less than 100 occurrences in the simulation. 
Model uses as following example

   Demo netlist
------------------------------------------------------------
simulator lang=spectre insensitive=yes
include "ms011_ms013_io33_v1p24_spe.lib" section=mos_mc
m1 (d1 g1 0 0 ) n12 w=10e-6 l=0.13e-6
vd1 (d1 0) vsource dc=1.2
vg1 (g1 0) vsource dc=1.2
save vd1:currents
mc1 montecarlo variations=all numruns=500 donominal=no \
savefamilyplots=yes { 
 dc1 dc dev=vg1 param=dc  values=[1.2]
}
---------------------------------------------------------------
7. demo netlist for mos mismatch
// this is a test
simulator lang=spectre insensitive=yes
include "ms011_ms013s_io33_v1p24_spe.lib" section=tt
vgs1 ( g1 0 ) vsource dc=1.2
vds1 ( d1 0 ) vsource dc=1.2
vds2 ( d2 0 ) vsource dc=1.2
m1 (d1 g1 0 0 ) n12_mis_ckt w=10u l=0.13u mr=1 mismod=1 
m2 (d2 g1 0 0 ) n12_mis_ckt w=10u l=0.13u mr=1 mismod=1 
save vds1:currents
save vds2:currents

mc1 montecarlo variations=mismatch seed=500 numruns=1000 donominal=no \
savefamilyplots=yes { 
dc1 dc dev=vgs1 param=dc  values=[1.2]
dcopinfo info what=oppoint extremes=yes
}


8. demo netlist for mim capacitor mismatch
****************************************************************************
// this is a test
simulator lang=spectre insensitive=yes
include "ms011_ms013s_io33_v1p24_spe.lib" section=mim_tt
settempoption options temp=25
v1 (1 0) vsource dc=0
x1 (2 0) mim1_ckt w=5u l=5u mr=1 mismod_mim=1
x2 (3 0) mim1_ckt w=5u l=5u mr=1 mismod_mim=1
r1 (1 2) resistor r=1e-3
r2 (1 3) resistor r=1e-3

mc1 montecarlo variations=mismatch seed=500 numruns=1000 donominal=no \
savefamilyplots=yes { 
dc1 dc dev=v1 param=dc  values=[1.0]
dcopinfo info what=oppoint extremes=yes
}