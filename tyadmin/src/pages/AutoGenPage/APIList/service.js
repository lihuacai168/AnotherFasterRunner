import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryAPI(params) {
  return request('/api/xadmin/v1/a_p_i', {
    params,
  });
}
export async function removeAPI(params) {
  return request(`/api/xadmin/v1/a_p_i/${params}`, {
    method: 'DELETE',
  });
}
export async function addAPI(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/a_p_i', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateAPI(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/a_p_i/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryAPIVerboseName(params) {
  return request('/api/xadmin/v1/a_p_i/verbose_name', {
    params,
  });
}
export async function queryAPIListDisplay(params) {
  return request('/api/xadmin/v1/a_p_i/list_display', {
    params,
  });
}
export async function queryAPIDisplayOrder(params) {
  return request('/api/xadmin/v1/a_p_i/display_order', {
    params,
  });
}


