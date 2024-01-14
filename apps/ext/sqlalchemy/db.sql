/*
 Navicat Premium Data Transfer

 Source Server         : MYSQL
 Source Server Type    : MySQL
 Source Server Version : 50740 (5.7.40)
 Source Host           : localhost:3306
 Source Schema         : db

 Target Server Type    : MySQL
 Target Server Version : 50740 (5.7.40)
 File Encoding         : 65001

 Date: 14/01/2024 23:05:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for atom
-- ----------------------------
DROP TABLE IF EXISTS `atom`;
CREATE TABLE `atom`  (
  `id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '主键id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '按钮名称',
  `sort` int(20) NULL DEFAULT NULL COMMENT '排序',
  `describe` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '按钮描述',
  `create_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id',
  `update_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id 、每次更新的是自动更新该字段',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of atom
-- ----------------------------
INSERT INTO `atom` VALUES ('079d099d-ac4d-4d1b-863d-ffb29f924e12', '测试按钮2', 100, '测试', '152f6384-4c03-4197-a576-548a9199868f', '152f6384-4c03-4197-a576-548a9199868f', '2023-07-26 03:22:49', '2023-08-21 07:03:04');
INSERT INTO `atom` VALUES ('21cfc6e2-5131-4aa9-9b7e-a8c8d8108ff1', '按钮1', 1, '这是按钮1', '152f6384-4c03-4197-a576-548a9199868f', '152f6384-4c03-4197-a576-548a9199868f', '2023-07-26 00:50:36', '2023-07-26 00:50:36');
INSERT INTO `atom` VALUES ('33b65eca-a849-4287-9caa-765e74423c76', '按钮2', 2, '这是按钮2', '152f6384-4c03-4197-a576-548a9199868f', '152f6384-4c03-4197-a576-548a9199868f', '2023-07-26 00:50:40', '2023-07-26 00:50:44');
INSERT INTO `atom` VALUES ('69183860-a113-4808-ab11-4f64196b700b', '按钮7', 7, '这是按钮7', '152f6384-4c03-4197-a576-548a9199868f', '152f6384-4c03-4197-a576-548a9199868f', '2023-07-26 02:24:10', '2023-07-26 02:24:10');
INSERT INTO `atom` VALUES ('70dfa78f-68b4-420e-9cd4-1ea83eb1fe67', '按钮8', 8, '这是按钮8', '152f6384-4c03-4197-a576-548a9199868f', '152f6384-4c03-4197-a576-548a9199868f', '2023-07-26 02:24:14', '2023-07-26 02:24:14');
INSERT INTO `atom` VALUES ('7a12f530-8d19-4e88-b9c3-cbb375bf6dd9', '按钮3', 3, '这是按钮3', '152f6384-4c03-4197-a576-548a9199868f', '152f6384-4c03-4197-a576-548a9199868f', '2023-07-26 00:49:15', '2023-07-26 00:49:15');
INSERT INTO `atom` VALUES ('a3bdafac-4cdf-4a6e-9ec9-cf62540ae4a8', '按钮4', 4, '这是按钮4', '152f6384-4c03-4197-a576-548a9199868f', '152f6384-4c03-4197-a576-548a9199868f', '2023-07-26 00:50:44', '2023-07-26 00:58:25');
INSERT INTO `atom` VALUES ('b96fe843-28fe-478b-863a-f6979de1b8c6', '按钮9', 9, '这是按钮9', '152f6384-4c03-4197-a576-548a9199868f', '152f6384-4c03-4197-a576-548a9199868f', '2023-07-26 02:24:18', '2023-07-26 02:24:18');
INSERT INTO `atom` VALUES ('efee6ad3-7fc0-4fcf-b88d-fe9a5612c6b6', '按钮5', 5, '这是按钮5', '152f6384-4c03-4197-a576-548a9199868f', '152f6384-4c03-4197-a576-548a9199868f', '2023-07-26 00:48:50', '2023-07-26 00:48:50');
INSERT INTO `atom` VALUES ('fb2b5e94-07e1-419d-b161-dfd867bfa069', '按钮6', 6, '这是按钮6', '152f6384-4c03-4197-a576-548a9199868f', '152f6384-4c03-4197-a576-548a9199868f', '2023-07-26 00:49:12', '2023-07-26 00:49:12');

-- ----------------------------
-- Table structure for dict
-- ----------------------------
DROP TABLE IF EXISTS `dict`;
CREATE TABLE `dict`  (
  `id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '主键id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '字典名称',
  `type` int(255) NOT NULL COMMENT '字典类型',
  `sort` int(255) NULL DEFAULT NULL COMMENT '排序',
  `status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '状态: 0: 禁用, 1: 开启',
  `describe` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '描述',
  `values` json NOT NULL COMMENT '字典值',
  `create_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id',
  `update_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id 、每次更新的是自动更新该字段',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of dict
-- ----------------------------

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu`  (
  `id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '主键id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '首页的组件名称',
  `path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '菜单路径',
  `grade` int(20) NOT NULL COMMENT '菜单等级',
  `superior_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '父级菜单id,如果没有,则为null',
  `menu_type` int(8) NOT NULL COMMENT '菜单类型: 1: 目录, 2: 菜单',
  `sort` int(20) NULL DEFAULT NULL COMMENT '排序',
  `is_out_lint` tinyint(1) NOT NULL COMMENT '是否外链',
  `out_lint` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '外链地址',
  `meta` json NOT NULL COMMENT '菜单的其他信息(名称 + icon)',
  `create_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id',
  `update_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id 、每次更新的是自动更新该字段',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `hidden` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否隐藏菜单',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES ('190720d23f44ecb9582e2e6c609956aa', 'role', '/role', 2, '2db5db4af8793c934f3a1896678e772d', 2, 3, 1, NULL, '{\"icon\": \"el-icon-bangzhu\", \"name\": \"角色管理\"}', 'admin', 'admin', '2023-11-06 15:17:32', '2023-11-06 15:31:12', 0);
INSERT INTO `menu` VALUES ('2db5db4af8793c934f3a1896678e772d', 'system', '/system', 2, NULL, 1, 1, 0, NULL, '{\"icon\": \"el-icon-s-tools\", \"name\": \"系统管理\"}', 'admin', 'admin', '2023-09-26 16:01:02', '2023-11-06 15:32:34', 0);
INSERT INTO `menu` VALUES ('5044421973f4383f7be6d4484ad45eba', 'permission', '/permission', 2, '2db5db4af8793c934f3a1896678e772d', 1, 1, 0, NULL, '{\"icon\": \"el-icon-coordinate\", \"name\": \"权限管理\"}', 'admin', 'admin', '2023-09-26 17:54:27', '2023-09-28 10:10:55', 0);
INSERT INTO `menu` VALUES ('658e635cd880a6d441629759b81c735b', 'menu', '/menu', 3, '5044421973f4383f7be6d4484ad45eba', 2, 1, 0, NULL, '{\"icon\": \"el-icon-menu\", \"name\": \"菜单管理\"}', 'admin', 'admin', '2023-11-06 11:55:44', '2023-11-06 15:33:48', 0);
INSERT INTO `menu` VALUES ('76aeadef398f70e971633feac409c29d', 'user', '/user', 2, '2db5db4af8793c934f3a1896678e772d', 2, 2, 0, NULL, '{\"icon\": \"el-icon-s-custom\", \"name\": \"用户管理\"}', 'admin', 'admin', '2023-11-06 11:46:37', '2023-11-06 15:13:55', 0);
INSERT INTO `menu` VALUES ('80a37bb30c1386adfbbc42230fa4ff1a', 'school', '/school/index', 1, NULL, 2, 1, 0, NULL, '{\"name\": \"学校主体关联\"}', 'admin', 'admin', '2023-11-14 09:21:07', '2023-11-14 09:21:07', 0);

-- ----------------------------
-- Table structure for menu_atom
-- ----------------------------
DROP TABLE IF EXISTS `menu_atom`;
CREATE TABLE `menu_atom`  (
  `id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '主键id',
  `menu_id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `atom_id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `create_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id',
  `update_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id 、每次更新的是自动更新该字段',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `menu_atom_menu_id_atom_id_unique`(`atom_id`, `menu_id`) USING BTREE,
  INDEX `menu_id`(`menu_id`) USING BTREE,
  CONSTRAINT `menu_atom_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `menu_atom_ibfk_2` FOREIGN KEY (`atom_id`) REFERENCES `atom` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of menu_atom
-- ----------------------------
INSERT INTO `menu_atom` VALUES ('1111', '5044421973f4383f7be6d4484ad45eba', '21cfc6e2-5131-4aa9-9b7e-a8c8d8108ff1', '11', '11', '2024-01-07 18:20:04', '2024-01-07 18:20:07');
INSERT INTO `menu_atom` VALUES ('2222', '5044421973f4383f7be6d4484ad45eba', '33b65eca-a849-4287-9caa-765e74423c76', '11', '11', '2024-01-07 18:20:04', '2024-01-07 18:20:07');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '主键id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '角色名称',
  `parent_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '角色的父级id',
  `sort` int(20) NULL DEFAULT NULL COMMENT '排序',
  `status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '角色状态: 0: 禁用, 1: 开启',
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '角色',
  `describe` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '角色描述',
  `create_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id',
  `update_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id 、每次更新的是自动更新该字段',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('24167cc2348a7aae52b4ffda8df549f3', '管理员', '', 1, 1, 'admin', '有用全部权限', 'admin', 'admin', '2023-09-26 11:48:52', '2023-11-06 17:42:50');

-- ----------------------------
-- Table structure for role_atom
-- ----------------------------
DROP TABLE IF EXISTS `role_atom`;
CREATE TABLE `role_atom`  (
  `id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '主键id',
  `role_id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `atom_id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `create_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id',
  `update_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id 、每次更新的是自动更新该字段',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `role_atom_role_id_atom_id_unique`(`atom_id`, `role_id`) USING BTREE,
  INDEX `role_id`(`role_id`) USING BTREE,
  CONSTRAINT `role_atom_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `role_atom_ibfk_2` FOREIGN KEY (`atom_id`) REFERENCES `atom` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of role_atom
-- ----------------------------

-- ----------------------------
-- Table structure for role_menu
-- ----------------------------
DROP TABLE IF EXISTS `role_menu`;
CREATE TABLE `role_menu`  (
  `id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '主键id',
  `menu_id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `role_id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `create_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id',
  `update_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id 、每次更新的是自动更新该字段',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `role_menu_menu_id_role_id_unique`(`role_id`, `menu_id`) USING BTREE,
  INDEX `menu_id`(`menu_id`) USING BTREE,
  CONSTRAINT `role_menu_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `role_menu_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of role_menu
-- ----------------------------
INSERT INTO `role_menu` VALUES ('1474c8d7a1db93e6c974325d9f6c7072', '190720d23f44ecb9582e2e6c609956aa', '24167cc2348a7aae52b4ffda8df549f3', 'admin', 'admin', '2023-11-06 17:42:50', '2023-11-06 17:42:50');
INSERT INTO `role_menu` VALUES ('607dc56e9107e5324a85db07c12c19c3', '76aeadef398f70e971633feac409c29d', '24167cc2348a7aae52b4ffda8df549f3', 'admin', 'admin', '2023-11-06 17:42:51', '2023-11-06 17:42:51');
INSERT INTO `role_menu` VALUES ('67cb7522a9bb69afbd8a493f4005dcbf', '2db5db4af8793c934f3a1896678e772d', '24167cc2348a7aae52b4ffda8df549f3', 'admin', 'admin', '2023-11-06 17:42:50', '2023-11-06 17:42:50');
INSERT INTO `role_menu` VALUES ('89d33c66477aac3a0883678b8d35bce3', '658e635cd880a6d441629759b81c735b', '24167cc2348a7aae52b4ffda8df549f3', 'admin', 'admin', '2023-11-06 17:42:50', '2023-11-06 17:42:50');
INSERT INTO `role_menu` VALUES ('d372d032d308b0064352ba8bc6e3600d', '5044421973f4383f7be6d4484ad45eba', '24167cc2348a7aae52b4ffda8df549f3', 'admin', 'admin', '2023-11-06 17:42:50', '2023-11-06 17:42:50');

-- ----------------------------
-- Table structure for systheme
-- ----------------------------
DROP TABLE IF EXISTS `systheme`;
CREATE TABLE `systheme`  (
  `id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '主键id',
  `logo` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '系统logo图片地址',
  `is_show_logo` tinyint(1) NULL DEFAULT 0 COMMENT '是否展示logo',
  `theme_colors` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '主题颜色',
  `theme_scheme` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '主题方法: 菜单颜色 + 顶部颜色 + 背景颜色',
  `fixed_header` tinyint(1) NULL DEFAULT 0 COMMENT '固定顶部不滑动',
  `btn_size` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '按钮大小',
  `font_size` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '字体大小',
  `ipt_size` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '输入框类型大小',
  `is_show_top_cache_menu` tinyint(1) NULL DEFAULT 0 COMMENT '是否展示顶部缓存的',
  `create_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id',
  `update_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id 、每次更新的是自动更新该字段',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of systheme
-- ----------------------------
INSERT INTO `systheme` VALUES ('5b913645d7ce6cf2088e17fbd7f5eb46', '', 1, '', '', 1, '', '', 'proident ad sit commodo', 0, 'admin', 'admin', '2023-09-26 11:50:23', '2023-09-26 11:50:23');
INSERT INTO `systheme` VALUES ('6cb8ec03ae7cd073a75e8b8c5d026a55', '', 1, 'red', '', 0, '', '', '', 0, 'admin', 'admin', '2023-11-07 11:13:49', '2023-11-07 11:13:49');
INSERT INTO `systheme` VALUES ('b022a217ca95c8fb8becab19c5948b06', 'esse tempor cupidatat labore deserunt', 1, 'red', 'laborum', 0, '10', '10', 'proident ad sit commodo', 0, 'admin', 'admin', '2023-09-26 11:51:06', '2023-09-26 11:51:06');
INSERT INTO `systheme` VALUES ('dfe3ba49be02187469e082857b58e135', '', 1, '', '', 1, '', '', 'proident ad sit commodo', 0, 'admin', 'admin', '2023-09-20 10:04:04', '2023-09-20 10:04:04');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '主键id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '角色名称',
  `sort` int(20) NULL DEFAULT NULL COMMENT '排序',
  `status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '角色状态: 0: 禁用, 1: 开启',
  `avatar` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录账号',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录密码',
  `introduction` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '描述',
  `systheme_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '描述',
  `create_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id',
  `update_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id 、每次更新的是自动更新该字段',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `u_username`(`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('391b4e2f5f7c50c5ef7030b59e36aeae', '超级管理员', 1, 1, 'http://106.13.226.9:6657/resource/16992604694585948.png', 'admin', '$2b$12$wa6vZO0KsMav1ick7tOkhOeY0jc7f97dAmjEimxbl0J3YSluITxGi', '超级管理员', 'b022a217ca95c8fb8becab19c5948b06', '', 'admin', '2023-09-14 15:58:45', '2023-11-06 16:47:52');
INSERT INTO `user` VALUES ('71b63a401f02b438dc121478c947d82c', '知细价点容风证', 19, 1, 'http://106.13.226.9:6657/resource/16992596955403934.jpg', 'luojinmin', 'e10adc3949ba59abbe56e057f20f883e', NULL, NULL, '', 'admin', '2023-09-18 17:21:03', '2023-11-06 16:39:42');
INSERT INTO `user` VALUES ('957591fac05ced0b83314e74621cd489', 'madaraw', NULL, 0, NULL, 'madara', 'e10adc3949ba59abbe56e057f20f883e', NULL, NULL, 'madara', 'madara', '2023-09-14 10:07:51', '2023-09-14 10:07:51');
INSERT INTO `user` VALUES ('987435bc-b22c-11ee-bdf2-581122d52e74', '111', 0, 0, '11111', '111', '11111', '11111', '11111', '11111', '11111', '2024-01-13 15:58:30', '2024-01-13 15:58:30');
INSERT INTO `user` VALUES ('b0dc772f121f4715e6b7c8321e323bce', '知细价点容风证', 19, 1, 'http://dummyimage.com/100x100', 'admin3', '32cacb2f994f6b42183a1300d9a3e8d6', NULL, 'dfe3ba49be02187469e082857b58e135', '', '', '2023-09-20 10:06:05', '2023-09-20 10:06:05');
INSERT INTO `user` VALUES ('b2ce58f2910916c7d3e08431a5ca1096', '知细价点容风证', 19, 1, 'http://dummyimage.com/100x100', 'admin2', 'c84258e9c39059a89ab77d846ddab909', NULL, 'dfe3ba49be02187469e082857b58e135', '', '', '2023-09-20 10:05:09', '2023-09-20 10:05:09');

-- ----------------------------
-- Table structure for user_role
-- ----------------------------
DROP TABLE IF EXISTS `user_role`;
CREATE TABLE `user_role`  (
  `id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '主键id',
  `user_id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `role_id` char(36) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `create_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id',
  `update_user` char(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '创建人的id 、每次更新的是自动更新该字段',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_role_role_id_user_id_unique`(`user_id`, `role_id`) USING BTREE,
  INDEX `role_id`(`role_id`) USING BTREE,
  CONSTRAINT `user_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_role
-- ----------------------------
INSERT INTO `user_role` VALUES ('3faec5f1076d099218724b573b475c68', '391b4e2f5f7c50c5ef7030b59e36aeae', '24167cc2348a7aae52b4ffda8df549f3', 'admin', 'admin', '2023-11-06 16:47:52', '2023-11-06 16:47:52');
INSERT INTO `user_role` VALUES ('db32aa3e9d94f5401351b196ca4eb9a7', '71b63a401f02b438dc121478c947d82c', '24167cc2348a7aae52b4ffda8df549f3', 'admin', 'admin', '2023-11-06 16:39:42', '2023-11-06 16:39:42');

SET FOREIGN_KEY_CHECKS = 1;
