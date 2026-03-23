const sanitizeHtml = require("sanitize-html");

function sanitizeInput(obj) {
  if (typeof obj === "string") {
    return sanitizeHtml(obj, {
      allowedTags: [],
      allowedAttributes: {},
    });
  }

  if (typeof obj === "object" && obj !== null) {
    for (let key in obj) {
      obj[key] = sanitizeInput(obj[key]);
    }
  }

  return obj;
}

module.exports = (req, res, next) => {
  req.body = sanitizeInput(req.body);
  req.query = sanitizeInput(req.query);
  req.params = sanitizeInput(req.params);
  next();
};