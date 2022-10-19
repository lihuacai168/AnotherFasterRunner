import component from './zh-CN/component';
import globalHeader from './zh-CN/globalHeader';
import menu from './zh-CN/menu';
import pwa from './zh-CN/pwa';
import settingDrawer from './zh-CN/settingDrawer';
import settings from './zh-CN/settings';

export default {
  'navBar.lang': '语言',
  'layout.user.link.help': '帮助',
  'layout.user.link.privacy': '隐私',
  'layout.user.link.terms': '条款',
  'app.preview.down.block': '下载此页面到本地项目',
  'app.welcome.link.fetch-blocks': '获取全部区块',
  'app.welcome.link.block-list': '基于 block 开发，快速构建标准页面',
  'app.docs.components.icon.search.placeholder': '在此搜索图标，点击图标进行选择',
  'app.docs.components.icon.outlined': '线框风格',
  'app.docs.components.icon.filled': '实底风格',
  'app.docs.components.icon.two-tone': '双色风格',
  'app.docs.components.icon.category.direction': '方向性图标',
  'app.docs.components.icon.category.suggestion': '提示建议性图标',
  'app.docs.components.icon.category.editor': '编辑类图标',
  'app.docs.components.icon.category.data': '数据类图标',
  'app.docs.components.icon.category.other': '网站通用图标',
  'app.docs.components.icon.category.logo': '品牌和标识',
  'app.docs.components.icon.pic-searcher.intro': 'AI 截图搜索上线了，快来体验吧！🎉',
  'app.docs.components.icon.pic-searcher.title': '上传图片搜索图标',
  'app.docs.components.icon.pic-searcher.upload-text': '点击/拖拽/粘贴上传图片',
  'app.docs.components.icon.pic-searcher.upload-hint':
    '我们会通过上传的图片进行匹配，得到最相似的图标',
  'app.docs.components.icon.pic-searcher.server-error': '识别服务暂不可用',
  'app.docs.components.icon.pic-searcher.matching': '匹配中...',
  'app.docs.components.icon.pic-searcher.modelloading': '神经网络模型加载中...',
  'app.docs.components.icon.pic-searcher.result-tip': '为您匹配到以下图标：',
  'app.docs.components.icon.pic-searcher.th-icon': '图标',
  'app.docs.components.icon.pic-searcher.th-score': '匹配度',
  ...globalHeader,
  ...menu,
  ...settingDrawer,
  ...settings,
  ...pwa,
  ...component,
};
