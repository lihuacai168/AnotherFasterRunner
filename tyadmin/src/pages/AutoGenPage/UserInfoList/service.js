import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryUserInfo(params) {
  return request('/api/xadmin/v1/user_info', {
    params,
  });
}
export async function removeUserInfo(params) {
  return request(`/api/xadmin/v1/user_info/${params}`, {
    method: 'DELETE',
  });
}
export async function addUserInfo(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/user_info', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateUserInfo(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/user_info/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryUserInfoVerboseName(params) {
  return request('/api/xadmin/v1/user_info/verbose_name', {
    params,
  });
}
export async function queryUserInfoListDisplay(params) {
  return request('/api/xadmin/v1/user_info/list_display', {
    params,
  });
}
export async function queryUserInfoDisplayOrder(params) {
  return request('/api/xadmin/v1/user_info/display_order', {
    params,
  });
}

export async function updateUserPassword(params) {
    return request('/api/xadmin/v1/list_change_password', {
     method: 'POST',
     data: { ...params},
});
}

