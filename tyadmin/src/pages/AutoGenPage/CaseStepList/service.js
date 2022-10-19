import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryCaseStep(params) {
  return request('/api/xadmin/v1/case_step', {
    params,
  });
}
export async function removeCaseStep(params) {
  return request(`/api/xadmin/v1/case_step/${params}`, {
    method: 'DELETE',
  });
}
export async function addCaseStep(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/case_step', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateCaseStep(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/case_step/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryCaseStepVerboseName(params) {
  return request('/api/xadmin/v1/case_step/verbose_name', {
    params,
  });
}
export async function queryCaseStepListDisplay(params) {
  return request('/api/xadmin/v1/case_step/list_display', {
    params,
  });
}
export async function queryCaseStepDisplayOrder(params) {
  return request('/api/xadmin/v1/case_step/display_order', {
    params,
  });
}


