<template>
    <el-table
        highlight-current-row
        :cell-style="{paddingTop: '4px', paddingBottom: '4px'}"
        strpe
        :height="height"
        :data="tableData"
        style="width: 100%;"
        @cell-mouse-enter="cellMouseEnter"
        @cell-mouse-leave="cellMouseLeave"
    >
        <el-table-column
            label="测试之前执行的方法"
            width="500">
            <template v-slot="scope">
                <el-input clearable
                          v-model="scope.row.setup"
                          placeholder="${ setup_hooks function($request, *args, **kwargs) }"
                >
                </el-input>
            </template>
        </el-table-column>

        <el-table-column
            label="测试之后执行的方法"
            width="500">
            <template v-slot="scope">
                <el-input clearable
                          v-model="scope.row.teardown"
                          placeholder="${ teardown_hooks function(response, *args, **kwargs) }"
                >
                </el-input>
            </template>
        </el-table-column>

        <el-table-column>
            <template v-slot="scope">
                <el-row v-show="scope.row === currentRow">
                    <el-button
                        icon="el-icon-circle-plus-outline"
                        size="mini"
                        type="info"
                        @click="handleEdit(scope.$index, scope.row)">
                    </el-button>

                    <el-button
                        icon="el-icon-delete"
                        size="mini"
                        type="danger"
                        v-show="scope.$index !== 0"
                        @click="handleDelete(scope.$index, scope.row)">
                    </el-button>
                </el-row>

            </template>
        </el-table-column>
    </el-table>

</template>

<script>
export default {
  props: {
    save: Boolean,
    hooks: {
      require: false
    }
  },
  computed: {
    height() {
      return window.screen.height - 440
    }
  },
  watch: {
    save: function() {
      this.$emit('hooks', this.parse_hooks(), this.tableData)
    },

    hooks: function() {
      if (this.hooks.length !== 0) {
        this.tableData = this.hooks
      }
    }
  },

  methods: {
    cellMouseEnter(row) {
      this.currentRow = row
    },

    cellMouseLeave(row) {
      this.currentRow = ''
    },

    handleEdit(index, row, flag) {
      this.tableData.push({
        setup: '',
        teardown: ''
      })
    },

    handleDelete(index, row) {
      this.tableData.splice(index, 1)
    },

    parse_hooks() {
      const hooks = {
        setup_hooks: [],
        teardown_hooks: []
      }
      for (const content of this.tableData) {
        if (content.setup !== '') {
          hooks.setup_hooks.push(content.setup)
        }
        if (content.teardown !== '') {
          hooks.teardown_hooks.push(content.teardown)
        }
      }
      return hooks
    }
  },
  data() {
    return {
      currentRow: '',
      tableData: [{
        setup: '',
        teardown: ''
      }]
    }
  },
  name: 'Hooks'
}
</script>

<style scoped>
</style>
