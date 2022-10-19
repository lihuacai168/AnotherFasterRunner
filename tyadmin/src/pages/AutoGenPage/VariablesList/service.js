import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryVariables(params) {
  return request('/api/xadmin/v1/variables', {
    params,
  });
}
export async function removeVariables(params) {
  return request(`/api/xadmin/v1/variables/${params}`, {
    method: 'DELETE',
  });
}
export async function addVariables(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/variables', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateVariables(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/variables/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryVariablesVerboseName(params) {
  return request('/api/xadmin/v1/variables/verbose_name', {
    params,
  });
}
export async function queryVariablesListDisplay(params) {
  return request('/api/xadmin/v1/variables/list_display', {
    params,
  });
}
export async function queryVariablesDisplayOrder(params) {
  return request('/api/xadmin/v1/variables/display_order', {
    params,
  });
}


