// apiListMixin.js
export default {
  methods: {
    getAPIList(params) {
      this.$nextTick(() => {
        const defaultParams = {
          page: this.listCurrentPage || 1, // 提供默认值
          node: this.currentNode || this.node, // 支持不同的命名
          project: this.project,
          search: this.search,
          tag: this.visibleTag || this.tag,
          rigEnv: this.rigEnv,
          onlyMe: this.onlyMe,
          showYAPI: this.showYAPI,
          creator: this.selectUser
        };

        // 使用传入的参数覆盖默认参数
        const apiParams = { ...defaultParams, ...params };

        this.$api.apiList({ params: apiParams }).then(res => {
          this.apiData = res;
        });
      });
    }
  }
};
