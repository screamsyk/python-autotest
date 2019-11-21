import pyautogui

# ------地图默认视图------

map_view = {
    'center': [106.5590013579515, 29.55910442310595],
    'zoom': 12
}
baidu_map_view = {
    'lng': 11862973.251148952,
    'lat': 3426754.14429871,
    'zoom': 13.590195544218748
}


# ------ autogui 方式------

# 鼠标滚动
scrolls = []
scrolls.extend([-1000 for i in range(8)])
scrolls.extend([1000 for i in range(15)])

# 鼠标拖动（构造螺旋形路径）
screen_width, screen_height = pyautogui.size()  # 屏幕大小
center_x, center_y = screen_width/2, screen_height/2
drags = []
direction = 'bottom'  # 拖动方向
drag_num = 0  # 方向上的拖动次数
drag_add_num = 1  # 每次增加的次数
for i in range(50):
    if direction == 'bottom':  # 向下
        drag_num = drag_num+drag_add_num
        drags.extend([{'from': (center_x, center_y+300),
                       'to': (center_x, center_y-300)} for i in range(drag_num)])
        direction = 'right'
    elif direction == 'right':  # 向右
        drags.extend([{'from': (center_x-300, center_y),
                       'to': (center_x+300, center_y)} for i in range(drag_num)])
        direction = 'top'
    elif direction == 'top':  # 向上
        drag_num = drag_num+drag_add_num
        drags.extend([{'from': (center_x, center_y-300),
                       'to': (center_x, center_y+300)} for i in range(drag_num)])
        direction = 'left'
    elif direction == 'left':  # 向左
        drags.extend([{'from': (center_x+300, center_y),
                       'to': (center_x-300, center_y)} for i in range(drag_num)])
        direction = 'bottom'

# drags.extend([{'from': (screen_width/2-300, screen_height/2),
#                'to': (screen_width/2+300, screen_height/2)} for i in range(8)])
# drags.extend([{'from': (screen_width/2+300, screen_height/2),
#                'to': (screen_width/2-300, screen_height/2)} for i in range(20)])
# drags.extend([{'from': (screen_width/2-300, screen_height/2),
#                'to': (screen_width/2+300, screen_height/2)} for i in range(10)])
# drags.extend([{'from': (screen_width/2+200, screen_height/2-200),
#                'to': (screen_width/2-200, screen_height/2+200)} for i in range(20)])


# ------ javascript 方式------

# 地图缩放所需的层级
zooms = list(range(6, 19))
zooms.extend(list(range(6, 18))[::-1])

# 地图移动所需的点
points = [
    [106.58358236184552, 29.568401400553967],
    [106.5773400083184, 29.576209652480216],
    [106.56810935141812, 29.579301541758312],
    [106.56155403267655, 29.578723044035854],
    [106.54526097648875, 29.57744124108754],
    [106.53671145677572, 29.572366328315155],
    [106.53564952893794, 29.56784147266349],
    [106.52653680974663, 29.56594566749412],
    [106.5168713074629, 29.56499418226028],
    [106.50655649726855, 29.566978939712],
    [106.49948084094342, 29.571019355720992],
    [106.48374869196732, 29.57732283009649],
    [106.4878881244374, 29.581553644573887],
    [106.50590989112573, 29.58463340460733],
    [106.51532264219884, 29.583062600812084],
    [106.52822063052008, 29.58330364908892],
    [106.53497979724239, 29.585608185295143],
    [106.54209547687424, 29.5879572636632],
    [106.55415331362747, 29.59161901488767],
    [106.56870542066144, 29.595413056819936],
    [106.5524552470041, 29.606449557668427],
    [106.5444729044591, 29.60665477504041],
    [106.53523537672777, 29.60593651254881],
    [106.54034230282718, 29.602643632665163],
    [106.55154127097876, 29.597242350658604],
    [106.57312928489182, 29.588846543622324],
    [106.5941362282233, 29.579922139325973],
    [106.57528394609244, 29.569807609727818],
    [106.56350020788523, 29.555106419034217],
    [106.54265942987774, 29.545552162785],
    [106.55401944254959, 29.530276423287347],
    [106.56823571793052, 29.521222576182865],
    [106.55538320662595, 29.511531662754308],
    [106.53220494490574, 29.512926842223436],
    [106.50911210831873, 29.51334680398361],
    [106.49057328766082, 29.51918015306103],
    [106.48399876072335, 29.526531595043423],
    [106.4818416421324, 29.531951425974256],
    [106.47502420955368, 29.536520238470274],
    [106.47858570234052, 29.541768670821412],
    [106.46926410147171, 29.550269644541885],
    [106.47732353500533, 29.554337342335046],
    [106.48813618111603, 29.559226283213874],
    [106.49502262263991, 29.566923611425395],
    [106.5119304331323, 29.57025136178501],
    [106.52885294899374, 29.575845169808062],
    [106.55547806209756, 29.575917135784138],
    [106.569038036596, 29.577479343360793],
    [106.59071653555088, 29.581906674719832],
    [106.6021540615742, 29.584822793488954],
    [106.6206115246373, 29.595649299127288],
    [106.60329555288536, 29.60079693432411],
    [106.58291180443882, 29.601401100498407],
    [106.5593669276684, 29.60450636705498],
    [106.53760391451021, 29.59820349474667],
    [106.51875401154325, 29.606963145946892],
    [106.49827669000183, 29.602207544112105],
    [106.48163476014304, 29.60605343784185],
    [106.4609836753292, 29.6155161013304],
    [106.48259435205466, 29.61595965511691],
    [106.49509642565658, 29.61990252982058],
    [106.50885216883967, 29.626202819778996],
    [106.52223955680392, 29.626937621830336],
    [106.53056565456745, 29.631978889663756],
    [106.53604790087434, 29.63592919976537],
    [106.5468851503332, 29.643235809868898],
    [106.53323000386138, 29.651083335441953],
    [106.50893676847284, 29.649201628063196],
    [106.49586546699788, 29.648085441353743],
    [106.46917124763615, 29.645786631853866],
    [106.45985871565688, 29.6541033319118],
    [106.48319773908088, 29.659334018567748],
    [106.49124436623993, 29.66054602407928],
    [106.50125676106632, 29.663069801761083],
    [106.51901870648794, 29.66899001915148],
    [106.53607826076495, 29.67970608932208],
    [106.51576669307292, 29.66900706500617],
    [106.49422197177853, 29.66042843068624],
    [106.47857363375783, 29.65066866345768],
    [106.46290833331432, 29.63960155663102],
    [106.45422361206909, 29.630913148509293],
    [106.43028577105497, 29.62356976614609],
    [106.41456794244311, 29.617490764830137],
    [106.39265476764763, 29.60822279144213],
    [106.40440401667911, 29.599130553491946],
    [106.37792702749175, 29.594171899880408],
    [106.35441557812806, 29.591109338726966],
    [106.33162353427929, 29.586544704182685],
    [106.3073441757465, 29.581465121905396],
    [106.28828597580991, 29.581254134319366],
    [106.26457286601953, 29.5863664346234],
    [106.2890392450895, 29.593350836642017],
    [106.27146476973292, 29.603539715339693],
    [106.28124617718049, 29.606718041521844],
    [106.3080537164717, 29.605786816151422],
    [106.33272356278303, 29.604158542956128],
    [106.35997221310186, 29.595786578578355],
    [106.38323548666631, 29.590950798449896],
    [106.40454978848777, 29.602426744150932],
    [106.41766405748047, 29.611055906719713],
    [106.41591021927889, 29.620478446351484],
    [106.49514029769398, 29.615992152374687]
]
