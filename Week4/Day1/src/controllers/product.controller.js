const ProductService = require("../services/product.service");

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