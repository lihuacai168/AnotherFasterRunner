export const datetimeObj2str = function (time, format = 'YYYY-MM-DD hh:mm:ss') {
    let date = new Date(time);
    let year = date.getFullYear(),
        month = (date.getMonth() + 1).toString().padStart(2, '0'),
        day = date.getDate().toString().padStart(2, '0'),
        hour = date.getHours().toString().padStart(2, '0'),
        min = date.getMinutes().toString().padStart(2, '0'),
        sec = date.getSeconds().toString().padStart(2, '0');

    let newTime = format.replace(/YYYY/g, year)
        .replace(/MM/g, month)
        .replace(/DD/g, day)
        .replace(/hh/g, hour)
        .replace(/mm/g, min)
        .replace(/ss/g, sec);

    return newTime;
}

export const timestamp2time = function (timestamp) {
    if (!timestamp) {
        return ''
    }
    let date = new Date(timestamp * 1000);
    const Y = date.getFullYear() + '-';

    // js的月份从0开始
    const month = date.getMonth() + 1;
    const M = (month < 10 ? '0' + month : month) + '-';

    const days = date.getDate();
    const D = (days + 1 < 10 ? '0' + days : days) + ' ';

    const hours = date.getHours();
    const h = (hours + 1 < 10 ? '0' + hours : hours) + ':';

    const minutes = date.getMinutes();
    const m = (minutes + 1 < 10 ? '0' + minutes : minutes) + ':';

    const seconds = date.getSeconds();
    const s = seconds + 1 < 10 ? '0' + seconds : seconds;

    return Y + M + D + h + m + s;
}
