import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryConfig(params) {
  return request('/api/xadmin/v1/config', {
    params,
  });
}
export async function removeConfig(params) {
  return request(`/api/xadmin/v1/config/${params}`, {
    method: 'DELETE',
  });
}
export async function addConfig(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/config', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateConfig(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/config/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryConfigVerboseName(params) {
  return request('/api/xadmin/v1/config/verbose_name', {
    params,
  });
}
export async function queryConfigListDisplay(params) {
  return request('/api/xadmin/v1/config/list_display', {
    params,
  });
}
export async function queryConfigDisplayOrder(params) {
  return request('/api/xadmin/v1/config/display_order', {
    params,
  });
}


