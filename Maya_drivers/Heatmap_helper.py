import maya.api.OpenMaya as api
import time 
def apply_api_colors(colors, indices, obj):
     start = time.time()
     colors = [api.MColor(i) for i in colors]
     selectionList = api.MSelectionList()
     selectionList.add(obj)
     nodeDagPath = selectionList.getDagPath(0)
     mfnMesh = api.MFnMesh(nodeDagPath)
     mfnMesh.setVertexColors(colors, indices)
     end = time.time()
     print("it took", end - start, " seconds for rig " + obj)
def only_show_mouth(obj, indices):
    new_list = []
    for i in range(1, 5064):
        if not i in indices:
        # if True:
            new_list.append(i)
    cols = [(0, 0, 0, 0) for i in new_list]
    colors = [api.MColor(i) for i in cols]
    selectionList = api.MSelectionList()
    selectionList.add(obj)
    nodeDagPath = selectionList.getDagPath(0)
    mfnMesh = api.MFnMesh(nodeDagPath)
    mfnMesh.setVertexColors(colors, new_list)
def get_key_vertices():
    vertex_list = []
    # [u'vocal_error_disp.vtx[359:367]', u'vocal_error_disp.vtx[380]', u'vocal_error_disp.vtx[391:402]', u'vocal_error_disp.vtx[417]', u'vocal_error_disp.vtx[458:461]', u'vocal_error_disp.vtx[510:511]', u'vocal_error_disp.vtx[558:561]', u'vocal_error_disp.vtx[576:577]', u'vocal_error_disp.vtx[579:580]', u'vocal_error_disp.vtx[584:591]', u'vocal_error_disp.vtx[594:613]', u'vocal_error_disp.vtx[622:629]', u'vocal_error_disp.vtx[746]', u'vocal_error_disp.vtx[771:774]', u'vocal_error_disp.vtx[795:798]', u'vocal_error_disp.vtx[938:939]', u'vocal_error_disp.vtx[963:968]', u'vocal_error_disp.vtx[990:996]', u'vocal_error_disp.vtx[1106:1107]', u'vocal_error_disp.vtx[1110:1117]', u'vocal_error_disp.vtx[1124:1125]', u'vocal_error_disp.vtx[1127:1137]', u'vocal_error_disp.vtx[1154]', u'vocal_error_disp.vtx[1157:1164]', u'vocal_error_disp.vtx[1166:1167]', u'vocal_error_disp.vtx[1170]', u'vocal_error_disp.vtx[1172]', u'vocal_error_disp.vtx[1174]', u'vocal_error_disp.vtx[1176:1185]', u'vocal_error_disp.vtx[1190]', u'vocal_error_disp.vtx[1201:1207]', u'vocal_error_disp.vtx[1209:1233]', u'vocal_error_disp.vtx[1267:1270]', u'vocal_error_disp.vtx[1338:1351]', u'vocal_error_disp.vtx[1386:1391]', u'vocal_error_disp.vtx[1430:1431]', u'vocal_error_disp.vtx[1435:1440]', u'vocal_error_disp.vtx[1558:1575]', u'vocal_error_disp.vtx[1939:1945]', u'vocal_error_disp.vtx[2062]', u'vocal_error_disp.vtx[2064]', u'vocal_error_disp.vtx[2073]', u'vocal_error_disp.vtx[2103:2110]', u'vocal_error_disp.vtx[2136:2140]', u'vocal_error_disp.vtx[2144:2158]', u'vocal_error_disp.vtx[2160:2161]', u'vocal_error_disp.vtx[2475:2476]', u'vocal_error_disp.vtx[2481:2483]', u'vocal_error_disp.vtx[2935:2938]', u'vocal_error_disp.vtx[2987:2988]', u'vocal_error_disp.vtx[3035:3038]', u'vocal_error_disp.vtx[3053:3054]', u'vocal_error_disp.vtx[3061:3068]', u'vocal_error_disp.vtx[3071:3090]', u'vocal_error_disp.vtx[3099:3106]', u'vocal_error_disp.vtx[3248:3251]', u'vocal_error_disp.vtx[3272:3275]', u'vocal_error_disp.vtx[3415:3416]', u'vocal_error_disp.vtx[3440:3445]', u'vocal_error_disp.vtx[3467:3473]', u'vocal_error_disp.vtx[3583:3584]', u'vocal_error_disp.vtx[3587:3594]', u'vocal_error_disp.vtx[3601:3614]', u'vocal_error_disp.vtx[3631]', u'vocal_error_disp.vtx[3634:3639]', u'vocal_error_disp.vtx[3643:3644]', u'vocal_error_disp.vtx[3647]', u'vocal_error_disp.vtx[3649]', u'vocal_error_disp.vtx[3651]', u'vocal_error_disp.vtx[3653:3656]', u'vocal_error_disp.vtx[3659:3662]', u'vocal_error_disp.vtx[3667]', u'vocal_error_disp.vtx[3678:3685]', u'vocal_error_disp.vtx[3689:3702]', u'vocal_error_disp.vtx[3705:3710]', u'vocal_error_disp.vtx[3744:3747]', u'vocal_error_disp.vtx[3815:3816]', u'vocal_error_disp.vtx[3818:3828]', u'vocal_error_disp.vtx[3863:3868]', u'vocal_error_disp.vtx[3907:3908]', u'vocal_error_disp.vtx[3912:3917]', u'vocal_error_disp.vtx[4035:4052]', u'vocal_error_disp.vtx[4416:4422]', u'vocal_error_disp.vtx[4541]', u'vocal_error_disp.vtx[4546]', u'vocal_error_disp.vtx[4550]', u'vocal_error_disp.vtx[4580:4587]', u'vocal_error_disp.vtx[4613:4617]', u'vocal_error_disp.vtx[4621:4635]', u'vocal_error_disp.vtx[4637:4638]', u'vocal_error_disp.vtx[4934:4935]', u'vocal_error_disp.vtx[4940:4942]']
    tim = cmds.ls( selection=True, shortNames=True)
    for item in tim:
        values = item.split("[")[1]
        if len(values.split(":")) == 2:
            start = int(values.split(":")[0])
            end = int(values.split(":")[1][:-1])
            for j in range(start, end+1):
                vertex_list.append(j)
        else:
            vertex_list.append(int(values[:-1]))
    print(vertex_list)
vertices = [359, 360, 361, 362, 363, 364, 365, 366, 367, 380, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 417, 458, 459, 460, 461, 510, 511, 558, 559, 560, 561, 576, 577, 579, 580, 584, 585, 586, 587, 588, 589, 590, 591, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 622, 623, 624, 625, 626, 627, 628, 629, 746, 771, 772, 773, 774, 795, 796, 797, 798, 938, 939, 963, 964, 965, 966, 967, 968, 990, 991, 992, 993, 994, 995, 996, 1106, 1107, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1124, 1125, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1134, 1135, 1136, 1137, 1154, 1157, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1166, 1167, 1170, 1172, 1174, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1190, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1267, 1268, 1269, 1270, 1338, 1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1386, 1387, 1388, 1389, 1390, 1391, 1430, 1431, 1435, 1436, 1437, 1438, 1439, 1440, 1558, 1559, 1560, 1561, 1562, 1563, 1564, 1565, 1566, 1567, 1568, 1569, 1570, 1571, 1572, 1573, 1574, 1575, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 2062, 2064, 2073, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2136, 2137, 2138, 2139, 2140, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2151, 2152, 2153, 2154, 2155, 2156, 2157, 2158, 2160, 2161, 2475, 2476, 2481, 2482, 2483, 2935, 2936, 2937, 2938, 2987, 2988, 3035, 3036, 3037, 3038, 3053, 3054, 3061, 3062, 3063, 3064, 3065, 3066, 3067, 3068, 3071, 3072, 3073, 3074, 3075, 3076, 3077, 3078, 3079, 3080, 3081, 3082, 3083, 3084, 3085, 3086, 3087, 3088, 3089, 3090, 3099, 3100, 3101, 3102, 3103, 3104, 3105, 3106, 3248, 3249, 3250, 3251, 3272, 3273, 3274, 3275, 3415, 3416, 3440, 3441, 3442, 3443, 3444, 3445, 3467, 3468, 3469, 3470, 3471, 3472, 3473, 3583, 3584, 3587, 3588, 3589, 3590, 3591, 3592, 3593, 3594, 3601, 3602, 3603, 3604, 3605, 3606, 3607, 3608, 3609, 3610, 3611, 3612, 3613, 3614, 3631, 3634, 3635, 3636, 3637, 3638, 3639, 3643, 3644, 3647, 3649, 3651, 3653, 3654, 3655, 3656, 3659, 3660, 3661, 3662, 3667, 3678, 3679, 3680, 3681, 3682, 3683, 3684, 3685, 3689, 3690, 3691, 3692, 3693, 3694, 3695, 3696, 3697, 3698, 3699, 3700, 3701, 3702, 3705, 3706, 3707, 3708, 3709, 3710, 3744, 3745, 3746, 3747, 3815, 3816, 3818, 3819, 3820, 3821, 3822, 3823, 3824, 3825, 3826, 3827, 3828, 3863, 3864, 3865, 3866, 3867, 3868, 3907, 3908, 3912, 3913, 3914, 3915, 3916, 3917, 4035, 4036, 4037, 4038, 4039, 4040, 4041, 4042, 4043, 4044, 4045, 4046, 4047, 4048, 4049, 4050, 4051, 4052, 4416, 4417, 4418, 4419, 4420, 4421, 4422, 4541, 4546, 4550, 4580, 4581, 4582, 4583, 4584, 4585, 4586, 4587, 4613, 4614, 4615, 4616, 4617, 4621, 4622, 4623, 4624, 4625, 4626, 4627, 4628, 4629, 4630, 4631, 4632, 4633, 4634, 4635, 4637, 4638, 4934, 4935, 4940, 4941, 4942]
print(len(vertices))
only_show_mouth("Jali_error_disp", vertices )
only_show_mouth("vocal_error_disp", vertices)
only_show_mouth("Jali_error_vel", vertices)
only_show_mouth("vocal_error_vel", vertices)
