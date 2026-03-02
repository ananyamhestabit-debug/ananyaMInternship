const ProductService = require("../services/product.service");
const { sendEmailJob } = require("../jobs/email.job");

exports.createProduct = async (req, res, next) => {
  try {
    const product = await ProductService.createProduct(req.body);

    await sendEmailJob({
      email: "admin@example.com",
      product: product.name,
    });

    res.status(201).json({
      success: true,
      product,
    });
  } catch (error) {
    next(error);
  }
};

exports.getProducts = async (req, res, next) => {
  try {
    const data = await ProductService.listProducts(req.query);
    res.json({ success: true, data });
  } catch (error) {
    next(error);
  }
};

exports.deleteProduct = async (req, res, next) => {
  try {
    const product = await ProductService.deleteProduct(req.params.id);
    res.json({ success: true, product });
  } catch (error) {
    next(error);
  }
};