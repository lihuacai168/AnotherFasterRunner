/*
 Navicat Premium Data Transfer

 Source Server         : localhost-13306
 Source Server Type    : MySQL
 Source Server Version : 80021
 Source Host           : localhost:13306
 Source Schema         : fast_db

 Target Server Type    : MySQL
 Target Server Version : 80021
 File Encoding         : 65001

 Date: 22/02/2022 21:49:47
*/

create database if not exists fast_db default charset utf8 collate utf8_general_ci;
use fast_db;


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for api
-- ----------------------------
DROP TABLE IF EXISTS `api`;
CREATE TABLE `api` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `body` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `method` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `relation` int NOT NULL,
  `project_id` int NOT NULL,
  `delete` int DEFAULT NULL,
  `rig_id` int DEFAULT NULL,
  `rig_env` int NOT NULL,
  `tag` int NOT NULL,
  `creator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updater` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `yapi_catid` int DEFAULT NULL,
  `yapi_id` int DEFAULT NULL,
  `ypai_add_time` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ypai_up_time` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ypai_username` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `API_project_id_a5a33dab_fk_Project_id` (`project_id`) USING BTREE,
  KEY `API_rig_id_b8d97be0` (`rig_id`) USING BTREE,
  KEY `API_url_c82eef4e` (`url`) USING BTREE,
  KEY `API_name_06ef6e67` (`name`) USING BTREE,
  KEY `create_time` (`create_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10977 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of api
-- ----------------------------
BEGIN;
INSERT INTO `api` VALUES (3729, '2019-11-19 10:05:31.914532', '2021-11-23 21:38:32.345070', '123', '{\'name\': \'登录-成功\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'$test_password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'test_user\': \'\'}, \'extract\': {\'token\': \'\'}}, \'extract\': [{\'token\': \'content.token\'}], \'validate\': [{\'equals\': [\'content.code\', \'0001\']}, {\'equals\': [\'content.user\', \'$test_user\']}, {\'length_equals\': [\'$token\', 201]}], \'variables\': [{\'test_user\': \'qa1\'}]}', '/api/user/login/', 'POST', 1, 7, 0, NULL, 0, 4, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3730, '2019-11-19 10:05:38.141352', '2020-05-09 13:08:31.473864', '注册', '{\'name\': \'注册\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/register/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'test\', \'password\': \'test123\', \'email\': \'lihuacai168@foxmail.com\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.code\', \'0001\']}]}', '/api/user/register/', 'POST', 1, 7, 1, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3731, '2019-11-19 11:47:16.916407', '2019-11-19 11:56:10.317463', '获取API列表-调用全局变量token-断言results列表第一个元素project字段', '{\'name\': \'获取API列表-调用全局变量token-断言results列表第一个元素project字段\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/api/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7]}]}', '/api/fastrunner/api/', 'GET', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3732, '2019-11-19 12:01:24.300060', '2019-11-19 12:01:24.300097', '搜索用例-用例名存在', '{\'name\': \'搜索用例-用例名存在\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \' \', \'project\': \'7\', \'search\': \'$case_name\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {\'case_name\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7]}, {\'equals\': [\'content.results.0.name\', \'$case_name\']}], \'variables\': [{\'case_name\': \'登录hook\'}]}', '/api/fastrunner/test/', 'GET', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3733, '2019-12-25 11:28:25.753428', '2019-12-25 11:28:25.753462', '获取全局变量', '{\'name\': \'获取全局变量\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/variables\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \' \'}}, \'desc\': {\'header\': {\'Authorization\': \'token是全局变量\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7]}]}', '/api/fastrunner/variables', 'GET', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3734, '2019-12-25 11:34:22.648255', '2019-12-25 11:34:22.648293', '登录-密码错误', '{\'name\': \'登录-密码错误\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'test1233\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.code\', \'0103\']}, {\'equals\': [\'content.msg\', \'用户名或密码错误\']}]}', '/api/user/login/', 'POST', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3735, '2019-12-25 11:37:22.904104', '2020-10-17 23:29:03.097688', '登录-用户未注册', '{\'name\': \'登录-用户未注册\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'test111\', \'password\': \'test123\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'username\': \'\', \'password\': \'\'}, \'extract\': {\'code\': \'\', \'msg\': \'\'}}, \'enabled\': {\'params\': {}, \'variables\': {\'username\': False, \'password\': False}, \'extract\': {\'code\': True, \'msg\': True}, \'validate\': [True, True]}, \'extract\': [{\'code\': \'content.code\'}, {\'msg\': \'content.msg\'}], \'validate\': [{\'equals\': [\'content.code\', \'0104\'], \'enabled\': True}, {\'equals\': [\'content.msg\', \'该用户未注册\'], \'enabled\': True}], \'variables\': [{\'username\': \'test111\'}, {\'password\': \'test123\'}]}', '/api/user/login/', 'POST', 1, 7, 1, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3736, '2019-12-25 11:43:18.519649', '2019-12-25 11:43:18.519689', '搜索用例-用例不存在', '{\'name\': \'搜索用例-用例不存在\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \' \', \'project\': \'7\', \'search\': \'$case_name\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'通过$token引用全局变量token\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {\'case_name\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results\', []]}, {\'equals\': [\'content.count\', 0]}], \'variables\': [{\'case_name\': \'注册\'}]}', '/api/fastrunner/test/', 'GET', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3737, '2019-12-25 11:47:34.038367', '2019-12-25 11:47:34.038411', ' 搜索用例-搜索条件为空,返回前11条', '{\'name\': \' 搜索用例-搜索条件为空,返回前11条\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \' \', \'project\': \'7\', \'search\': \'\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {\'case_name\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7]}, {\'greater_than_or_equals\': [\'content.count\', 3]}], \'variables\': [{\'case_name\': \'搜索用例\'}]}', '/api/fastrunner/test/', 'GET', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3738, '2019-12-28 19:51:58.774046', '2020-05-09 13:08:27.364782', '注册-失败', '{\'name\': \'注册-失败\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/register/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'test\', \'password\': \'test123\', \'email\': \'lihuacai168@foxmail.com\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.code\', \'0101\']}]}', '/api/user/register/', 'POST', 1, 7, 1, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3739, '2019-12-29 23:28:41.665208', '2019-12-29 23:28:41.665244', '登录-密码错误-setup修改请求参数', '{\'name\': \'登录-密码错误-setup修改请求参数\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'错误的密码\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.code\', \'0001\']}, {\'equals\': [\'content.msg\', \'login success\']}], \'setup_hooks\': [\'${set_up($request)}\']}', '/api/user/login/', 'POST', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3740, '2019-12-29 23:39:55.362395', '2019-12-29 23:39:55.362440', '登录-成功-teardown-修改返回结果', '{\'name\': \'登录-成功-teardown-修改返回结果\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'$test_password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'token\': \'抽取默认的返回token\', \'mytoken\': \'\'}}, \'extract\': [{\'token\': \'content.token\'}, {\'mytoken\': \'teardown.mytoken\'}], \'validate\': [{\'equals\': [\'content.code\', \'0001\']}, {\'equals\': [\'content.user\', \'$test_user\']}, {\'equals\': [\'$mytoken\', \'$token\']}], \'teardown_hooks\': [\'${teardown($response)}\']}', '/api/user/login/', 'POST', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3741, '2019-12-30 00:17:58.083349', '2019-12-30 00:17:58.083400', '登录-失败-参数化', '{\'name\': \'登录-失败-参数化\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$username\', \'password\': \'$password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'msg\': \'\'}, \'extract\': {}}, \'validate\': [{\'startswith\': [\'content.code\', \'01\']}], \'variables\': [{\'msg\': \'${param_msg()}\'}]}', '/api/user/login/', 'POST', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3742, '2020-01-06 13:52:39.881538', '2020-08-16 23:22:32.985374', '获取API列表-调用驱动函数获取token', '{\'name\': \'获取API列表-调用驱动函数获取token\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/api/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'${get_token()}\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}, \'variables\': {\'test\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', \'7\']}], \'variables\': [{\'test\': \'\'}]}', '/api/fastrunner/api/', 'GET', 1, 7, 0, NULL, 1, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (3743, '2020-05-29 19:25:55.902320', '2020-05-29 19:26:06.023802', '获取API列表-调用驱动函数获取token1', '{\'name\': \'获取API列表-调用驱动函数获取token1\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/api/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'${get_token()}\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}, \'variables\': {\'test\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7]}], \'variables\': [{\'test\': \'\'}]}', '/api/fastrunner/api/', 'GET', 1, 7, 1, NULL, 1, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4066, '2020-09-14 23:14:47.097633', '2020-09-14 23:14:47.097660', '聚合数据-笑话大全', '{\'name\': \'聚合数据-笑话大全\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://v.juhe.cn/joke/content/list.php\', \'method\': \'GET\', \'verify\': False, \'params\': {\'sort\': \'desc\', \'page\': \'1\', \'pagesize\': \'10\', \'time\': \'1600096122\', \'key\': \'e2ec0aecb1a2fc282f59b6fe961478e2\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {\'sort\': \'desc:指定时间之前发布的，asc:指定时间之后发布的\', \'page\': \'当前页数,默认1,最大20\\t\', \'pagesize\': \'每次返回条数,默认1,最大20\\t\', \'time\': \'时间戳（10位），如：1418816972\\t\', \'key\': \'请求密钥\'}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.result.data.0\', {\'content\': \'某先生是地方上的要人。一天，他像往常一样在书房里例览当日报纸，突然对妻子大声喊道：喂，安娜，你看到今天早报上的流言蜚语了吗？真可笑！他们说，你收拾行装出走了。你听见了吗？安娜、你在哪儿？安娜？啊！\', \'hashId\': \'90B182FC7F74865B40B1E5807CFEBF41\', \'unixtime\': 1418745227, \'updatetime\': \'2014-12-16 23:53:47\'}]}, {\'equals\': [\'content.reason\', \'Success\']}]}', 'http://v.juhe.cn/joke/content/list.php', 'GET', 2, 7, 0, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4067, '2020-09-15 02:17:49.877744', '2020-09-15 02:17:49.877770', '全国房产信息', '{\'name\': \'全国房产信息\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://route.showapi.com/1610-1\', \'method\': \'GET\', \'verify\': False, \'params\': {\'cityName\': \'广州\', \'hourseName\': \'星河湾\', \'page\': \'1\', \'showapi_appid\': \'366062\', \'showapi_sign\': \'3492b4075b0f4c5db16c21f9164e8ee0\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {\'cityName\': \'\', \'hourseName\': \'\', \'page\': \'\', \'showapi_appid\': \'\', \'showapi_sign\': \'\'}, \'variables\': {}, \'extract\': {}}}', 'http://route.showapi.com/1610-1', 'GET', 2, 7, 0, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4071, '2020-09-22 20:32:41.601814', '2020-09-22 20:32:41.601837', '获取API列表-调用驱动函数获取token-1', '{\'name\': \'获取API列表-调用驱动函数获取token-1\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/api/?page=1&node=&project=12&search=&tag=&rigEnv=&onlyMe=false\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'${get_token()}\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'test\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', \'7\']}], \'variables\': [{\'test\': \'\'}]}', '/api/fastrunner/api/?page=1&node=&project=12&search=&tag=&rigEnv=&onlyMe=false', 'GET', 3, 7, 0, NULL, 1, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4076, '2020-10-18 22:03:30.652747', '2020-10-18 22:03:30.652793', 'xxx', '{\'name\': \'xxx\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'ddd\', \'method\': \'POST\', \'verify\': False}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\"d\'d\": \'\'}, \'extract\': {}}, \'enabled\': {\'params\': {}, \'variables\': {}, \'extract\': {}, \'validate\': {}}, \'variables\': [{\"d\'d\": \'点点点\'}]}', 'ddd', 'POST', 1, 7, 1, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4077, '2020-10-18 22:10:58.384006', '2020-10-18 22:10:58.384102', 'dd', '{\'name\': \'dd\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'fff\', \'method\': \'POST\', \'verify\': False, \'params\': {\'pp\': \'123\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {\'pp\': \'\'}, \'variables\': {\'dd\': \'\', \'1dd2\': \'\'}, \'extract\': {}}, \'enabled\': {\'params\': {}, \'variables\': {\'dd\': True, \'1dd2\': True}, \'extract\': {}, \'validate\': {}}, \'variables\': [{\'dd\': \'dsdd\'}, {\'1dd2\': \'ddd\'}]}', 'fff', 'POST', 1, 7, 1, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4078, '2020-10-19 00:01:32.283833', '2020-10-23 01:07:54.670273', ' 搜索用例-搜索条件为空,返回前11条1', '{\'name\': \' 搜索用例-搜索条件为空,返回前11条1\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'api\', \'node\': \' \', \'project\': \'7\', \'search\': \'\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {\'a\': \'\', \'ss\': \'\'}, \'extract\': {\'c\': \'描述c\'}}, \'enabled\': {\'params\': {\'caseNameOrUrl\': True, \'node\': True, \'project\': True, \'search\': True}, \'variables\': {\'a\': True, \'ss\': True}, \'extract\': {\'c\': True}, \'validate\': [True, True, True]}, \'extract\': [{\'c\': \'content.count\'}], \'validate\': [{\'equals\': [\'content.count\', 6], \'enabled\': True}, {\'equals\': [\'content.count\', 6], \'enabled\': True}, {\'equals\': [\'content.count\', 6], \'enabled\': True}], \'variables\': [{\'a\': \'b32\'}, {\'ss\': \'44\'}, {\'ss\': \'44\'}]}', '/api/fastrunner/test/', 'GET', 1, 7, 1, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4079, '2020-10-19 13:15:19.355818', '2020-10-19 13:15:19.355862', ' 搜索用例-搜索条件为空,返回前11条15', '{\'name\': \' 搜索用例-搜索条件为空,返回前11条15\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'api\', \'node\': \' \', \'project\': \'7\', \'search\': \'\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {\'a\': \'\'}, \'extract\': {\'c\': \'描述c\'}}, \'enabled\': {\'params\': {\'caseNameOrUrl\': True, \'node\': True, \'project\': True, \'search\': True}, \'variables\': {\'a\': True}, \'extract\': {\'c\': True}, \'validate\': [True, True, True]}, \'extract\': [{\'c\': \'content.count\'}], \'validate\': [{\'equals\': [\'content.count\', \'6\'], \'enabled\': True}, {\'equals\': [\'content.count\', \'6\'], \'enabled\': True}, {\'equals\': [\'content.count\', \'6\'], \'enabled\': True}], \'variables\': [{\'a\': \'b32\'}]}', '/api/fastrunner/test/', 'GET', 1, 7, 1, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4087, '2020-11-19 19:25:45.938999', '2020-11-19 19:25:45.939115', '登录-成功1', '{\'name\': \'登录-成功1\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'$test_password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'test_user\': \'\', \'intV\': \'\'}, \'extract\': {\'token\': \'\'}}, \'extract\': [{\'token\': \'content.token\'}], \'validate\': [{\'equals\': [\'content.code\', \'0001\']}, {\'equals\': [\'content.user\', \'$test_user\']}, {\'length_equals\': [\'$token\', 201]}, {\'equals\': [\'content.code\', \'$intV\']}], \'variables\': [{\'test_user\': \'qa1\'}, {\'intV\': 1}]}', '/api/user/login/', 'POST', 3, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4088, '2020-12-05 13:44:45.113155', '2020-12-05 13:44:49.919439', '获取API列表-调用驱动函数获取token-188', '{\'name\': \'获取API列表-调用驱动函数获取token-188\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/api/?page=1&node=&project=12&search=&tag=&rigEnv=&onlyMe=false\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'${get_token()}\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'test\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', \'7\']}], \'variables\': [{\'test\': \'\'}]}', '/api/fastrunner/api/?page=1&node=&project=12&search=&tag=&rigEnv=&onlyMe=false', 'GET', 1, 7, 0, NULL, 1, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4089, '2020-12-05 14:37:19.910588', '2020-12-05 14:37:19.910629', '全国房产信息', '{\'name\': \'全国房产信息\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://route.showapi.com/1610-1\', \'method\': \'GET\', \'verify\': False, \'params\': {\'cityName\': \'广州\', \'hourseName\': \'星河湾\', \'page\': \'1\', \'showapi_appid\': \'366062\', \'showapi_sign\': \'3492b4075b0f4c5db16c21f9164e8ee0\'}, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {\'cityName\': \'\', \'hourseName\': \'\', \'page\': \'\', \'showapi_appid\': \'\', \'showapi_sign\': \'\'}, \'variables\': {}, \'extract\': {}}}', 'http://route.showapi.com/1610-1', 'GET', 1, 7, 0, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4090, '2020-12-05 14:37:24.981317', '2020-12-05 14:37:24.981404', '聚合数据-笑话大全', '{\'name\': \'聚合数据-笑话大全\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://v.juhe.cn/joke/content/list.php\', \'method\': \'GET\', \'verify\': False, \'params\': {\'sort\': \'desc\', \'page\': \'1\', \'pagesize\': \'10\', \'time\': \'1600096122\', \'key\': \'e2ec0aecb1a2fc282f59b6fe961478e2\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {\'sort\': \'desc:指定时间之前发布的，asc:指定时间之后发布的\', \'page\': \'当前页数,默认1,最大20\\t\', \'pagesize\': \'每次返回条数,默认1,最大20\\t\', \'time\': \'时间戳（10位），如：1418816972\\t\', \'key\': \'请求密钥\'}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.result.data.0\', {\'content\': \'某先生是地方上的要人。一天，他像往常一样在书房里例览当日报纸，突然对妻子大声喊道：喂，安娜，你看到今天早报上的流言蜚语了吗？真可笑！他们说，你收拾行装出走了。你听见了吗？安娜、你在哪儿？安娜？啊！\', \'hashId\': \'90B182FC7F74865B40B1E5807CFEBF41\', \'unixtime\': 1418745227, \'updatetime\': \'2014-12-16 23:53:47\'}]}, {\'equals\': [\'content.reason\', \'Success\']}]}', 'http://v.juhe.cn/joke/content/list.php', 'GET', 1, 7, 0, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (4091, '2020-12-05 14:37:29.120743', '2020-12-05 14:37:29.120788', '获取API列表-调用驱动函数获取token', '{\'name\': \'获取API列表-调用驱动函数获取token\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/api/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'${get_token()}\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}, \'json\': {}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}, \'variables\': {\'test\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', \'7\', \'\']}], \'variables\': [{\'test\': \'\'}]}', '/api/fastrunner/api/', 'GET', 1, 7, 0, NULL, 1, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10789, '2021-06-06 21:08:01.282618', '2021-06-06 21:13:26.565489', ' 搜索用例-', '{\'name\': \' 搜索用例-\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'11\', \'search\': \'\'}, \'json\': {}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {}, \'extract\': {}}, \'teardown_hooks\': [\'${wait(1)}\']}', '/api/fastrunner/test/', 'GET', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10904, '2021-06-25 12:29:15.469013', '2021-06-25 12:29:15.469053', 'xml', '{\'name\': \'xml\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'https://6ab4c55f-6803-446a-8aff-2994ab3169ae.mock.pstmn.io/api/fastrunner/ci/\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', 'https://6ab4c55f-6803-446a-8aff-2994ab3169ae.mock.pstmn.io/api/fastrunner/ci/', 'POST', 1, 7, 0, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10905, '2021-06-25 12:29:40.649634', '2021-12-24 16:11:48.498098', '获取全局变量-异常', '{\'name\': \'获取全局变量-异常\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/variables\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \' \'}, \'json\': {}}, \'desc\': {\'header\': {\'Authorization\': \'token是全局变量\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7, \'\']}]}', '/api/fastrunner/variables', 'GET', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10943, '2021-07-26 21:25:14.659699', '2021-07-26 21:25:19.933582', 'mock-dict', '{\'name\': \'mock-dict\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/dict\', \'method\': \'GET\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}]}', '$mock_url/dict', 'GET', 31, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10944, '2021-07-26 21:25:26.113888', '2021-07-26 21:25:26.113914', 'mock-list', '{\'name\': \'mock-list\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/list\', \'method\': \'GET\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}]}', '$mock_url/list', 'GET', 31, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10945, '2021-07-26 22:24:26.177438', '2021-07-26 22:24:26.177487', 'mock-list', '{\'name\': \'mock-list\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/list\', \'method\': \'GET\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}]}', '$mock_url/list', 'GET', 36, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10946, '2021-07-26 22:24:28.749289', '2021-12-24 16:11:42.142161', 'mock-dict', '{\'name\': \'mock-dict\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/dict\', \'method\': \'GET\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}]}', '$mock_url/dict', 'GET', 31, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10949, '2021-08-03 11:23:09.358488', '2021-12-24 16:11:56.365280', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 32, 7, 0, NULL, 0, 4, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10950, '2021-11-29 14:24:24.489830', '2021-11-29 14:28:09.591827', '用户登录', '{\'name\': \'用户登录\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/system/user-auth/login\', \'method\': \'POST\', \'verify\': False, \'json\': {\'login_name\': \'17319070664\', \'password\': \'71143f7d2dfb1a2f0743a09495772868\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/api/system/user-auth/login', 'POST', 36, 7, 1, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10951, '2021-12-08 14:26:15.086539', '2021-12-08 14:26:15.086559', 'test', '{\'name\': \'test\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://www.baidu.com\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', 'http://www.baidu.com', 'POST', 1, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10952, '2021-12-27 10:31:54.783005', '2021-12-27 10:31:54.783028', 'sss', '{\'name\': \'sss\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/login\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/login', 'POST', 47, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10953, '2021-12-27 10:38:34.481462', '2021-12-27 10:38:34.481483', '测试百度', '{\'name\': \'测试百度\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://www.baidu.com\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', 'http://www.baidu.com', 'POST', 47, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10954, '2021-12-27 10:43:04.766402', '2021-12-27 10:43:04.766424', 'sss', '{\'name\': \'sss\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://www.baidu.com\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', 'http://www.baidu.com', 'POST', 48, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10955, '2021-12-30 15:41:49.665342', '2021-12-30 15:41:49.665364', '测试百度', '{\'name\': \'测试百度\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://www.baidu.com\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', 'http://www.baidu.com', 'POST', 47, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10956, '2022-01-04 18:02:04.341448', '2022-01-04 18:02:04.341469', '0000', '{\'name\': \'0000\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/api/', 'POST', 36, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10957, '2022-01-10 14:38:00.082844', '2022-01-10 14:38:00.082871', 'sss', '{\'name\': \'sss\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://www.baidu.com\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', 'http://www.baidu.com', 'POST', 48, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10958, '2022-01-12 23:29:09.506854', '2022-01-12 23:29:09.506876', '接口名称', '{\'name\': \'接口名称\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'urlpath\', \'method\': \'POST\', \'verify\': False, \'headers\': {\'header\': \'header\'}, \'data\': {\'req\': \'req\'}, \'json\': {}}, \'desc\': {\'header\': {\'header\': \'\'}, \'data\': {\'req\': \'\'}, \'files\': {}, \'params\': {}, \'variables\': {\'var\': \'\'}, \'extract\': {\'ext\': \'\'}}, \'extract\': [{\'ext\': \'ext\'}], \'validate\': [{\'equals\': [\'val\', \'\', None]}], \'variables\': [{\'var\': \'\'}]}', 'urlpath', 'POST', 30, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10959, '2022-01-14 14:17:03.702949', '2022-01-14 14:17:03.702970', '普通用户登录成功', '{\'name\': \'普通用户登录成功\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/v1/login\', \'method\': \'POST\', \'verify\': False, \'headers\': {\'Authorization\': \'jwt ssssss\'}, \'params\': {\'a\': \'1\'}, \'json\': {\'username\': \'$username\', \'password\': \'123456\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'a\': \'\'}, \'variables\': {\'username\': \'登录名称\'}, \'extract\': {\'token\': \'\'}}, \'extract\': [{\'token\': \'${token}\'}], \'validate\': [{\'equals\': [\'200\', \'response.data\', \'\']}], \'variables\': [{\'username\': \'admin\'}], \'setup_hooks\': [\'${hook1}\'], \'teardown_hooks\': [\'${hook55}\']}', '/api/v1/login', 'POST', 49, 7, 0, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10960, '2022-01-18 18:27:02.134354', '2022-01-18 18:27:02.134374', '获取全局变量-异常', '{\'name\': \'获取全局变量-异常\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/variables\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \' \'}, \'json\': {}}, \'desc\': {\'header\': {\'Authorization\': \'token是全局变量\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7, \'\']}]}', '/api/fastrunner/variables', 'GET', 1, 7, 0, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10961, '2022-01-18 18:27:16.550287', '2022-01-18 18:27:16.550309', '获取全局变量-异常', '{\'name\': \'获取全局变量-异常\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/variables\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \' \'}, \'json\': {}}, \'desc\': {\'header\': {\'Authorization\': \'token是全局变量\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7, \'\']}]}', '/api/fastrunner/variables', 'GET', 1, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10962, '2022-01-20 14:03:44.220274', '2022-01-20 14:03:44.220297', '查询所有项目', '{\'name\': \'查询所有项目\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/v1/project/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'jwt {{ACCESS_TOKEN}}\'}, \'json\': {}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/api/v1/project/', 'GET', 1, 8, 0, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10963, '2022-01-20 14:11:42.310390', '2022-01-20 14:11:42.310412', '登录接口', '{\'name\': \'登录接口\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/v1/auth/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'admin\', \'password\': \'123456\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/api/v1/auth/login/', 'POST', 1, 8, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10964, '2022-01-20 17:50:42.236645', '2022-01-20 17:50:42.236665', '登录', '{\'name\': \'登录\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/v1/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/api/v1/login/', 'POST', 4, 8, 0, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10965, '2022-01-27 22:48:52.275329', '2022-01-27 22:48:52.275347', '123123', '{\'name\': \'123123\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/get\', \'method\': \'POST\', \'verify\': False, \'params\': {\'123\': \'123\'}, \'data\': {\'123\': \'123\'}, \'json\': {\'key\': 123}}, \'desc\': {\'header\': {}, \'data\': {\'123\': \'\'}, \'files\': {}, \'params\': {\'123\': \'\'}, \'variables\': {}, \'extract\': {}}}', '/get', 'POST', 1, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10966, '2022-01-28 10:46:38.394743', '2022-01-28 10:46:38.394763', '123123', '{\'name\': \'123123\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/get\', \'method\': \'POST\', \'verify\': False, \'params\': {\'123\': \'123\'}, \'data\': {\'123\': \'123\'}, \'json\': {\'key\': 123}}, \'desc\': {\'header\': {}, \'data\': {\'123\': \'\'}, \'files\': {}, \'params\': {\'123\': \'\'}, \'variables\': {}, \'extract\': {}}}', '/get', 'POST', 1, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10967, '2022-02-03 20:16:34.154587', '2022-02-03 20:16:34.154607', '普通用户登录成功', '{\'name\': \'普通用户登录成功\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/v1/login\', \'method\': \'POST\', \'verify\': False, \'headers\': {\'Authorization\': \'jwt ssssss\'}, \'params\': {\'a\': \'1\'}, \'json\': {\'username\': \'$username\', \'password\': \'123456\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'a\': \'\'}, \'variables\': {\'username\': \'登录名称\'}, \'extract\': {\'token\': \'\'}}, \'extract\': [{\'token\': \'${token}\'}], \'validate\': [{\'equals\': [\'200\', \'response.data\', \'\']}], \'variables\': [{\'username\': \'admin\'}], \'setup_hooks\': [\'${hook1}\'], \'teardown_hooks\': [\'${hook55}\']}', '/api/v1/login', 'POST', 49, 7, 0, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10968, '2022-02-07 11:31:24.762084', '2022-02-07 11:31:24.762104', '登录失败', '{\'name\': \'登录失败\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/v1/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'admin\', \'password\': \'123456\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/api/v1/login/', 'POST', 1, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10969, '2022-02-07 11:32:06.738827', '2022-02-07 11:36:39.135153', '登录异常', '{\'name\': \'登录异常\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/v1/login/\', \'method\': \'POST\', \'verify\': False, \'headers\': {\'Authorization\': \'jwt dsdsdsiwefjskdsdfjsfksffdnncncsieeieieie\', \'Content-Type\': \'application/json\'}, \'data\': {\'username\': \'jkc\', \'password\': \'111111\'}, \'json\': {\'username\': \'admin1\', \'passowrd\': \'888889\'}}, \'desc\': {\'header\': {\'Authorization\': \'认证信息\', \'Content-Type\': \'请求方式\'}, \'data\': {\'username\': \'用户A\', \'password\': \'用户A对应的密码\'}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/api/v1/login/', 'POST', 1, 7, 0, NULL, 0, 2, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10970, '2022-02-07 14:33:27.829949', '2022-02-08 16:06:50.555965', '接口名称123', '{\'name\': \'接口名称123\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/v1/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/v1/login/', 'POST', 1, 7, 0, NULL, 0, 1, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10971, '2022-02-08 11:09:18.442494', '2022-02-08 11:09:18.442514', '1111', '{\'name\': \'1111\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'1111\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'1111\': \'\'}}, \'extract\': [{\'1111\': \'1111\'}]}', '1111', 'POST', 31, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10972, '2022-02-08 11:18:50.071892', '2022-02-08 11:18:50.071918', '登录', '{\'name\': \'登录\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/v1/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/api/v1/login/', 'POST', 4, 8, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10973, '2022-02-08 16:59:42.822673', '2022-02-08 16:59:42.822694', '接口名称123', '{\'name\': \'接口名称123\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/v1/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/v1/login/', 'POST', 1, 7, 0, NULL, 0, 0, 'test', NULL, 0, 0, '', '', '');
INSERT INTO `api` VALUES (10974, '2022-02-11 13:48:45.522968', '2022-02-11 13:48:45.522988', '123123', '{\'name\': \'123123\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'123123\', \'method\': \'POST\', \'verify\': False, \'json\': {\'abc\': 123}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '123123', 'POST', 31, 7, 0, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10975, '2022-02-12 15:27:48.237246', '2022-02-12 16:29:15.396717', '登录接口', '{\'name\': \'登录接口\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/udx/service\', \'method\': \'POST\', \'verify\': False, \'json\': {\'LoginInfo\': {\'ClientType\': \'IOS\'}, \'MethodName\': \'Login\', \'ObjectData\': {\'Password\': \'13823207170\', \'UserId\': \'abc123\', \'JiGuangId\': \'101d855909e128c11df\'}, \'SensorsInfo\': {\'AppName\': \'试衣到家app\', \'PlatformType\': \'iOS\', \'DistinctId\': \'3d8043dd-d70d-428d-bccc-640850514e4c\'}, \'Tag\': \'\', \'UniqueKey\': \'FitApp.FitCustomerLoginDomain\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/udx/service', 'POST', 54, 7, 1, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
INSERT INTO `api` VALUES (10976, '2022-02-12 16:29:10.332753', '2022-02-12 16:39:39.702360', '登录接口', '{\'name\': \'登录接口\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/udx/service\', \'method\': \'POST\', \'verify\': False, \'headers\': {\'Udx-Method\': \'FitApp.FitCustomerLoginDomain.Login\'}, \'json\': {\'LoginInfo\': {\'ClientType\': \'IOS\'}, \'MethodName\': \'Login\', \'ObjectData\': {\'Password\': \'13823207170\', \'UserId\': \'abc123\', \'JiGuangId\': \'101d855909e128c11df\'}, \'SensorsInfo\': {\'AppName\': \'试衣到家app\', \'PlatformType\': \'iOS\', \'DistinctId\': \'3d8043dd-d70d-428d-bccc-640850514e4c\'}, \'Tag\': \'\', \'UniqueKey\': \'FitApp.FitCustomerLoginDomain\'}}, \'desc\': {\'header\': {\'Udx-Method\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/udx/service', 'POST', 54, 7, 1, NULL, 0, 0, 'test', 'test', 0, 0, '', '', '');
COMMIT;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;
INSERT INTO `auth_group` VALUES (4, 'g1');
INSERT INTO `auth_group` VALUES (2, '开发组');
INSERT INTO `auth_group` VALUES (1, '测试组1');
INSERT INTO `auth_group` VALUES (3, '超级管理员');
COMMIT;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`) USING BTREE,
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissions_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
BEGIN;
INSERT INTO `auth_group_permissions` VALUES (1, 1, 65);
INSERT INTO `auth_group_permissions` VALUES (2, 1, 66);
INSERT INTO `auth_group_permissions` VALUES (3, 1, 67);
INSERT INTO `auth_group_permissions` VALUES (4, 1, 68);
INSERT INTO `auth_group_permissions` VALUES (5, 1, 69);
INSERT INTO `auth_group_permissions` VALUES (6, 1, 70);
INSERT INTO `auth_group_permissions` VALUES (7, 1, 71);
INSERT INTO `auth_group_permissions` VALUES (8, 1, 72);
INSERT INTO `auth_group_permissions` VALUES (9, 1, 73);
INSERT INTO `auth_group_permissions` VALUES (10, 1, 74);
INSERT INTO `auth_group_permissions` VALUES (11, 1, 75);
INSERT INTO `auth_group_permissions` VALUES (12, 1, 76);
INSERT INTO `auth_group_permissions` VALUES (25, 3, 1);
INSERT INTO `auth_group_permissions` VALUES (26, 3, 2);
INSERT INTO `auth_group_permissions` VALUES (27, 3, 3);
INSERT INTO `auth_group_permissions` VALUES (28, 3, 4);
INSERT INTO `auth_group_permissions` VALUES (29, 3, 5);
INSERT INTO `auth_group_permissions` VALUES (30, 3, 6);
INSERT INTO `auth_group_permissions` VALUES (31, 3, 7);
INSERT INTO `auth_group_permissions` VALUES (32, 3, 8);
INSERT INTO `auth_group_permissions` VALUES (33, 3, 9);
INSERT INTO `auth_group_permissions` VALUES (34, 3, 10);
INSERT INTO `auth_group_permissions` VALUES (35, 3, 11);
INSERT INTO `auth_group_permissions` VALUES (36, 3, 12);
INSERT INTO `auth_group_permissions` VALUES (37, 3, 13);
INSERT INTO `auth_group_permissions` VALUES (38, 3, 14);
INSERT INTO `auth_group_permissions` VALUES (39, 3, 15);
INSERT INTO `auth_group_permissions` VALUES (40, 3, 16);
INSERT INTO `auth_group_permissions` VALUES (41, 3, 17);
INSERT INTO `auth_group_permissions` VALUES (42, 3, 18);
INSERT INTO `auth_group_permissions` VALUES (43, 3, 19);
INSERT INTO `auth_group_permissions` VALUES (44, 3, 20);
INSERT INTO `auth_group_permissions` VALUES (45, 3, 21);
INSERT INTO `auth_group_permissions` VALUES (46, 3, 22);
INSERT INTO `auth_group_permissions` VALUES (47, 3, 23);
INSERT INTO `auth_group_permissions` VALUES (48, 3, 24);
INSERT INTO `auth_group_permissions` VALUES (49, 3, 25);
INSERT INTO `auth_group_permissions` VALUES (50, 3, 26);
INSERT INTO `auth_group_permissions` VALUES (51, 3, 27);
INSERT INTO `auth_group_permissions` VALUES (52, 3, 28);
INSERT INTO `auth_group_permissions` VALUES (53, 3, 29);
INSERT INTO `auth_group_permissions` VALUES (54, 3, 30);
INSERT INTO `auth_group_permissions` VALUES (55, 3, 31);
INSERT INTO `auth_group_permissions` VALUES (56, 3, 32);
INSERT INTO `auth_group_permissions` VALUES (57, 3, 33);
INSERT INTO `auth_group_permissions` VALUES (58, 3, 34);
INSERT INTO `auth_group_permissions` VALUES (59, 3, 35);
INSERT INTO `auth_group_permissions` VALUES (60, 3, 36);
INSERT INTO `auth_group_permissions` VALUES (61, 3, 37);
INSERT INTO `auth_group_permissions` VALUES (62, 3, 38);
INSERT INTO `auth_group_permissions` VALUES (63, 3, 39);
INSERT INTO `auth_group_permissions` VALUES (64, 3, 40);
INSERT INTO `auth_group_permissions` VALUES (65, 3, 41);
INSERT INTO `auth_group_permissions` VALUES (66, 3, 42);
INSERT INTO `auth_group_permissions` VALUES (67, 3, 43);
INSERT INTO `auth_group_permissions` VALUES (68, 3, 44);
INSERT INTO `auth_group_permissions` VALUES (69, 3, 45);
INSERT INTO `auth_group_permissions` VALUES (70, 3, 46);
INSERT INTO `auth_group_permissions` VALUES (71, 3, 47);
INSERT INTO `auth_group_permissions` VALUES (72, 3, 48);
INSERT INTO `auth_group_permissions` VALUES (73, 3, 49);
INSERT INTO `auth_group_permissions` VALUES (74, 3, 50);
INSERT INTO `auth_group_permissions` VALUES (75, 3, 51);
INSERT INTO `auth_group_permissions` VALUES (76, 3, 52);
INSERT INTO `auth_group_permissions` VALUES (77, 3, 53);
INSERT INTO `auth_group_permissions` VALUES (78, 3, 54);
INSERT INTO `auth_group_permissions` VALUES (79, 3, 55);
INSERT INTO `auth_group_permissions` VALUES (80, 3, 56);
INSERT INTO `auth_group_permissions` VALUES (81, 3, 57);
INSERT INTO `auth_group_permissions` VALUES (82, 3, 58);
INSERT INTO `auth_group_permissions` VALUES (83, 3, 59);
INSERT INTO `auth_group_permissions` VALUES (84, 3, 60);
INSERT INTO `auth_group_permissions` VALUES (85, 3, 61);
INSERT INTO `auth_group_permissions` VALUES (86, 3, 62);
INSERT INTO `auth_group_permissions` VALUES (87, 3, 63);
INSERT INTO `auth_group_permissions` VALUES (88, 3, 64);
INSERT INTO `auth_group_permissions` VALUES (89, 3, 65);
INSERT INTO `auth_group_permissions` VALUES (90, 3, 66);
INSERT INTO `auth_group_permissions` VALUES (91, 3, 67);
INSERT INTO `auth_group_permissions` VALUES (92, 3, 68);
INSERT INTO `auth_group_permissions` VALUES (93, 3, 69);
INSERT INTO `auth_group_permissions` VALUES (94, 3, 70);
INSERT INTO `auth_group_permissions` VALUES (95, 3, 71);
INSERT INTO `auth_group_permissions` VALUES (96, 3, 72);
INSERT INTO `auth_group_permissions` VALUES (97, 3, 73);
INSERT INTO `auth_group_permissions` VALUES (98, 3, 74);
INSERT INTO `auth_group_permissions` VALUES (99, 3, 75);
INSERT INTO `auth_group_permissions` VALUES (100, 3, 76);
INSERT INTO `auth_group_permissions` VALUES (101, 3, 77);
INSERT INTO `auth_group_permissions` VALUES (102, 3, 78);
INSERT INTO `auth_group_permissions` VALUES (103, 3, 79);
INSERT INTO `auth_group_permissions` VALUES (104, 3, 80);
INSERT INTO `auth_group_permissions` VALUES (105, 3, 81);
INSERT INTO `auth_group_permissions` VALUES (106, 3, 82);
INSERT INTO `auth_group_permissions` VALUES (107, 3, 83);
INSERT INTO `auth_group_permissions` VALUES (108, 3, 84);
INSERT INTO `auth_group_permissions` VALUES (109, 3, 85);
INSERT INTO `auth_group_permissions` VALUES (110, 3, 86);
INSERT INTO `auth_group_permissions` VALUES (111, 3, 87);
INSERT INTO `auth_group_permissions` VALUES (112, 3, 88);
INSERT INTO `auth_group_permissions` VALUES (113, 3, 89);
INSERT INTO `auth_group_permissions` VALUES (114, 3, 90);
INSERT INTO `auth_group_permissions` VALUES (115, 3, 91);
INSERT INTO `auth_group_permissions` VALUES (116, 3, 92);
INSERT INTO `auth_group_permissions` VALUES (117, 3, 93);
INSERT INTO `auth_group_permissions` VALUES (118, 3, 94);
INSERT INTO `auth_group_permissions` VALUES (119, 3, 95);
INSERT INTO `auth_group_permissions` VALUES (120, 3, 96);
INSERT INTO `auth_group_permissions` VALUES (121, 3, 97);
INSERT INTO `auth_group_permissions` VALUES (122, 3, 98);
INSERT INTO `auth_group_permissions` VALUES (123, 3, 99);
INSERT INTO `auth_group_permissions` VALUES (124, 3, 100);
INSERT INTO `auth_group_permissions` VALUES (125, 3, 101);
INSERT INTO `auth_group_permissions` VALUES (126, 3, 102);
INSERT INTO `auth_group_permissions` VALUES (127, 3, 103);
INSERT INTO `auth_group_permissions` VALUES (128, 3, 104);
INSERT INTO `auth_group_permissions` VALUES (129, 3, 105);
INSERT INTO `auth_group_permissions` VALUES (130, 3, 106);
INSERT INTO `auth_group_permissions` VALUES (131, 3, 107);
INSERT INTO `auth_group_permissions` VALUES (132, 3, 108);
INSERT INTO `auth_group_permissions` VALUES (133, 3, 109);
INSERT INTO `auth_group_permissions` VALUES (134, 3, 110);
INSERT INTO `auth_group_permissions` VALUES (135, 3, 111);
INSERT INTO `auth_group_permissions` VALUES (136, 3, 112);
COMMIT;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`) USING BTREE,
  CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 'add_logentry', 1);
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 'change_logentry', 1);
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 'delete_logentry', 1);
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 'view_logentry', 1);
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 'add_permission', 2);
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 'change_permission', 2);
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 'delete_permission', 2);
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 'view_permission', 2);
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 'add_group', 3);
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 'change_group', 3);
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 'delete_group', 3);
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 'view_group', 3);
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 'add_contenttype', 4);
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 'change_contenttype', 4);
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 'delete_contenttype', 4);
INSERT INTO `auth_permission` VALUES (16, 'Can view content type', 'view_contenttype', 4);
INSERT INTO `auth_permission` VALUES (17, 'Can add session', 'add_session', 5);
INSERT INTO `auth_permission` VALUES (18, 'Can change session', 'change_session', 5);
INSERT INTO `auth_permission` VALUES (19, 'Can delete session', 'delete_session', 5);
INSERT INTO `auth_permission` VALUES (20, 'Can view session', 'view_session', 5);
INSERT INTO `auth_permission` VALUES (21, 'Can add 用例信息', 'add_case', 6);
INSERT INTO `auth_permission` VALUES (22, 'Can change 用例信息', 'change_case', 6);
INSERT INTO `auth_permission` VALUES (23, 'Can delete 用例信息', 'delete_case', 6);
INSERT INTO `auth_permission` VALUES (24, 'Can view 用例信息', 'view_case', 6);
INSERT INTO `auth_permission` VALUES (25, 'Can add 项目信息', 'add_project', 7);
INSERT INTO `auth_permission` VALUES (26, 'Can change 项目信息', 'change_project', 7);
INSERT INTO `auth_permission` VALUES (27, 'Can delete 项目信息', 'delete_project', 7);
INSERT INTO `auth_permission` VALUES (28, 'Can view 项目信息', 'view_project', 7);
INSERT INTO `auth_permission` VALUES (29, 'Can add 测试报告', 'add_report', 8);
INSERT INTO `auth_permission` VALUES (30, 'Can change 测试报告', 'change_report', 8);
INSERT INTO `auth_permission` VALUES (31, 'Can delete 测试报告', 'delete_report', 8);
INSERT INTO `auth_permission` VALUES (32, 'Can view 测试报告', 'view_report', 8);
INSERT INTO `auth_permission` VALUES (33, 'Can add 全局变量', 'add_variables', 9);
INSERT INTO `auth_permission` VALUES (34, 'Can change 全局变量', 'change_variables', 9);
INSERT INTO `auth_permission` VALUES (35, 'Can delete 全局变量', 'delete_variables', 9);
INSERT INTO `auth_permission` VALUES (36, 'Can view 全局变量', 'view_variables', 9);
INSERT INTO `auth_permission` VALUES (37, 'Can add 测试报告详情', 'add_reportdetail', 10);
INSERT INTO `auth_permission` VALUES (38, 'Can change 测试报告详情', 'change_reportdetail', 10);
INSERT INTO `auth_permission` VALUES (39, 'Can delete 测试报告详情', 'delete_reportdetail', 10);
INSERT INTO `auth_permission` VALUES (40, 'Can view 测试报告详情', 'view_reportdetail', 10);
INSERT INTO `auth_permission` VALUES (41, 'Can add 树形结构关系', 'add_relation', 11);
INSERT INTO `auth_permission` VALUES (42, 'Can change 树形结构关系', 'change_relation', 11);
INSERT INTO `auth_permission` VALUES (43, 'Can delete 树形结构关系', 'delete_relation', 11);
INSERT INTO `auth_permission` VALUES (44, 'Can view 树形结构关系', 'view_relation', 11);
INSERT INTO `auth_permission` VALUES (45, 'Can add HOST配置', 'add_hostip', 12);
INSERT INTO `auth_permission` VALUES (46, 'Can change HOST配置', 'change_hostip', 12);
INSERT INTO `auth_permission` VALUES (47, 'Can delete HOST配置', 'delete_hostip', 12);
INSERT INTO `auth_permission` VALUES (48, 'Can view HOST配置', 'view_hostip', 12);
INSERT INTO `auth_permission` VALUES (49, 'Can add 驱动库', 'add_debugtalk', 13);
INSERT INTO `auth_permission` VALUES (50, 'Can change 驱动库', 'change_debugtalk', 13);
INSERT INTO `auth_permission` VALUES (51, 'Can delete 驱动库', 'delete_debugtalk', 13);
INSERT INTO `auth_permission` VALUES (52, 'Can view 驱动库', 'view_debugtalk', 13);
INSERT INTO `auth_permission` VALUES (53, 'Can add 环境信息', 'add_config', 14);
INSERT INTO `auth_permission` VALUES (54, 'Can change 环境信息', 'change_config', 14);
INSERT INTO `auth_permission` VALUES (55, 'Can delete 环境信息', 'delete_config', 14);
INSERT INTO `auth_permission` VALUES (56, 'Can view 环境信息', 'view_config', 14);
INSERT INTO `auth_permission` VALUES (57, 'Can add 用例信息 Step', 'add_casestep', 15);
INSERT INTO `auth_permission` VALUES (58, 'Can change 用例信息 Step', 'change_casestep', 15);
INSERT INTO `auth_permission` VALUES (59, 'Can delete 用例信息 Step', 'delete_casestep', 15);
INSERT INTO `auth_permission` VALUES (60, 'Can view 用例信息 Step', 'view_casestep', 15);
INSERT INTO `auth_permission` VALUES (61, 'Can add 接口信息', 'add_api', 16);
INSERT INTO `auth_permission` VALUES (62, 'Can change 接口信息', 'change_api', 16);
INSERT INTO `auth_permission` VALUES (63, 'Can delete 接口信息', 'delete_api', 16);
INSERT INTO `auth_permission` VALUES (64, 'Can view 接口信息', 'view_api', 16);
INSERT INTO `auth_permission` VALUES (65, 'Can add 用户信息', 'add_userinfo', 19);
INSERT INTO `auth_permission` VALUES (66, 'Can change 用户信息', 'change_userinfo', 19);
INSERT INTO `auth_permission` VALUES (67, 'Can delete 用户信息', 'delete_userinfo', 19);
INSERT INTO `auth_permission` VALUES (68, 'Can view 用户信息', 'view_userinfo', 19);
INSERT INTO `auth_permission` VALUES (69, 'Can add 用户登陆token', 'add_usertoken', 20);
INSERT INTO `auth_permission` VALUES (70, 'Can change 用户登陆token', 'change_usertoken', 20);
INSERT INTO `auth_permission` VALUES (71, 'Can delete 用户登陆token', 'delete_usertoken', 20);
INSERT INTO `auth_permission` VALUES (72, 'Can view 用户登陆token', 'view_usertoken', 20);
INSERT INTO `auth_permission` VALUES (73, 'Can add user', 'add_myuser', 17);
INSERT INTO `auth_permission` VALUES (74, 'Can change user', 'change_myuser', 17);
INSERT INTO `auth_permission` VALUES (75, 'Can delete user', 'delete_myuser', 17);
INSERT INTO `auth_permission` VALUES (76, 'Can view user', 'view_myuser', 17);
INSERT INTO `auth_permission` VALUES (77, 'Can add crontab', 'add_crontabschedule', 21);
INSERT INTO `auth_permission` VALUES (78, 'Can change crontab', 'change_crontabschedule', 21);
INSERT INTO `auth_permission` VALUES (79, 'Can delete crontab', 'delete_crontabschedule', 21);
INSERT INTO `auth_permission` VALUES (80, 'Can view crontab', 'view_crontabschedule', 21);
INSERT INTO `auth_permission` VALUES (81, 'Can add interval', 'add_intervalschedule', 22);
INSERT INTO `auth_permission` VALUES (82, 'Can change interval', 'change_intervalschedule', 22);
INSERT INTO `auth_permission` VALUES (83, 'Can delete interval', 'delete_intervalschedule', 22);
INSERT INTO `auth_permission` VALUES (84, 'Can view interval', 'view_intervalschedule', 22);
INSERT INTO `auth_permission` VALUES (85, 'Can add periodic task', 'add_periodictask', 18);
INSERT INTO `auth_permission` VALUES (86, 'Can change periodic task', 'change_periodictask', 18);
INSERT INTO `auth_permission` VALUES (87, 'Can delete periodic task', 'delete_periodictask', 18);
INSERT INTO `auth_permission` VALUES (88, 'Can view periodic task', 'view_periodictask', 18);
INSERT INTO `auth_permission` VALUES (89, 'Can add periodic tasks', 'add_periodictasks', 23);
INSERT INTO `auth_permission` VALUES (90, 'Can change periodic tasks', 'change_periodictasks', 23);
INSERT INTO `auth_permission` VALUES (91, 'Can delete periodic tasks', 'delete_periodictasks', 23);
INSERT INTO `auth_permission` VALUES (92, 'Can view periodic tasks', 'view_periodictasks', 23);
INSERT INTO `auth_permission` VALUES (93, 'Can add task state', 'add_taskmeta', 24);
INSERT INTO `auth_permission` VALUES (94, 'Can change task state', 'change_taskmeta', 24);
INSERT INTO `auth_permission` VALUES (95, 'Can delete task state', 'delete_taskmeta', 24);
INSERT INTO `auth_permission` VALUES (96, 'Can view task state', 'view_taskmeta', 24);
INSERT INTO `auth_permission` VALUES (97, 'Can add saved group result', 'add_tasksetmeta', 25);
INSERT INTO `auth_permission` VALUES (98, 'Can change saved group result', 'change_tasksetmeta', 25);
INSERT INTO `auth_permission` VALUES (99, 'Can delete saved group result', 'delete_tasksetmeta', 25);
INSERT INTO `auth_permission` VALUES (100, 'Can view saved group result', 'view_tasksetmeta', 25);
INSERT INTO `auth_permission` VALUES (101, 'Can add task', 'add_taskstate', 26);
INSERT INTO `auth_permission` VALUES (102, 'Can change task', 'change_taskstate', 26);
INSERT INTO `auth_permission` VALUES (103, 'Can delete task', 'delete_taskstate', 26);
INSERT INTO `auth_permission` VALUES (104, 'Can view task', 'view_taskstate', 26);
INSERT INTO `auth_permission` VALUES (105, 'Can add worker', 'add_workerstate', 27);
INSERT INTO `auth_permission` VALUES (106, 'Can change worker', 'change_workerstate', 27);
INSERT INTO `auth_permission` VALUES (107, 'Can delete worker', 'delete_workerstate', 27);
INSERT INTO `auth_permission` VALUES (108, 'Can view worker', 'view_workerstate', 27);
INSERT INTO `auth_permission` VALUES (109, 'Can add visit', 'add_visit', 28);
INSERT INTO `auth_permission` VALUES (110, 'Can change visit', 'change_visit', 28);
INSERT INTO `auth_permission` VALUES (111, 'Can delete visit', 'delete_visit', 28);
INSERT INTO `auth_permission` VALUES (112, 'Can view visit', 'view_visit', 28);
COMMIT;

-- ----------------------------
-- Table structure for case
-- ----------------------------
DROP TABLE IF EXISTS `case`;
CREATE TABLE `case` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `relation` int NOT NULL,
  `project_id` int NOT NULL,
  `length` int NOT NULL,
  `tag` int NOT NULL DEFAULT '2',
  `creator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updater` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `Case_project_id_16a36ccb_fk_Project_id` (`project_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=254 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of case
-- ----------------------------
BEGIN;
INSERT INTO `case` VALUES (122, '2019-11-19 11:30:41.778168', '2021-11-04 02:14:37.595537', '登录hook', 1, 7, 4, 3, 'test', 'test');
INSERT INTO `case` VALUES (135, '2019-12-25 11:48:33.037726', '2020-09-26 23:41:57.571012', '搜索用例', 1, 7, 4, 3, 'test', 'test');
INSERT INTO `case` VALUES (136, '2019-12-30 01:23:33.399871', '2020-08-13 21:15:05.892709', '登录失败-参数化', 1, 7, 1, 3, 'test', 'test');
INSERT INTO `case` VALUES (152, '2020-08-28 18:08:31.905648', '2020-08-28 18:08:31.905730', '阿呆测试', 1, 7, 4, 3, 'test', 'test');
INSERT INTO `case` VALUES (155, '2020-09-26 23:59:22.218377', '2021-11-01 13:45:54.531350', '登录用例', 24, 7, 3, 2, 'test', 'test');
INSERT INTO `case` VALUES (164, '2020-10-17 10:43:53.597015', '2021-07-28 15:24:05.102137', '登录失败，未注册--111', 24, 7, 1, 2, 'test', 'test');
INSERT INTO `case` VALUES (184, '2021-01-18 23:47:37.875592', '2021-01-18 23:48:06.717190', 'xx', 1, 7, 1, 2, 'test', 'test');
INSERT INTO `case` VALUES (185, '2021-01-18 23:53:31.070217', '2021-01-19 00:41:33.030119', '6666', 1, 7, 1, 2, 'test', 'test');
INSERT INTO `case` VALUES (188, '2021-01-19 00:53:51.435476', '2021-01-19 00:53:57.280237', '66662', 1, 7, 1, 2, 'test', 'test');
INSERT INTO `case` VALUES (201, '2021-06-06 21:16:14.470994', '2021-06-07 15:56:24.472693', 'wait1', 25, 7, 2, 2, 'test', 'test');
INSERT INTO `case` VALUES (202, '2021-06-06 21:16:19.711189', '2021-06-06 23:14:13.720618', 'wait2', 25, 7, 1, 2, 'test', 'test');
INSERT INTO `case` VALUES (203, '2021-06-06 21:16:27.188846', '2021-06-06 21:25:00.521573', 'wait3', 25, 7, 1, 2, 'test', 'test');
INSERT INTO `case` VALUES (204, '2021-06-25 10:43:04.300482', '2021-11-26 10:30:38.614309', '登录失败，未注册22', 24, 7, 2, 2, 'test', 'test');
INSERT INTO `case` VALUES (205, '2021-06-25 10:43:26.498775', '2021-06-25 10:43:26.498821', '登录失败，未注册225555', 1, 7, 2, 2, 'test', 'test');
INSERT INTO `case` VALUES (206, '2021-06-25 10:43:37.514972', '2021-08-03 14:31:37.847768', '动态修改userId', 25, 7, 2, 2, 'test', 'test');
INSERT INTO `case` VALUES (228, '2021-07-26 22:25:05.633099', '2021-07-26 22:29:22.915101', '提取步骤1的响应，动态设置到步骤2，包含模式', 26, 7, 2, 2, 'test', 'test');
INSERT INTO `case` VALUES (229, '2021-07-26 22:28:04.852843', '2021-11-03 11:00:49.983089', '提取步骤1的响应，动态设置到步骤2，排除模式', 26, 7, 4, 2, 'test', 'test');
INSERT INTO `case` VALUES (246, '2021-08-21 15:09:59.460889', '2022-01-10 14:42:55.073152', '登录失败，未注册225555-用了其他项目的api', 1, 7, 19, 2, 'test', 'test');
INSERT INTO `case` VALUES (247, '2021-11-26 13:51:57.216498', '2021-11-26 13:51:57.216517', '冒烟', 24, 7, 2, 3, 'test', NULL);
INSERT INTO `case` VALUES (248, '2021-11-26 22:32:41.697400', '2021-12-24 16:52:11.899193', 'q', 27, 7, 2, 2, 'test', 'test');
INSERT INTO `case` VALUES (249, '2022-01-06 01:03:48.787791', '2022-01-10 14:38:45.488062', '集成', 31, 7, 4, 2, 'test', NULL);
INSERT INTO `case` VALUES (250, '2022-01-11 16:29:41.927027', '2022-01-18 18:28:26.766914', '哈哈', 1, 7, 7, 2, 'test', 'test');
COMMIT;

-- ----------------------------
-- Table structure for case_step
-- ----------------------------
DROP TABLE IF EXISTS `case_step`;
CREATE TABLE `case_step` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `body` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `method` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `step` int NOT NULL,
  `case_id` int NOT NULL,
  `source_api_id` int NOT NULL,
  `creator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updater` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `CaseStep_case_id_7a6ec54f_fk_Case_id` (`case_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=560 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of case_step
-- ----------------------------
BEGIN;
INSERT INTO `case_step` VALUES (1, '2019-11-19 11:30:41.814675', '2022-01-11 13:52:03.998353', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 122, 0, NULL, 'test');
INSERT INTO `case_step` VALUES (2, '2019-11-19 11:30:41.846493', '2019-11-19 11:30:41.846533', '登录', '{\'name\': \'登录\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'$test_password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.code\', \'0001\']}]}', '/api/user/login/', 'POST', 1, 122, 2, NULL, 'test');
INSERT INTO `case_step` VALUES (27, '2019-12-25 11:38:51.130813', '2019-12-25 11:38:51.130882', '登录-用户未注册', '{\'name\': \'登录-用户未注册\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'test111\', \'password\': \'test123\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.code\', \'0104\']}, {\'equals\': [\'content.msg\', \'该用户未注册\']}]}', '/api/user/login/', 'POST', 2, 122, 27, NULL, 'test');
INSERT INTO `case_step` VALUES (28, '2019-12-25 11:38:51.157869', '2019-12-25 11:38:51.157921', '登录-密码错误', '{\'name\': \'登录-密码错误\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'test1233\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.code\', \'0103\']}, {\'equals\': [\'content.msg\', \'用户名或密码错误\']}]}', '/api/user/login/', 'POST', 3, 122, 28, NULL, 'test');
INSERT INTO `case_step` VALUES (29, '2019-12-25 11:48:33.055095', '2022-01-11 13:52:04.002871', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 135, 0, NULL, 'admin');
INSERT INTO `case_step` VALUES (33, '2019-12-25 13:56:28.457484', '2019-12-25 13:56:28.457526', '登录-成功', '{\'name\': \'登录-成功\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'$test_password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'token\': \'\'}}, \'extract\': [{\'token\': \'content.token\'}], \'validate\': [{\'equals\': [\'content.code\', \'0001\']}, {\'equals\': [\'content.user\', \'$test_user\']}]}', '/api/user/login/', 'POST', 1, 135, 33, NULL, 'admin');
INSERT INTO `case_step` VALUES (34, '2019-12-30 00:13:11.204972', '2019-12-30 00:13:11.205010', '登录-成功-teardown-修改返回结果', '{\'name\': \'登录-成功-teardown-修改返回结果\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'$test_password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'token\': \'抽取默认的返回token\', \'mytoken\': \'\'}}, \'extract\': [{\'token\': \'content.token\'}, {\'mytoken\': \'teardown.mytoken\'}], \'validate\': [{\'equals\': [\'content.code\', \'0001\']}, {\'equals\': [\'content.user\', \'$test_user\']}, {\'equals\': [\'$mytoken\', \'$token\']}], \'teardown_hooks\': [\'${teardown($response)}\']}', '/api/user/login/', 'POST', 4, 122, 34, NULL, 'test');
INSERT INTO `case_step` VALUES (36, '2019-12-30 01:23:33.418851', '2021-11-04 02:17:48.280382', '框架本身-参数化', '{\'name\': \'框架本身-参数化\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\'}, \'variables\': {}, \'parameters\': {\'username\': \'\', \'password\': \'\'}}, \'parameters\': [{\'username\': \'${param_username()}\'}, {\'password\': \'${param_password()}\'}]}', '', 'config', 0, 136, 0, NULL, NULL);
INSERT INTO `case_step` VALUES (37, '2019-12-30 01:23:33.433242', '2019-12-30 01:23:33.433266', '登录-失败-参数化', '{\'name\': \'登录-失败-参数化\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$username\', \'password\': \'$password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'msg\': \'\'}, \'extract\': {}}, \'validate\': [{\'startswith\': [\'content.code\', \'01\']}], \'variables\': [{\'msg\': \'${param_msg()}\'}]}', '/api/user/login/', 'POST', 1, 136, 0, NULL, NULL);
INSERT INTO `case_step` VALUES (38, '2020-05-09 12:30:40.418459', '2020-05-09 12:30:40.418459', ' 搜索用例-搜索条件为空,返回前11条', '{\'name\': \' 搜索用例-搜索条件为空,返回前11条\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \' \', \'project\': \'7\', \'search\': \'\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {\'case_name\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7]}, {\'greater_than_or_equals\': [\'content.count\', 4]}], \'variables\': [{\'case_name\': \'搜索用例\'}]}', '/api/fastrunner/test/', 'GET', 2, 135, 33, NULL, 'admin');
INSERT INTO `case_step` VALUES (39, '2020-05-09 12:30:40.436414', '2020-05-09 12:30:40.436414', '搜索用例-用例不存在', '{\'name\': \'搜索用例-用例不存在\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \' \', \'project\': \'7\', \'search\': \'$case_name\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'通过$token引用全局变量token\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {\'case_name\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results\', []]}, {\'equals\': [\'content.count\', 0]}], \'variables\': [{\'case_name\': \'注册\'}]}', '/api/fastrunner/test/', 'GET', 3, 135, 39, NULL, 'admin');
INSERT INTO `case_step` VALUES (40, '2020-05-09 12:30:40.459352', '2020-05-09 12:30:40.459352', '搜索用例-用例名存在', '{\'name\': \'搜索用例-用例名存在\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \' \', \'project\': \'7\', \'search\': \'$case_name\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {\'case_name\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7]}, {\'equals\': [\'content.results.0.name\', \'$case_name\']}], \'variables\': [{\'case_name\': \'登录hook\'}]}', '/api/fastrunner/test/', 'GET', 4, 135, 40, NULL, 'admin');
INSERT INTO `case_step` VALUES (135, '2020-08-28 18:08:31.910241', '2022-01-11 13:52:04.005946', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 152, 0, 'qa1', 'qa1');
INSERT INTO `case_step` VALUES (136, '2020-08-28 18:08:31.912365', '2020-08-28 18:08:31.912403', '登录-成功', '{\'name\': \'登录-成功\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'$test_password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'token\': \'\'}}, \'extract\': [{\'token\': \'content.token\'}], \'validate\': [{\'equals\': [\'content.code\', \'0001\']}, {\'equals\': [\'content.user\', \'$test_user\']}]}', '/api/user/login/', 'POST', 1, 152, 0, 'qa1', 'qa1');
INSERT INTO `case_step` VALUES (137, '2020-08-28 18:08:31.914140', '2020-08-28 18:08:31.914186', ' 搜索用例-搜索条件为空,返回前11条', '{\'name\': \' 搜索用例-搜索条件为空,返回前11条\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \' \', \'project\': \'7\', \'search\': \'\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {\'case_name\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7]}, {\'equals\': [\'content.results.0.name\', \'$case_name\']}], \'variables\': [{\'case_name\': \'搜索用例\'}]}', '/api/fastrunner/test/', 'GET', 2, 152, 38, 'qa1', 'qa1');
INSERT INTO `case_step` VALUES (138, '2020-08-28 18:08:31.915770', '2020-08-28 18:08:31.915806', '搜索用例-用例不存在', '{\'name\': \'搜索用例-用例不存在\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \' \', \'project\': \'7\', \'search\': \'$case_name\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'通过$token引用全局变量token\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {\'case_name\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results\', []]}, {\'equals\': [\'content.count\', 0]}], \'variables\': [{\'case_name\': \'注册\'}]}', '/api/fastrunner/test/', 'GET', 3, 152, 39, 'qa1', 'qa1');
INSERT INTO `case_step` VALUES (139, '2020-08-28 18:08:31.917257', '2020-08-28 18:08:31.917291', '搜索用例-用例名存在', '{\'name\': \'搜索用例-用例名存在\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \' \', \'project\': \'7\', \'search\': \'$case_name\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {\'case_name\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7]}, {\'equals\': [\'content.results.0.name\', \'$case_name\']}], \'variables\': [{\'case_name\': \'登录hook\'}]}', '/api/fastrunner/test/', 'GET', 4, 152, 40, 'qa1', 'qa1');
INSERT INTO `case_step` VALUES (150, '2020-09-26 23:59:22.230376', '2022-01-11 13:52:04.009784', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 155, 0, 'admin', 'admin');
INSERT INTO `case_step` VALUES (151, '2020-09-26 23:59:22.230464', '2020-09-26 23:59:22.230474', '登录-密码错误', '{\'name\': \'登录-密码错误\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'test1233\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.code\', \'0103\']}, {\'equals\': [\'content.msg\', \'用户名或密码错误\']}]}', '/api/user/login/', 'POST', 3, 155, 3734, 'admin', 'admin');
INSERT INTO `case_step` VALUES (152, '2020-09-26 23:59:22.230526', '2021-11-01 13:45:54.511400', '123', '{\'name\': \'登录-成功\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'$test_password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'test_user\': \'\'}, \'extract\': {\'token\': \'\'}}, \'extract\': [{\'token\': \'content.token\'}], \'validate\': [{\'equals\': [\'content.code\', \'0001\']}, {\'equals\': [\'content.user\', \'$test_user\']}, {\'length_equals\': [\'$token\', 201]}], \'variables\': [{\'test_user\': \'qa1\'}]}', '/api/user/login/', 'POST', 1, 155, 3729, 'admin', 'test');
INSERT INTO `case_step` VALUES (198, '2020-12-05 19:48:52.487095', '2020-12-05 19:48:52.487144', '获取API列表-调用驱动函数获取token', '{\'name\': \'获取API列表-调用驱动函数获取token\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/api/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'${get_token()}\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}, \'variables\': {\'test\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', \'7\']}], \'variables\': [{\'test\': \'\'}]}', '/api/fastrunner/api/', 'GET', 2, 155, 4091, 'admin', 'admin');
INSERT INTO `case_step` VALUES (213, '2021-01-18 23:47:40.720990', '2021-01-18 23:47:40.721045', '获取API列表-调用驱动函数获取token', '{\'name\': \'获取API列表-调用驱动函数获取token\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/api/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'${get_token()}\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\', \'tag\': \'\', \'rigEnv\': \'\'}, \'variables\': {\'test\': \'\'}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', \'7\']}], \'variables\': [{\'test\': \'\'}]}', '/api/fastrunner/api/', 'GET', 0, 184, 4091, 'admin', 'admin');
INSERT INTO `case_step` VALUES (216, '2021-01-19 00:24:31.739341', '2021-01-19 00:24:31.739386', '聚合数据-笑话大全', '{\'name\': \'聚合数据-笑话大全\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://v.juhe.cn/joke/content/list.php\', \'method\': \'GET\', \'verify\': False, \'params\': {\'sort\': \'desc\', \'page\': \'1\', \'pagesize\': \'10\', \'time\': \'1600096122\', \'key\': \'e2ec0aecb1a2fc282f59b6fe961478e2\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {\'sort\': \'desc:指定时间之前发布的，asc:指定时间之后发布的\', \'page\': \'当前页数,默认1,最大20\\t\', \'pagesize\': \'每次返回条数,默认1,最大20\\t\', \'time\': \'时间戳（10位），如：1418816972\\t\', \'key\': \'请求密钥\'}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.result.data.0\', {\'content\': \'某先生是地方上的要人。一天，他像往常一样在书房里例览当日报纸，突然对妻子大声喊道：喂，安娜，你看到今天早报上的流言蜚语了吗？真可笑！他们说，你收拾行装出走了。你听见了吗？安娜、你在哪儿？安娜？啊！\', \'hashId\': \'90B182FC7F74865B40B1E5807CFEBF41\', \'unixtime\': 1418745227, \'updatetime\': \'2014-12-16 23:53:47\'}]}, {\'equals\': [\'content.reason\', \'Success\']}]}', 'http://v.juhe.cn/joke/content/list.php', 'GET', 1, 185, 4090, 'admin', 'admin');
INSERT INTO `case_step` VALUES (217, '2021-01-19 00:41:33.005822', '2021-01-19 00:41:33.005874', '框架本身2', '{\'name\': \'框架本身2\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\'}}, \'desc\': {\'header\': {\'Content-Type\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'parameters\': {}}}', '', 'config', 0, 185, 0, 'admin', NULL);
INSERT INTO `case_step` VALUES (218, '2021-01-19 00:53:51.446683', '2021-01-19 00:53:51.446729', '聚合数据-笑话大全', '{\'name\': \'聚合数据-笑话大全\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://v.juhe.cn/joke/content/list.php\', \'method\': \'GET\', \'verify\': False, \'params\': {\'sort\': \'desc\', \'page\': \'1\', \'pagesize\': \'10\', \'time\': \'1600096122\', \'key\': \'e2ec0aecb1a2fc282f59b6fe961478e2\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {\'sort\': \'desc:指定时间之前发布的，asc:指定时间之后发布的\', \'page\': \'当前页数,默认1,最大20\\t\', \'pagesize\': \'每次返回条数,默认1,最大20\\t\', \'time\': \'时间戳（10位），如：1418816972\\t\', \'key\': \'请求密钥\'}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.result.data.0\', {\'content\': \'某先生是地方上的要人。一天，他像往常一样在书房里例览当日报纸，突然对妻子大声喊道：喂，安娜，你看到今天早报上的流言蜚语了吗？真可笑！他们说，你收拾行装出走了。你听见了吗？安娜、你在哪儿？安娜？啊！\', \'hashId\': \'90B182FC7F74865B40B1E5807CFEBF41\', \'unixtime\': 1418745227, \'updatetime\': \'2014-12-16 23:53:47\'}]}, {\'equals\': [\'content.reason\', \'Success\']}]}', 'http://v.juhe.cn/joke/content/list.php', 'GET', 1, 188, 4090, 'admin', 'admin');
INSERT INTO `case_step` VALUES (220, '2021-01-19 00:53:57.256332', '2021-01-19 00:53:57.256379', '框架本身21', '{\'name\': \'框架本身21\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\'}}, \'desc\': {\'header\': {\'Content-Type\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'parameters\': {}}}', '', 'config', 0, 188, 0, 'admin', NULL);
INSERT INTO `case_step` VALUES (271, '2021-06-06 21:16:14.484977', '2022-01-11 13:52:04.013294', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 201, 0, 'admin', 'admin');
INSERT INTO `case_step` VALUES (272, '2021-06-06 21:16:14.485211', '2021-06-06 21:25:16.013005', ' 搜索用例-', '{\'name\': \' 搜索用例-\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'11\', \'search\': \'\'}, \'json\': {}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {}, \'extract\': {}}}', '/api/fastrunner/test/', 'GET', 1, 201, 0, 'admin', 'admin');
INSERT INTO `case_step` VALUES (273, '2021-06-06 21:16:19.718379', '2022-01-11 13:52:04.017189', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 202, 0, 'admin', 'admin');
INSERT INTO `case_step` VALUES (274, '2021-06-06 21:16:19.722855', '2021-06-06 21:25:16.013005', ' 搜索用例-', '{\'name\': \' 搜索用例-\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'11\', \'search\': \'\'}, \'json\': {}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {}, \'extract\': {}}, \'teardown_hooks\': [\'${wait(5)}\']}', '/api/fastrunner/test/', 'GET', 1, 202, 0, 'admin', 'admin');
INSERT INTO `case_step` VALUES (275, '2021-06-06 21:16:27.197678', '2022-01-11 13:52:04.020932', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 203, 0, 'admin', 'admin');
INSERT INTO `case_step` VALUES (276, '2021-06-06 21:16:27.203576', '2021-06-06 21:16:27.203623', ' 搜索用例-', '{\'name\': \' 搜索用例-\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/test/\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'11\', \'search\': \'\'}, \'json\': {}}, \'desc\': {\'header\': {\'Authorization\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {\'caseNameOrUrl\': \'\', \'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {}, \'extract\': {}}, \'teardown_hooks\': [\'${wait(1)}\']}', '/api/fastrunner/test/', 'GET', 1, 203, 0, 'admin', 'admin');
INSERT INTO `case_step` VALUES (277, '2021-06-06 22:52:31.808393', '2021-06-06 22:52:31.808417', '登录-成功1', '{\'name\': \'登录-成功1\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'$test_password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'test_user\': \'\', \'intV\': \'\'}, \'extract\': {\'token\': \'\'}}, \'extract\': [{\'token\': \'content.token\'}], \'validate\': [{\'equals\': [\'content.code\', \'0001\']}, {\'equals\': [\'content.user\', \'$test_user\']}, {\'length_equals\': [\'$token\', 201]}, {\'equals\': [\'content.code\', \'$intV\']}], \'variables\': [{\'test_user\': \'qa1\'}, {\'intV\': 1}]}', '/api/user/login/', 'POST', 2, 201, 0, 'admin', 'admin');
INSERT INTO `case_step` VALUES (278, '2021-06-25 10:43:04.315154', '2022-01-11 13:52:04.024014', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 204, 0, '李华才', '李华才');
INSERT INTO `case_step` VALUES (280, '2021-06-25 10:43:04.327699', '2021-06-25 10:43:04.327747', '登录-用户未注册', '{\'name\': \'登录-用户未注册\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'test111\', \'password\': \'test123\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'username\': \'\', \'password\': \'\'}, \'extract\': {\'code\': \'\', \'msg\': \'\'}}, \'enabled\': {\'params\': {}, \'variables\': {\'username\': False, \'password\': False}, \'extract\': {\'code\': True, \'msg\': True}, \'validate\': [True, True]}, \'extract\': [{\'code\': \'content.code\'}, {\'msg\': \'content.msg\'}], \'validate\': [{\'equals\': [\'content.code\', \'0104\'], \'enabled\': True}, {\'equals\': [\'content.msg\', \'该用户未注册\'], \'enabled\': True}], \'variables\': [{\'username\': \'test111\'}, {\'password\': \'test123\'}]}', '/api/user/login/', 'POST', 1, 204, 3735, '李华才', '李华才');
INSERT INTO `case_step` VALUES (284, '2021-06-25 10:43:04.352028', '2021-06-25 10:43:04.352067', '登录-成功1', '{\'name\': \'登录-成功1\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'$test_password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'test_user\': \'\', \'intV\': \'\'}, \'extract\': {\'token\': \'\'}}, \'extract\': [{\'token\': \'content.token\'}], \'validate\': [{\'equals\': [\'content.code\', \'0001\']}, {\'equals\': [\'content.user\', \'$test_user\']}, {\'length_equals\': [\'$token\', 201]}, {\'equals\': [\'content.code\', \'$intV\']}], \'variables\': [{\'test_user\': \'qa1\'}, {\'intV\': 1}]}', '/api/user/login/', 'POST', 2, 204, 4087, '李华才', '李华才');
INSERT INTO `case_step` VALUES (287, '2021-06-25 10:43:26.507689', '2022-01-11 13:52:04.027608', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 205, 0, '李华才', '李华才');
INSERT INTO `case_step` VALUES (288, '2021-06-25 10:43:26.512571', '2021-06-25 10:43:26.512642', '登录-用户未注册', '{\'name\': \'登录-用户未注册\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'test111\', \'password\': \'test123\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.code\', \'0104\']}, {\'equals\': [\'content.msg\', \'该用户未注册\']}]}', '/api/user/login/', 'POST', 1, 205, 3735, '李华才', '李华才');
INSERT INTO `case_step` VALUES (289, '2021-06-25 10:43:26.516796', '2021-06-25 10:43:26.516841', '登录-成功1', '{\'name\': \'登录-成功1\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/user/login/\', \'method\': \'POST\', \'verify\': False, \'json\': {\'username\': \'$test_user\', \'password\': \'$test_password\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {\'test_user\': \'\', \'intV\': \'\'}, \'extract\': {\'token\': \'\'}}, \'extract\': [{\'token\': \'content.token\'}], \'validate\': [{\'equals\': [\'content.code\', \'0001\']}, {\'equals\': [\'content.user\', \'$test_user\']}, {\'length_equals\': [\'$token\', 201]}, {\'equals\': [\'content.code\', \'$intV\']}], \'variables\': [{\'test_user\': \'qa1\'}, {\'intV\': 1}]}', '/api/user/login/', 'POST', 2, 205, 4087, '李华才', '李华才');
INSERT INTO `case_step` VALUES (290, '2021-06-25 10:43:37.522849', '2022-01-11 13:52:04.031588', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 206, 0, '李华才', '李华才');
INSERT INTO `case_step` VALUES (376, '2021-07-26 22:25:05.646687', '2022-01-11 13:52:04.034946', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 228, 0, '李华才', '李华才');
INSERT INTO `case_step` VALUES (377, '2021-07-26 22:25:05.646912', '2021-07-26 22:25:05.646941', '获取dict类型返回值', '{\'name\': \'获取dict类型返回值\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/dict\', \'method\': \'GET\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}]}', '$mock_url/dict', 'GET', 1, 228, 10946, '李华才', '李华才');
INSERT INTO `case_step` VALUES (378, '2021-07-26 22:25:05.647111', '2021-07-26 22:25:05.647139', '把第一步的返回值，动态设置到当前步骤', '{\'name\': \'把第一步的返回值，动态设置到当前步骤\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/dict\', \'method\': \'GET\', \'verify\': False, \'json\': {\'a\': \'\', \'b\': \'\', \'c\': \'\', \'d\': \'\', \'e\': {\'in_a\': \'val_in_a\', \'in_b\': \'val_in_b\', \'in_c\': \'c\'}}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}], \'setup_hooks\': [\'${set_json($request,$data,a-b-c)}\', \'${set_json($request,$data,e)}\']}', '$mock_url/dict', 'GET', 2, 228, 10946, '李华才', '李华才');
INSERT INTO `case_step` VALUES (379, '2021-07-26 22:28:04.860466', '2022-01-11 13:52:04.041177', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 229, 0, '李华才', 'test');
INSERT INTO `case_step` VALUES (380, '2021-07-26 22:28:04.864184', '2021-07-26 22:28:04.864232', '获取dict类型返回值', '{\'name\': \'获取dict类型返回值\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/dict\', \'method\': \'GET\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}]}', '$mock_url/dict', 'GET', 1, 229, 10946, '李华才', 'test');
INSERT INTO `case_step` VALUES (381, '2021-07-26 22:28:04.868314', '2021-07-26 22:28:04.868364', '把第一步的返回值，动态设置到当前步骤', '{\'name\': \'把第一步的返回值，动态设置到当前步骤\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/dict\', \'method\': \'GET\', \'verify\': False, \'json\': {\'a\': \'\', \'b\': \'\', \'c\': \'\', \'d\': \'\', \'e\': {\'in_a\': \'val_in_a\', \'in_b\': \'val_in_b\', \'in_c\': \'c\'}}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}], \'setup_hooks\': [\'${set_json_e($request,$data,a-b-c)}\']}', '$mock_url/dict', 'GET', 2, 229, 10946, '李华才', 'test');
INSERT INTO `case_step` VALUES (386, '2021-07-28 15:24:05.074294', '2022-01-11 13:52:04.044771', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 164, 0, '李华才', NULL);
INSERT INTO `case_step` VALUES (387, '2021-07-28 15:24:05.079037', '2021-07-28 15:24:05.079087', 'mock-dict', '{\'name\': \'mock-dict\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/dict\', \'method\': \'GET\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}]}', '$mock_url/dict', 'GET', 1, 164, 0, '李华才', NULL);
INSERT INTO `case_step` VALUES (461, '2021-08-03 11:45:06.381349', '2021-08-03 11:45:06.381396', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}, \'teardown_hooks\': [\'${make_g()}\']}', '$cdh2/post', 'POST', 1, 206, 461, '李华才', '李华才');
INSERT INTO `case_step` VALUES (462, '2021-08-03 11:45:06.389034', '2021-08-03 11:45:06.389078', 'userId已经改变', '{\'name\': \'userId已经改变\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 2, 206, 462, '李华才', '李华才');
INSERT INTO `case_step` VALUES (485, '2021-08-21 15:09:59.470314', '2022-01-11 13:52:04.048702', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 246, 0, '李华才', 'test');
INSERT INTO `case_step` VALUES (490, '2021-11-02 22:47:17.651593', '2021-11-02 22:47:17.651620', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 1, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (494, '2021-11-02 23:12:40.741957', '2021-11-02 23:12:40.741989', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 19, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (495, '2021-11-02 23:12:42.862503', '2021-11-02 23:12:42.862535', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 18, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (496, '2021-11-02 23:12:44.917069', '2021-11-02 23:12:44.917102', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 17, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (497, '2021-11-02 23:15:29.145825', '2021-11-02 23:15:29.145856', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 16, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (498, '2021-11-02 23:15:30.149127', '2021-11-02 23:15:30.149159', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 4, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (505, '2021-11-02 23:18:31.726367', '2021-11-02 23:18:31.726394', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 2, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (506, '2021-11-02 23:18:31.734987', '2021-11-02 23:18:31.735011', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 3, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (517, '2021-11-02 23:18:50.856749', '2021-11-02 23:18:50.856780', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 11, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (518, '2021-11-02 23:18:50.866046', '2021-11-02 23:18:50.866078', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 14, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (519, '2021-11-02 23:18:50.873744', '2021-11-02 23:18:50.873772', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 15, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (520, '2021-11-02 23:18:51.225554', '2021-11-02 23:18:51.225584', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 12, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (521, '2021-11-02 23:18:51.255814', '2021-11-02 23:18:51.255849', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 13, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (525, '2021-11-02 23:18:53.232276', '2021-11-02 23:18:53.232304', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 5, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (526, '2021-11-02 23:18:53.240427', '2021-11-02 23:18:53.240454', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 8, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (527, '2021-11-02 23:18:53.252927', '2021-11-02 23:18:53.252956', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 10, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (528, '2021-11-02 23:18:53.816119', '2021-11-02 23:18:53.816168', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 6, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (529, '2021-11-02 23:18:54.313601', '2021-11-02 23:18:54.313638', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 7, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (530, '2021-11-02 23:18:54.322857', '2021-11-02 23:18:54.322897', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 9, 246, 10949, 'test', 'test');
INSERT INTO `case_step` VALUES (531, '2021-11-03 11:00:49.970800', '2021-11-03 11:00:49.970830', '把第一步的返回值，动态设置到当前步骤', '{\'name\': \'把第一步的返回值，动态设置到当前步骤\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/dict\', \'method\': \'GET\', \'verify\': False, \'json\': {\'a\': \'\', \'b\': \'\', \'c\': \'\', \'d\': \'\', \'e\': {\'in_a\': \'val_in_a\', \'in_b\': \'val_in_b\', \'in_c\': \'c\'}}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}], \'setup_hooks\': [\'${set_json_e($request,$data,a-b-c)}\']}', '$mock_url/dict', 'GET', 3, 229, 10946, 'test', NULL);
INSERT INTO `case_step` VALUES (532, '2021-11-03 11:00:49.978798', '2021-11-03 11:00:49.978832', 'list断言', '{\'name\': \'list断言\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$cdh2/post\', \'method\': \'POST\', \'verify\': False, \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'k0\': \'val-j0\', \'k1\': \'val-1\'}, {\'k0\': \'val-m0\', \'k1\': \'val-1\'}]}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '$cdh2/post', 'POST', 4, 229, 10949, 'test', NULL);
INSERT INTO `case_step` VALUES (533, '2021-11-26 13:51:57.220495', '2022-01-11 13:52:04.054804', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', 'http://localhost:8000', 'config', 0, 247, 0, 'test', NULL);
INSERT INTO `case_step` VALUES (534, '2021-11-26 13:51:57.220569', '2021-11-26 13:51:57.220578', 'mock-list', '{\'name\': \'mock-list\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/list\', \'method\': \'GET\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}]}', '$mock_url/list', 'GET', 1, 247, 10944, 'test', NULL);
INSERT INTO `case_step` VALUES (535, '2021-11-26 13:51:57.220624', '2021-11-26 13:51:57.220632', 'mock-list', '{\'name\': \'mock-list\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/list\', \'method\': \'GET\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}]}', '$mock_url/list', 'GET', 2, 247, 10944, 'test', NULL);
INSERT INTO `case_step` VALUES (536, '2021-11-26 22:32:41.701325', '2022-01-11 13:52:04.060289', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', 'http://localhost:8000', 'config', 0, 248, 0, 'test', NULL);
INSERT INTO `case_step` VALUES (537, '2021-11-26 22:32:41.701399', '2021-12-24 16:52:11.893477', '获取全局变量-异常', '{\'name\': \'获取全局变量-异常\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/variables\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \' \'}, \'json\': {}}, \'desc\': {\'header\': {\'Authorization\': \'token是全局变量\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7, \'\']}]}', '/api/fastrunner/variables', 'GET', 1, 248, 10905, 'test', 'test');
INSERT INTO `case_step` VALUES (538, '2021-11-26 22:32:41.701461', '2021-12-24 16:52:11.893477', '获取全局变量-异常', '{\'name\': \'获取全局变量-异常\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/fastrunner/variables\', \'method\': \'GET\', \'verify\': False, \'headers\': {\'Authorization\': \'$token\'}, \'params\': {\'node\': \' \', \'project\': \'7\', \'search\': \' \'}, \'json\': {}}, \'desc\': {\'header\': {\'Authorization\': \'token是全局变量\'}, \'data\': {}, \'files\': {}, \'params\': {\'node\': \'\', \'project\': \'\', \'search\': \'\'}, \'variables\': {}, \'extract\': {}}, \'validate\': [{\'equals\': [\'content.results.0.project\', 7, \'\']}]}', '/api/fastrunner/variables', 'GET', 2, 248, 10905, 'test', 'test');
INSERT INTO `case_step` VALUES (539, '2022-01-06 01:03:48.793811', '2022-01-06 01:03:48.793828', '全局配置', '{\'name\': \'全局配置\', \'request\': {\'base_url\': \'https://www.baidu.com\', \'headers\': {\'Content-Type\': \'x-www-form-urlencode\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'头部信息content-type\'}, \'variables\': {}, \'parameters\': {}}}', 'https://www.baidu.com', 'config', 0, 249, 0, 'test', NULL);
INSERT INTO `case_step` VALUES (540, '2022-01-06 01:03:48.793904', '2022-01-06 01:03:48.793918', '全国房产信息', '{\'name\': \'全国房产信息\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://route.showapi.com/1610-1\', \'method\': \'GET\', \'verify\': False, \'params\': {\'cityName\': \'广州\', \'hourseName\': \'星河湾\', \'page\': \'1\', \'showapi_appid\': \'366062\', \'showapi_sign\': \'3492b4075b0f4c5db16c21f9164e8ee0\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {\'cityName\': \'\', \'hourseName\': \'\', \'page\': \'\', \'showapi_appid\': \'\', \'showapi_sign\': \'\'}, \'variables\': {}, \'extract\': {}}}', 'http://route.showapi.com/1610-1', 'GET', 1, 249, 4067, 'test', NULL);
INSERT INTO `case_step` VALUES (541, '2022-01-06 01:03:48.793971', '2022-01-06 01:03:48.793979', '全国房产信息', '{\'name\': \'全国房产信息\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://route.showapi.com/1610-1\', \'method\': \'GET\', \'verify\': False, \'params\': {\'cityName\': \'广州\', \'hourseName\': \'星河湾\', \'page\': \'1\', \'showapi_appid\': \'366062\', \'showapi_sign\': \'3492b4075b0f4c5db16c21f9164e8ee0\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {\'cityName\': \'\', \'hourseName\': \'\', \'page\': \'\', \'showapi_appid\': \'\', \'showapi_sign\': \'\'}, \'variables\': {}, \'extract\': {}}}', 'http://route.showapi.com/1610-1', 'GET', 2, 249, 4067, 'test', NULL);
INSERT INTO `case_step` VALUES (542, '2022-01-06 01:03:48.794027', '2022-01-06 01:03:48.794035', '全国房产信息', '{\'name\': \'全国房产信息\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://route.showapi.com/1610-1\', \'method\': \'GET\', \'verify\': False, \'params\': {\'cityName\': \'广州\', \'hourseName\': \'星河湾\', \'page\': \'1\', \'showapi_appid\': \'366062\', \'showapi_sign\': \'3492b4075b0f4c5db16c21f9164e8ee0\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {\'cityName\': \'\', \'hourseName\': \'\', \'page\': \'\', \'showapi_appid\': \'\', \'showapi_sign\': \'\'}, \'variables\': {}, \'extract\': {}}}', 'http://route.showapi.com/1610-1', 'GET', 3, 249, 4067, 'test', NULL);
INSERT INTO `case_step` VALUES (543, '2022-01-06 01:03:48.794081', '2022-01-06 01:03:48.794089', '全国房产信息', '{\'name\': \'全国房产信息\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://route.showapi.com/1610-1\', \'method\': \'GET\', \'verify\': False, \'params\': {\'cityName\': \'广州\', \'hourseName\': \'星河湾\', \'page\': \'1\', \'showapi_appid\': \'366062\', \'showapi_sign\': \'3492b4075b0f4c5db16c21f9164e8ee0\'}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {\'cityName\': \'\', \'hourseName\': \'\', \'page\': \'\', \'showapi_appid\': \'\', \'showapi_sign\': \'\'}, \'variables\': {}, \'extract\': {}}}', 'http://route.showapi.com/1610-1', 'GET', 4, 249, 4067, 'test', NULL);
INSERT INTO `case_step` VALUES (544, '2022-01-11 16:29:41.931187', '2022-01-11 16:29:41.931205', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', '', 'config', 0, 250, 0, 'test', 'test');
INSERT INTO `case_step` VALUES (545, '2022-01-11 16:29:41.931264', '2022-01-11 16:29:41.931273', 'test', '{\'name\': \'test\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://www.baidu.com\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', 'http://www.baidu.com', 'POST', 2, 250, 10951, 'test', 'test');
INSERT INTO `case_step` VALUES (546, '2022-01-11 16:29:41.931317', '2022-01-11 16:29:41.931325', 'xml', '{\'name\': \'xml\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'https://6ab4c55f-6803-446a-8aff-2994ab3169ae.mock.pstmn.io/api/fastrunner/ci/\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', 'https://6ab4c55f-6803-446a-8aff-2994ab3169ae.mock.pstmn.io/api/fastrunner/ci/', 'POST', 1, 250, 10904, 'test', 'test');
INSERT INTO `case_step` VALUES (547, '2022-01-11 18:59:01.667226', '2022-01-11 18:59:01.667254', 'sss', '{\'name\': \'sss\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://www.baidu.com\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', 'http://www.baidu.com', 'POST', 3, 250, 10954, 'test', 'test');
INSERT INTO `case_step` VALUES (548, '2022-01-11 18:59:01.671630', '2022-01-11 18:59:01.671652', 'sss', '{\'name\': \'sss\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/login\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/login', 'POST', 4, 250, 10952, 'test', 'test');
INSERT INTO `case_step` VALUES (549, '2022-01-11 18:59:01.675930', '2022-01-11 18:59:01.675948', 'mock-list', '{\'name\': \'mock-list\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'$mock_url/list\', \'method\': \'GET\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {\'data\': \'\'}}, \'extract\': [{\'data\': \'content\'}]}', '$mock_url/list', 'GET', 5, 250, 10945, 'test', 'test');
INSERT INTO `case_step` VALUES (550, '2022-01-11 18:59:01.683058', '2022-01-11 18:59:01.683077', '0000', '{\'name\': \'0000\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'/api/\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', '/api/', 'POST', 6, 250, 10956, 'test', 'test');
INSERT INTO `case_step` VALUES (551, '2022-01-11 18:59:01.687527', '2022-01-11 18:59:01.687544', '测试百度', '{\'name\': \'测试百度\', \'rig_id\': None, \'times\': 1, \'request\': {\'url\': \'http://www.baidu.com\', \'method\': \'POST\', \'verify\': False, \'json\': {}}, \'desc\': {\'header\': {}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'extract\': {}}}', 'http://www.baidu.com', 'POST', 7, 250, 10953, 'test', 'test');
COMMIT;

-- ----------------------------
-- Table structure for celery_taskmeta
-- ----------------------------
DROP TABLE IF EXISTS `celery_taskmeta`;
CREATE TABLE `celery_taskmeta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `result` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `hidden` tinyint(1) NOT NULL,
  `meta` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `task_id` (`task_id`) USING BTREE,
  KEY `celery_taskmeta_hidden_23fd02dc` (`hidden`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of celery_taskmeta
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for celery_tasksetmeta
-- ----------------------------
DROP TABLE IF EXISTS `celery_tasksetmeta`;
CREATE TABLE `celery_tasksetmeta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `taskset_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `result` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `date_done` datetime(6) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `taskset_id` (`taskset_id`) USING BTREE,
  KEY `celery_tasksetmeta_hidden_593cfc24` (`hidden`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of celery_tasksetmeta
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for config
-- ----------------------------
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `body` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `base_url` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `project_id` int NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `creator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updater` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `Config_project_id_55b26806_fk_Project_id` (`project_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of config
-- ----------------------------
BEGIN;
INSERT INTO `config` VALUES (29, '2019-11-19 10:03:34.969812', '2022-01-11 13:52:04.070027', '框架本身', '{\'name\': \'框架本身\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'$userId\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\', \'userId\': \'\'}, \'variables\': {\'mock_url\': \'\', \'cdh2\': \'\', \'userId\': \'\', \'x\': \'\'}, \'parameters\': {}}, \'variables\': [{\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\'}, {\'cdh2\': \'http://localhost:9000\'}, {\'userId\': \'var\'}, {\'x\': \'abc\'}]}', 'http://localhost:8000', 7, 1, NULL, 'test');
INSERT INTO `config` VALUES (30, '2019-12-30 00:13:47.167552', '2021-11-04 02:17:48.289700', '框架本身-参数化', '{\'name\': \'框架本身-参数化\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'\'}, \'variables\': {}, \'parameters\': {\'username\': \'\', \'password\': \'\'}}, \'parameters\': [{\'username\': \'${param_username()}\'}, {\'password\': \'${param_password()}\'}]}', 'http://localhost:8000', 7, 0, NULL, 'test');
INSERT INTO `config` VALUES (51, '2021-01-19 00:55:48.669512', '2021-01-19 00:55:48.669590', '框架本身21', '{\'name\': \'框架本身21\', \'request\': {\'base_url\': \'http://localhost:8000\', \'headers\': {\'Content-Type\': \'application/json;charset=utf-8\'}}, \'desc\': {\'header\': {\'Content-Type\': \'\'}, \'data\': {}, \'files\': {}, \'params\': {}, \'variables\': {}, \'parameters\': {}}}', 'http://localhost:8000', 7, 0, 'admin', 'admin');
INSERT INTO `config` VALUES (52, '2021-11-25 14:35:36.368652', '2021-11-25 14:35:36.368680', 'aaa', '{\'name\': \'aaa\', \'request\': {\'base_url\': \'\', \'json\': {}}, \'desc\': {\'header\': {}, \'variables\': {}, \'parameters\': {}}}', '', 7, 0, 'test', NULL);
INSERT INTO `config` VALUES (54, '2021-12-07 13:21:13.849899', '2021-12-07 13:21:30.345661', '全局配置', '{\'name\': \'全局配置\', \'request\': {\'base_url\': \'https://www.baidu.com\', \'headers\': {\'Content-Type\': \'x-www-form-urlencode\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'头部信息content-type\'}, \'variables\': {}, \'parameters\': {}}}', 'https://www.baidu.com', 7, 0, 'test', 'test');
INSERT INTO `config` VALUES (55, '2021-12-07 16:38:56.176416', '2021-12-07 16:40:16.348985', '发生大', '{\'name\': \'发生大\', \'request\': {\'base_url\': \'\', \'json\': {}}, \'desc\': {\'header\': {}, \'variables\': {}, \'parameters\': {}}}', '', 7, 0, 'test', 'test');
INSERT INTO `config` VALUES (56, '2021-12-07 18:04:45.365815', '2021-12-09 01:00:59.239126', '嘎达', '{\'name\': \'嘎达\', \'request\': {\'base_url\': \'\', \'headers\': {\'h\': \'1\'}, \'json\': {}}, \'desc\': {\'header\': {\'h\': \'1\'}, \'variables\': {\'a\': \'\'}, \'parameters\': {}}, \'variables\': [{\'a\': \'1\'}]}', '', 7, 0, 'test', 'test');
INSERT INTO `config` VALUES (57, '2022-01-13 17:56:49.688856', '2022-01-13 17:56:49.688877', '配置333', '{\'name\': \'配置333\', \'request\': {\'base_url\': \'http://127.0.0.1:8000\', \'headers\': {\'Accept\': \'ss\', \'Accept-Charset\': \'ddd\'}, \'json\': {}}, \'desc\': {\'header\': {\'Accept\': \'描述1\', \'Accept-Charset\': \'描述1\'}, \'variables\': {}, \'parameters\': {}}}', 'http://127.0.0.1:8000', 7, 0, 'test', NULL);
INSERT INTO `config` VALUES (58, '2022-01-13 18:06:19.510151', '2022-01-14 13:36:22.842694', 'kkk', '{\'name\': \'kkk\', \'request\': {\'base_url\': \'http://127.0.0.1:8000\', \'headers\': {\'Content-Type\': \'json\'}, \'json\': {}}, \'desc\': {\'header\': {\'Content-Type\': \'描述信息1\'}, \'variables\': {\'timestamp\': \'\'}, \'parameters\': {}}, \'variables\': [{\'timestamp\': \'1222222\'}], \'setup_hooks\': [\'${took}\'], \'teardown_hooks\': [\'${hook4}\']}', 'http://127.0.0.1:8000', 7, 0, 'test', 'test');
INSERT INTO `config` VALUES (59, '2022-01-20 13:59:36.392038', '2022-01-20 14:02:04.779704', '测试环境', '{\'name\': \'测试环境\', \'request\': {\'base_url\': \'http://127.0.0.1:8000\', \'json\': {}}, \'desc\': {\'header\': {}, \'variables\': {\'ACCESS_TOKEN\': \'token值\'}, \'parameters\': {}}, \'variables\': [{\'ACCESS_TOKEN\': \'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjczNTk1OTgzLCJqdGkiOiJiOWRlMTQ4OTc5NjU0MjcxODFiMWM1Njk2ZDNkY2Y3ZiIsInVzZXJfaWQiOjF9.Tw26V93G4dOKqtYlBHXweB6PSqABdFFiqLi1u9geD50\'}]}', 'http://127.0.0.1:8000', 8, 0, 'test', 'test');
COMMIT;

-- ----------------------------
-- Table structure for debugtalk
-- ----------------------------
DROP TABLE IF EXISTS `debugtalk`;
CREATE TABLE `debugtalk` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `project_id` int NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `creator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `update_time` datetime(6) NOT NULL,
  `updater` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `project_id` (`project_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of debugtalk
-- ----------------------------
BEGIN;
INSERT INTO `debugtalk` VALUES (7, '# write you code\nimport time\nimport json\nimport datetime\nimport random\nimport uuid\nimport requests\n# from faker import Faker\nfrom httprunner.builtin.time_helper import get_ts\nfrom httprunner.runner import Hrun\n\nimport httprunner.logger\nimport threading\nimport os\nimport sys\ntest_password = \"gg9tKGBjK8GEgg9tKGBjK8GE\"\n# userId = \'var\'\nprint(1234455)\n\ndef get_msg_id():\n    return str(uuid.uuid1())\n\ndef make_g():\n    global g\n    g = \'global\'\n    g = get_ts()\n    # Hrun.set_step_var(\'b\', \'abcde\')\n    Hrun.set_config_header(\'userId\', get_ts())\n    return \'xx\'\n\nprint(make_g())\n\n# 装饰器导致返回None\n# @func_run_time()\ndef get_token():\n    data = {\"username\": \"qa1\", \"password\": test_password}\n    url = \'http://localhost:8000/api/user/login/\'\n    my_headers = {\"Content-Type\": \"application/json;charset=UTF-8\"}\n    res = requests.post(url=url,headers=my_headers,data=json.dumps(data)).json()\n    return res.get(\'token\')\n\ndef get_none():\n    return None\n\n\ndef set_up(request):\n    print(\"******\")\n    print(request)\n    request_data = request[\'json\']\n    request_data[\"password\"] = test_password\n    \ndef teardown(resp):\n    print(\"*\" * 50)\n    # print(dir(resp))\n    print(type(resp.resp_obj))\n    # resp = resp.resp_obj.json()\n    # print(resp)2212\n    resp.teardown = {\"mytoken\":resp.resp_obj.json()[\'token\']}\n    print(resp.json)\n\n\ndef param_username():\n    return [{\"username\": \"qa2\"},{\"username\": \"qa3\"}]\n    \ndef param_password():\n    return [{\"password\": \"password233\"},{\"password\": \"abcdeed\"}]\n\n\nmsg = [{\"msg\": \"login success\"},{\"msg\": \"用户名或密码错误\"},{\"msg\": \"用户名或密码错误\"},{\"msg\": \"用户名或密码错误\"}]\ndef param_msg():\n    return msg[::-1].pop()[\'msg\']\n    ', 7, '2020-08-16 23:20:17.165262', NULL, '2020-08-16 23:20:17.258195', 'test');
INSERT INTO `debugtalk` VALUES (8, '# write you code\r\n\r\n\r\n\r\n@pytest.fixture\r\ndef test_demo():\r\n    print(f\"撒啊啊啊啊啊啊\")', 8, '2022-01-13 16:14:25.887657', NULL, '2022-01-13 16:14:25.887676', 'test');
COMMIT;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`) USING BTREE,
  KEY `django_admin_log_user_id_c564eba6_fk_fastuser_myuser_id` (`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_ibfk_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `fastuser_myuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (21, 'djcelery', 'crontabschedule');
INSERT INTO `django_content_type` VALUES (22, 'djcelery', 'intervalschedule');
INSERT INTO `django_content_type` VALUES (18, 'djcelery', 'periodictask');
INSERT INTO `django_content_type` VALUES (23, 'djcelery', 'periodictasks');
INSERT INTO `django_content_type` VALUES (24, 'djcelery', 'taskmeta');
INSERT INTO `django_content_type` VALUES (25, 'djcelery', 'tasksetmeta');
INSERT INTO `django_content_type` VALUES (26, 'djcelery', 'taskstate');
INSERT INTO `django_content_type` VALUES (27, 'djcelery', 'workerstate');
INSERT INTO `django_content_type` VALUES (16, 'fastrunner', 'api');
INSERT INTO `django_content_type` VALUES (6, 'fastrunner', 'case');
INSERT INTO `django_content_type` VALUES (15, 'fastrunner', 'casestep');
INSERT INTO `django_content_type` VALUES (14, 'fastrunner', 'config');
INSERT INTO `django_content_type` VALUES (13, 'fastrunner', 'debugtalk');
INSERT INTO `django_content_type` VALUES (12, 'fastrunner', 'hostip');
INSERT INTO `django_content_type` VALUES (7, 'fastrunner', 'project');
INSERT INTO `django_content_type` VALUES (11, 'fastrunner', 'relation');
INSERT INTO `django_content_type` VALUES (8, 'fastrunner', 'report');
INSERT INTO `django_content_type` VALUES (10, 'fastrunner', 'reportdetail');
INSERT INTO `django_content_type` VALUES (9, 'fastrunner', 'variables');
INSERT INTO `django_content_type` VALUES (28, 'fastrunner', 'visit');
INSERT INTO `django_content_type` VALUES (17, 'fastuser', 'myuser');
INSERT INTO `django_content_type` VALUES (19, 'fastuser', 'userinfo');
INSERT INTO `django_content_type` VALUES (20, 'fastuser', 'usertoken');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');
COMMIT;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2020-04-28 01:25:12.854339');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2020-04-28 01:25:12.912339');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2020-04-28 01:25:12.972339');
INSERT INTO `django_migrations` VALUES (4, 'fastuser', '0001_initial', '2020-04-28 01:25:13.203340');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0001_initial', '2020-04-28 01:25:13.392337');
INSERT INTO `django_migrations` VALUES (6, 'admin', '0002_logentry_user', '2020-04-28 01:25:13.461339');
INSERT INTO `django_migrations` VALUES (7, 'djcelery', '0001_initial', '2020-04-28 01:25:13.697337');
INSERT INTO `django_migrations` VALUES (8, 'fastrunner', '0001_initial', '2020-04-28 01:25:14.188340');
INSERT INTO `django_migrations` VALUES (9, 'fastuser', '0002_auto_20200428_0124', '2020-04-28 01:25:14.353338');
INSERT INTO `django_migrations` VALUES (10, 'sessions', '0001_initial', '2020-04-28 01:25:14.378337');
INSERT INTO `django_migrations` VALUES (11, 'admin', '0002_logentry_remove_auto_add', '2020-08-13 21:07:50.991366');
INSERT INTO `django_migrations` VALUES (12, 'admin', '0003_logentry_add_action_flag_choices', '2020-08-13 21:07:51.005901');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0002_alter_permission_name_max_length', '2020-08-13 21:07:51.045702');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0003_alter_user_email_max_length', '2020-08-13 21:07:51.097017');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0004_alter_user_username_opts', '2020-08-13 21:07:51.109009');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0005_alter_user_last_login_null', '2020-08-13 21:07:51.122195');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0006_require_contenttypes_0002', '2020-08-13 21:07:51.124431');
INSERT INTO `django_migrations` VALUES (18, 'auth', '0007_alter_validators_add_error_messages', '2020-08-13 21:07:51.136439');
INSERT INTO `django_migrations` VALUES (19, 'auth', '0008_alter_user_username_max_length', '2020-08-13 21:07:51.149007');
INSERT INTO `django_migrations` VALUES (20, 'auth', '0009_alter_user_last_name_max_length', '2020-08-13 21:07:51.161260');
INSERT INTO `django_migrations` VALUES (21, 'auth', '0010_alter_group_name_max_length', '2020-08-13 21:07:51.176103');
INSERT INTO `django_migrations` VALUES (22, 'auth', '0011_update_proxy_permissions', '2020-08-13 21:07:51.208644');
INSERT INTO `django_migrations` VALUES (23, 'fastrunner', '0002_auto_20200509_1122', '2020-08-13 21:07:51.230761');
INSERT INTO `django_migrations` VALUES (24, 'fastrunner', '0003_casestep_source_api_id', '2020-08-13 21:07:51.287174');
INSERT INTO `django_migrations` VALUES (25, 'fastuser', '0002_auto_20200509_1122', '2020-08-13 21:07:51.299407');
INSERT INTO `django_migrations` VALUES (26, 'fastuser', '0003_merge_20200813_2107', '2020-08-13 21:07:51.302079');
INSERT INTO `django_migrations` VALUES (27, 'fastrunner', '0004_auto_20200814_1605', '2020-08-16 23:20:17.156113');
INSERT INTO `django_migrations` VALUES (28, 'fastrunner', '0005_auto_20200814_1728', '2020-08-16 23:20:17.335890');
INSERT INTO `django_migrations` VALUES (29, 'fastuser', '0003_merge_20200813_1655', '2020-08-16 23:20:17.338241');
INSERT INTO `django_migrations` VALUES (30, 'fastuser', '0004_auto_20200814_1605', '2020-08-16 23:20:17.405262');
INSERT INTO `django_migrations` VALUES (31, 'fastuser', '0005_merge_20200816_2319', '2020-08-16 23:20:17.407626');
INSERT INTO `django_migrations` VALUES (32, 'fastrunner', '0006_api_case_id', '2020-08-23 12:29:15.668533');
INSERT INTO `django_migrations` VALUES (33, 'fastrunner', '0007_auto_20200822_1119', '2020-08-23 12:29:15.711045');
INSERT INTO `django_migrations` VALUES (34, 'fastrunner', '0008_auto_20200822_1139', '2020-08-23 12:29:15.790162');
INSERT INTO `django_migrations` VALUES (35, 'fastrunner', '0009_auto_20200822_1206', '2020-08-23 12:29:15.855729');
INSERT INTO `django_migrations` VALUES (36, 'fastrunner', '0010_remove_case_apis', '2020-08-23 12:29:15.903528');
INSERT INTO `django_migrations` VALUES (37, 'fastuser', '0005_auto_20200914_2222', '2020-09-14 22:22:52.842512');
INSERT INTO `django_migrations` VALUES (38, 'fastrunner', '0011_auto_20201012_2355', '2020-10-12 23:56:49.154141');
INSERT INTO `django_migrations` VALUES (39, 'fastrunner', '0012_auto_20201013_1029', '2020-10-13 10:31:01.108517');
INSERT INTO `django_migrations` VALUES (40, 'fastrunner', '0013_visit_ip', '2020-10-13 11:37:01.144306');
INSERT INTO `django_migrations` VALUES (41, 'fastrunner', '0014_auto_20201013_1505', '2020-10-13 15:06:00.485276');
INSERT INTO `django_migrations` VALUES (42, 'fastrunner', '0015_auto_20201017_1623', '2020-10-17 16:23:26.955095');
INSERT INTO `django_migrations` VALUES (43, 'fastrunner', '0016_auto_20201017_1624', '2020-10-17 16:25:05.564873');
INSERT INTO `django_migrations` VALUES (44, 'fastrunner', '0017_visit_project', '2020-11-05 14:45:35.451571');
INSERT INTO `django_migrations` VALUES (48, 'fastrunner', '0018_auto_20210410_1950', '2021-04-11 12:46:12.740916');
INSERT INTO `django_migrations` VALUES (49, 'fastrunner', '0019_auto_20210411_2040', '2021-04-11 20:40:26.743613');
INSERT INTO `django_migrations` VALUES (50, 'fastuser', '0006_myuser_show_hosts', '2021-04-19 21:36:37.479682');
INSERT INTO `django_migrations` VALUES (51, 'fastrunner', '0020_auto_20210525_1844', '2021-05-25 18:45:56.693976');
INSERT INTO `django_migrations` VALUES (52, 'fastrunner', '0021_auto_20210525_2113', '2021-05-25 21:13:32.199028');
INSERT INTO `django_migrations` VALUES (53, 'fastrunner', '0022_auto_20210525_2145', '2021-05-25 21:45:26.109433');
INSERT INTO `django_migrations` VALUES (54, 'fastrunner', '0023_auto_20210910_1155', '2021-10-28 01:57:22.366781');
COMMIT;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  KEY `django_session_expire_date_a5c62663` (`expire_date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of django_session
-- ----------------------------
BEGIN;
INSERT INTO `django_session` VALUES ('2vc66mq73oiksygcxxq3av9d9lu4kd4j', 'ZDU4NzczNmM0YzM1NmYzNDhmMmY1ODM2MWVlODk1NWYzODA1ZDYwMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhMzhhYzIwNmU2MWNjYTU2MjM0NzFlZDE2NTEzMTk2NWFlNTQ2NjBlIn0=', '2020-09-28 22:09:47.554236');
INSERT INTO `django_session` VALUES ('66ptafjgjo7776axz4u4a9w2gnxeo0tj', 'YzBlNjUzNzQ0OGRhYTJmMDI0NDI5MmM4NjczNWVkMDlhODI3NzU3Nzp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3MDI2YWQwYzRlZmVlZmM2NWI3ZDQyN2Q5ZWY2NTIzMGQ1OTJjM2EyIn0=', '2022-03-08 21:28:48.243051');
INSERT INTO `django_session` VALUES ('6g7ncgk5apmb7145ba22j02hy6y3f9k7', 'ZDU4NzczNmM0YzM1NmYzNDhmMmY1ODM2MWVlODk1NWYzODA1ZDYwMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhMzhhYzIwNmU2MWNjYTU2MjM0NzFlZDE2NTEzMTk2NWFlNTQ2NjBlIn0=', '2021-07-16 15:56:49.389057');
INSERT INTO `django_session` VALUES ('7qts8m8w4ctt69een4gbtsscocyvurx5', 'ZjQ0ODBlN2M0YmQzYjM4NzRlYTkzZjFiM2E0NDI2N2Y4YTc3YmViYjp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3YWVhNmQwNzg5MTEwOTg1MGM0OTAwYTUxN2M1YzBkZTllN2VmZTY1In0=', '2022-01-27 16:26:32.883009');
INSERT INTO `django_session` VALUES ('93vmt65w4mq6xsl6u8r5ixv4dvzr797g', 'OWNhMmJiOTg4ODZiN2QyZDcwMzdjZDczZjc5MjQ0MDdhZmNiODAwZTp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5N2RkOGVjZTI4MzNjZTY5MWZmOTQ4M2RmMjQyNzljYTM4MTQ4NWUwIn0=', '2020-07-15 17:53:06.459884');
INSERT INTO `django_session` VALUES ('9wnzura3p931dr22szb0qlo1gdyz8qiv', 'NDVhNTllNmVhMjE2NDhmMDI5ZmViNzA4ZmQxNGNmY2EyYzE0OTJjODp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTkwNzU3Y2VhN2Y1MmFiNDFmNmMzN2I0ZmUyNWVkOGQ2MGY2YzAwIn0=', '2020-08-31 09:53:48.300413');
INSERT INTO `django_session` VALUES ('ajozdgf8wkt3jy3h7jkcskdjdu8fw1n8', 'M2FlNTAxMjgyMmE0YjgwMGFjYTI3MTg3MmRiNDY2YjUxNmM3YjM0MDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4NjM3YTEwOGViYThiYjgwY2MyYmU5Mjk5NTc5Yzg0ZWY0YTJkZjFjIn0=', '2020-05-20 11:55:28.450612');
INSERT INTO `django_session` VALUES ('eggkpaz1sim5iy2bftgys83kd9n883o7', 'M2FlNTAxMjgyMmE0YjgwMGFjYTI3MTg3MmRiNDY2YjUxNmM3YjM0MDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4NjM3YTEwOGViYThiYjgwY2MyYmU5Mjk5NTc5Yzg0ZWY0YTJkZjFjIn0=', '2020-06-02 23:31:49.427757');
INSERT INTO `django_session` VALUES ('hbd34qc8npo2q3hkd4p2pmyytc7fn3q4', 'ZDU4NzczNmM0YzM1NmYzNDhmMmY1ODM2MWVlODk1NWYzODA1ZDYwMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhMzhhYzIwNmU2MWNjYTU2MjM0NzFlZDE2NTEzMTk2NWFlNTQ2NjBlIn0=', '2020-12-26 16:31:35.653136');
INSERT INTO `django_session` VALUES ('jcktz5h2obdm8wrwwc3twcejpl7qp03m', 'ZDU4NzczNmM0YzM1NmYzNDhmMmY1ODM2MWVlODk1NWYzODA1ZDYwMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhMzhhYzIwNmU2MWNjYTU2MjM0NzFlZDE2NTEzMTk2NWFlNTQ2NjBlIn0=', '2021-11-11 02:28:53.691557');
INSERT INTO `django_session` VALUES ('jltw9xxdyqit8hsmyavzfgwlo1vpw66q', 'M2FlNTAxMjgyMmE0YjgwMGFjYTI3MTg3MmRiNDY2YjUxNmM3YjM0MDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4NjM3YTEwOGViYThiYjgwY2MyYmU5Mjk5NTc5Yzg0ZWY0YTJkZjFjIn0=', '2020-06-12 18:48:37.048601');
INSERT INTO `django_session` VALUES ('juqlewrznixch2j992qe6y48hfhha2bm', 'ZDU4NzczNmM0YzM1NmYzNDhmMmY1ODM2MWVlODk1NWYzODA1ZDYwMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhMzhhYzIwNmU2MWNjYTU2MjM0NzFlZDE2NTEzMTk2NWFlNTQ2NjBlIn0=', '2021-04-06 23:43:51.887972');
INSERT INTO `django_session` VALUES ('k5cckoxgbtbmc256tpa0wvj1q8vst8ej', 'OWYyNzY1MDk1OTEwMWU1M2E4MzUwNzM1ZDc1YzVkYjIyNmY3ZDI4Yzp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYzAyOTc1MzkwYTlmNjIxNzc4MGIyNjM3NGM1OTI0NWEyMGI3ZmFmIn0=', '2020-08-27 14:58:47.597317');
INSERT INTO `django_session` VALUES ('mhlkxnlvjlipw9iet6z3ekhaw5ptnyxv', 'ZDU4NzczNmM0YzM1NmYzNDhmMmY1ODM2MWVlODk1NWYzODA1ZDYwMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhMzhhYzIwNmU2MWNjYTU2MjM0NzFlZDE2NTEzMTk2NWFlNTQ2NjBlIn0=', '2020-09-01 17:18:14.126484');
INSERT INTO `django_session` VALUES ('xiug5y0smzm2nb4y3n88yx096xnpenwq', 'ZDU4NzczNmM0YzM1NmYzNDhmMmY1ODM2MWVlODk1NWYzODA1ZDYwMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhMzhhYzIwNmU2MWNjYTU2MjM0NzFlZDE2NTEzMTk2NWFlNTQ2NjBlIn0=', '2021-06-08 21:55:33.334101');
INSERT INTO `django_session` VALUES ('ymflt06ksp89g5bzzhalpqikb68iatap', 'ZDU4NzczNmM0YzM1NmYzNDhmMmY1ODM2MWVlODk1NWYzODA1ZDYwMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhMzhhYzIwNmU2MWNjYTU2MjM0NzFlZDE2NTEzMTk2NWFlNTQ2NjBlIn0=', '2020-10-27 13:04:51.243451');
INSERT INTO `django_session` VALUES ('ytmc6pkcvb6qt2x4aii9hwmnw42zl1rm', 'ZDU4NzczNmM0YzM1NmYzNDhmMmY1ODM2MWVlODk1NWYzODA1ZDYwMDp7Il9hdXRoX3VzZXJfaWQiOiI0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhMzhhYzIwNmU2MWNjYTU2MjM0NzFlZDE2NTEzMTk2NWFlNTQ2NjBlIn0=', '2020-10-27 17:57:53.698866');
INSERT INTO `django_session` VALUES ('znm4q5l0ejsozx1r3dqngha4tcf6xi5k', 'OWQxZGJjMTQ4Nzc0ZmFhZTQ1ZjgwMzVkMTI1MjZkZjAzMGQ5ZjVkYTp7Il9hdXRoX3VzZXJfaWQiOiIxNCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMWU4MzMyMjIzNjRjNmNjYjQ3ODRiYTQ0ZjBhOGEyNzcwMjFlZTY2YiJ9', '2021-04-06 23:46:35.608949');
COMMIT;

-- ----------------------------
-- Table structure for djcelery_crontabschedule
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_crontabschedule`;
CREATE TABLE `djcelery_crontabschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `minute` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `hour` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `day_of_week` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `day_of_month` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `month_of_year` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of djcelery_crontabschedule
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for djcelery_intervalschedule
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_intervalschedule`;
CREATE TABLE `djcelery_intervalschedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `every` int NOT NULL,
  `period` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of djcelery_intervalschedule
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for djcelery_periodictask
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_periodictask`;
CREATE TABLE `djcelery_periodictask` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `task` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `args` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `kwargs` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `queue` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `exchange` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `routing_key` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `crontab_id` int DEFAULT NULL,
  `interval_id` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE,
  KEY `djcelery_periodictas_crontab_id_75609bab_fk_djcelery_` (`crontab_id`) USING BTREE,
  KEY `djcelery_periodictas_interval_id_b426ab02_fk_djcelery_` (`interval_id`) USING BTREE,
  CONSTRAINT `djcelery_periodictask_ibfk_1` FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `djcelery_periodictask_ibfk_2` FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of djcelery_periodictask
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for djcelery_periodictasks
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_periodictasks`;
CREATE TABLE `djcelery_periodictasks` (
  `ident` smallint NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of djcelery_periodictasks
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for djcelery_taskstate
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_taskstate`;
CREATE TABLE `djcelery_taskstate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `state` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `task_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tstamp` datetime(6) NOT NULL,
  `args` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `kwargs` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `eta` datetime(6) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `result` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `traceback` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `runtime` double DEFAULT NULL,
  `retries` int NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `worker_id` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `task_id` (`task_id`) USING BTREE,
  KEY `djcelery_taskstate_state_53543be4` (`state`) USING BTREE,
  KEY `djcelery_taskstate_name_8af9eded` (`name`) USING BTREE,
  KEY `djcelery_taskstate_tstamp_4c3f93a1` (`tstamp`) USING BTREE,
  KEY `djcelery_taskstate_hidden_c3905e57` (`hidden`) USING BTREE,
  KEY `djcelery_taskstate_worker_id_f7f57a05_fk_djcelery_workerstate_id` (`worker_id`) USING BTREE,
  CONSTRAINT `djcelery_taskstate_ibfk_1` FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of djcelery_taskstate
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for djcelery_workerstate
-- ----------------------------
DROP TABLE IF EXISTS `djcelery_workerstate`;
CREATE TABLE `djcelery_workerstate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hostname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_heartbeat` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `hostname` (`hostname`) USING BTREE,
  KEY `djcelery_workerstate_last_heartbeat_4539b544` (`last_heartbeat`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of djcelery_workerstate
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for fastuser_myuser
-- ----------------------------
DROP TABLE IF EXISTS `fastuser_myuser`;
CREATE TABLE `fastuser_myuser` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `show_hosts` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `username` (`username`) USING BTREE,
  UNIQUE KEY `phone` (`phone`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of fastuser_myuser
-- ----------------------------
BEGIN;
INSERT INTO `fastuser_myuser` VALUES (4, 'pbkdf2_sha256$150000$2ZQUTmy2m73w$Dj8Tqyz6g+7Z80aDXPOdrSB98GyCCp/kT4gZspD/YA8=', '2022-02-22 21:28:48.233250', 1, 'admin', '', '', 'lihuacai168@gmail.com', 1, 1, '2020-07-01 17:30:00.000000', '', 0);
INSERT INTO `fastuser_myuser` VALUES (6, 'pbkdf2_sha256$150000$8fDo70qQ8rKS$FNqsIQDIfVFjVWlxZOYsBb3Gb7NcLX6cZly64r7PWUo=', NULL, 0, 'test', '', '', 'test@baibu.la', 0, 1, '2020-08-16 10:15:54.984186', '18666123456', 0);
INSERT INTO `fastuser_myuser` VALUES (7, 'pbkdf2_sha256$150000$LnzEtAW5ysrS$HfU2o2B6QFhzTp7lDO6nxjz6vAlX45WkvtHccy6iTvo=', '2022-01-13 16:25:57.113112', 1, 'root', '', '', '', 1, 1, '2022-01-13 16:11:30.737809', NULL, 0);
COMMIT;

-- ----------------------------
-- Table structure for fastuser_myuser_groups
-- ----------------------------
DROP TABLE IF EXISTS `fastuser_myuser_groups`;
CREATE TABLE `fastuser_myuser_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `myuser_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `fastuser_myuser_groups_myuser_id_group_id_bcffdd61_uniq` (`myuser_id`,`group_id`) USING BTREE,
  KEY `fastuser_myuser_groups_group_id_03c0ddaa_fk_auth_group_id` (`group_id`) USING BTREE,
  CONSTRAINT `fastuser_myuser_groups_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fastuser_myuser_groups_ibfk_2` FOREIGN KEY (`myuser_id`) REFERENCES `fastuser_myuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of fastuser_myuser_groups
-- ----------------------------
BEGIN;
INSERT INTO `fastuser_myuser_groups` VALUES (1, 4, 1);
COMMIT;

-- ----------------------------
-- Table structure for fastuser_myuser_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `fastuser_myuser_user_permissions`;
CREATE TABLE `fastuser_myuser_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `myuser_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `fastuser_myuser_user_per_myuser_id_permission_id_9cbaf04a_uniq` (`myuser_id`,`permission_id`) USING BTREE,
  KEY `fastuser_myuser_user_permission_id_2d3661ab_fk_auth_perm` (`permission_id`) USING BTREE,
  CONSTRAINT `fastuser_myuser_user_permissions_ibfk_1` FOREIGN KEY (`myuser_id`) REFERENCES `fastuser_myuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fastuser_myuser_user_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of fastuser_myuser_user_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for host_ip
-- ----------------------------
DROP TABLE IF EXISTS `host_ip`;
CREATE TABLE `host_ip` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `value` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `project_id` int NOT NULL,
  `creator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updater` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `host_ip_project_id_f746c53c` (`project_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of host_ip
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `desc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `responsible` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `creator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updater` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `yapi_base_url` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `yapi_openapi_token` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `jira_bearer_token` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `jira_project_key` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of project
-- ----------------------------
BEGIN;
INSERT INTO `project` VALUES (7, '2019-11-19 10:00:25.568775', '2021-10-28 02:16:19.301240', '示例项目', '用来查看FasterRunner常用操作', 'admin', '李华才', '李华才', '', '', '', '');
INSERT INTO `project` VALUES (8, '2022-01-13 16:14:25.882615', '2022-01-13 16:14:25.882640', 'test-1', 'test1', 'root', NULL, NULL, '', '', '', '');
COMMIT;

-- ----------------------------
-- Table structure for relation
-- ----------------------------
DROP TABLE IF EXISTS `relation`;
CREATE TABLE `relation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tree` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `type` int NOT NULL,
  `project_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `Relation_project_id_1ea3da13_fk_Project_id` (`project_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of relation
-- ----------------------------
BEGIN;
INSERT INTO `relation` VALUES (13, '[{\'id\': 1, \'y_id\': 134, \'label\': \'测试分组1\', \'children\': [{\'id\': 2, \'label\': \'聚合数据\', \'children\': [{\'id\': 50, \'label\': \'通天塔\', \'children\': []}]}, {\'id\': 3, \'label\': \'eee\', \'children\': [{\'id\': 46, \'label\': \'asdfasdfasdf\', \'children\': []}]}, {\'id\': 39, \'label\': \'safasdf\', \'children\': [{\'id\': 40, \'label\': \'asdfsadf\', \'children\': [{\'id\': 42, \'label\': \'asdfasdf\', \'children\': [{\'id\': 43, \'label\': \'sdfweaf\', \'children\': []}, {\'id\': 44, \'label\': \'afdawefaew\', \'children\': []}]}]}, {\'id\': 41, \'label\': \'asfadsf\', \'children\': []}]}, {\'id\': 51, \'label\': \'开\', \'children\': []}, {\'id\': 30, \'label\': \'222\', \'children\': []}, {\'id\': 32, \'label\': \'httpbin\', \'children\': []}]}, {\'id\': 31, \'label\': \'mock-redis\', \'children\': []}, {\'id\': 33, \'label\': \'00000\', \'children\': []}, {\'id\': 34, \'label\': \'1111\', \'children\': []}, {\'id\': 35, \'label\': \'test\', \'children\': []}, {\'id\': 36, \'label\': \'用户管理\', \'children\': []}, {\'id\': 37, \'label\': \'cper\', \'children\': [{\'id\': 38, \'label\': \'123\', \'children\': [{\'id\': 45, \'label\': \'asdfasdf\', \'children\': []}]}]}, {\'id\': 47, \'label\': \'12312312\', \'children\': []}, {\'id\': 48, \'label\': \'123123123\', \'children\': [{\'id\': 49, \'label\': \'22\', \'children\': []}]}, {\'id\': 52, \'label\': \'测试0212\', \'children\': [{\'id\': 54, \'label\': \'登录\', \'children\': []}]}, {\'id\': 53, \'label\': \'子节点\', \'children\': []}]', 1, 7);
INSERT INTO `relation` VALUES (14, '[{\'id\': 1, \'label\': \'用例1\', \'children\': [{\'id\': 31, \'label\': \'3232\', \'children\': []}]}, {\'id\': 24, \'label\': \'登录\', \'children\': []}, {\'id\': 25, \'label\': \'wait\', \'children\': []}, {\'id\': 26, \'label\': \'mock-redis\', \'children\': []}, {\'id\': 27, \'label\': \'0000\', \'children\': []}, {\'id\': 28, \'label\': \'1\', \'children\': []}, {\'id\': 29, \'label\': \'2\', \'children\': []}, {\'id\': 30, \'label\': \'3\', \'children\': []}, {\'id\': 32, \'label\': \'fff\', \'children\': []}, {\'id\': 33, \'label\': \'123456\', \'children\': [{\'id\': 35, \'label\': \'ggg\', \'children\': []}]}, {\'id\': 34, \'label\': \'ttt\', \'children\': []}, {\'id\': 36, \'label\': \'22\', \'children\': []}]', 2, 7);
INSERT INTO `relation` VALUES (15, '[{\'id\': 1, \'label\': \'1\', \'children\': [{\'id\': 4, \'label\': \'4\', \'children\': []}, {\'id\': 5, \'label\': \'5\', \'children\': []}]}, {\'id\': 2, \'label\': \'2\', \'children\': []}, {\'id\': 3, \'label\': \'3\', \'children\': []}, {\'id\': 6, \'label\': \'22\', \'children\': [{\'id\': 7, \'label\': \'12\', \'children\': [{\'id\': 8, \'label\': \'33\', \'children\': []}]}]}]', 1, 8);
INSERT INTO `relation` VALUES (16, '[{\'id\': 1, \'label\': \'xx\', \'children\': []}]', 2, 8);
COMMIT;

-- ----------------------------
-- Table structure for report
-- ----------------------------
DROP TABLE IF EXISTS `report`;
CREATE TABLE `report` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `type` int NOT NULL,
  `status` tinyint(1) NOT NULL,
  `summary` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `project_id` int NOT NULL,
  `creator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updater` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ci_metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ci_job_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ci_project_id` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `ci_job_id` (`ci_job_id`) USING BTREE,
  KEY `report_project_id_e21733bf` (`project_id`) USING BTREE,
  KEY `report_ci_project_id_4d3e81e6` (`ci_project_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of report
-- ----------------------------
BEGIN;
INSERT INTO `report` VALUES (1, '2022-02-22 01:12:00.883075', '2022-02-22 01:12:00.883109', 'mock-list', 1, 1, '{\"success\": true, \"stat\": {\"testsRun\": 1, \"failures\": 0, \"errors\": 0, \"skipped\": 0, \"expectedFailures\": 0, \"unexpectedSuccesses\": 0, \"successes\": 1}, \"time\": {\"start_at\": 1645463519.1411793, \"setup_hooks_duration\": 0, \"teardown_hooks_duration\": 0, \"duration\": 0.727}, \"platform\": {\"httprunner_version\": \"1.5.15\", \"python_version\": \"CPython 3.6.15\", \"platform\": \"Linux-5.10.47-linuxkit-x86_64-with\"}}', 7, 'test', NULL, '{}', NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for report_detail
-- ----------------------------
DROP TABLE IF EXISTS `report_detail`;
CREATE TABLE `report_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `summary_detail` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `report_id` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `report_id` (`report_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of report_detail
-- ----------------------------
BEGIN;
INSERT INTO `report_detail` VALUES (1, '[{\'success\': True, \'stat\': {\'testsRun\': 1, \'failures\': 0, \'errors\': 0, \'skipped\': 0, \'expectedFailures\': 0, \'unexpectedSuccesses\': 0, \'successes\': 1}, \'time\': {\'start_at\': 1645463519.1411793, \'setup_hooks_duration\': 0, \'teardown_hooks_duration\': 0, \'duration\': 0.727}, \'records\': [{\'name\': \'mock-list\', \'status\': \'success\', \'attachment\': \'\', \'meta_data\': {\'request\': {\'url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io/list\', \'method\': \'GET\', \'headers\': {\'User-Agent\': \'python-requests/2.22.0\', \'Accept-Encoding\': \'gzip, deflate\', \'Accept\': \'*/*\', \'Connection\': \'keep-alive\', \'Content-Type\': \'application/json;charset=utf-8\', \'userId\': \'var\', \'Content-Length\': \'2\'}, \'start_timestamp\': 1645463519.141939, \'setup_hooks_start\': 1645463519.1416297, \'setup_hooks_duration\': 0, \'json\': {}, \'verify\': False, \'body\': \'{}\'}, \'response\': {\'status_code\': 200, \'headers\': {\'Date\': \'Mon, 21 Feb 2022 17:12:00 GMT\', \'Content-Type\': \'text/html; charset=utf-8\', \'Transfer-Encoding\': \'chunked\', \'Connection\': \'close\', \'Server\': \'nginx\', \'x-srv-trace\': \'v=1;t=f7cf8f21059ee614\', \'x-srv-span\': \'v=1;s=e4f7f56c4e2f2ec4\', \'Access-Control-Allow-Origin\': \'*\', \'X-RateLimit-Limit\': \'120\', \'X-RateLimit-Remaining\': \'119\', \'X-RateLimit-Reset\': \'1624356286\', \'ETag\': \'W/\"7-n4nHQM60bXQYySSnisV5QdXpZSA\"\', \'Vary\': \'Accept-Encoding\', \'Content-Encoding\': \'gzip\'}, \'content_size\': 131, \'response_time_ms\': 1728.78, \'elapsed_ms\': 726.999, \'encoding\': \'utf-8\', \'content\': \'[{\\n    \"k0\": \"val-0\",\\n    \"k1\": \"val-1\"\\n},\\n{\\n    \"j0\": \"val-j0\",\\n    \"j1\": \"val-j1\"\\n},\\n{\\n    \"m0\": \"val-m0\",\\n    \"m1\": \"val-m1\"\\n}\\n]\\n\', \'content_type\': \'text/html; charset=utf-8\', \'ok\': True, \'url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io/list\', \'reason\': \'OK\', \'cookies\': {}, \'text\': \'[{\\n    \"k0\": \"val-0\",\\n    \"k1\": \"val-1\"\\n},\\n{\\n    \"j0\": \"val-j0\",\\n    \"j1\": \"val-j1\"\\n},\\n{\\n    \"m0\": \"val-m0\",\\n    \"m1\": \"val-m1\"\\n}\\n]\', \'json\': [{\'k0\': \'val-0\', \'k1\': \'val-1\'}, {\'j0\': \'val-j0\', \'j1\': \'val-j1\'}, {\'m0\': \'val-m0\', \'m1\': \'val-m1\'}], \'teardown_hooks_start\': 1645463520.8710752, \'teardown_hooks_duration\': 0}, \'curl\': \"curl -X GET -H \'Accept: */*\' -H \'Accept-Encoding: gzip, deflate\' -H \'Connection: keep-alive\' -H \'Content-Length: 2\' -H \'Content-Type: application/json;charset=utf-8\' -H \'User-Agent: python-requests/2.22.0\' -H \'userId: var\' -d \'{}\' --compressed https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io/list\", \'validators\': []}}], \'name\': \'mock-list\', \'base_url\': \'http://localhost:8000\', \'in_out\': {\'in\': {\'mock_url\': \'https://748b3235-eb1b-4d69-8be3-95005f353b52.mock.pstmn.io\', \'cdh2\': \'http://localhost:9000\', \'userId\': \'var\', \'x\': \'abc\', \'token\': None, \'test_user\': \'qa1\', \'test_password\': \'gg9tKGBjK8GEgg9tKGBjK8GE\', \'test_user2\': \'qa1\', \'test_user211\': \'qa1\', \'22\': \'333\', \'g\': \'1645463519\', \'msg\': [{\'msg\': \'login success\'}, {\'msg\': \'用户名或密码错误\'}, {\'msg\': \'用户名或密码错误\'}, {\'msg\': \'用户名或密码错误\'}]}, \'out\': {}}}]', 1);
COMMIT;

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `level` int NOT NULL,
  `creator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updater` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `username` (`username`) USING BTREE,
  UNIQUE KEY `email` (`email`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of user_info
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_token
-- ----------------------------
DROP TABLE IF EXISTS `user_token`;
CREATE TABLE `user_token` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `token` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_id` int NOT NULL,
  `creator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updater` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `user_id` (`user_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of user_token
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for variables
-- ----------------------------
DROP TABLE IF EXISTS `variables`;
CREATE TABLE `variables` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `value` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `project_id` int NOT NULL,
  `description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `creator` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updater` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `Variables_project_id_70a90149_fk_Project_id` (`project_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of variables
-- ----------------------------
BEGIN;
INSERT INTO `variables` VALUES (34, '2019-11-19 11:54:12.856013', '2019-11-19 11:54:12.856051', 'token', '${get_token()}', 7, NULL, NULL, NULL);
INSERT INTO `variables` VALUES (35, '2020-05-09 12:08:42.736563', '2020-09-15 14:42:08.900954', 'test_user', 'qa1', 7, '测试用户', NULL, NULL);
INSERT INTO `variables` VALUES (36, '2020-05-09 12:09:18.022871', '2020-09-15 14:41:49.763212', 'test_password', 'gg9tKGBjK8GEgg9tKGBjK8GE', 7, 'qa1测试用户的密码11', NULL, NULL);
INSERT INTO `variables` VALUES (60, '2020-09-15 14:43:25.780936', '2020-09-15 14:43:25.780963', 'test_user2', 'qa1', 7, '测试用户', NULL, NULL);
INSERT INTO `variables` VALUES (61, '2020-09-15 15:33:50.285982', '2020-09-15 15:33:50.286054', 'test_user211', 'qa1', 7, '测试用户', NULL, NULL);
INSERT INTO `variables` VALUES (62, '2020-09-15 15:33:56.508908', '2020-09-15 15:33:56.508938', '22', '333', 7, '测试用户', NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for visit
-- ----------------------------
DROP TABLE IF EXISTS `visit`;
CREATE TABLE `visit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `request_method` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `request_body` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `request_params` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `project` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `visit_create_time_18fc002a` (`create_time`) USING BTREE,
  KEY `visit_ip_8eea545d` (`ip`) USING BTREE,
  KEY `visit_path_de3cc23d` (`path`) USING BTREE,
  KEY `visit_request_method_a2142cb8` (`request_method`) USING BTREE,
  KEY `visit_request_params_cf929175` (`request_params`) USING BTREE,
  KEY `visit_url_35d78337` (`url`) USING BTREE,
  KEY `visit_user_8de779fe` (`user`) USING BTREE,
  KEY `visit_project_41603a2f` (`project`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of visit
-- ----------------------------
BEGIN;
INSERT INTO `visit` VALUES (1, 'admin', '/admin/', 'GET', '2022-02-22 21:49:21.296817', '', '192.168.80.1', '/admin/', '', '0');
INSERT INTO `visit` VALUES (2, 'admin', '/admin/', 'GET', '2022-02-22 21:49:23.492589', '', '192.168.80.1', '/admin/', '', '0');
INSERT INTO `visit` VALUES (3, 'admin', '/admin/', 'GET', '2022-02-22 21:49:24.512008', '', '192.168.80.1', '/admin/', '', '0');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
