
# 说明

目标一共有两个，一个是[Intel官方地图](https://www.ingress.com/intel)，另一个是游戏使用的API

本文只做相关API赏析，请不要做违反[TOS](https://www.ingress.com/terms)的事情

已经打包成库

`pip3 install ingressAPI`

`from ingressAPI import IntelMap`

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

[代码](https://github.com/lc4t/ingress-api)

# Game API(iOS)

## 获取API

1. 使用Charles作为中转，iPhone转发到Charles，之后转到ss
2. 安装HTTPS证书

## 注意事项

1. 在HTTP Request Headers中，同样有X-XsrfToken
2. 还有固定值User-Agent: Nemesis (gzip), Accept-Encoding: gzip, Accept-Language: 你自己设置的语言
3. 还需要Authorization在HTTP Request Headers中
4. 身份认证：
5.
6. 没特殊说明的，都是POST请求
7. API用到的域名：(gstatic)|(upsight-api)|(appspot.com)|(google-analytics.com)
8. google-analytics一会就一个，都是GET请求，在游戏过程中的这种包懒得写了

## Google数据统计

在此期间 User-Agent是Ingress/1.110.0 CFNetwork/808.2.16 Darwin/16.3.0

### Start

在打开游戏时，第一个请求是发向https://www.googleadservices.com/pagead/conversion/999636601/的

说下参数

	appversion: 1.110.0
	auto: 1
	bundleid: com.google.ingress
	lat: 1
	muid: n4nISlWfVzY2pH_42u0NMw
	osversion: 10.2
	sdkversion: ct-sdk-i-v3.1.1
	timestamp: 1457613595.596337
	usage_tracking_enabled: 1

只有timestamp是变化的

### Config

之后是POST请求配置文件，https://bootstrap.upsight-api.com/config/v1/f1f4c1b2962446b38f72d5a456aac73c/

注意这里开始，Headers里带了一个X-US-Ref-Id(当向upsight-api.com请求的时候都要有，其他几个API站用X-XsrfToken), 每次启动APP值不容

这个请求的内容很多，
```json
{
	"sdk.version": "4.0.2",
	"device.manufacturer": "Apple",
	"screen.width": 375,
	"app.token": "f1f4c1b2962446b38f72d5a456aac73c",
	"app.version": "1.110.0",
	"device.limit_ad_tracking": true,
	"screen.height": 667,
	"bundle.hash": *,
	"ids.idfv": *,
	"sdk.build": "+release.91a51d8",
	"request_ts": 1481902230,
	"device.carrier": "中国联通",
	"device.hardware": "iPhone8,1",
	"locale": "zh_CN",
	"app.bundleid": "com.google.ingress",
	"sid": "622357641234265637",
	"location.tz": "+0800",
	"device.connection": "Wifi",
	"device.os_version": "10.2",
	"device.type": "phone",
	"identifiers": "pub",
	"opt_out": false,
	"device.jailbroken": false,
	"screen.scale": 2,
	"device.os": "ios",
	"sessions": [{
		"session_num": 5558,
		"install_ts": 1457609995,
		"session_start": 1481901886,
		"events": [{
			"ts": 1481902230,
			"seq_id": 252628,
			"type": "upsight.config.expired",
			"user_attributes": {
				"days_inactive": -1,
				"hashed_user_id": *,
				"player_approx_lat": 30.76,
				"player_approx_lng": 103.93,
				"language": "zh_CN",
				"faction": "ALIENS",
				"distance_to_portal": -1,
				"agent_level": 13
			}
		}],
		"past_session_time": 2873649
	}]
}```

可以看到这里实际上是上传了session的备份，设备信息，APP信息

会返回一个配置

```json
{
	"errobj": null,
	"response": [{
		"content": {
			"configurationList": [{
				"configuration": {
					"queues": [{
						"max_age": 120,
						"count_network_fail_retries": false,
						"name": "batch",
						"retry_interval": 60,
						"host": "batch.upsight-api.com",
						"max_retry_count": 3,
						"url_fmt": "{protocol}://{host}/batch/{version}/{app_token}/",
						"protocol": "https",
						"max_size": 50
					}, {
						"max_age": 0,
						"count_network_fail_retries": true,
						"name": "immediate",
						"retry_interval": 5,
						"host": "single.upsight-api.com",
						"max_retry_count": 1,
						"url_fmt": "{protocol}://{host}/sdk/{version}/events/{app_token}/",
						"protocol": "https",
						"max_size": 1
					}, {
						"max_age": 0,
						"count_network_fail_retries": true,
						"name": "config",
						"retry_interval": 15,
						"host": "bootstrap.upsight-api.com",
						"max_retry_count": 2,
						"url_fmt": "{protocol}://{host}/config/{version}/{app_token}/",
						"protocol": "https",
						"max_size": 1
					}],
					"identifiers": [{
						"ids": ["ids.idfv", "ids.android_id"],
						"name": "pub"
					}, {
						"ids": ["ids.idfa", "ids.aid"],
						"name": "ad"
					}],
					"route_filters": [{
						"filter": "*",
						"queues": ["batch", "trash"]
					}, {
						"filter": "upsight.*",
						"queues": ["batch", "trash"]
					}, {
						"filter": "upsight.milestone",
						"queues": ["immediate", "batch", "trash"]
					}, {
						"filter": "upsight.uxm.enumerate",
						"queues": ["immediate", "batch", "trash"]
					}, {
						"filter": "upsight.content.unrendered",
						"queues": ["immediate", "batch", "trash"]
					}, {
						"filter": "upsight.campaign.*",
						"queues": ["immediate", "batch", "trash"]
					}, {
						"filter": "upsight.content.*",
						"queues": ["immediate", "batch", "trash"]
					}, {
						"filter": "upsight.comm.register",
						"queues": ["immediate", "batch", "trash"]
					}, {
						"filter": "upsight.comm.unregister",
						"queues": ["immediate", "batch", "trash"]
					}, {
						"filter": "upsight.session.start",
						"queues": ["immediate", "batch", "trash"]
					}, {
						"filter": "pub.RequestContentSize.*",
						"queues": ["trash"]
					}, {
						"filter": "pub.RequestDuration.*",
						"queues": ["trash"]
					}, {
						"filter": "pub.RequestPayloadSize.*",
						"queues": ["trash"]
					}, {
						"filter": "upsight.config.expired",
						"queues": ["config", "trash"]
					}, {
						"filter": "upsight.monetization.iap",
						"queues": ["immediate", "batch", "trash"]
					}, {
						"filter": "upsight.data_collection",
						"queues": ["immediate", "batch", "trash"]
					}],
					"identifier_filters": [{
						"filter": "*",
						"identifiers": "pub"
					}]
				},
				"type": "upsight.configuration.dispatcher"
			}, {
				"configuration": {
					"retryMultiplier": 120,
					"requestInterval": 3600,
					"retryPowerBase": 1.61,
					"retryPowerExponentMax": 10
				},
				"type": "upsight.configuration.configurationManager"
			}, {
				"configuration": {
					"push_token_ttl": 604800,
					"auto_register": true
				},
				"type": "upsight.configuration.push"
			}]
		},
		"type": "upsight.configuration"
	}],
	"error": null
}
```

这里就不细说了



### batch

这个是POST给https://batch.upsight-api.com/batch/v1/f1f4c1b2962446b38f72d5a456aac73c/



```json
{
	"sdk.version": "4.0.2",
	"device.manufacturer": "Apple",
	"screen.width": 375,
	"app.token": "*",
	"app.version": "1.110.0",
	"device.limit_ad_tracking": true,
	"screen.height": 667,
	"bundle.hash": "*",
	"ids.idfv": "*",
	"sdk.build": "+release.91a51d8",
	"request_ts": 1481902232,
	"device.carrier": "中国联通",
	"device.hardware": "iPhone8,1",
	"locale": "zh_CN",
	"app.bundleid": "com.google.ingress",
	"sid": *,
	"location.tz": "+0800",
	"device.connection": "Wifi",
	"device.os_version": "10.2",
	"device.type": "phone",
	"identifiers": "pub",
	"opt_out": false,
	"device.jailbroken": false,
	"screen.scale": 2,
	"device.os": "ios",
	"sessions": [{
		"session_num": 5558,
		"install_ts": 1457609995,
		"session_start": 1481901886,
		"events": [{
			"ts": 1481902146,
			"seq_id": 252627,
			"type": "upsight.session.pause",
			"user_attributes": {
				"days_inactive": -1,
				"hashed_user_id": "*",
				"player_approx_lat": *,
				"player_approx_lng": *,
				"language": "zh_CN",
				"faction": "ALIENS",
				"distance_to_portal": -1,
				"agent_level": 13
			}
		}, {
			"ts": 1481902230,
			"seq_id": 252629,
			"type": "upsight.session.resume",
			"user_attributes": {
				"days_inactive": -1,
				"hashed_user_id": "*",
				"player_approx_lat": *,
				"player_approx_lng": *,
				"language": "zh_CN",
				"faction": "ALIENS",
				"distance_to_portal": -1,
				"agent_level": 13
			}
		}, {
			"ts": 1481902230,
			"pub_data": {
				"ui_type": "FOREGROUND",
				"GL_MAX_TEXTURE_SIZE": 4096
			},
			"seq_id": 252630,
			"type": "pub.Stats.GL_MAX_TEXTURE_SIZE",
			"user_attributes": {
				"days_inactive": -1,
				"hashed_user_id": "*",
				"player_approx_lat": *,
				"player_approx_lng": *,
				"language": "zh_CN",
				"faction": "ALIENS",
				"distance_to_portal": -1,
				"agent_level": 13
			}
		}],
		"past_session_time": 2873649
	}]
}
```
和上面的差别在于event， 有兴趣的diff一下

返回什么呢：

```json
{
	"errobj": null,
	"error": null,
	"response": []
}
```

### OAuth2登录

这里是OAuth2的认证，不是重点，都略去

最后一个API是POST到https://www.googleapis.com/oauth2/v4/token，**form**包含了

	client_id
	code
	grant_type
	redirect_uri
	verifier

然后仍然是返回一个JSON，
```json
{
	"access_token": *,
	"token_type": "Bearer",
	"expires_in": 3600,
	"refresh_token": *,
	"id_token": *
}
```

**从这里之后就要带上Authorizatoin了** （向appspot请求时）

其格式就是 `Bearer access_token`

#### collect

之后，ingress会发送一个统计信息，GET传参到`https://ssl.google-analytics.com/collect`

这里的User-Agent被设置为`GoogleAnalytics/3.10 (iPhone; U; CPU iPhone OS 10.2 like Mac OS X; zh-hans-cn-cn)`

下面说一下参数


	an: niantic-ingress
	av: 1.110.0
	a: 1360117771
	tid: UA-30116200-4
	cd: NiOSAuthenticationInfoViewController
	t: screenview
	cid: *
	ul: zh-hans-cn
	aid: com.google.ingress
	ds: app
	_u: *
	sr: 375x667
	v: 1
	_crc: 0
	_v: mi3.1.0
	sf: 100
	ht: 1481901425098
	qt: 155026
	z: *

### hanshake

URL: https://m-dot-betaspike.appspot.com/handshake

这里仍然是POST form提交，但是内容是JSON的，怀疑是设置错了

```json
{
"nemesisSoftwareVersion": "2016-11-18T13:44:21Z+c90631584ea7-i+opt",
"deviceSoftwareVersion": "10.2",
"a": *,
"reason": "SUP"
}
```

返回的东西很重要
首先是一个crack串`)]}'`
然后是一个巨大的JSON，返回了：
```json
{
    "result": {
        "playerEntity": [user_guid, 1481899737145, {
            "playerPersonal": {
                "ap": "14031060",
                "energy": 10255,
                "allowNicknameEdit": false,
                "allowFactionChoice": false,
                "verifiedLevel": 13,
                "mediaHighWaterMarks": {
                    "General": 1809,
                    "RESISTANCE": 1328,
                    "ALIENS": 1327
                },
                "energyState": "XM_OK",
                "notificationSettings": {
                    "shouldSendEmail": false,
                    "maySendPromoEmail": false,
                    "shouldPushNotifyForAtPlayer": true,
                    "shouldPushNotifyForPortalAttacks": true,
                    "shouldPushNotifyForInvitesAndFactionInfo": true,
                    "shouldPushNotifyForNewsOfTheDay": true,
                    "shouldPushNotifyForEventsAndOpportunities": true,
                    "locale": "zh-Hans-CN"
                },
                "profileSettings": {
                    "areMetricsPublic": false
                },
                "verificationState": "UNVERIFIED",
                "extraXmTankEnergy": 0
            },
            "controllingTeam": {
                "team": "RESISTANCE"
            },
            "avatar": {
                "foreground": {
                    "layerId": "foreground4",
                    "tintColor": 16249235,
                    "imageUrl": "http://lh3.googleusercontent.com/COPtJLf8PEP0dgeehOg425-ASLkkQtrphoViG6Hy19mbHtyBDvanqWB4a6jPCaHhYpLYNaw9Ot9-0cfYm0Qc"
                },
                "background": {
                    "layerId": "background3",
                    "tintColor": 481625,
                    "imageUrl": "http://lh3.googleusercontent.com/WorWGSonh3XJrC7RWpVuBkTKcHoF2QtsolzqhmNUrZcaHKmfRgpTO_5QmpYTbBvkLkbTlF5LRW9gS_xDmTdY"
                }
            }
        }],
        "nickname": *,
        "xsrfToken": *,
        "storage": {
            "tutorial_complete_scanner_intro": "true:delim:1481895477261:delim:true",
            "game_intro_has_played": "true:delim:1457410095779:delim:true",
            "mission_complete_7": "ENDED_BY_NAGGING:delim:1457876587760:delim:true",
            "mission_complete_6": "ENDED_BY_NAGGING:delim:1457876587759:delim:true",
            "mission_complete_5": "ENDED_BY_NAGGING:delim:1457876587758:delim:true",
            "mission_complete_4": "SUCCESS:delim:1457876587753:delim:true",
            "mission_complete_3": "ENDED_BY_NAGGING:delim:1457876587757:delim:true",
            "mission_complete_0": "ENDED_BY_NAGGING:delim:1457876587754:delim:true",
            "mission_complete_1": "ENDED_BY_NAGGING:delim:1457876587755:delim:true",
            "mission_complete_2": "ENDED_BY_NAGGING:delim:1457876587756:delim:true",
            "all_missions_complete_announcement_made": "true:delim:1457410237730:delim:true",
            "tutorial_complete_hack": "true:delim:1457410237722:delim:true",
            "training_portal_photo_url": "http://lh6.ggpht.com/xZU07oPfUpRDnz_2og2L1E3O4T74iMUyCVtB5lL6m16lh0PnZPtBMf8XjkpYbq8Veby0eHNhCGNRwQrYNg:delim:1457439507178:delim:true",
            "training_portal_lng_degrees": *,
            "training_portal_lat_degrees": *,
            "training_portal_title": "本科9栋:delim:1457439507178:delim:true",
            "tutorial_complete_xm": "true:delim:1457412143790:delim:true",
            "tutorial_complete_xmp": "true:delim:1457412131239:delim:true",
            "tutorial_complete_profile_link": "true:delim:1457422332944:delim:true",
            "tutorial_complete_deploy": "true:delim:1457488741871:delim:true"
        },
        "pregameStatus": {
            "action": "NO_ACTIONS_REQUIRED",
            "dialogText": ""
        },
        "initialKnobs": {
            "bundleMap": {
                "ClientFeatureKnobs": {
                    "enableEmbeddedYouTubePlayback": true,
                    "showGlobalMap": true,
                    "logSkipRegex": "\\b\\B",
                    "enableParticleFilter": true,
                    "enableGAViolationReporting": false,
                    "portalKeyCardRefreshIntervalSecs": 5,
                    "portalInfoRefreshIntervalSecs": 2,
                    "enableInviteNag": true,
                    "inviteNagDelayDays": 14,
                    "enableVerificationNag": false,
                    "verificationNagDelayDays": 3,
                    "refreshTimeMs": "-1",
                    "playerProfileCacheExpirationSecs": "60",
                    "enableDelayGpsPause": true,
                    "enableAdvancedAnalytics": true,
                    "playerVerificationEnabled": 0,
                    "enableExtraNativeRenderedText": -1,
                    "enableShareMission": 10740,
                    "profileUrlFormat": "http://plus.google.com/%s",
                    "profileUrlFormatApp": "gplus://plus.google.com/%s",
                    "factionChoiceBeforeSpaceToFace": true,
                    "minGlobBundleSizeXm": 1500,
                    "enableMissions": 10610,
                    "enableBadAnalyticsTrackingEventLogging": 10570,
                    "enableIOSPushNotifications": 10640,
                    "iOSPortalDiscoveryProcessIntervalMS": "200000",
                    "enableMissionsConnectivityRecovery": 10610,
                    "enableMissionsStatePolling": 10610,
                    "enableHackLongPressIndicator": 10612,
                    "enableIOSNativeYoutubePlayer": 10620,
                    "enableIOSPortalDetailPanel": 10630,
                    "enableIOSMultiPhotoViewer": 10640,
                    "enableIOSPhotoSubmission": 10640,
                    "enableIOSGridPhotoViewer": 10650,
                    "enableCommunityTab": 10740,
                    "enableBoostRechargeV2": 10760,
                    "enableSetLocale": 10771,
                    "disableNewPortalSubmissions": -1,
                    "enableLocalLinkChecks": 10790,
                    "enableStore": 10851,
                    "enableRecycleConfirmationDialog": 0,
                    "enableGlyphCommandChannel": 10900,
                    "enableGlyphRedoButton": 10910,
                    "upsightLocationDecimalPlacesToRound": 2,
                    "enableExtendedFireMenu": 11010
                },
                "SmartNotificationsClientKnobs": {
                    "enableSmartNotifications": 10670,
                    "maximumCachedHandshakeResultAgeMs": "43200000",
                    "enableR": 10691,
                    "enableRIOS": 10700,
                    "playerRProbabilityE6": 1000000,
                    "rLPlayerMs": "864000000",
                    "rMinPollingDelayMs": "900000",
                    "maximumPortalCacheSize": 5000,
                    "portalCacheEntryExpirationTimeMs": "1209600000",
                    "nearbyPortalDistanceM": 200,
                    "loiteringMs": "300000",
                    "noLongerNearbyDistanceM": 100,
                    "rNearbyPortalDistanceGrowthRate": 50,
                    "rMaxGrownNearbyPortalDistanceM": 1000,
                    "rWaitPeriodsMs": ["86400000", "172800000", "259200000", "432000000"],
                    "rIOSAlwaysLocationAccessMinIntervalMs": "5256000000",
                    "amSessionLengthMs": "1800000",
                    "enableAm": 10700,
                    "playerAmProbabilityE6": 1000000,
                    "amNearbyPortalDistanceM": 37,
                    "amNoLongerNearbyDistanceM": 40,
                    "amAndroidLocationRequestPriority": 102,
                    "amAndroidLocationRequestIntervalMs": "30000",
                    "amAndroidLocationRequestFastestIntervalMs": "5000",
                    "amAndroidLocationRequestSmallestDisplacementM": 0
                },
                "TranslationClientKnobs": {
                    "enableCloudTranslations": 10860,
                    "translationUrls": {
                        "zh_TW.json": "http://storage.googleapis.com/ingress-translations/2016.11.04/zh_TW.json",
                        "ru": "http://storage.googleapis.com/ingress-translations/2016.11.04/ru.json",
                        "fr": "http://storage.googleapis.com/ingress-translations/2016.11.04/fr.json",
                        "en": "http://storage.googleapis.com/ingress-translations/2016.11.04/en.json",
                        "nl": "http://storage.googleapis.com/ingress-translations/2016.11.04/nl.json",
                        "pt": "http://storage.googleapis.com/ingress-translations/2016.11.04/pt.json",
                        "no": "http://storage.googleapis.com/ingress-translations/2016.11.04/no.json",
                        "de": "http://storage.googleapis.com/ingress-translations/2016.11.04/de.json",
                        "ko": "http://storage.googleapis.com/ingress-translations/2016.11.04/ko.json",
                        "it": "http://storage.googleapis.com/ingress-translations/2016.11.04/it.json",
                        "sv": "http://storage.googleapis.com/ingress-translations/2016.11.04/sv.json",
                        "pl": "http://storage.googleapis.com/ingress-translations/2016.11.04/pl.json",
                        "cs": "http://storage.googleapis.com/ingress-translations/2016.11.04/cs.json",
                        "zh_CN.json": "http://storage.googleapis.com/ingress-translations/2016.11.04/zh_CN.json",
                        "ja": "http://storage.googleapis.com/ingress-translations/2016.11.04/ja.json",
                        "es": "http://storage.googleapis.com/ingress-translations/2016.11.04/es.json"
                    }
                },
                "GlyphCommandClientKnobs": {
                    "commands": {
                        "ikj": "GLYPH_ACCEPT_MORE_KEYS",
                        "jkgh": "GLYPH_ACCEPT_COMPLEX_HACK",
                        "hkg": "GLYPH_ACCEPT_LESS_KEYS",
                        "ji": "GLYPH_ACCEPT_SIMPLE_HACK"
                    },
                    "hints": ["GLYPH_HINT_LESS_KEYS", "GLYPH_HINT_MORE_KEYS", "GLYPH_HINT_SIMPLE_HACK"]
                },
                "StagingKnobs": {
                    "playerStoreProbabilityE6": 1000000,
                    "oldAnalyticsProbabilityE6": 1000000,
                    "newAnalyticsProbabilityE6": 1000000
                },
                "InventoryKnobs": {
                    "maxInventoryItems": 2000,
                    "resourceLimits": {
                        "KEY_CAPSULE": 5
                    },
                    "cmuRestockItemId": "ingress.cmu.large",
                    "itemRestockResourceToId": {},
                    "powerupRestockToId": {
                        "LOOK": "ingress.beacon.look",
                        "RES": "ingress.beacon.res",
                        "NIA": "ingress.beacon.nia",
                        "ENL": "ingress.beacon.enl",
                        "FRACK": "ingress.fracker",
                        "MEET": "ingress.beacon.meet"
                    }
                },
                "PortalKnobs": {
                    "resonatorLimits": {
                        "bands": [{
                            "remaining": 1,
                            "applicableLevels": [8]
                        }, {
                            "remaining": 4,
                            "applicableLevels": [2]
                        }, {
                            "remaining": 8,
                            "applicableLevels": [1]
                        }, {
                            "remaining": 2,
                            "applicableLevels": [5]
                        }, {
                            "remaining": 4,
                            "applicableLevels": [3]
                        }, {
                            "remaining": 2,
                            "applicableLevels": [6]
                        }, {
                            "remaining": 4,
                            "applicableLevels": [4]
                        }, {
                            "remaining": 1,
                            "applicableLevels": [7]
                        }]
                    },
                    "maxModsPerPlayer": 2,
                    "radiusParamsSet": [],
                    "allowRegionSpecificSubmissions": false,
                    "minLevelForSubmission": 2
                },
                "recycleKnobs": {
                    "recycleValuesMap": {
                        "BOOSTED_POWER_CUBE": [160, 160, 160, 160, 160, 160, 160, 160],
                        "MULTIHACK": [20, 40, 60, 80, 100, 120, 140, 160],
                        "EMP_BURSTER": [20, 40, 60, 80, 100, 120, 140, 160],
                        "INTEREST_CAPSULE": [20, 40, 60, 80, 100, 120, 140, 160],
                        "TURRET": [20, 40, 60, 80, 100, 120, 140, 160],
                        "MEDIA": [20, 40, 60, 80, 100, 120, 140, 160],
                        "EXTRA_SHIELD": [20, 40, 60, 80, 100, 120, 140, 160],
                        "ULTRA_STRIKE": [20, 40, 60, 80, 100, 120, 140, 160],
                        "POWER_CUBE": [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000],
                        "FLIP_CARD": [20, 40, 60, 80, 100, 120, 140, 160],
                        "ULTRA_LINK_AMP": [20, 40, 60, 80, 100, 120, 140, 160],
                        "CAPSULE": [20, 40, 60, 80, 100, 120, 140, 160],
                        "HEATSINK": [20, 40, 60, 80, 100, 120, 140, 160],
                        "RES_SHIELD": [20, 40, 60, 80, 100, 120, 140, 160],
                        "PORTAL_POWERUP": [20, 40, 60, 80, 100, 120, 140, 160],
                        "LINK_AMPLIFIER": [20, 40, 60, 80, 100, 120, 140, 160],
                        "EMITTER_A": [20, 40, 60, 80, 100, 120, 140, 160],
                        "PORTAL_LINK_KEY": [500, 500, 500, 500, 500, 500, 500, 500],
                        "KEY_CAPSULE": [20, 40, 60, 80, 100, 120, 140, 160],
                        "FORCE_AMP": [20, 40, 60, 80, 100, 120, 140, 160]
                    }
                },
                "WeaponRangeKnobs": {
                    "xmpDamageRangeMap": {
                        "1": 42,
                        "3": 58,
                        "2": 48,
                        "5": 90,
                        "4": 72,
                        "7": 138,
                        "6": 112,
                        "8": 168
                    },
                    "ultraStrikeDamageRangeMap": {
                        "1": 10,
                        "3": 16,
                        "2": 13,
                        "5": 21,
                        "4": 18,
                        "7": 27,
                        "6": 24,
                        "8": 30
                    },
                    "maxPowerBoostPercentage": 20,
                    "powerBoostPeriodHardS": 0.6,
                    "powerBoostPeriodEasyS": 1.5,
                    "powerBoostWindowHardS": 0.06,
                    "powerBoostWindowEasyS": 0.1,
                    "powerBoostPowAnimation": 1.0,
                    "powerBoostPowScore": 1.0,
                    "maxFireRateSeconds": 1.5
                },
                "XmCostKnobs": {
                    "xmpFiringCostByLevel": [50, 100, 150, 200, 250, 300, 350, 400],
                    "shieldDeployCostByLevel": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                    "linkAmplifierDeployCostByLevel": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                    "forceAmplifierDeployCostByLevel": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                    "heatsinkDeployCostByLevel": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                    "multihackDeployCostByLevel": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                    "turretDeployCostByLevel": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                    "resonatorDeployCostByLevel": [50, 100, 150, 200, 250, 300, 350, 400],
                    "resonatorUpgradeCostByLevel": [50, 100, 150, 200, 250, 300, 350, 400],
                    "portalHackFriendlyCostByLevel": [50, 100, 150, 200, 250, 300, 350, 400],
                    "portalHackNeutralCostByLevel": [50, 100, 150, 200, 250, 300, 350, 400],
                    "portalHackEnemyCostByLevel": [50, 100, 150, 200, 250, 300, 350, 400],
                    "flipCardCostByLevel": [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000],
                    "portalModByLevel": {
                        "MULTIHACK": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                        "HEATSINK": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                        "TURRET": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                        "EXTRA_SHIELD": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                        "FORCE_AMP": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                        "ULTRA_LINK_AMP": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                        "RES_SHIELD": [200, 400, 600, 800, 1000, 1200, 1400, 1600],
                        "LINK_AMPLIFIER": [200, 400, 600, 800, 1000, 1200, 1400, 1600]
                    },
                    "powerupByLevel": {
                        "PORTAL_POWERUP": [200, 400, 600, 800, 1000, 1200, 1400, 1600]
                    },
                    "boostRechargeResonatorsCost": 15000
                },
                "ScannerKnobs": {
                    "updateIntervalMs": 30000,
                    "updateDistanceM": 10,
                    "maxUpdateIntervalMs": 30000,
                    "minUpdateIntervalMs": 5000,
                    "updateIntervalThrottlingTriggerVelocityMps": 3.0,
                    "updateIntervalThrottlingRate": 0.65,
                    "rangeM": 300,
                    "missionsUpdateIntervalMs": 60000,
                    "missionsUpdateDistanceM": 500,
                    "maxLinkAutoCheckRangeM": 200000,
                    "reportRequestPerformancePercentE6": 0,
                    "crittercismSendPerfDataProbabilityE6": 0,
                    "crittercismSendLogcatProbabilityE6": 0
                },
                "PortalModSharedKnobs": {
                    "diminishingValues": {
                        "FORCE_AMPLIFIER": [1000, 250, 125, 125],
                        "ATTACK_FREQUENCY": [1000, 250, 125, 125],
                        "LINK_RANGE_MULTIPLIER": [1000, 250, 125, 125],
                        "TEMP_LINK_RANGE_MULTIPLIER_SORTED": [1000, 250, 125, 125],
                        "TEMP_ATTACK_FREQUENCY_SORTED": [1000, 250, 125, 125],
                        "BURNOUT_INSULATION": [1000, 500, 500, 500],
                        "HACK_SPEED": [1000, 500, 500, 500],
                        "TEMP_FORCE_AMPLIFIER_SORTED": [1000, 250, 125, 125]
                    },
                    "directValues": {
                        "OUTGOING_LINKS_BONUS": [8, 8, 8, 8]
                    }
                },
                "NearbyPortalKnobs": {
                    "repopulateDistanceMeters": 500.0,
                    "repopulateTimeMilliseconds": "30000"
                },
                "PlayerAnnounceSharedKnobs": {
                    "featureActivationDate": "1377241200000"
                },
                "PlayerVerificationSharedKnobs": {
                    "unverifiedXmCapacity": 3000,
                    "unverifiedInventoryCapacity": 100,
                    "unverifiedApCapacity": 19999,
                    "enableVerificationFeature": false,
                    "enableVerifiedGameActions": false,
                    "numPinCodeDigits": 4
                },
                "PlayerLevelKnobs": {
                    "levelUpRequirements": {
                        "11": {
                            "apRequired": "6000000",
                            "achievementsRequired": {
                                "SILVER": 6,
                                "GOLD": 4
                            }
                        },
                        "10": {
                            "apRequired": "4000000",
                            "achievementsRequired": {
                                "SILVER": 5,
                                "GOLD": 2
                            }
                        },
                        "13": {
                            "apRequired": "12000000",
                            "achievementsRequired": {
                                "PLATINUM": 1,
                                "GOLD": 7
                            }
                        },
                        "12": {
                            "apRequired": "8400000",
                            "achievementsRequired": {
                                "SILVER": 7,
                                "GOLD": 6
                            }
                        },
                        "15": {
                            "apRequired": "24000000",
                            "achievementsRequired": {
                                "PLATINUM": 3
                            }
                        },
                        "14": {
                            "apRequired": "17000000",
                            "achievementsRequired": {
                                "PLATINUM": 2
                            }
                        },
                        "16": {
                            "apRequired": "40000000",
                            "achievementsRequired": {
                                "PLATINUM": 4,
                                "BLACK": 2
                            }
                        },
                        "1": {
                            "apRequired": "0",
                            "achievementsRequired": {}
                        },
                        "3": {
                            "apRequired": "20000",
                            "achievementsRequired": {}
                        },
                        "2": {
                            "apRequired": "2500",
                            "achievementsRequired": {}
                        },
                        "5": {
                            "apRequired": "150000",
                            "achievementsRequired": {}
                        },
                        "4": {
                            "apRequired": "70000",
                            "achievementsRequired": {}
                        },
                        "7": {
                            "apRequired": "600000",
                            "achievementsRequired": {}
                        },
                        "6": {
                            "apRequired": "300000",
                            "achievementsRequired": {}
                        },
                        "9": {
                            "apRequired": "2400000",
                            "achievementsRequired": {
                                "SILVER": 4,
                                "GOLD": 1
                            }
                        },
                        "8": {
                            "apRequired": "1200000",
                            "achievementsRequired": {}
                        }
                    },
                    "maxPlayerLevel": 16,
                    "xmCapacityByLevel": {
                        "11": 14500,
                        "10": 13000,
                        "13": 17500,
                        "12": 16000,
                        "15": 20500,
                        "14": 19000,
                        "16": 22000,
                        "1": 3000,
                        "3": 5000,
                        "2": 4000,
                        "5": 7000,
                        "4": 6000,
                        "7": 9000,
                        "6": 8000,
                        "9": 11500,
                        "8": 10000
                    },
                    "boostedPowerCubeCapacityByLevel": {
                        "11": 40800,
                        "10": 38400,
                        "13": 45600,
                        "12": 43200,
                        "15": 50400,
                        "14": 48000,
                        "16": 52800,
                        "1": 18000,
                        "3": 22500,
                        "2": 20250,
                        "5": 27000,
                        "4": 24750,
                        "7": 31500,
                        "6": 29250,
                        "9": 36000,
                        "8": 33750
                    }
                },
                "MapCompositionRootKnobs": {
                    "mapAreas": [{
                        "description": "S Korea",
                        "epoch": 1,
                        "mapProvider": "OSM",
                        "boundingRects": [{
                            "north": 37.69547616496338,
                            "south": 34.83562779241368,
                            "east": 131.16790087890627,
                            "west": 124.44700830078114
                        }, {
                            "north": 37.69547616496338,
                            "south": 33.025620228813466,
                            "east": 128.76189501953127,
                            "west": 124.44700830078114
                        }, {
                            "north": 37.84094374831599,
                            "south": 37.561299473030594,
                            "east": 126.86126025390627,
                            "west": 126.18010156249989
                        }, {
                            "north": 38.358197906100926,
                            "south": 37.62589818166485,
                            "east": 129.34966357421877,
                            "west": 126.65800683593739
                        }, {
                            "north": 38.634814820135226,
                            "south": 38.358197906100926,
                            "east": 128.55040820312502,
                            "west": 128.14116113281239
                        }]
                    }, {
                        "description": "World",
                        "epoch": -1,
                        "mapProvider": "GMM",
                        "mapProviderName": "",
                        "boundingRects": [{
                            "north": 90.0,
                            "south": -90.0,
                            "east": 180.0,
                            "west": -180.0
                        }]
                    }],
                    "mapProviders": [{
                        "name": "GMM",
                        "baseUrl": "http://mobilemaps.clients.google.com/glm/mmap",
                        "queryFormat": ""
                    }, {
                        "name": "OSM",
                        "baseUrl": "http://maps.nianticlabs.com",
                        "queryFormat": "ntp-maptiles/epoch-%04d/%s.gmm"
                    }]
                }
            },
            "syncTimestamp": "1481903753065"
        }
    }
}
```

这里的东西可以做一个教程了，基本上，各种物品的效果，升级的要求都在里面写的很清楚，欢迎其他同学做个统计

比如ultraStrikeDamageRangeMap里说明了各个级别的US作用距离

这里大概是为了热更新，把设置放在服务端（反正跑的又不是我的流量，gg）



### setLocale

然后是POST到https://m-dot-betaspike.appspot.com/rpc/emptyBasket/setLocale

直接form内容简单暴力

	{"params":["zh-Hans-CN"]}

返回也是一个空的{}

### globalRegionMap

这次是GET到https://m-dot-betaspike.appspot.com/globalRegionMap获取游戏开始那张转动的地球的图

Response是一张256*128的黑绿红图


### batch 第二次

又触发一次设备信息上传，除了request_ts更新了，有一点不同，在events中

```json
"pub_data": {
	"type": "upsight.session.pause",
	"ui_type": "FOREGROUND"
},
...,
"type": "pub.StartupWheelsOfAdaSubActivity",
```



这之前都是在点击`我明白了`按钮之前的请求


## Game API

### getGameScore

显然是用来获取游戏的比分的

	API URL: https://m-dot-betaspike.appspot.com/rpc/playerUndecorated/getGameScore
	API Request: params: []
	API Response:

```json
{
	"result": {
		"alienScore": "569243223",
		"resistanceScore": "723155462"
	},
	"gameBasket": {
		"gameEntities": [],
		"inventory": [],
		"deletedEntityGuids": []
	}
}
```

懒得解释了，直接贴返回的包吧

## getObjectsInCells

用来获得地图元素

	API URL： https://m-dot-betaspike.appspot.com/rpc/gameplay/getObjectsInCells
	API Request: params: {clientBasket: {clientBlob}, knobSyncTimestamp, energyGlobGuids: [], playerLocation: value, dates: [value], cellsAsHex: [...], cells}

这里clientBasket是验证信息，整个过程中不会变，大概要逆一下知道算法

playerLocation是'hex,hex'这样的串，纬度经度(保留6位小数后去掉小数点)转成16进制后空格连接

dates是20个0组成的list（不确定）

cellsAsHex是cell分片的token，20个16位hex值组成的list


	API Response:

```json
{
	"result": "1481906071300",
	"gameBasket": {
		"gameEntities": [
			[guid, time, {
				"capturedRegion": {
					"vertexA": {
						"guid": guid,
						"location": {
							"latE6": *,
							"lngE6": *
						}
					},
					"vertexB": {
						...
					},
					"vertexC": {
						...
					}
				},
				"entityScore": {
					"entityScore": "8"
				},
				"creator": {
					"creatorGuid": user_guid,
					"creationTime": time
				},
				"controllingTeam": {
					"team": "RESISTANCE"
				}
			}],
			...,
			[guid, time, {
				"photoStreamInfo": {
					"coverPhoto": {
						"portalImageGuid": *,
						"imageUrl": *,
						"attributionMarkup": ["PLAYER", {
							"plain": agent_name,
							"guid": guid,
							"team": "ALIENS"
						}],
						"voteCount": 0
					},
					"photoCount": 1
				},
				"locationE6": {
					"latE6": *,
					"lngE6": *
				},
				"discoverer": {
					"playerMarkupArgSet": {
						"plain": agent_name,
						"guid": *,
						"team": "ALIENS"
					}
				},
				"resonatorArray": {
					"resonators": [{
						"level": 3,
						"distanceToPortal": 28,
						"ownerGuid": agent_guid,
						"energyTotal": 1327,
						"slot": 0,
						"id": uuid
					}, ...]
				},
				"descriptiveText": {
					"map": {
						"TITLE": *,
						"ADDRESS": *
					}
				},
				"turret": {},
				"portalV2": {
					"linkedEdges": [],
					"linkedModArray": [{
						"installingUser": agent_guid,
						"stats": {
							"MITIGATION": "30",
							"REMOVAL_STICKINESS": "0"
						},
						"rarity": "COMMON",
						"displayName": "Portal Shield",
						"type": "RES_SHIELD"
					}, ...],
					"missionStartPoint": false
				},
				"controllingTeam": {
					"team": "RESISTANCE"
				},
				"captured": {
					"capturingPlayerId": agent_guid
				},
				"defaultActionRange": {}
			}],
			...,

			[guide, time, {
				"edge": {
					"originPortalGuid": guid,
					"destinationPortalGuid": guid,
					"originPortalLocation": {
						"latE6": *,
						"lngE6": *
					},
					"destinationPortalLocation": {
						"latE6": *,
						"lngE6": *
					}
				},
				"creator": {
					"creatorGuid": *,
					"creationTime": *
				},
				"controllingTeam": {
					"team": "RESISTANCE"
				}
			}],
			...,
			[guid, time, {
				"imageByUrl": {
					"imageUrl": *
				},
				"photoStreamInfo": {
					"coverPhoto": {
						"portalImageGuid": guid,
						"imageUrl": *,
						"attributionMarkup": ["PLAYER", {
							"plain": agent_name,
							"guid": guid,
							"team": "ALIENS"
						}],
						"voteCount": 5
					},
					"photoCount": 1
				},
				"locationE6": {
					"latE6": *,
					"lngE6": *
				},
				"discoverer": {
					"playerMarkupArgSet": {
						"plain": agent_name,
						"guid": *,
						"team": "ALIENS"
					}
				},
				"resonatorArray": {
					"resonators": [...]
				},
				"descriptiveText": {
					"map": {
						"TITLE": *,
						"DESCRIPTION": *,
						"ADDRESS": *
					}
				},
				"turret": {},
				"portalV2": {
					"linkedEdges": [{
						"edgeGuid": guid,
						"otherPortalGuid": guid",
						"isOrigin": false
					}, ...],
					"linkedModArray": [..., null],
					"missionStartPoint": false
				},
				"controllingTeam": {
					"team": "RESISTANCE"
				},
				"captured": {
					"capturingPlayerId": agent_guid
				},
				"defaultActionRange": {}
			}],
			...,
			[guid, time, {
				"timedPowerupSet": {
					"powerUpItems": []
				},
				"imageByUrl": {
					"imageUrl": *
				},
				"photoStreamInfo": {
					"coverPhoto": {
						"portalImageGuid": guid,
						"imageUrl": *,
						"attributionMarkup": ["PLAYER", {
							"plain": agent_user,
							"guid": guid,
							"team": "ALIENS"
						}],
						"voteCount": 2
					},
					"photoCount": 1
				},
				"locationE6": {
					"latE6": *,
					"lngE6": *
				},
				"discoverer": {
					"playerMarkupArgSet": {
						"plain": agent_user,
						"guid": guid,
						"team": "ALIENS"
					}
				},
				"resonatorArray": {
					"resonators": [...]
				},
				"descriptiveText": {
					"map": {
						"ADDRESS": *,
						"TITLE": (
					}
				},
				"turret": {},
				"portalV2": {
					"linkedEdges": [...],
					"linkedModArray": [null, null, null, null],
					"missionStartPoint": false
				},
				"controllingTeam": {
					"team": "RESISTANCE"
				},
				"captured": {
					"capturingPlayerId": agent_guid
				},
				"defaultActionRange": {}
			}],
			...,
		}],
		"apGains": [],
		"inventory": [],
		"deletedEntityGuids": [],
		"energyGlobGuids": [guid, ...],
		"energyGlobTimestamp": "1481906071300",
		"refreshEntityGuids": [guid, ...]
	}
}
```

很清楚。。。不说了

### getCurrentMission

	API URL: https://m-dot-betaspike.appspot.com/rpc/gameplay/getCurrentMission
	API Request: params: {clientBasket: {clientBlob}, knobSyncTimestamp, energyGlobGuids: [], playerLocation: value}
	API Response: 任务和gameBasket，这里因为我没当前任务，略掉


### getNewsOfTheDay


	API URL:https://m-dot-betaspike.appspot.com/rpc/playerUndecorated/getNewsOfTheDay
	API Request: params: [value]

这个value是一个不造什么鬼的串

	API Response:  gameBasket: {gameEntities: [], inventory: [], deletedEntityGuids: [] }


这个API得等有活动的时候测试

### getPaginatedPlexts

获得comm消息


	API URL: https://m-dot-betaspike.appspot.com/rpc/gameplay/getPaginatedPlexts

	API Request:
```json
{
	"params": {
		"clientBasket": {
			"clientBlob": *
		},
		"knobSyncTimestamp": *,
		"energyGlobGuids": [],
		"playerLocation": value,
		"categories": -1,
		"ascendingTimestampOrder": false,
		"desiredNumItems": 100,
		"maxTimestampMs": -1,
		"minTimestampMs": 1481900888021,
		"cellsAsHex": [...],
		"factionOnly": false
	}
}
```

这个的参数可以参考Intel Map的

	API Response:

```json
{
	"result": [
		[guid, time, {
			"locationE6": {
				"latE6": *,
				"lngE6": *
			},
			"plext": {
				"text": *,
				"team": "ALIENS",
				"markup": [
					["SENDER", {
						"plain": agent_name,
						"guid": *,
						"team": "ALIENS"
					}],
					["TEXT", {
						"plain": ""
					}],
					["AT_PLAYER", {
						"plain": *,
						"guid": guid,
						"team": "ALIENS"
					}],
					["TEXT", {
						"plain": *
					}]
				],
				"plextType": "PLAYER_GENERATED",
				"categories": 1
			}
		}]
	],
	"gameBasket": {
		"gameEntities": [],
		"playerEntity": [...],
		"apGains": [],
		"inventory": [],
		"deletedEntityGuids": [],
		"serverBlob": *
	}
}
```

省略了一些重复的，这里也可以参考Intel Map的API


### getInventory

	API URL: https://m-dot-betaspike.appspot.com/rpc/playerUndecorated/getInventory
	API Request:
```json
{
	"params": {
		"lastQueryTimestamp": timestamp
	}
}
```

	API Response:(只返回更新的物品)

```
{
	"result": "1481911112158",
	"gameBasket": {
		"gameEntities": [],
		"inventory": [
		["56b24e20197240d2a2330e7fb60fa6a1.5", 1473951636802, {
						"inInventory": {
							"playerId": *,
							"acquisitionTimestampMs": *
						},
						"modResource": {
							"displayName": "Heat Sink",
							"stats": {
								"REMOVAL_STICKINESS": "0",
								"HACK_SPEED": "200000"
							},
							"rarity": "COMMON",
							"resourceType": "HEATSINK"
						},
						"displayName": {
							"displayName": "Heat Sink",
							"displayDescription": "Mod that reduces cooldown time between Portal hacks."
						}
				}],...,
		],
		"deletedEntityGuids": []
	}
}
```
inventory能看到更新的物品是什么，强制同步后，这个里面就是所有东西，非常大。。（毕竟每个物品一个list...）

### registerForApn

	API URL: https://m-dot-betaspike.appspot.com/rpc/emptyBasket/registerForApn
	API Request: params: [key, "com.google.ingress", "2048"]
	API Response: {}

用来注册token


### unregisterForApn

	API URL: https://m-dot-betaspike.appspot.com/rpc/emptyBasket/unregisterForApn
	API Request:
	API Response: {}



### getInviteInfo

	API URL: https://m-dot-betaspike.appspot.com/rpc/playerUndecorated/getInviteInfo
	API Request: params: []
	API Response:

```json
{
	"result": {
		"numAvailableInvites": 298,
		"inviteeToStatusMap": {
			email: status,
			...
		},
		"apGainOnInviteAccepted": "3000"
	},
	"gameBasket": {
		"gameEntities": [],
		"inventory": [
		],
		"deletedEntityGuids": []
	}
}
```



这个API不错，能看到自己邀请的所有人和状态，甚至是ACCEPTED_ANOTHER_PLAYERS_INVITE

### putBulkPlayerStorage

	API URL:https://m-dot-betaspike.appspot.com/rpc/playerUndecorated/putBulkPlayerStorage
	API Request: prams: [{tutorial_complete_scanner_intro: value}]

这个value是一个`true:delim:1481912306360:delim:true`格式的串

	API Response:
```json
{
	"result": "SUCCESS",
	"gameBasket": {
		"gameEntities": [],
		"inventory": [],
		"deletedEntityGuids": []
	}
}
```


### getPlayerProfile2

这个是用来获取自己的信息的

	API URL: https://m-dot-betaspike.appspot.com/rpc/playerUndecorated/getPlayerProfile2
	API Request: params: [agent_name]
	API Response: result: {team, avatar: {foregroundLayer: {id, imageURL, layer}, backgroundLayer: {id, imageUrl, layer}, avatarColorForeground, avatarColorBackground}, metrics: [{metricName, metricCategory, formattedValueAllTime, formattedValue30Days, formattedValue7Days}, ...], highlightedAchievements: [title, description, group, tiers: [{value, badgeImageUrl, locked}, ...], timestampAwarded], firstAchievementContinuationToken, ap, verifiedLeve, achievementCounts: {SILVER, GOLD, BLACK, PLATINUM, BRONZE}, gPlusId, highlightedMissionBadges: [{missionGuid, missionTitle, missionDescription, imageUrl}, ...], firstMissionBadgeContinuationToken}, gameBasket: {gameEntities, inventory, deletedEntityGuids}

都是自注释

metrics是数据统计，例如Unique Portals Visite

highlightedAchievements是牌子信息

highlightedMissionBadges是任务信息


### getPaginatedMissionBadges

	API URL: https://m-dot-betaspike.appspot.com/rpc/playerUndecorated/getPaginatedMissionBadges
	API Request: params: [{continuationToken, nickname}]

这个continuationToken是上面那个API返回的firstMissionBadgeContinuationToken或者是自己返回的continuationToken

	API Response:
```json
{
	"result": {
		"missionBadges": [{
			"missionGuid": guid,
			"missionTitle": *,
			"missionDescription": *,
			"imageUrl": *
		}, ...],
		"continuationToken": *
	},
	"gameBasket": {
		"gameEntities": [],
		"inventory": [],
		"deletedEntityGuids": []
	}
}
```

这个API是用来获取任务图标和详情的

### getNearbyMissions

	API URL: https://m-dot-betaspike.appspot.com/rpc/gameplay/getNearbyMissions
	API Request:
```json
{
	"params": {
		"clientBasket": {
			"clientBlob": *
		},
		"knobSyncTimestamp": *,
		"energyGlobGuids": [],
		"location": value,
		"continuationToken": value
	}
}
```

这里的value也是逗号分隔的两个hex

continueationToken为null表示第一次查看任务，之后值为这个API自己返回的continuationToken

	API Response:
```
{
	"result": {
		"missionSnippets": [{
			"header": {
				"guid": guid,
				"title": *,
				"logoUrl": *,
				"startLocation": value,
				"badgeUrl": *,
				"stats": {
					"ratingE6": "0",
					"medianCompletionTimeMs": "0",
					"numUniqueCompletedPlayers": "0"
				},
				"status": "NOT_STARTED",
				"authorNickname": agent_name,
				"authorTeam": "ALIENS"
			},
			"version": "2"
		},...],
		"continuationToken": value
	},
	"gameBasket": {
		"gameEntities": [],
		"playerEntity": [guid, 1481912305897, {
			"avatar": {
				"foreground": {
					"layerId": "foreground4",
					"tintColor": 16249235,
					"imageUrl": *
				},
				"background": {
					"layerId": "background3",
					"tintColor": 481625,
					"imageUrl": *
				}
			},
			"playerPersonal": {
				"ap": "14031060",
				"energy": 17500,
				"allowNicknameEdit": false,
				"allowFactionChoice": false,
				"verifiedLevel": 13,
				"mediaHighWaterMarks": {
					"General": 1809,
					"RESISTANCE": 1328,
					"ALIENS": 1327
				},
				"energyState": "XM_OK",
				"notificationSettings": {
					"shouldSendEmail": false,
					"maySendPromoEmail": false,
					"shouldPushNotifyForAtPlayer": true,
					"shouldPushNotifyForPortalAttacks": true,
					"shouldPushNotifyForInvitesAndFactionInfo": true,
					"shouldPushNotifyForNewsOfTheDay": true,
					"shouldPushNotifyForEventsAndOpportunities": true,
					"locale": "zh-Hans-CN"
				},
				"profileSettings": {
					"areMetricsPublic": false
				},
				"verificationState": "UNVERIFIED",
				"extraXmTankEnergy": 0
			},
			"controllingTeam": {
				"team": "RESISTANCE"
			}
		}],
		"apGains": [],
		"inventory": [],
		"deletedEntityGuids": [],
		"serverBlob": *,
		"refreshEntityGuids": [guid, ...]
	}
}
```

### getNickNamesFromPlayerIds

	API URL: https://m-dot-betaspike.appspot.com/rpc/playerUndecorated/getNickNamesFromPlayerIds
	API Request: params: [agent_guid]
	API Response: result: [agent_name], gameBasket: {gameEntities: , inventory: , deletedEntityGuids: }


### collectItemsOrGlyphsFromPortal


	API URL: https://m-dot-betaspike.appspot.com/rpc/gameplay/collectItemsOrGlyphsFromPortal

#### Without Glyphs


	API Request:
```json
{
	"params": {
		"glyphGameRequested": false,
		"spewInfluenceGlyphSequence": null,
		"userInputGlyphSequence": null,
		"clientBasket": {
			"clientBlob": *
		},
		"knobSyncTimestamp": *,
		"energyGlobGuids": [],
		"portalGuid": guid,
		"location": value
	}
}
```

	API Response:
```json
{
	"result": {
		"items": {
			"addedGuids": [guid, ...],
			"baseHackMultiplier": "1"
		}
	},
	"gameBasket": {
		"playerDamages": [],
		"gameEntities": [],
		"playerEntity": [guid, 1481913704637, {
			"playerPersonal": {
				...,
				"energyState": "XM_OK",
				"notificationSettings": ...,
				"profileSettings": {
					"areMetricsPublic": false
				},
				"verificationState": "UNVERIFIED",
				"extraXmTankEnergy": 0
			},
			"controllingTeam": {
				"team": "RESISTANCE"
			},
			"avatar": {
				...
			}
		}],
		"apGains": [],
		"inventory": [
			[guid, 1481913704513, {
				"modResource": {
					"displayName": "Portal Shield",
					"stats": {
						"REMOVAL_STICKINESS": "0",
						"MITIGATION": "30"
					},
					"rarity": "COMMON",
					"resourceType": "RES_SHIELD"
				},
				"displayName": {
					"displayName": "Portal Shield",
					"displayDescription": "Mod which shields Portal from attacks."
				},
				"inInventory": {
					"playerId": agent_guid,
					"acquisitionTimestampMs": *
				}
			}],
			...
		],
		"deletedEntityGuids": [],
		"serverBlob": *,
		"refreshEntityGuids": [guid]
	}
}
```

#### With Glyphs

	API Request:
```json
{
	"params": {
		"glyphGameRequested": true,
		"spewInfluenceGlyphSequence": null,
		"userInputGlyphSequence": null,
		"clientBasket": {
			"clientBlob": *
		},
		"knobSyncTimestamp": 1481912295011,
		"energyGlobGuids": [],
		"portalGuid": guid,
		"location": value
	}
}
```json

	API Response:

```json
{
	"result": {
		"glyphs": {
			"glyphSequence": [{
				"glyphOrder": "ejgahic"
			}, {
				"glyphOrder": "ga"
			}, {
				"glyphOrder": "jkgh"
			}, {
				"glyphOrder": "ejka"
			}, {
				"glyphOrder": "gkhijd"
			}],
			"isPrompted": false,
			"maxInputTimeMs": "15000",
			"timeToDemoMs": "500"
		}
	},
	"gameBasket": {
		*
	}
}
```

### collectItemsFromPortalWithGlyphResponse

	API URL: https://m-dot-betaspike.appspot.com/rpc/gameplay/collectItemsFromPortalWithGlyphResponse
	API Request:
```json
{
	"params": {
		"glyphGameRequested": false,
		"spewInfluenceGlyphSequence": {
			"inputTimeMs": 1233,
			"bypassed": false,
			"glyphSequence": [{
				"glyphOrder": "hgkj"
			}, {
				"glyphOrder": "gkh"
			}]
		},
		"userInputGlyphSequence": {
			"inputTimeMs": 8683,
			"bypassed": false,
			"glyphSequence": [{
				"glyphOrder": "fgah"
			}, {
				"glyphOrder": "egjihc"
			}, {
				"glyphOrder": "egahc"
			}, {
				"glyphOrder": "ega"
			}, {
				"glyphOrder": "efabhkjd"
			}]
		},
		"clientBasket": {
			"clientBlob": *
		},
		"knobSyncTimestamp": 1481912295011,
		"energyGlobGuids": [],
		"portalGuid": "3e2bcc15c58d486fae24e2ade2bf7327.16",
		"location": "01d553fe,0631e166"
	}
}
```

	API Response:

```
{
	"result": {
		"addedGuids": ["a4f754d8e8f0448c88a6fe349f303ebc.5", "c07c542b6e0c4fea9b66b66fcc110c37.5", "c7995bba88c4442eac1ac2c8008d419c.5", "3264136a3f414efba8e88a401786bc25.5", "4d928a839c3546658abc025fb8170981.5", "65916b9be8944fe986abe47433ad4c75.5", "0e9b7f761b8f41d8b149447dfd10ca0d.5", "995fddb948bf41caab25ad1d0496e57a.5", "36ecac7a73ba43bfb21f6d4dbdd84a1f.5", "afe79b3bd18941b995557eb0d0bcef41.5"],
		"glyphResponse": {
			"glyphResponses": [true, true, true, true, true],
			"powerBoostInMillion": 1630000,
			"timeBonusBoostInMillion": 421133,
			"displayNames": ["PURSUE", "CONFLICT", "WAR", "ADVANCE", "CHAOS"],
			"bonusGuids": ["a4f754d8e8f0448c88a6fe349f303ebc.5", "c07c542b6e0c4fea9b66b66fcc110c37.5", "3264136a3f414efba8e88a401786bc25.5", "4d928a839c3546658abc025fb8170981.5", "65916b9be8944fe986abe47433ad4c75.5", "afe79b3bd18941b995557eb0d0bcef41.5"]
		},
		"baseHackMultiplier": "1"
	},
	"gameBasket": {
		"playerDamages": [],
		"gameEntities": [],
		"playerEntity": [*, 1481914255972, {
			"avatar": {
				*
			},
			"playerPersonal": {
				"ap": "14031565",
				"energy": 17100,
				"allowNicknameEdit": false,
				"allowFactionChoice": false,
				"verifiedLevel": 13,
				"mediaHighWaterMarks": {
					"General": 1809,
					"RESISTANCE": 1328,
					"ALIENS": 1327
				},
				"energyState": "XM_OK",
				"notificationSettings": {
					"shouldSendEmail": false,
					"maySendPromoEmail": false,
					"shouldPushNotifyForAtPlayer": true,
					"shouldPushNotifyForPortalAttacks": true,
					"shouldPushNotifyForInvitesAndFactionInfo": true,
					"shouldPushNotifyForNewsOfTheDay": true,
					"shouldPushNotifyForEventsAndOpportunities": true,
					"locale": "zh-Hans-CN"
				},
				"profileSettings": {
					"areMetricsPublic": false
				},
				"verificationState": "UNVERIFIED",
				"extraXmTankEnergy": 0
			},
			"controllingTeam": {
				"team": "RESISTANCE"
			}
		}],
		"apGains": [{
			"apTrigger": "GLYPH_HACK",
			"apGainAmount": "405"
		}],
		"inventory": [
			["a4f754d8e8f0448c88a6fe349f303ebc.5", 1481914255823, {
				"resourceWithLevels": {
					"resourceType": "EMITTER_A",
					"level": 8
				},
				"displayName": {
					"displayName": "Resonator",
					"displayDescription": "XM object used to power-up a Portal and align it to a Faction."
				},
				"inInventory": {
					"playerId": *,
					"acquisitionTimestampMs": "1481914255794"
				},
				"accessLevel": {
					"requiredLevel": 8,
					"failure": {
						"isAllowed": false,
						"requiredLevel": 8
					}
				}
			}],
			["c07c542b6e0c4fea9b66b66fcc110c37.5", 1481914255823, {
				"resourceWithLevels": {
					"resourceType": "EMP_BURSTER",
					"level": 8
				},
				"displayName": {
					"displayName": "Xmp Burster",
					"displayDescription": "Exotic Matter Pulse weapons which can destroy enemy Resonators and Mods and neutralize enemy Portals."
				},
				"empWeapon": {
					"level": 8,
					"ammo": 1
				},
				"inInventory": {
					"playerId": *,
					"acquisitionTimestampMs": "1481914255779"
				},
				"accessLevel": {
					"requiredLevel": 8,
					"failure": {
						"isAllowed": false,
						"requiredLevel": 8
					}
				}
			}],
			["c7995bba88c4442eac1ac2c8008d419c.5", 1481914255823, {
				"resourceWithLevels": {
					"resourceType": "EMITTER_A",
					"level": 7
				},
				"displayName": {
					"displayName": "Resonator",
					"displayDescription": "XM object used to power-up a Portal and align it to a Faction."
				},
				"inInventory": {
					"playerId": *,
					"acquisitionTimestampMs": "1481914255777"
				},
				"accessLevel": {
					"requiredLevel": 7,
					"failure": {
						"isAllowed": false,
						"requiredLevel": 7
					}
				}
			}],
			["3264136a3f414efba8e88a401786bc25.5", 1481914255823, {
				"resourceWithLevels": {
					"resourceType": "EMP_BURSTER",
					"level": 7
				},
				"displayName": {
					"displayName": "Xmp Burster",
					"displayDescription": "Exotic Matter Pulse weapons which can destroy enemy Resonators and Mods and neutralize enemy Portals."
				},
				"empWeapon": {
					"level": 7,
					"ammo": 1
				},
				"inInventory": {
					"playerId": *,
					"acquisitionTimestampMs": "1481914255794"
				},
				"accessLevel": {
					"requiredLevel": 7,
					"failure": {
						"isAllowed": false,
						"requiredLevel": 7
					}
				}
			}],
			["4d928a839c3546658abc025fb8170981.5", 1481914255823, {
				"resourceWithLevels": {
					"resourceType": "EMITTER_A",
					"level": 8
				},
				"displayName": {
					"displayName": "Resonator",
					"displayDescription": "XM object used to power-up a Portal and align it to a Faction."
				},
				"inInventory": {
					"playerId": *,
					"acquisitionTimestampMs": "1481914255779"
				},
				"accessLevel": {
					"requiredLevel": 8,
					"failure": {
						"isAllowed": false,
						"requiredLevel": 8
					}
				}
			}],
			["65916b9be8944fe986abe47433ad4c75.5", 1481914255823, {
				"resourceWithLevels": {
					"resourceType": "EMITTER_A",
					"level": 8
				},
				"displayName": {
					"displayName": "Resonator",
					"displayDescription": "XM object used to power-up a Portal and align it to a Faction."
				},
				"inInventory": {
					"playerId": *,
					"acquisitionTimestampMs": "1481914255780"
				},
				"accessLevel": {
					"requiredLevel": 8,
					"failure": {
						"isAllowed": false,
						"requiredLevel": 8
					}
				}
			}],
			["0e9b7f761b8f41d8b149447dfd10ca0d.5", 1481914255823, {
				"resourceWithLevels": {
					"resourceType": "EMITTER_A",
					"level": 8
				},
				"displayName": {
					"displayName": "Resonator",
					"displayDescription": "XM object used to power-up a Portal and align it to a Faction."
				},
				"inInventory": {
					"playerId": *,
					"acquisitionTimestampMs": "1481914255778"
				},
				"accessLevel": {
					"requiredLevel": 8,
					"failure": {
						"isAllowed": false,
						"requiredLevel": 8
					}
				}
			}],
			["995fddb948bf41caab25ad1d0496e57a.5", 1481914255823, {
				"resourceWithLevels": {
					"resourceType": "POWER_CUBE",
					"level": 8
				},
				"displayName": {
					"displayName": "Power Cube",
					"displayDescription": "Store of XM which can be used to recharge Scanner."
				},
				"inInventory": {
					"playerId": *,
					"acquisitionTimestampMs": "1481914255778"
				},
				"accessLevel": {
					"requiredLevel": 8,
					"failure": {
						"isAllowed": false,
						"requiredLevel": 8
					}
				},
				"powerCube": {
					"energy": 8000
				}
			}],
			["36ecac7a73ba43bfb21f6d4dbdd84a1f.5", 1481914255823, {
				"resourceWithLevels": {
					"resourceType": "EMITTER_A",
					"level": 8
				},
				"displayName": {
					"displayName": "Resonator",
					"displayDescription": "XM object used to power-up a Portal and align it to a Faction."
				},
				"inInventory": {
					"playerId": *,
					"acquisitionTimestampMs": "1481914255778"
				},
				"accessLevel": {
					"requiredLevel": 8,
					"failure": {
						"isAllowed": false,
						"requiredLevel": 8
					}
				}
			}],
			["afe79b3bd18941b995557eb0d0bcef41.5", 1481914255823, {
				"resourceWithLevels": {
					"resourceType": "POWER_CUBE",
					"level": 8
				},
				"displayName": {
					"displayName": "Power Cube",
					"displayDescription": "Store of XM which can be used to recharge Scanner."
				},
				"inInventory": {
					"playerId": *,
					"acquisitionTimestampMs": "1481914255779"
				},
				"accessLevel": {
					"requiredLevel": 8,
					"failure": {
						"isAllowed": false,
						"requiredLevel": 8
					}
				},
				"powerCube": {
					"energy": 8000
				}
			}]
		],
		"deletedEntityGuids": [],
		"serverBlob": *,
		"refreshEntityGuids": [guid]
	}
}
```

这里把所有提交和得到的参数都列明了，说明一下画图的字母代表哪个位置：

从上到下，从左到右依次是

	a
	fb
	gh
	k
	ejic
	d

也就是 ALL命令从最上方顶点顺时针依次是abcd(最下面)dfa; Strong命令从左上角开始顺时针ghij;中心是k

#结语

	用了两个晚上统计了下API。
	本来打算也写一份Game API的库，但是因为不能生成客户端blob并没有意义，以后用到再说，Intel Map已经ok了。
	在游戏过程中，batch会在移动的时候触发
	获取地图更新是定时轮询:getInventory（毕竟还可以passcode获取物品，所有得一直get）,getPaginatedPlexts,getObjectsInCells
