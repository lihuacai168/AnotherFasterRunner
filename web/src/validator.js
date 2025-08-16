export const isNumArray = (rule, value, callback) => {
    if (value === ""){
        callback()
    }
    const numStr = /^[0-9,]*$/
    if (!numStr.test(value)) {
        callback(new Error('只能为整数和英文逗号, 且不能包含空格'))
        try {
            eval(value.split(","))
        } catch (err) {
            callback(new Error('字符串转换为整数列表错误: ' + err))
        }
    } else {
        callback()
    }
}

// Crontab表达式校验函数
export const validateCrontab = (rule, value, callback) => {
    if (!value || value.trim() === '') {
        callback(new Error('请输入crontab表达式'))
        return
    }

    const crontabValue = value.trim()
    
    // 分割为5个部分：分钟 小时 日 月 星期
    const parts = crontabValue.split(/\s+/)
    
    if (parts.length !== 5) {
        callback(new Error('crontab表达式必须包含5个字段：分钟 小时 日 月 星期'))
        return
    }

    // 定义各字段的有效范围
    const ranges = [
        { min: 0, max: 59, name: '分钟' },   // 分钟: 0-59
        { min: 0, max: 23, name: '小时' },   // 小时: 0-23
        { min: 1, max: 31, name: '日' },     // 日: 1-31
        { min: 1, max: 12, name: '月' },     // 月: 1-12
        { min: 0, max: 7, name: '星期' }     // 星期: 0-7 (0和7都表示周日)
    ]

    for (let i = 0; i < parts.length; i++) {
        const part = parts[i]
        const range = ranges[i]
        
        if (!validateCrontabField(part, range.min, range.max)) {
            callback(new Error(`${range.name}字段格式错误: ${part} (有效范围: ${range.min}-${range.max})`))
            return
        }
    }

    callback()
}

// 验证单个crontab字段
function validateCrontabField(field, min, max) {
    // 允许通配符 *
    if (field === '*') {
        return true
    }

    // 允许步长表达式，如 */5, 0-30/2
    if (field.includes('/')) {
        const [range, step] = field.split('/')
        if (!step || isNaN(step) || parseInt(step) <= 0) {
            return false
        }
        
        if (range === '*') {
            return true
        }
        
        // 验证范围部分
        if (!validateCrontabField(range, min, max)) {
            return false
        }
        
        return true
    }

    // 允许范围表达式，如 1-5
    if (field.includes('-')) {
        const [start, end] = field.split('-')
        if (isNaN(start) || isNaN(end)) {
            return false
        }
        
        const startNum = parseInt(start)
        const endNum = parseInt(end)
        
        return startNum >= min && startNum <= max && 
               endNum >= min && endNum <= max && 
               startNum <= endNum
    }

    // 允许列表表达式，如 1,3,5
    if (field.includes(',')) {
        const values = field.split(',')
        for (const value of values) {
            if (!validateCrontabField(value.trim(), min, max)) {
                return false
            }
        }
        return true
    }

    // 单个数字
    if (isNaN(field)) {
        return false
    }
    
    const num = parseInt(field)
    return num >= min && num <= max
}
