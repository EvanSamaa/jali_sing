# test = cmds.createNode( 'pairBlend', n='Ih_pointer'+'_pairBlend_M_Vnot' )
# Connect the translation of two nodes together
# cmds.connectAttr( 'Pitch_Sensitivity.pitch_sensitivity', 'Ih_pointer'+'_pairBlend_M_Vnot.weight' )

VOWELS_JALI = set(
    ["Ih_pointer", "Ee_pointer", "Eh_pointer", "Aa_pointer", "U_pointer", "Uh_pointer", "Oo_pointer", "Oh_pointer",
     "Schwa_pointer", "Eu_pointer", "Ah_pointer"])
CONSONANTS_JALI = set(
    ["BP_pointer", "M_pointer", "JY_pointer", "Th_pointer", "ShChZh_pointer", "SZ_pointer", "GK_pointer",
     "LNTD_pointer", "R_pointer", "W_pointer", "FV_pointer"])
CONSONANTS_NOJAW_JALI = set(
    ["Ya_pointer", "Ja_pointer", "Ra_pointer", "FVa_pointer", "LNTDa_pointer", "Ma_pointer", "BPa_pointer",
     "Wa_pointer", "Tha_pointer", "GKa_pointer"])

JALI_SLIDERS_SET = set.union(VOWELS_JALI, CONSONANTS_JALI, CONSONANTS_NOJAW_JALI)

for item in list(JALI_SLIDERS_SET):
    try:
        cmds.delete(item + '_pairBlend_M_Pnot')
        cmds.delete(item + '_pairBlend_M_P')
        cmds.delete(item + '_pairBlend_P')
    except:
        pass
    try:
        cmds.delete(item + '_Mnot_Pnot')
    except:
        pass
    try:
        cmds.delete(item + '_M_Pnot')
    except:
        pass
    try:
        cmds.delete(item + '_Mnot_P')
    except:
        pass
    try:
        cmds.delete(item + '_M_P')
    except:
        pass

    # this blends between two sets of musical articulation without pitch sensitivity
    cmds.createNode('pairBlend', n=item + '_pairBlend_M_Pnot')
    # this blends between two sets of musical articulation with pitch sensitivity
    cmds.createNode('pairBlend', n=item + '_pairBlend_M_P')
    # this blends between two sets of musical articulation with pitch sensitivity
    cmds.createNode('pairBlend', n=item + '_pairBlend_P')
    cmds.connectAttr('Musical_Articulation.musical_articulation', item + '_pairBlend_M_P.weight')
    cmds.connectAttr('Musical_Articulation.musical_articulation', item + '_pairBlend_M_Pnot.weight')
    cmds.connectAttr('Pitch_Sensitivity.pitch_sensitivity', item + '_pairBlend_P.weight')
    cmds.connectAttr(item + '_pairBlend_M_P.outTranslateX', item + '_pairBlend_P.inTranslateX2')
    cmds.connectAttr(item + '_pairBlend_M_Pnot.outTranslateX', item + '_pairBlend_P.inTranslateX1')
    cmds.connectAttr(item + '_pairBlend_P.outTranslate.outTranslateX', item + '.translate.translateY')

    cmds.createNode('animCurveTL', n=item + '_M_P')
    cmds.createNode('animCurveTL', n=item + '_Mnot_P')
    cmds.createNode('animCurveTL', n=item + '_M_Pnot')
    cmds.createNode('animCurveTL', n=item + '_Mnot_Pnot')

    cmds.connectAttr(item + '_M_P.output', item + '_pairBlend_M_P.inTranslateX2')
    cmds.connectAttr(item + '_Mnot_P.output', item + '_pairBlend_M_P.inTranslateX1')
    cmds.connectAttr(item + '_M_Pnot.output', item + '_pairBlend_M_Pnot.inTranslateX2')
    cmds.connectAttr(item + '_Mnot_Pnot.output', item + '_pairBlend_M_Pnot.inTranslateX1')

vowel_mod_sliders = [["Dimple", "Dimple"], ["Pucker", "Pucker"],
                     ["Ee_pointer", "lipCornerPull"], ["Ee_pointer", "lipStretch"],
                     ["Eh_pointer", "lipCornerPull"], ["Eh_pointer", "lipStretch"],
                     ["Oo_pointer", "lipPucker"], ["U_pointer", "lipPucker"]]
for item in list(vowel_mod_sliders):
    try:
        cmds.delete(item[0] + "_" + item[1] + '_M')
    except:
        pass
    try:
        cmds.delete(item[0] + "_" + item[1] + '_Mnot')
    except:
        pass
    try:
        cmds.delete('pairBlend', n=item[0] + "_" + item[1] + '_pairBlend_M')
    except:
        pass
    cmds.createNode('pairBlend', n=item[0] + "_" + item[1] + '_pairBlend_M')
    cmds.connectAttr('Musical_Articulation.musical_articulation', item[0] + "_" + item[1] + '_pairBlend_M.weight')
    cmds.createNode('animCurveTL', n=item[0] + "_" + item[1] + '_M')
    cmds.createNode('animCurveTL', n=item[0] + "_" + item[1] + '_Mnot')
    cmds.connectAttr(item[0] + "_" + item[1] + '_M.output', item[0] + "_" + item[1] + '_pairBlend_M.inTranslateX2')
    cmds.connectAttr(item[0] + "_" + item[1] + '_Mnot.output', item[0] + "_" + item[1] + '_pairBlend_M.inTranslateX1')
    cmds.connectAttr(item[0] + "_" + item[1] + '_pairBlend_M.outTranslate.outTranslateX', item[0] + "." + item[1])












