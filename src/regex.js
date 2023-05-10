var target = process.argv[2]
var rexp = process.argv[3]
var re = new RegExp(rexp);
var result_bool = re.test(target);
result_int = Number(result_bool);
console.log(result_int);