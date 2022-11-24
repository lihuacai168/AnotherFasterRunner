export const isNumArray = (rule, value, callback) => {
  if (value === "") {
    callback();
  }
  const numStr = /^[0-9,]*$/;
  if (!numStr.test(value)) {
    callback(new Error("只能为整数和英文逗号, 且不能包含空格"));
    try {
      eval(value.split(","));
    } catch (err) {
      callback(new Error("字符串转换为整数列表错误: " + err));
    }
  } else {
    callback();
  }
};
