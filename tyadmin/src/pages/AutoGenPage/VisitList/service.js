import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryVisit(params) {
  return request('/api/xadmin/v1/visit', {
    params,
  });
}
export async function removeVisit(params) {
  return request(`/api/xadmin/v1/visit/${params}`, {
    method: 'DELETE',
  });
}
export async function addVisit(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/visit', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateVisit(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/visit/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryVisitVerboseName(params) {
  return request('/api/xadmin/v1/visit/verbose_name', {
    params,
  });
}
export async function queryVisitListDisplay(params) {
  return request('/api/xadmin/v1/visit/list_display', {
    params,
  });
}
export async function queryVisitDisplayOrder(params) {
  return request('/api/xadmin/v1/visit/display_order', {
    params,
  });
}


