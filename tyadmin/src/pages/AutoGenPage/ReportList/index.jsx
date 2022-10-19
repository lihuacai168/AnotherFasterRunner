import { DeleteOutlined, DownOutlined, EditOutlined, PlusOutlined, ExportOutlined } from '@ant-design/icons';
import { notification, Button, Col, Descriptions, Divider, Dropdown, Form, Input, Menu, message, Popconfirm, Popover, Row, Select, Tag, Transfer, Switch } from 'antd';
import React, { useEffect, useRef, useState } from 'react';
import KeyOutlined from '@ant-design/icons/lib/icons/KeyOutlined';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import ProTable from 'mtianyan-pro-table';
import CreateForm from './components/CreateForm';
import { addReport, queryReport, removeReport, updateReport, queryReportVerboseName, queryReportListDisplay, queryReportDisplayOrder} from './service';
import UpdateForm from './components/UpdateForm';
import UploadAvatar from '@/components/UploadAvatar';
import {queryProject, queryProjectVerboseName} from '@/pages/AutoGenPage/ProjectList/service';

import moment from 'moment';
const { Option } = Select;
import { BooleanFormItem, dealManyToManyFieldTags, fileUpload, twoColumns, richForm, richCol, dealPureSelectField, orderForm, exportExcelCurrent, exportExcelAll, getUpdateColumns, dealRemoveError, dealError, BooleanDisplay, dealDateTimeDisplay, dealManyToManyField, dealTime, deepCopy, fieldErrorHandle, getTableColumns, renderManyToMany, richTrans, dealForeignKeyField, renderForeignKey, fieldsLevelErrorHandle } from '@/utils/utils';
import 'braft-editor/dist/index.css'
const FormItem = Form.Item;
const TableList = () => {
  const [createModalVisible, handleModalVisible] = useState(false);
  const [updateModalVisible, handleUpdateModalVisible] = useState(false);
 
  const [updateFormValues, setUpdateFormValues] = useState({});
  const actionRef = useRef();
  const addFormRef = useRef();
  const updateFormRef = useRef();

  const handleAdd = async fields => {
    const hide = message.loading('正在添加');

    try {
      await addReport({ ...fields });
      hide();
      message.success('添加成功');
      return true;
    } catch (error) {
      return dealError(error, addFormRef, hide, "添加");
    }
  };

  const handleUpdate = async (value, current_id) => {
    const hide = message.loading('正在修改');

    try {
      await updateReport(value, current_id);
      hide();
      message.success('修改成功');
      return true;
    } catch (error) {
      return dealError(error, updateFormRef, hide, "修改");
    }
  };

  const handleRemove = async selectedRows => {
    const hide = message.loading('正在删除');
    if (!selectedRows) return true;

    try {
      const ids = selectedRows.map(row => row.id).join(',');
      await removeReport(ids);
      hide();
      message.success('删除成功');
      return true;
    } catch (error) {
      hide()
      return dealRemoveError(error, "删除");
    }
  };
 
  const dateFieldList = ["create_time","update_time"]
  const base_columns = [{
                             title: 'id',
                             
        hideInForm: true,
        hideInSearch: true,
        
                             
                             dataIndex: 'id',
                             valueType: 'digit',
                             rules: [
                                     
                             ],
                             
                             
                        },
                      {
                             title: '创建时间',
                             
                             
                             dataIndex: 'create_time',
                             valueType: 'dateTime',
                             rules: [
                                     
                             ],
                             
                             
                        },
                      {
                             title: '更新时间',
                             
            hideInForm: true,
            
                             
                             dataIndex: 'update_time',
                             valueType: 'dateTime',
                             rules: [
                                     
                             ],
                             
                             
                        },
                      {
                             title: '创建人',
                             
                             
                             dataIndex: 'creator',
                             
                             rules: [
                                     {
                      required: true,
                      message: '创建人为必填项',
                     },
                             ],
                             
                             
                        },
                      {
                             title: '更新人',
                             
                             
                             dataIndex: 'updater',
                             
                             rules: [
                                     {
                      required: true,
                      message: '更新人为必填项',
                     },
                             ],
                             
                             
                        },
                      {
                             title: '报告名称',
                             
                             
                             dataIndex: 'name',
                             
                             rules: [
                                     {
                      required: true,
                      message: '报告名称为必填项',
                     },
                             ],
                             
                             
                        },
                      {
                             title: '报告类型',
                             
                             
                             dataIndex: 'type',
                             
                             rules: [
                                     {
                      required: true,
                      message: '报告类型为必填项',
                     },
                             ],
                             
                             valueEnum:{"1":"调试","2":"异步","3":"定时","4":"部署"}
                        },
                      {
                             title: '报告状态',
                             
                             
                             dataIndex: 'status',
                             
                             rules: [
                                     
                             ],
                             
                                     render: (text, record) => {
                                  return BooleanDisplay(text);
                                },
                        renderFormItem: (item, {value, onChange}) => {
                          return BooleanFormItem(value, onChange);
                        },
        
                             valueEnum:{"0":"失败","1":"成功"}
                        },
                      {
                             title: '报告基础信息',
                             
                             
                             dataIndex: 'summary',
                             valueType: 'textarea',
                             rules: [
                                     {
                      required: true,
                      message: '报告基础信息为必填项',
                     },
                             ],
                             
                             
                        },
                      {
                             title: 'project',
                             
                             
                             dataIndex: 'project',
                             
                             rules: [
                                     {
                      required: true,
                      message: 'project为必填项',
                     },
                             ],
                             
                        renderFormItem: (item, {value, onChange}) => {
                                          return dealForeignKeyField(item, value, onChange, projectForeignKeyList);
                                  },
                        render: (text, record) => {
                              return renderForeignKey(text, projectVerboseNameMap);
                            },
                             
                        },
                      {
                             title: 'ci_metadata',
                             
                             initialValue: "<class 'dict'>",
                             dataIndex: 'ci_metadata',
                             
                             rules: [
                                     
                             ],
                             
                             
                        },
                      {
                             title: 'gitlab的项目id',
                             
                             initialValue: 0,
                             dataIndex: 'ci_project_id',
                             valueType: 'digit',
                             rules: [
                                     
                             ],
                             
                             
                        },
                      {
                             title: 'gitlab的项目id',
                             
                             
                             dataIndex: 'ci_job_id',
                             
                             rules: [
                                     
                             ],
                             
                             
                        },
                          {
                              title: '操作',
                              dataIndex: 'option',
                              valueType: 'option',
                                    fixed: 'right',
          width: 100,
                              render: (text, record) => (
                                <>

                                  <EditOutlined title="编辑" className="icon" onClick={async () => {
                                   record.create_time = record.create_time === null ? record.create_time : moment(record.create_time);record.update_time = record.update_time === null ? record.update_time : moment(record.update_time);
                                    handleUpdateModalVisible(true);
                                    setUpdateFormValues(record);
                                  }} />
                                  <Divider type="vertical" />
                                  <Popconfirm
                                    title="您确定要删除测试报告吗？"
                                    placement="topRight"
                                    onConfirm={() => {
                                      handleRemove([record])
                                      actionRef.current.reloadAndRest();
                                    }}
                                    okText="确定"
                                    cancelText="取消"
                                  >
                                    <DeleteOutlined title="删除" className="icon" />
                                  </Popconfirm>
                                </>
                              ),
                            },];

  let cp = deepCopy(base_columns);

  const [formOrder, setFormOrder] = useState([]);

  useEffect(() => {
    queryReportDisplayOrder().then(r => {
      setFormOrder(r.form_order)
    })
  }, [])
  const table_columns = getTableColumns(cp);

  let order_cp = deepCopy(base_columns);
  const form_ordered = orderForm(formOrder, order_cp);

  const create_columns = [...form_ordered];
  const update_cp = deepCopy(form_ordered)
  const update_columns = getUpdateColumns(update_cp);

  const [columnsStateMap, setColumnsStateMap] = useState({});

  const [paramState, setParamState] = useState({});

  useEffect(() => {
    queryReportListDisplay().then(value => {
      setColumnsStateMap(value)
    })
  }, [])


   
                                const [projectForeignKeyList, setProjectForeignKeyList] = useState([]);
                                useEffect(() => {
                                queryProject({all: 1}).then(value => {
                                     setProjectForeignKeyList(value);
                                });
                                }, []);
                                const [projectVerboseNameMap, setProjectVerboseNameMap] = useState([]);
                                useEffect(() => {
                                queryProjectVerboseName().then(value => {
                                    setProjectVerboseNameMap(value);
                                });
                                }, []);

   
  return (
    <PageHeaderWrapper>
      <ProTable
        beforeSearchSubmit={(params => {
          dealTime(params, dateFieldList);
          return params;
        })}
        params={paramState}
        scroll={{ x: '100%' }}
        columnsStateMap={columnsStateMap}
        onColumnsStateChange={(map) => setColumnsStateMap(map)}
        headerTitle="测试报告表格"
        actionRef={actionRef}
        rowKey="id"
        toolBarRender={(action, { selectedRows }) => [
          <Button type="primary" onClick={() => handleModalVisible(true)}>
            <PlusOutlined /> 新建
          </Button>,
          <Button type="primary" onClick={() => exportExcelAll(paramState, queryReport, table_columns, '测试报告-All')}>
            <ExportOutlined /> 导出全部
          </Button>,
          <Input.Search style={{ marginRight: 20 }} placeholder="搜索测试报告" onSearch={value => {
            setParamState({
              search: value,
            });
            actionRef.current.reload();
          }} />,
          selectedRows && selectedRows.length > 0 && (
            <Dropdown
              overlay={
                <Menu
                  onClick={async e => {
                    if (e.key === 'remove') {
                      await handleRemove(selectedRows);
                      actionRef.current.reloadAndRest();
                    }
                    else if (e.key === 'export_current') {
                      exportExcelCurrent(selectedRows, table_columns, '测试报告-select')
                    }
                  }}
                  selectedKeys={[]}
                >
                  <Menu.Item key="remove">批量删除</Menu.Item>
                  <Menu.Item key="export_current">导出已选</Menu.Item>
                </Menu>
              }
            >
              <Button>
                批量操作 <DownOutlined />
              </Button>
            </Dropdown>
          ),
        ]}
        tableAlertRender={({ selectedRowKeys, selectedRows }) => (
          selectedRowKeys.length > 0 ? <div>
            已选择{' '}
            <a
              style={{
                fontWeight: 600,
              }}
            >
              {selectedRowKeys.length}
            </a>{' '}
            项&nbsp;&nbsp;
          </div> : false

        )}
        request={(params, sorter, filter) => queryReport({ ...params, sorter, filter })}
        columns={table_columns}
        rowSelection={{}}
      />
      <CreateForm onCancel={() => handleModalVisible(false)} modalVisible={createModalVisible}>
        <ProTable
          formRef={addFormRef}
          onSubmit={async value => {
            richTrans(value);
            const success = await handleAdd(value);

            if (success) {
              handleModalVisible(false);

              if (actionRef.current) {
                actionRef.current.reload();
              }
            }
          }}
          rowKey="key"
          type="form"
          search={twoColumns}
          form={
            {
              labelCol: { span: 6 },
              labelAlign: 'left',
            }}
          columns={create_columns}
          rowSelection={{}}
        />
      </CreateForm>
      <UpdateForm onCancel={() => handleUpdateModalVisible(false)} modalVisible={updateModalVisible}>
        <ProTable
          formRef={updateFormRef}
          onSubmit={async value => {
            richTrans(value);
            const success = await handleUpdate(value, updateFormValues.id);

            if (success) {
              handleUpdateModalVisible(false);

              if (actionRef.current) {
                actionRef.current.reload();
              }
            }
          }}
          rowKey="key"
          search={twoColumns}
          type="form"
          form={{
            initialValues: updateFormValues, labelCol: { span: 6 },
            labelAlign: 'left',
          }}
          columns={update_columns}
          rowSelection={{}}
        />
      </UpdateForm>
       
    </PageHeaderWrapper>
  );
};

export default TableList;
