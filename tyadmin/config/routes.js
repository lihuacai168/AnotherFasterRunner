[
    {
        name: 'Home',
        path: '/xadmin/index',
        icon: 'dashboard',
        component: './TyAdminBuiltIn/DashBoard'
    },
    {
        path: '/xadmin/',
        redirect: '/xadmin/index',
    },
    {
        name: '认证和授权',
        icon: 'BarsOutlined',
        path: '/xadmin/auth',
        routes:
        [
            {
                name: '权限',
                path: '/xadmin/auth/permission',
                component: './AutoGenPage/PermissionList',
            },
            {
                name: '组',
                path: '/xadmin/auth/group',
                component: './AutoGenPage/GroupList',
            }
        ]
    },
    {
        name: 'Fastrunner',
        icon: 'BarsOutlined',
        path: '/xadmin/fastrunner',
        routes:
        [
            {
                name: '项目信息',
                path: '/xadmin/fastrunner/project',
                component: './AutoGenPage/ProjectList',
            },
            {
                name: '驱动库',
                path: '/xadmin/fastrunner/debugtalk',
                component: './AutoGenPage/DebugtalkList',
            },
            {
                name: '环境信息',
                path: '/xadmin/fastrunner/config',
                component: './AutoGenPage/ConfigList',
            },
            {
                name: '接口信息',
                path: '/xadmin/fastrunner/a_p_i',
                component: './AutoGenPage/APIList',
            },
            {
                name: '用例信息',
                path: '/xadmin/fastrunner/case',
                component: './AutoGenPage/CaseList',
            },
            {
                name: '用例信息 Step',
                path: '/xadmin/fastrunner/case_step',
                component: './AutoGenPage/CaseStepList',
            },
            {
                name: 'HOST配置',
                path: '/xadmin/fastrunner/host_i_p',
                component: './AutoGenPage/HostIPList',
            },
            {
                name: '全局变量',
                path: '/xadmin/fastrunner/variables',
                component: './AutoGenPage/VariablesList',
            },
            {
                name: '测试报告',
                path: '/xadmin/fastrunner/report',
                component: './AutoGenPage/ReportList',
            },
            {
                name: '测试报告详情',
                path: '/xadmin/fastrunner/report_detail',
                component: './AutoGenPage/ReportDetailList',
            },
            {
                name: '树形结构关系',
                path: '/xadmin/fastrunner/relation',
                component: './AutoGenPage/RelationList',
            },
            {
                name: 'visit',
                path: '/xadmin/fastrunner/visit',
                component: './AutoGenPage/VisitList',
            }
        ]
    },
    {
        name: 'Fastuser',
        icon: 'BarsOutlined',
        path: '/xadmin/fastuser',
        routes:
        [
            {
                name: '用户信息',
                path: '/xadmin/fastuser/user_info',
                component: './AutoGenPage/UserInfoList',
            },
            {
                name: '用户登陆token',
                path: '/xadmin/fastuser/user_token',
                component: './AutoGenPage/UserTokenList',
            },
            {
                name: '用户',
                path: '/xadmin/fastuser/my_user',
                component: './AutoGenPage/MyUserList',
            }
        ]
    },
    {
        name: 'TyadminBuiltin',
        icon: 'VideoCamera',
        path: '/xadmin/sys',
        routes:
        [
            {
                name: 'TyAdminLog',
                icon: 'smile',
                path: '/xadmin/sys/ty_admin_sys_log',
                component: './TyAdminBuiltIn/TyAdminSysLogList'
            },
            {
                name: 'TyAdminVerify',
                icon: 'smile',
                path: '/xadmin/sys/ty_admin_email_verify_record',
                component: './TyAdminBuiltIn/TyAdminEmailVerifyRecordList'
            }
        ]
    },
    {
        name: 'passwordModify',
        path: '/xadmin/account/change_password',
        hideInMenu: true,
        icon: 'dashboard',
        component: './TyAdminBuiltIn/ChangePassword',
    },
    {
        component: './404',
    },
]
