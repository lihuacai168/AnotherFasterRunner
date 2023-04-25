export const datetimeObj2str = function(time, format = 'YY-MM-DD hh:mm:ss') {
  const date = new Date(time)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const min = date.getMinutes()
  const sec = date.getSeconds()
  const preArr = Array.apply(null, Array(10)).map(function(elem, index) {
    return '0' + index
  })

  const newTime = format.replace(/YY/g, year)
    .replace(/MM/g, preArr[month] || month)
    .replace(/DD/g, preArr[day] || day)
    .replace(/hh/g, preArr[hour] || hour)
    .replace(/mm/g, preArr[min] || min)
    .replace(/ss/g, preArr[sec] || sec)

  return newTime
}

export const timestamp2time = function(timestamp) {
  if (!timestamp) {
    return ''
  }
  const date = new Date(timestamp * 1000)
  const Y = date.getFullYear() + '-'

  // js的月份从0开始
  const month = date.getMonth() + 1
  const M = (month < 10 ? '0' + month : month) + '-'

  const days = date.getDate()
  const D = (days + 1 < 10 ? '0' + days : days) + ' '

  const hours = date.getHours()
  const h = (hours + 1 < 10 ? '0' + hours : hours) + ':'

  const minutes = date.getMinutes()
  const m = (minutes + 1 < 10 ? '0' + minutes : minutes) + ':'

  const seconds = date.getSeconds()
  const s = seconds + 1 < 10 ? '0' + seconds : seconds

  return Y + M + D + h + m + s
}
