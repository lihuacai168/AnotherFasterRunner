import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryReport(params) {
  return request('/api/xadmin/v1/report', {
    params,
  });
}
export async function removeReport(params) {
  return request(`/api/xadmin/v1/report/${params}`, {
    method: 'DELETE',
  });
}
export async function addReport(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/report', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateReport(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/report/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryReportVerboseName(params) {
  return request('/api/xadmin/v1/report/verbose_name', {
    params,
  });
}
export async function queryReportListDisplay(params) {
  return request('/api/xadmin/v1/report/list_display', {
    params,
  });
}
export async function queryReportDisplayOrder(params) {
  return request('/api/xadmin/v1/report/display_order', {
    params,
  });
}


