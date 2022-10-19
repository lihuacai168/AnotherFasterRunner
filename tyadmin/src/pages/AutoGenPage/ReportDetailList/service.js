import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryReportDetail(params) {
  return request('/api/xadmin/v1/report_detail', {
    params,
  });
}
export async function removeReportDetail(params) {
  return request(`/api/xadmin/v1/report_detail/${params}`, {
    method: 'DELETE',
  });
}
export async function addReportDetail(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/report_detail', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateReportDetail(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/report_detail/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryReportDetailVerboseName(params) {
  return request('/api/xadmin/v1/report_detail/verbose_name', {
    params,
  });
}
export async function queryReportDetailListDisplay(params) {
  return request('/api/xadmin/v1/report_detail/list_display', {
    params,
  });
}
export async function queryReportDetailDisplayOrder(params) {
  return request('/api/xadmin/v1/report_detail/display_order', {
    params,
  });
}


