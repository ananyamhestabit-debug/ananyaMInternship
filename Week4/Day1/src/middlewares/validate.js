const Joi = require("joi");

exports.validateProduct = (req, res, next) => {
  const schema = Joi.object({
    name: Joi.string().trim().min(3).required(),
    price: Joi.number().min(0).required(),
    tags: Joi.array().items(Joi.string()).optional(),
  }).options({ stripUnknown: true });

  const { error, value } = schema.validate(req.body);

  if (error) {
    return res.status(400).json({
      success: false,
      message: error.details[0].message,
      code: "VALIDATION_ERROR",
      timestamp: new Date().toISOString(),
      path: req.originalUrl,
    });
  }

  req.body = value;
  next();
};