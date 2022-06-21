document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').addEventListener('submit', function() {
        alert('hello, ');
    });
});



// console.log("hello")
// const mariadb = require('mariadb');
// const pool = mariadb.createPool({
//      host: 'localhost', 
//      user:'frank', 
//      password: 'password',
//      database:'datalog',
//      connectionLimit: 5
// });

// async function asyncFunction() {
//   let conn;
//   try {
// 	conn = await pool.getConnection();
// 	const rows = await conn.query("SELECT * FROM thlog2 ORDER BY id DESC LIMIT 1");
// 	console.log(rows);

//   } catch (err) {
// 	throw err;
//   } finally {
// 	if (conn) return conn.end();
//   }
// }