import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryUserToken(params) {
  return request('/api/xadmin/v1/user_token', {
    params,
  });
}
export async function removeUserToken(params) {
  return request(`/api/xadmin/v1/user_token/${params}`, {
    method: 'DELETE',
  });
}
export async function addUserToken(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/user_token', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateUserToken(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/user_token/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryUserTokenVerboseName(params) {
  return request('/api/xadmin/v1/user_token/verbose_name', {
    params,
  });
}
export async function queryUserTokenListDisplay(params) {
  return request('/api/xadmin/v1/user_token/list_display', {
    params,
  });
}
export async function queryUserTokenDisplayOrder(params) {
  return request('/api/xadmin/v1/user_token/display_order', {
    params,
  });
}

export async function updateUserPassword(params) {
    return request('/api/xadmin/v1/list_change_password', {
     method: 'POST',
     data: { ...params},
});
}

