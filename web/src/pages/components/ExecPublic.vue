<template>
	<div>
		<publicTable
            :tableData="tableData"
            :columObj="columObj"
            :pageObj="pageObj"
            @switchChange="switchChange"
            @editInputBlur="editInputBlur"
            @rowClick="rowClick"
			@handleSizeChange="handleSizeChange"
            @handleCurrentChange="handleCurrentChange">
		</publicTable>
	</div>
</template>
<script>
    import PublicTable from './PublicTable.vue';
	export default {
        name: "ExecPublic",
		components: {PublicTable},
		data() {
			return {
				pageObj: { //分页对象
					position: "left", //分页组件位置
					total: 20,
					pageData: {
						page: 1,
						size: 10
					}
				},
				tableData: [{
					id: '1',
					date: '2016-05-02',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1518 弄',
					switchs: true,
					img: '',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '2',
					date: '2016-05-04',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1517 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '3',
					date: '2016-05-01',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1519 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '4',
					date: '2016-05-03',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1516 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				},{
					id: '1',
					date: '2016-05-02',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1518 弄',
					switchs: true,
					img: '',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '2',
					date: '2016-05-04',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1517 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '3',
					date: '2016-05-01',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1519 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '4',
					date: '2016-05-03',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1516 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				},{
					id: '1',
					date: '2016-05-02',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1518 弄',
					switchs: true,
					img: '',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '2',
					date: '2016-05-04',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1517 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '3',
					date: '2016-05-01',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1519 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '4',
					date: '2016-05-03',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1516 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				},{
					id: '1',
					date: '2016-05-02',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1518 弄',
					switchs: true,
					img: '',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '2',
					date: '2016-05-04',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1517 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '3',
					date: '2016-05-01',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1519 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}, {
					id: '4',
					date: '2016-05-03',
					name: '王小虎',
					address: '上海市普陀区金沙江路 1516 弄',
					switchs: true,
					img: 'file/964355654_58490652-91c5-412e-a74b-0c3d86ff1525.png',
					objmsg: {
						msg: '啊啊啊啊啊啊啊啊'
					}
				}],
				columObj: {
					// 选择框
					selection: true,
					// 选择框根据条件是否可选
					selectable: (row, index) => {
						if (row.switchs) {
							return true;
						}
					},
					lazy: "true",
					//column列,columType(列类型,可选text(默认为普通文字模式),input(input可编辑框),switch(switch开关),image(图片),operation(操作按钮))
					//prop(参数),label(列名),width(宽度),align(对齐方式),sortable(是否支持排序)
					columnData: [{
							text: true,
							prop: "date",
							label: "默认样式",
							width: "",
							align: "center",
						}, {
							text: true,
							prop: "id",
							label: "可以排序",
							width: "",
							align: "center",
							sortable: true, //开启排序

						},
						{
							status: true,
							prop: "objmsg",
							label: "obj类型（mesage）",
							width: "",
							align: "center",
							sortable: false,
						},
						{
							ownDefined: true,
							prop: "address",
							label: "自定义返回内容",
							width: "",
							align: "center",
							sortable: false,
							ownDefinedReturn: (row, $index) => {
								return row.address + '-' + row.id
							}
						},
						{
							switch: true,
							prop: "switchs",
							label: "switch开关",
							width: "",
							align: "center",
							openText: "打开",
							closeText: "关闭",
							sortable: false,
						},
						{
							image: true,
							prop: "img",
							label: "图片",
							width: "",
							align: "center",
							sortable: false,
						},
						{
							text: true,
							editRow: null,
							prop: "name",
							label: "点击可编辑",
							width: "",
							align: "center",
							sortable: false,
						},
						//如果为操作列,则需要填写需要的操作按钮,类型为Object。operation(操作类型,可选edit,delete,see),type(按钮样式,参考el—botton类型),label(按钮文字)icon(参考el-icon),color(字体颜色)
						{
							isOperation: true,
							label: "操作",
							width: "150",
							align: "center",
							sortable: false,
							fixed: "right",
							operation: [{
								type: "primary",
								label: "",
								circle: false,
								icon: "el-icon-edit-outline",
								color: '',
								buttonClick:this.rowOperation,
								isShow: (row, $index) => {
									return true;
								}
							}, {
								type: "danger",
								label: "删除",
								icon: "",
								color: 'black',
								buttonClick:this.rowOperation,
								isShow: (row, $index) => {
									return true;
								}
							}, {
								type: "info",
								label: "查看",
								icon: "",
								color: '',
								buttonClick:this.rowOperation,
								isShow: (row, $index) => {
									return true;
								}
							}]
						},

					],
				},
			}
		},
		beforeCreate() {},
		created: function() { //在模板渲染成html前调用
		},
		beforeMount() {

		},
		mounted() { //在模板渲染成html后调用
		},
		beforeUpdate() {

		},
		updated() {

		},
		methods: {
			rowOperation(row, $index) {
				console.log(row, $index)
			},
			switchChange(row, $index, prop) {
				console.log(row, $index, prop)
			},
			rowClick(row, column, event) {
				// 点击行触发，编辑点击的所在列，排除selection选择框
				if (column.type !== 'selection' && this.columObj.columnData[column.index].editRow === null) {
					this.columObj.columnData[column.index].editRow = row.rowIndex;
				}
			},
			editInputBlur(row, $index, prop, columIndex) {
				this.columObj.columnData[columIndex].editRow = null;
			},
			//页码变化
			handleCurrentChange(e) {
				this.pageObj.pageData.page = e;
			},
			//条数变化
			handleSizeChange(e) {
				this.pageObj.pageData.size = e;
				this.pageObj.pageData.page = 1;
			},
		},
		watch: { //监听
		},
		destroyed() { //销毁后
		}
	}
</script>
<style lang="scss">
</style>
<!-- ————————————————
版权声明：本文为CSDN博主「邹田聪」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_37346639/article/details/115556605 -->
