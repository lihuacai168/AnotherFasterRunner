import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryCase(params) {
  return request('/api/xadmin/v1/case', {
    params,
  });
}
export async function removeCase(params) {
  return request(`/api/xadmin/v1/case/${params}`, {
    method: 'DELETE',
  });
}
export async function addCase(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/case', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateCase(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/case/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryCaseVerboseName(params) {
  return request('/api/xadmin/v1/case/verbose_name', {
    params,
  });
}
export async function queryCaseListDisplay(params) {
  return request('/api/xadmin/v1/case/list_display', {
    params,
  });
}
export async function queryCaseDisplayOrder(params) {
  return request('/api/xadmin/v1/case/display_order', {
    params,
  });
}


