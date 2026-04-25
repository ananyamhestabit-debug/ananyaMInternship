const OrderService = require("../services/order.service");

exports.createOrder = async (req, res, next) => {
  try {
    const order = await OrderService.createOrder(req.body);

    res.status(201).json({
      success: true,
      order,
    });
  } catch (err) {
    next(err);
  }
};

exports.getOrder = async (req, res, next) => {
  try {
    const order = await OrderService.getOrder(req.params.id);

    res.json({
      success: true,
      order,
    });
  } catch (err) {
    next(err);
  }
};