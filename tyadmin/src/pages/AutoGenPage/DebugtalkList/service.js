import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryDebugtalk(params) {
  return request('/api/xadmin/v1/debugtalk', {
    params,
  });
}
export async function removeDebugtalk(params) {
  return request(`/api/xadmin/v1/debugtalk/${params}`, {
    method: 'DELETE',
  });
}
export async function addDebugtalk(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/debugtalk', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateDebugtalk(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/debugtalk/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryDebugtalkVerboseName(params) {
  return request('/api/xadmin/v1/debugtalk/verbose_name', {
    params,
  });
}
export async function queryDebugtalkListDisplay(params) {
  return request('/api/xadmin/v1/debugtalk/list_display', {
    params,
  });
}
export async function queryDebugtalkDisplayOrder(params) {
  return request('/api/xadmin/v1/debugtalk/display_order', {
    params,
  });
}


