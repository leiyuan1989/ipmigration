.title DiffOpamp
* DiffOpamp
* Include device models
.lib '../models/hspice/ms018_v1p7.lib' tt
.option scale=1e-6
.options savecurrents

.param w1 = {w1}  l1 = {l1}  w2 = {w2}  l2 = {l2}  w3 = {w3}  l3 = {l3}  w4 = {w4}  l4 = {l4}	w5 = {w5}  l5 = {l5}   cc={cc}  cr={cr}  

* the power supply 3.3 V and current bias
Vdd dd 0 3.3
ibias dd net7 dc {ib}

* the input signal for dc and tran simulation
vin inn 0 dc 1.65 ac -0.5
vip inp 0 dc 1.65 ac 0.5

* the circuit
.include    '../ckt_netlist/twoStageOpamp2.cir' 
Xopamp dd 0 inp inn net7 out  diff_opamp
cl out 0 2pf

* control language script
.control
op
*ac DEC 10 0.1 100e9
save all @m.xopamp.m1[vdsat] @m.xopamp.m2[vdsat] @m.xopamp.m3[vdsat] @m.xopamp.m4[vdsat] @m.xopamp.m5[vdsat] @m.xopamp.m6[vdsat] @m.xopamp.m7[vdsat] @m.xopamp.m8[vdsat]

wrdata $inputdir/old_data_output_filename @m.xopamp.m1[vdsat] @m.xopamp.m2[vdsat] @m.xopamp.m3[vdsat] @m.xopamp.m4[vdsat] @m.xopamp.m5[vdsat] @m.xopamp.m6[vdsat] @m.xopamp.m7[vdsat] @m.xopamp.m8[vdsat]

.endc
.end

