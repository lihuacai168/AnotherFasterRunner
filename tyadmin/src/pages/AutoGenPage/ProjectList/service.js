import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryProject(params) {
  return request('/api/xadmin/v1/project', {
    params,
  });
}
export async function removeProject(params) {
  return request(`/api/xadmin/v1/project/${params}`, {
    method: 'DELETE',
  });
}
export async function addProject(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/project', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateProject(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/project/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryProjectVerboseName(params) {
  return request('/api/xadmin/v1/project/verbose_name', {
    params,
  });
}
export async function queryProjectListDisplay(params) {
  return request('/api/xadmin/v1/project/list_display', {
    params,
  });
}
export async function queryProjectDisplayOrder(params) {
  return request('/api/xadmin/v1/project/display_order', {
    params,
  });
}


