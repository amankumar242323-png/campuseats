const { ApolloServer } = require("@apollo/server");
const { expressMiddleware } = require("@as-integrations/express5");
const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const db = require("./db");

const typeDefs = fs.readFileSync(
  path.join(__dirname, "schema.graphql"),
  "utf8"
);

const resolvers = {
  Query: {
    dishes: async () => {
      const [rows] = await db.execute(
        "SELECT id, name, price, available FROM dishes ORDER BY id"
      );
      return rows.map(row => ({
        ...row,
        price: Number(row.price),
        available: Boolean(row.available)
      }));
    },
    dish: async (_, { id }) => {
      const [rows] = await db.execute(
        "SELECT id, name, price, available FROM dishes WHERE id = ?",
        [id]
      );
      if (!rows.length) return null;
      return {
        ...rows[0],
        price: Number(rows[0].price),
        available: Boolean(rows[0].available)
      };
    }
  },
  Mutation: {
    addDish: async (_, { input }) => {
      const name = input.name.trim();
      if (!name || !Number.isFinite(input.price) || input.price <= 0) {
        throw new Error("Dish name and a positive price are required.");
      }
      const [result] = await db.execute(
        "INSERT INTO dishes (name, price, available) VALUES (?, ?, TRUE)",
        [name, input.price]
      );
      const [rows] = await db.execute(
        "SELECT id, name, price, available FROM dishes WHERE id = ?",
        [result.insertId]
      );
      return {
        ...rows[0],
        price: Number(rows[0].price),
        available: Boolean(rows[0].available)
      };
    }
  }
};

async function start() {
  const app = express();
  const server = new ApolloServer({ typeDefs, resolvers });
  await server.start();

  app.use(cors());
  app.use(express.json());
  app.use("/graphql", expressMiddleware(server));
  app.use(express.static(path.join(__dirname, "public")));

  app.listen(4000, () => {
    console.log("CampusEats page: http://localhost:4000/");
    console.log("GraphQL endpoint: http://localhost:4000/graphql");
  });
}

start().catch(error => {
  console.error("Server startup failed:", error.message);
  process.exit(1);
});
