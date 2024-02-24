// treeMixin.js
export default {
  methods: {
    getTree(callback) {
      this.$api.getTree(this.$route.params.id, { params: { type: 1 } }).then(resp => {
        this.dataTree = resp['tree'];

        // 如果有提供回调函数，则调用它
        if (callback && typeof callback === 'function') {
          callback(resp);
        }
      });
    }
  }
};
