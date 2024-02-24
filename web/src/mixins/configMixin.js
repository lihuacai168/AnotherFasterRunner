// configMixin.js
export default {
  data() {
    return {
      configOptions: [],
      currentConfig: null
    };
  },
  methods: {
    getConfig({ addPlaceholder = false, setDefaultConfig = false } = {}) {
      this.$api.getAllConfig(this.$route.params.id).then(resp => {
        this.configOptions = resp;

        // 根据配置决定是否添加占位符，并设置默认选项
        if (addPlaceholder) {
          const placeHolderOption = { name: '请选择' };
          if (setDefaultConfig) {
            this.configOptions.unshift(placeHolderOption);
            const _config = this.configOptions.find(item => item.is_default === true);
            this.currentConfig = _config || placeHolderOption;
          } else {
            this.configOptions.push(placeHolderOption);
          }
        }
      });
    }
  }
};
