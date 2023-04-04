const setLocalValue = function (name, value) {
  if (window.localStorage) {
    localStorage.setItem(name, value);
  } else {
    alert("This browser does NOT support localStorage");
  }
};

const getLocalValue = function (name) {
  const value = localStorage.getItem(name);
  if (value) {
    // localStorage只能存字符串，布尔类型需要转换
    if (value === "false" || value === "true") {
      return eval(value);
    }
    return value;
  } else {
    return "";
  }
};

const getViewportSize = function () {
  return {
    width: window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth,
    height: window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight,
  };
};

const getCookieValue = function (name) {
  var arr,
    reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
  if ((arr = document.cookie.match(reg))) return unescape(arr[2]);
  else return null;
};

const setCookieValue = function (name, value) {
  var Days = 30;
  var exp = new Date();
  exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
  document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
};

export default {
  install(Vue, options) {
    Vue.prototype.getLocalValue = getLocalValue;
    Vue.prototype.getViewportSize = getViewportSize;
    Vue.prototype.setLocalValue = setLocalValue;
    Vue.prototype.getCookieValue = getCookieValue;
    Vue.prototype.setCookieValue = setCookieValue;
  },
};
