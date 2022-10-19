import request from 'umi-request';

import { buildFileFormData } from '@/utils/utils'
export async function queryMyUser(params) {
  return request('/api/xadmin/v1/my_user', {
    params,
  });
}
export async function removeMyUser(params) {
  return request(`/api/xadmin/v1/my_user/${params}`, {
    method: 'DELETE',
  });
}
export async function addMyUser(params) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request('/api/xadmin/v1/my_user', {
    method: 'POST',
    data: fileData,
  });
}
export async function updateMyUser(params, id) {
  let fileFieldList = []
  let fileData = buildFileFormData(params, fileFieldList);
  return request(`/api/xadmin/v1/my_user/${id}`, {
    method: 'PUT',
    data: fileData,
  });
}
export async function queryMyUserVerboseName(params) {
  return request('/api/xadmin/v1/my_user/verbose_name', {
    params,
  });
}
export async function queryMyUserListDisplay(params) {
  return request('/api/xadmin/v1/my_user/list_display', {
    params,
  });
}
export async function queryMyUserDisplayOrder(params) {
  return request('/api/xadmin/v1/my_user/display_order', {
    params,
  });
}

export async function updateUserPassword(params) {
    return request('/api/xadmin/v1/list_change_password', {
     method: 'POST',
     data: { ...params},
});
}

