import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryRelation(params) {
  return request('/api/xadmin/v1/relation', {
    params,
  });
}
export async function removeRelation(params) {
  return request(`/api/xadmin/v1/relation/${params}`, {
    method: 'DELETE',
  });
}
export async function addRelation(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/relation', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateRelation(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/relation/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryRelationVerboseName(params) {
  return request('/api/xadmin/v1/relation/verbose_name', {
    params,
  });
}
export async function queryRelationListDisplay(params) {
  return request('/api/xadmin/v1/relation/list_display', {
    params,
  });
}
export async function queryRelationDisplayOrder(params) {
  return request('/api/xadmin/v1/relation/display_order', {
    params,
  });
}


