const express = require("express");
const mongoose = require("mongoose");

const app = express();

mongoose.connect(process.env.MONGO_URL || "mongodb://mongo:27017/testdb")
  .then(() => console.log("Mongo Connected"))
  .catch(err => console.log(err));

app.get("/", (req, res) => {
  res.send("Server Running");
});

app.listen(5000, () => {
  console.log("Server running on port 5000");
});