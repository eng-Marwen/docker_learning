var express = require("express");
var path = require("path");
var bodyParser = require("body-parser");
var app = express();

app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);
app.use(bodyParser.json());

app.get("/", function (req, res) {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.post("/update-profile", function (req, res) {
  var userObj = req.body;
  // Just return what was sent
  res.send(userObj);
});

app.get("/", function (req, res) {
  // Always return default values
  res.send({
    name: "Marwen Boussabat",
    email: "marwen.smith@example.com",
    interests: "coding",
  });
});

app.listen(3000, function () {
  console.log("app listening on port 3000!");
});
