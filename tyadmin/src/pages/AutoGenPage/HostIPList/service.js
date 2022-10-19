import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryHostIP(params) {
  return request('/api/xadmin/v1/host_i_p', {
    params,
  });
}
export async function removeHostIP(params) {
  return request(`/api/xadmin/v1/host_i_p/${params}`, {
    method: 'DELETE',
  });
}
export async function addHostIP(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/host_i_p', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateHostIP(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/host_i_p/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryHostIPVerboseName(params) {
  return request('/api/xadmin/v1/host_i_p/verbose_name', {
    params,
  });
}
export async function queryHostIPListDisplay(params) {
  return request('/api/xadmin/v1/host_i_p/list_display', {
    params,
  });
}
export async function queryHostIPDisplayOrder(params) {
  return request('/api/xadmin/v1/host_i_p/display_order', {
    params,
  });
}


