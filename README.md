
# 说明

目标一共有两个，一个是[Intel官方地图](https://www.ingress.com/intel)，另一个是游戏使用的API

本文只做相关API赏析，请不要做违反[TOS](https://www.ingress.com/terms)的事情
# Intel Map

## 获取API

1. 登录Google账户后，打开intel界面，Chrome打开Network选项卡
2. 刷新页面来获取一下所有xhr请求
![chrome](https://ww1.sinaimg.cn/large/006tNbRwgw1farvi9y1ymj30qq0tujvn.jpg)
3. 这些`get*`的请求就是ingress的API了，不着急，一个一个看

## 注意事项

1. HTTP Request Headers里有一个`x-csrftoken`,具体释义请翻各类白帽子教程。这个参数的值和Cookie的csrftoken相同![csrftoken-same-cookie](https://ww4.sinaimg.cn/large/006tNbRwgw1farvqqqf7mj30r20vi12i.jpg)
2. HTTP Request Headers里面有一堆以`:`开头的参数，将之忽略也不要紧
3. ingress所有API都是POST JSON数据交互，所以HTTP Method和Conten-Type确定,下面不再重复了
4. 贯穿Intel Map API的参数v相当于Session，至于如何获取，请在登录状态下看Intel主页源码最后，js的名字就包含了v值，即下图打码的部分![v](http://ww3.sinaimg.cn/large/006tNbRwgw1farw1l250nj31kw0atdkd.jpg)

## getGameScore

显而易见，这个API用来得到整个游戏的比分

	API URL: https://www.ingress.com/r/getGameScore
	API Request: v,
	API Response: result: [Enl, Res],

**example**:


![getGameScore](https://ww3.sinaimg.cn/large/006tNbRwgw1farw9fbte8j31fc06sgnj.jpg)
![getGameScore](https://ww3.sinaimg.cn/large/006tNbRwgw1farw6qgzgwj30ac05wq37.jpg)


## getRegionScoreDetails

这个API用来得到当前那区域的比分

	API URL: https://www.ingress.com/r/getRegionScoreDetails
	API Request: latE6, lngE6, v,
	API Response: result: {gameScore: [Res, Enl], regionName, regionVertices: [[Res, Enl], ...], scoreHistory: [[id, Enl, Res], ...], timeToEndOfBaseCycleMs, topAgents:[{nick, team}]}

	具体latE6,lngE6看下面getEntities API



**example**:
![code](http://ww1.sinaimg.cn/large/006tNbRwgw1fasr0bg6ehj31kw0aiwhd.jpg)
![getRegionScoreDetails](https://ww2.sinaimg.cn/large/006tNbRwgw1fasqwpmodij30jy1csaf2.jpg)
![getRegionScoreDetails](https://ww4.sinaimg.cn/large/006tNbRwgw1fasqwqamvwj30k00pywgy.jpg)


## getEntities

这个是用来获取Entity,也就是link, field, portal的

	API URL: https://www.ingress.com/r/getEntities
	API Request: tileKeys: [tilename1, tilename2, ...], v,
	API Response: result: {map: {tilename1: {gameEntities: [[guid, time, [type, faction, guid1, Lng1, Lat1, ...]], ...]}, ...}}

来解释一下各个变量都是什么意思

tileKeys是一个字符串，表示一个矩形，是一个可控参数的高级MBR(最小单元矩阵)，这是典型二维地图的查询参数，具体格式为`zoom_x_y_minlevel_maxlevel_health`，其中zoom表示区域放大的级别（恰好是Cookie中ingress.intelmap.zoom的值，点一次+或-按钮，地图缩放，值±1,在intel上，这个值得范围是3-21，最大时，显示的portal越少，范围越小）；x，y表示当前zoom的区域编号，可以参考[tilenames](http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames)

后面三个就简单了，最小,对应Intel上选择Level和Health的三个值，即最小po等级，最大po等级，最大健康百分比

这是涉及到tilename中的经纬度和实际经纬度的转换，参考[github-iitc](https://github.com/iitc-project/ingress-intel-total-conversion/blob/7dc38a89e708318eb94c201d9cc6f2b5e158ab36/code/map_data_calc_tools.js#L159)

下面的代码是进行经纬tile互转的
![lat-lng](https://ww4.sinaimg.cn/large/006tNbRwgw1farzd3oygpj31kw0q7jx0.jpg)

另外，返回值的Lng_x_, Lat_x_,是6位小数，time是确定到毫秒的Unix时间戳

guid是每一个entity的标识，所有用户，物品，link，portal，...都具有唯一标识guid

type是指这个entity的类型，e: lin(后面直接跟6个元素，两组guid经纬度), r: field(后面是一个list，三组guid经纬度), p: portal(一组guid经纬度,之后是等级，能量(0.0-100.0),脚数，po图，po名，[], false, false, null(这4个不太懂是啥), 更新时间戳)

faction代表阵营，E: Enl, R: Res

**example**

![code](https://ww4.sinaimg.cn/large/006tNbRwgw1farzwpfnizj31g20aowh0.jpg)
太长了，贴个部分
![example](https://ww2.sinaimg.cn/large/006tNbRwgw1farzyfwdnwj31kw1astif.jpg)


## getPortalDetails

用来获取portal的详细信息

	API URL: https://www.ingress.com/r/getPortalDetail
	API Request: guid, v
	API Response: result: [type, faction, lng, lat, level, energy, resonator_nums, picurl, name, [], false, false, null, updatetime, [[agentname, modtype, modlevel, {a: value, b: value}],...], [['agentname', resonator_level, energy],...], belongs, ["", "", []]]

意义很明确了，就是portal的详细信息

{a: value, b: value}表示的是mod的效果，看下面的图很容易理解

**example**

![code](http://ww1.sinaimg.cn/large/006tNbRwgw1fas0j4xa0aj31h80amq5m.jpg)
![example1](https://ww1.sinaimg.cn/large/006tNbRwgw1fas0ggoxy3j31fk1c4jz2.jpg)
![example2](https://ww1.sinaimg.cn/large/006tNbRwgw1fas0gkdjpej314c1ccgp5.jpg)
![example3](https://ww3.sinaimg.cn/large/006tNbRwgw1fas0gn6bk8j30hi07m74b.jpg)

## getArtifactPortals

猜测是查看是否生成新的portal

	API URL: https://www.ingress.com/r/getArtifactPortals
	API Request: v
	APi Resonse: 同上

## getPlexts

用来获得comm信息

	API URL: https://www.ingress.com/r/getPlexts
	API Request: ascendingTimestampOrder, maxLatE6, maxLngE6, minLatE6 , minLngE6, maxTimestampMs, minTimestampMs, tab, v
	API Response: result: [[guid, updatetime, {plext: {categories, plextType, team, text, markup: [#]}}],...]
	根据不同的categories(1=all, 2=faction)，不同plextType，markup的list不同，说明一下#的内容
	SYSTEM_BROADCAST：
		[PLATER: {plain, team}], [TEXT: {plain}], [PORTAL: {name, address, latE6, lngE6, name, plain, team}], [TEXT: {plain}], [TEXT: {plain}], [TEXT: {plain}]
		后面三个是消息尾部，比如 '-' '28' 'Mus'
		也有可能是2个尾部，比如[TEXT] [PORTAL]
		也有可能没有消息尾部，比如destroyed行为
	PLAYER_GENERATED：
		[SECURE: {plain}]
		[SENDER: {plain, team}], [TEXT: {plain}] [AT_PLAYER: {plain, team}]

	显然[SECURE]是可选的
	每出现一个@，就会导致[AT_PLAYER]出现并把文字用[TEXT]填上，因此这个list不定长(我猜的,2333)


解释一下E6，明显这是4个点，确定了一个矩形区域，那么捕获的消息就来自这个区域

ascendingTimestampOrder(Bool)表示是否按照时间asc输出

![code](https://ww2.sinaimg.cn/large/006tNbRwgw1fas1zzzm12j31kw0hv43f.jpg)
![example](https://ww2.sinaimg.cn/large/006tNbRwgw1fas1yjmqelj31kw0nhq7w.jpg)

## https://www.ingress.com/r/sendPlext

发出消息

	API URL:
	API Request: latE6, lngE6, message, tab, v,
	API Response: result

这个API，看上边接收消息的就可以了，注意tab的值是all或faction

## redeemReward

使用passcode

	API URL: https://www.ingress.com/r/redeemReward
	API Request: passcode, v,
	API Response:
		1. error


## sendInviteEmail

邀请

	API URL: https://www.ingress.com/r/sendInviteEmail
	API Request: inviteeEmailAddress, v
	API Response: result

## 第一部分结束

	代码

# Game API

	等下篇吧，2333
