const mysql = require("mysql2/promise");

const pool = mysql.createPool({
  host: "localhost",
  user: "root",
  password: process.env.DB_PASSWORD,
  database: "campuseats_graphql",
  waitForConnections: true,
  connectionLimit: 10
});

module.exports = pool;
