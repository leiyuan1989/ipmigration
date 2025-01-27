*** SMIC SPICE model for 40nm logic low leakge 1.1V/1.8V/2.5V 1P10M process ***
*** For Spectre only ***

1. Update History:

	V0.0:Initiate
	V1.4_1r:a. All models (MOS, BJT, Diode, resistor and interconnect etc) parameters are re-extracted due to process change (V2.0 process).
                b. All the attachment has been updated.

2. Files:
	l0040ll_v1p4_1r_spe_readme.txt 				.... This file		
	l0040ll_v1p4_1r_spe.lib					.... Corner values for MOSFETs, Diode,BJT, Resistor, MOM and Varactor	
	l0040ll_v1p4_1r_spe.mdl					.... Model parameters file for 1.1V/2.5V MOS	
	l0040ll_v1p4_1r_dio_spe.mdl				.... Model parameters file for 1.1V/2.5V Diode	
	l0040ll_v1p4_1r_res_spe.ckt				.... Macro model parameters file for Resistor	
	l0040ll_v1p4_1r_var_spe.ckt				.... Macro model parameters file for Varactor	
	l0040ll_v1p4_1r_mom_spe.ckt				.... Macro model parameters file for MOM Capacitor	
        l0040ll_v1p4_1r_ldmos_spe.ckt                           .... Macro model parameters file for LDMOS.
	l0040ll_lpe_v1p4_1r_n11ll_spe.mdl			.... LPE Model parameters file for 1.1V NMOS	
	l0040ll_lpe_v1p4_1r_p11ll_spe.mdl			.... LPE Model parameters file for 1.1V PMOS	
	l0040ll_lpe_v1p4_1r_nhvt11ll_spe.mdl			.... LPE Model parameters file for 1.1V HVT NMOS	
	l0040ll_lpe_v1p4_1r_phvt11ll_spe.mdl			.... LPE Model parameters file for 1.1V HVT PMOS	
	l0040ll_lpe_v1p4_1r_nlvt11ll_spe.mdl			.... LPE Model parameters file for 1.1V LVT NMOS	
	l0040ll_lpe_v1p4_1r_plvt11ll_spe.mdl			.... LPE Model parameters file for 1.1V LVT PMOS	
	l0040ll_lpe_v1p4_1r_n25ll_spe.mdl			.... LPE Model parameters file for 2.5V NMOS	
	l0040ll_lpe_v1p4_1r_p25ll_spe.mdl			.... LPE Model parameters file for 2.5V PMOS	
	l0040ll_lpe_v1p4_1r_nod33ll_spe.mdl			.... LPE Model parameters file for 2.5V OD 3.3V NMOS	
	l0040ll_lpe_v1p4_1r_pod33ll_spe.mdl			.... LPE Model parameters file for 2.5V OD 3.3V PMOS	
	l0040ll_lpe_v1p4_1r_nud18ll_spe.mdl			.... LPE Model parameters file for 2.5V UD 1.8V NMOS	
	l0040ll_lpe_v1p4_1r_pud18ll_spe.mdl			.... LPE Model parameters file for 2.5V UD 1.8V PMOS	
	npn11a4ll_spe.mdl					.... Model parameters file for 1.1V NPN BJT (Emitter Area=2x2um^2)
	npn11a25ll_spe.mdl					.... Model parameters file for 1.1V NPN BJT (Emitter Area=5x5um^2)
	npn11a100ll_spe.mdl					.... Model parameters file for 1.1V NPN BJT (Emitter Area=10x10um^2)
	npn25a4ll_spe.mdl					.... Model parameters file for 2.5V NPN BJT (Emitter Area=2x2um^2)
	npn25a25ll_spe.mdl					.... Model parameters file for 2.5V NPN BJT (Emitter Area=5x5um^2)
	npn25a100ll_spe.mdl					.... Model parameters file for 2.5V NPN BJT (Emitter Area=10x10um^2)
	pnp11a4ll_spe.mdl					.... Model parameters file for 1.1V PNP BJT (Emitter Area=2x2um^2)
	pnp11a25ll_spe.mdl					.... Model parameters file for 1.1V PNP BJT (Emitter Area=5x5um^2)
	pnp11a100ll_spe.mdl					.... Model parameters file for 1.1V PNP BJT (Emitter Area=10x10um^2)
	pnp25a4ll_spe.mdl					.... Model parameters file for 2.5V PNP BJT (Emitter Area=2x2um^2)
	pnp25a25ll_spe.mdl					.... Model parameters file for 2.5V PNP BJT (Emitter Area=5x5um^2)
	pnp25a100ll_spe.mdl					.... Model parameters file for 2.5V PNP BJT (Emitter Area=10x10um^2)
	gc.va							.... Varactor modules
	res.va							.... Resistor modules
	l0040ll_v1p4_1r_interconnect_struct_1.txt		.... Interconnect tables for structure-1 (Parallel lines above a bottom plate)			
	l0040ll_v1p4_1r_interconnect_struct_2.txt		.... Interconnect tables for structure-2 (Parallel lines between two plates)			
	simulator_version.txt					.... Simulation version list	

3. How to use SMIC SPICE models in SPECTRE:
      Add the following statements to SPECTRE netlist.
      
      a. Specify MOS, Diode ,BJT,Resistor, Varactor and MOM Capacitor model corner by the 'include' statement;

         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=TT
                                                            ^^ MOS model corner
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=DIO_TT
                                                              ^^ Diode model corner
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=BJT_TT
                                                               ^^ BJT model corner 
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=RES_TT
                                                               ^^ Resistor model corner  
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=VAR_TT
                                                               ^^ Varactor model corner  
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=MOM_TT
                                                               ^^ MOM model corner  
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=LDMOS_TT
                                                            ^^ LDMOS model corner

      b. Specify MOS, Diode ,BJT,Resistor, Varactor and MOM Capacitor Monte Carlo model by the 'include' statement;

         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=MOS_MC
                                                               ^^ MOS Monte Carlo model 
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=BJT_MC
                                              	               ^^ BJT model corner 
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=RES_MC
                                                               ^^ resistor Monte Carlo model 
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=VAR_MC
                                                               ^^ MOS varactor Monte Carlo model
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=MOM_MC
                                                               ^^ MOM Monte Carlo model 
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=LDMOS_MC
                                                               ^^ LDMOS Monte Carlo model 

      c. Include MOS model parameters by the 'include' statement;
         
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.mdl'
         (then add the following statement in your netlist to define subcircuit condition you want to simulate.)

         e.g. 1.1V Core NMOS
	xm1 D G S B  n11ll_ckt w=1e-6 l=1e-6 sa=0 sb=0 sd=0 as=0 ad=0 ps=0 pd=0 nrd=0 nrs=0 sca=0 scb=0 scc=0 nf=1 mr=1 globalmod=1 mismod=0 dps=0.126u dpcs=0.072u dsts=1u lpemod=0 prelayout=0 dcn=0

      d. Include Diode model parameters by the 'include' statement;
         include '/xxx/xxx/l0040ll_v1p4_1r_dio_spe.mdl'

      e. Include BJT model parameters by the 'include' statement;
 
        include '/xxx/xxx/bjt/pnp11a100ll_spe.mdl'
        (then add the following statement in your netlist to define subcircuit condition you want to simulate.)

        e.g. 1.1V PNP BJT (Emitter Area=10*10^um2)
	xq1 c b e pnp11a100ll_ckt mismod=0


      f. Call resistor macro model subcircuit by the following statement;
         
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=DIO_TT
                                                               ^^ diode model corner
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=RES_TT
                                                               ^^ resistor model corner
        
         then add the following statement in your netlist to define  
	 subcircuit condition you want to simulate. 

         e.g. nwell resistor under STI
        
         X1 rnwsti_3t_ckt w=2u l=10u
            
         Where '/xxx/xxx/' is the directory where mdl and lib files are located.  

      g. Call MOS varactor model by the following statement;
         
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=VAR_TT
                                                               ^^ varactor model corner
         include '/xxx/xxx/l0040ll_v1p4_1r_dio_spe.lib' section=dio_TT
                                                                   ^^ diode model corner      
         then add the following statement in your netlist to define subcircuit condition
         you want to simulate.
         
         e.g. XCKT 1 2 pvar11ll_ckt lr=10u wr=10u mr=1  

      h. Call MOM capacitor model by the following statement;
         
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=MOM_TT
                                                               ^^ mom model corner
         then add the following statement in your netlist to define subcircuit condition
         you want to simulate.
         e.g. xc1 1 2 B mom_3t_ckt l=10 nn=10 mm=1 tm=5 bm=1 mismod=1 
         Where 'tm' means top metal, 'bm' means bottom metal,and 'tm' need to <=6, 'bm' should smaller than 'tm'.
	 '/xxx/xxx/' is the directory where mdl and lib files are located. 

      i. For the pre-layout simulation of mos and 3-T poly resistor model corner by the 'include' statement;
         
         Please notice that the library "pre_layout" need to be placed behind tt/ff/ss/fnsp/snfp/mos_mc and res_tt/res_ff/res_ss/res_mc sections to prevent from the redefine(these two flags change back to 0)

         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=tt
                                                            ^^ mos model corner 
         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=res_tt
                                                               ^^ resistor model corner  
         ...
         ...

         include '/xxx/xxx/l0040ll_v1p4_1r_spe.lib' section=pre_layout
                                                               ^^ pre-layout simulation 


4. The Capability of Model

   	a. MOS Model 
	*--------------------------------------------------------------*									
	|	MOSFET	type	      | 	name	| Lmin	| Wmin |
	|==============================================================|									
	|	1.1V	NMOS	      |  n11ll_ckt	| 0.04um|0.12um|
	*--------------------------------------------------------------*									
	|	1.1V	PMOS	      |  p11ll_ckt	|0.04um	|0.12um|
	*--------------------------------------------------------------*									
	|   1.1V  Native NMOS 	      |  nt11ll_ckt	| 0.3um	|0.4um |
	*--------------------------------------------------------------*									
	|   1.1V  HVT  NMOS	      |  nhvt11ll_ckt	|0.04um	|0.12um|
	*--------------------------------------------------------------*									
	|   1.1V  HVT  PMOS	      |  phvt11ll_ckt	|0.04um	|0.12um|
	*--------------------------------------------------------------*									
	|   1.1V  LVT  NMOS	      |  nlvt11ll_ckt	|0.04um	|0.12um|
	*--------------------------------------------------------------*									
	|   1.1V  LVT  PMOS	      |  plvt11ll_ckt	|0.04um	|0.12um|
	*--------------------------------------------------------------*									
	|	2.5V  NMOS	      |  n25ll_ckt	|0.27um	|0.32um|
	*--------------------------------------------------------------*									
	|	2.5V  PMOS	      |  p25ll_ckt	|0.27um	|0.32um|
	*--------------------------------------------------------------*									
	|  2.5V Native NMOS	      |  nt25ll_ckt	|1.2um	|0.4um |
	*--------------------------------------------------------------*									
	|  2.5V(OD 3.3V) NMOS	      |  nod33ll_ckt	|0.55um	|0.32um|
	*--------------------------------------------------------------*									
	|  2.5V(OD 3.3V) PMOS	      |  pod33ll_ckt	|0.44um	|0.32um|
	*--------------------------------------------------------------*									
	|  2.5V(OD 3.3V) Native NMOS  |  ntod33ll_ckt	|1.2um	|0.4um |
	*--------------------------------------------------------------*									
	|  2.5V(UD 1.8V) NMOS	      |  nud18ll_ckt	|0.24um	|0.32um|
	*--------------------------------------------------------------*									
	|  2.5V(UD 1.8V) PMOS	      |  pud18ll_ckt	|0.24um	|0.32um|
	*--------------------------------------------------------------*									
	|  2.5V(UD 1.8V) Native NMOS  |  ntud18ll_ckt	|1.2um	|0.4um |
	*--------------------------------------------------------------*									
	|  1.1V NMOS in DNW	      |  n11ll_dnw_ckt  |0.04um |0.12um|
	*--------------------------------------------------------------*									
	|  1.1V HVT NMOS in DNW	      |nhvt11ll_dnw_ckt |0.04um |0.12um|
	*--------------------------------------------------------------*									
	|  1.1V LVT NMOS in DNW	      |nlvt11ll_dnw_ckt |0.04um |0.12um|
	*--------------------------------------------------------------*									
	|  2.5V NMOS in DNW	      | n25ll_dnw_ckt   |0.27um |0.32um|
	*--------------------------------------------------------------*									
	|  2.5V (OD3.3V) NMOS in DNW  | nod33ll_dnw_ckt |0.55um |0.32um|
	*--------------------------------------------------------------*									
	|  2.5V (UD1.8V) NMOS in DNW  | nud18ll_dnw_ckt |0.24um |0.32um|
	*--------------------------------------------------------------*									

  	temperature range:-40C~125C

	b. BJT Model
        *--------------------------------------------------------* 
        |      BJT type     |     name             | Emitter Area|
        |========================================================|
        |   1.1V PNP_10X10  |  pnp12a100ll_ckt     | 10*10 um^2  |
        *--------------------------------------------------------* 
        |   1.1V PNP_5X5    |  pnp12a25ll_ckt      | 5*5 um^2    |
        *--------------------------------------------------------* 
        |   1.1V PNP_2X2    |  pnp12a4ll_ckt       | 2*2 um^2    |
        *--------------------------------------------------------* 
        |   2.5V PNP_10X10  |  pnp25a100ll_ckt     | 10*10 um^2  |
        *--------------------------------------------------------* 
        |   2.5V PNP_5X5    |  pnp25a25ll_ckt      | 5*5 um^2    |
        *--------------------------------------------------------* 
        |   2.5V PNP_2X2    |  pnp25a4ll_ckt       | 2*2 um^2    |
        *--------------------------------------------------------* 
        |   1.1V NPN_10X10  |  npn12a100ll_ckt     | 10*10 um^2  |
        *--------------------------------------------------------* 
        |   1.1V NPN_5X5    |  npn12a25ll_ckt      |  5*5 um^2   |
        *--------------------------------------------------------* 
        |   1.1V NPN_2X2    |  npn12a4ll_ckt       |  2*2 um^2   |
        *--------------------------------------------------------* 
        |   2.5V NPN_10X10  |  npn25a100ll_ckt     |  10*10 um^2 |
        *--------------------------------------------------------* 
        |   2.5V NPN_5X5    |  npn25a25ll_ckt      |  5*5 um^2   |
        *--------------------------------------------------------* 
        |   2.5V NPN_2X2    |  npn25a4ll_ckt       |  2*2 um^2   |
        *--------------------------------------------------------* 
        |   1.1V PNP_10X10  |  pnp12a100ll_sba_ckt | 10*10 um^2  |
        *--------------------------------------------------------*  
        |   1.1V PNP_5X5    |  pnp12a25ll_sba_ckt  | 5*5 um^2    |
        *--------------------------------------------------------* 
        |   1.1V PNP_2X2    |  pnp12a4ll_sba_ckt   | 2*2 um^2    |
        *--------------------------------------------------------* 
        |   2.5V PNP_10X10  |  pnp25a100ll_sba_ckt | 10*10 um^2  |
        *--------------------------------------------------------* 
        |   2.5V PNP_5X5    |  pnp25a25ll_sba_ckt  | 5*5 um^2    |
        *--------------------------------------------------------* 
        |   2.5V PNP_2X2    |  pnp25a4ll_sba_ckt   | 2*2 um^2    |
        *--------------------------------------------------------* 
        |   1.1V NPN_10X10  |  npn12a100ll_sba_ckt | 10*10 um^2  |
        *--------------------------------------------------------* 
        |   1.1V NPN_5X5    |  npn12a25ll_sba_ckt  |  5*5 um^2   |
        *--------------------------------------------------------* 
        |   1.1V NPN_2X2    |  npn12a4ll_sba_ckt   |  2*2 um^2   |
        *--------------------------------------------------------* 
        |   2.5V NPN_10X10  |  npn25a100ll_sba_ckt |  10*10 um^2 |
        *--------------------------------------------------------* 
        |   2.5V NPN_5X5    |  npn25a25ll_sba_ckt  |  5*5 um^2   |
        *--------------------------------------------------------* 
        |   2.5V NPN_2X2    |  npn25a4ll_sba_ckt   |  2*2 um^2   |
        *--------------------------------------------------------* 

        temperature range:-40C~125C

	c. Diode Model   
         *------------------------------------------------* 
        | Junction Diode type |     1.1V     |   2.5V    |  
        |================================================|
        |                     |   ndio11ll   |           |
        |      N+/PWELL       | ndio11llHVT  | ndio25ll  |
        |                     | ndio11llLVT  |           |
        |------------------------------------------------|
        |                     |   pdio11ll   |           |
        |      P+/NWELL       | pdio11llHVT  | pdio25ll  | 
        |                     | pdio11llLVT  |           |
        |------------------------------------------------|
        |   Native N+/Psub    |  ntdio11ll   | ntdio25ll |
        |------------------------------------------------|
        |      Nwell/Pwell    |          nwdioll         |  
        |------------------------------------------------|
        |      n+/rwell       |   dnd11ll    |  dnd25ll  |   
        |------------------------------------------------|
        |    rwell/dnwell     |          rwd11ll         |   
        |------------------------------------------------|
        |     dnwell/psub     |          dnwd11ll        | 
        *------------------------------------------------*
        |     nwell/psub      |parasitic_nwd | (na)      |
        |------------------------------------------------|
        |    rwell/dnwell     |parasitic_rwd | (na)      |
        |------------------------------------------------|
        |     dnwell/psub     |parasitic_dnwd| (na)      |
        *------------------------------------------------*

	temperature range:-40C~125C

        d. Resistor Model
        *--------------------------------------------------------------*  
        |       resistor type                       |   1.1v/2.5v      | 
        |==============================================================|  
        | silicide n+ diffusion (three terminal)    |     rndif_3t_ckt | 
        *--------------------------------------------------------------*  
        | silicide p+ diffusion(three terminal)     |     rpdif_3t_ckt | 
        *--------------------------------------------------------------*  
        | silicide n+ poly (three terminal)         |     rnpo_3t_ckt  | 
        *--------------------------------------------------------------*  
        | silicide p+ poly (three terminal)         |     rppo_3t_ckt  | 
        *--------------------------------------------------------------*  
        | nwell under sti(three terminal)           |     rnwsti_3t_ckt|
        *--------------------------------------------------------------*  
        | nwell under aa  (three terminal)          |     rnwaa_3t_ckt |
        *--------------------------------------------------------------*  
        | non-silicide n+ diffusion(three terminal) |  rndifsab_3t_ckt |
        *--------------------------------------------------------------*  
        | non-silicide p+ diffusion (three terminal)|  rpdifsab_3t_ckt |
        *--------------------------------------------------------------*  
        | non-silicide n+ poly (three terminal)     |    rnposab_3t_ckt|
        *--------------------------------------------------------------*  
        | non-silicide p+ poly (three terminal)     |   rpposab_3t_ckt |
        *--------------------------------------------------------------*  
        | non-silicide hr poly (three terminal)     |   rhrpo_3t_ckt   |
        *--------------------------------------------------------------*  
        | silicide n+ diffusion (two terminal)      |     rndif_2t_ckt | 
        *--------------------------------------------------------------*  
        | silicide p+ diffusion(two terminal)       |     rpdif_2t_ckt | 
        *--------------------------------------------------------------*  
        | silicide n+ poly (two terminal)           |     rnpo_2t_ckt  | 
        *--------------------------------------------------------------*  
        | silicide p+ poly (two terminal)           |     rppo_2t_ckt  | 
        *--------------------------------------------------------------*  
        | nwell under sti(two terminal)             |     rnwsti_2t_ckt|
        *--------------------------------------------------------------*  
        | nwell under aa  (two terminal)            |     rnwaa_2t_ckt |
        *--------------------------------------------------------------*  
        | non-silicide n+ diffusion(two terminal)   |  rndifsab_2t_ckt |
        *--------------------------------------------------------------*  
        | non-silicide p+ diffusion (two terminal)  |  rpdifsab_2t_ckt |
        *--------------------------------------------------------------*  
        | non-silicide n+ poly (two terminal)       |    rnposab_2t_ckt|
        *--------------------------------------------------------------*  
        | non-silicide p+ poly (two terminal)       |   rpposab_2t_ckt |
        *--------------------------------------------------------------*  
        | non-silicide hr poly (two terminal)       |   rhrpo_2t_ckt   |
        *--------------------------------------------------------------*  
        |          metal 1 (two terminal)           |      rm1_2t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 1 (three terminal)         |      rm1_3t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 2 (two terminal)           |      rm2_2t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 2 (three terminal)         |      rm2_3t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 3 (two terminal)           |      rm3_2t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 3 (three terminal)         |      rm3_3t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 4 (two terminal)           |      rm4_2t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 4 (three terminal)         |      rm4_3t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 5 (two terminal)           |      rm5_2t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 5 (three terminal)         |      rm5_3t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 6 (two terminal)           |      rm6_2t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 6 (three terminal)         |      rm6_3t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 7 (two terminal)           |      rm7_2t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 7 (three terminal)         |      rm7_3t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 8 (two terminal)           |      rm8_2t_ckt  |
        *--------------------------------------------------------------*  
        |          metal 8 (three terminal)         |      rm8_3t_ckt  |
        *--------------------------------------------------------------*  
        |        top metal 1 (two terminal)         |      rtm1_2t_ckt |  
        *--------------------------------------------------------------*  
        |        top metal 1 (three terminal)       |      rtm1_3t_ckt |
        *--------------------------------------------------------------*  
        |        top metal 2 (two terminal)         |      rtm2_2t_ckt |  
        *--------------------------------------------------------------*  
        |        top metal 2 (three terminal)       |      rtm2_3t_ckt |
        *--------------------------------------------------------------*  
        | Ultra Thick Tope Metal(two terminal)      |      rutm_2t_ckt |  
        *--------------------------------------------------------------*  
        | Ultra Thick Tope Metal(three terminal)    |      rutm_3t_ckt |  
        *--------------------------------------------------------------*  
        |  alpa (two terminal,thickness=1.45um)     |      ralpa_2t_ckt|
        *--------------------------------------------------------------* 
        |  alpa  (threeterminal,thickness=1.45um)   |      ralpa_3t_ckt|
        *--------------------------------------------------------------*  
        |  alpa (two terminal,thickness=2.8um)      |  ralpa_2p8_2t_ckt|
        *--------------------------------------------------------------* 
        |  alpa  (three terminal,thickness=2.8um)   |  ralpa_2p8_3t_ckt|
        *--------------------------------------------------------------*  
        temperature range:-40C~125C

       e. N+poly/NW MOS Varactor Model
        *---------------------------------------------------------------*
        |   mos varactor subckt   |      1.1v        |       2.5v       |
        |=========================|==================|==================|
        |     n+poly/nwell        |   pvar11ll_ckt   |   pvar25ll_ckt   | 
        *---------------------------------------------------------------*
        |     n+poly/dnwell       | dnwpvar11ll_ckt  |  dnwpvar25ll_ckt | 
        *---------------------------------------------------------------*
        |     p+poly/pwell        |   nvar11ll_ckt   |   nvar25ll_ckt   | 
        *---------------------------------------------------------------*
        |  p+poly/pwell in DNW    |  dnwnvar11ll_ckt |  dnwnvar25ll_ckt | 
        *---------------------------------------------------------------*
        temperature range:-40C~125C

        f.MOM model
        *----------------------------------------------------------------------------------------------*
        |                           40nm MOM Capacitor for 3-terminal and 2-terminal                   |
        *----------------------------------------------------------------------------------------------*
        |   MOM type |     name    |      L    |  Fix Width  |    Fix Space    |       Finger number   | 
        |==============================================================================================|
        |    M1~M6   |   mom_3t_ckt|   4~60um  |   0.07um    |     0.07um      |       20 ~ 400        |
        *--------------------------------------=-------------------------------------------------------*
        |    M1~M6   |   mom_2t_ckt|   4~60um  |   0.07um    |     0.07um      |       20 ~ 400        |
        *--------------------------------------=-------------------------------------------------------*
        temperature range:-40C~125C

   	g. LDMOS Model
	*--------------------------------------------------------------*									
	|	MOSFET	type	      | 	name	| Lmin	| Wmin |
	|==============================================================|									
	|	2.5V N LDMOS          |  nld50ll_ckt	| 0.28um| 2um  |
	*--------------------------------------------------------------*									
	|	2.5V P LDMOS 	      |  pld50ll_ckt	| 0.26um| 2um  |
	*--------------------------------------------------------------*									
	|   2.5V OD3.3V N LDMOS       |  nld50llod_ckt	| 0.28um| 2um  |
	*--------------------------------------------------------------*									
	|   2.5V OD3.3V P LDMOS       |  pld50llod_ckt	|0.26um	| 2um  |
	*--------------------------------------------------------------*									
        temperature range:-40C~125C
 
5. Corner Model 

      Five model corners are provided for MOSFETs, LDMOS.
      three model corners are provided for Diode,
      three model corners are provided for BJT.
      three model corners are provided for RES.
      three model corners are provided for Varactor.
      three model corners are provided for MOM.

      They are
        
      ----------------------------------------------------
      MOS        name : corner
      ----------------------------------------------------
                 TT : Typical case
                 SS : Slow case
                 FF : Fast case
                 SNFP : Slow N Fast P case    
                 FNSP : Fast N Slow P case    
      ----------------------------------------------------
      LDMOS      name : corner
      ----------------------------------------------------
                 LDMOS_TT : Typical case
                 LDMOS_SS : Slow case
                 LDMOS_FF : Fast case
                 LDMOS_FNSP : Slow N Fast P case    
                 LDMOS_SNFP : Fast N Slow P case    
      ----------------------------------------------------
      Diode      name : corner
      ----------------------------------------------------
                 DIO_TT : Typical case
                 DIO_SS : Slow case
                 DIO_FF : Fast case 
      ----------------------------------------------------
      BJT        name : corner
      ----------------------------------------------------
                 BJT_TT : Typical case
                 BJT_SS : Slow case
                 BJT_FF : Fast case 
      ----------------------------------------------------
      RES        name : corner
      ----------------------------------------------------
                 RES_TT : Typical case
                 RES_SS : Slow case
                 RES_FF : Fast case 
      ----------------------------------------------------
      Varactor   name : corner
      ----------------------------------------------------
                 VAR_TT : Typical case
                 VAR_SS : Slow case
                 VAR_FF : Fast case 
      ----------------------------------------------------
      MOM        name : corner
      ----------------------------------------------------
                 MOM_TT : Typical case
                 MOM_SS : Slow case
                 MOM_FF : Fast case 
      ----------------------------------------------------

6. Monte Carlo Statistical model
   Demo netlist
------------------------------------------------------------
simulator lang=spectre insensitive=yes
include "l0040ll_v1p4_1r_spe.lib" section=mos_mc
m1 (d1 g1 0 0 ) n11ll_ckt w=10e-6 l=0.04e-6
vd1 (d1 0) vsource dc=1.1
vg1 (g1 0) vsource dc=1.1
save vd1:currents
mc1 montecarlo variations=all numruns=500 donominal=no \
savefamilyplots=yes { 
 dc1 dc dev=vg1 param=dc  values=[1.1]
}
*---------------------------------------------------------*

7. Demo netlist for MOSFET mismatch model  (tt corner only)
*------------------------------------------------------------------*
//
simulator lang=spectre insensitive=yes
include "l0040ll_v1p4_1r_spe.lib" section=tt
vgs1 ( g1 0 ) vsource dc=1.1
vds1 ( d1 0 ) vsource dc=1.1
vds2 ( d2 0 ) vsource dc=1.1
m1 (d1 g1 0 0 ) n11ll_ckt w=10e-6 l=0.04e-6 mismod=1
m2 (d2 g1 0 0 ) n11ll_ckt w=10e-6 l=0.04e-6 mismod=1
save vds1:currents
save vds2:currents

mc1 montecarlo variations=mismatch seed=50 numruns=100 donominal=no \
savefamilyplots=yes { 
dc1 dc dev=vgs1 param=dc  values=[1.1]
dcOpInfo info what=oppoint extremes=yes
}

*-------------------------------------------------------------------*

8. Demo netlist for Resistor mismatch model (res_tt corner only)
*------------------------------------------------------------------*
//
simulator lang=spectre insensitive=yes
include "l0040ll_v1p4_1r_spe.lib" section=res_tt
include "l0040ll_v1p4_1r_res_spe.ckt"


xnposab1 (n1 n2) rnposab_3t_ckt w=1u l=8u mismod=1
vn1 (n1 0) vsource dc=1
vn2 (n2 0) vsource dc=0

xnposab2 (n3 n4) rnposab_3t_ckt w=1u l=8u mismod=1
vn3 (n3 0) vsource dc=1
vn4 (n4 0) vsource dc=0

save vn1:currents 
save vn3:currents 

mc1 montecarlo variations=mismatch seed=50 numruns=100 donominal=no \ 
savefamilyplots=yes {  

 dc1 dc dev=vn2 param=dc  values=[0]
 dcOpInfo info what=oppoint extremes=yes

 } 

*-------------------------------------------------------------------*

9. Demo netlist for MOM capacitor mismatch model(mom_tt corner only)
*------------------------------------------------------------------*

//QA for MOM mismatch model
simulator lang=spectre
include "l0040ll_v1p4_1r_spe.lib" section=mom_tt
SetTempOption options temp=25
V1 (1 0) vsource dc=0
X1 (2 0) mom_3t_ckt l=5 nn=20 bm=1 tm=2 mm=1 mismod=1
X2 (3 0) mom_3t_ckt l=5 nn=20 bm=1 tm=2 mm=1 mismod=1
R1 (1 2) resistor r=1e-3
R2 (1 3) resistor r=1e-3

mc1 montecarlo variations=mismatch seed=50 numruns=100 donominal=no \
savefamilyplots=yes { 
dc1 dc dev=V1 param=dc  values=[1.0]
dcOpInfo info what=oppoint extremes=yes
}

*-------------------------------------------------------------------*

10. Parameter alignment between model, PDK and techfiles.

*=========================================================================================================================================================================================*
|               |      scale         |            flag_cc              |        prelayout            |           mismod           |           globalmod           |        LPEMOD         |
|   Parameters  |--------------------|---------------------------------|-----------------------------|----------------------------|-------------------------------|-----------------------|
|               |(scaling settings)  |coupling capacitance of resistor)|(contact-gate capacitance)   |(mismatch simulation switch)|(global variation simu. switch)|(LPE simulation switch)|
|               |                    |(0=turn off; 1=turn on)          |(0=turn off; 1=turn on)      |(0=turn off; 1=turn on)     |(0=turn off; 1=turn on)        |(0=turn off; 1=turn on)|    
*=========================================================================================================================================================================================*
|     PDK       |ADE scale option=0.9|            default=1            |        default=1            |          default=1         |          default=1            |        default=1      |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      | HSPICE |  scale=0.9         |  default=0  (use additional     |  default=0 (use additional  |          default=1         |          default=1            |        default=1      |
|      |        |                    |  corner to control)             |corner to control)           |                            |                               |                       |
| Model|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      | Spectre|  scale=0.9         |  default=0  (use additional     |  default=0 (use additional  |          default=1         |          default=1            |        default=1      |
|      |        |                    |  corner to control)             |corner to control)           |                            |                               |                       |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     LVS       |        NA          |            always = 0           |        always = 0           |          default=1         |          default=1            |        default=1      |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     RCX       |  scale=0.9         |  always extract coupling cap    |always extract cont-gate cap |             N/A            |             N/A               |           N/A         |
*=========================================================================================================================================================================================*

