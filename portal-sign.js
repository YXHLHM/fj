// var t = {
//     "pageNo": 1,
//     "pageSize": 20,
//     "total": 0,
//     "AREACODE": "",
//     "M_PROJECT_TYPE": "",
//     "KIND": "GCJS",
//     "GGTYPE": "1",
//     "PROTYPE": "",
//     "timeType": "6",
//     "BeginTime": "2022-11-19 00:00:00",
//     "EndTime": "2023-05-19 23:59:59",
//     "createTime": [],
//     "ts": (new Date).getTime()
// }
var r = "3637CB36B2E54A72A7002978D0506CDF"

function d(t) { // 主函数
    for (var e in t)
        "" !== t[e] && void 0 !== t[e] || delete t[e];
    var n = r + l(t);
    // return s(n).toLocaleLowerCase()
    return md5(n)
}


function l(t) {
    for (var e = Object.keys(t).sort(u), n = "", a = 0; a < e.length; a++)
        if (void 0 !== t[e[a]])
            if (t[e[a]] && t[e[a]] instanceof Object || t[e[a]] instanceof Array) {
                var i = JSON.stringify(t[e[a]]);
                n += e[a] + i
            } else
                n += e[a] + t[e[a]];
    return n
}

function u(t, e) {
    return t.toString().toUpperCase() > e.toString().toUpperCase() ? 1 : t.toString().toUpperCase() == e.toString().toUpperCase() ? 0 : -1
}

const crypto = require("crypto");

function md5(res) {
    return crypto.createHash('md5').update(res).digest('hex')
}

// console.log(t)
// console.log(d(t))