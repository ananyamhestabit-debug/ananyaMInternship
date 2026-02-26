const Product = require("../models/Product");

class ProductRepository {
  async find(filter, options) {
    return Product.find(filter)
      .sort(options.sort)
      .skip(options.skip)
      .limit(options.limit);
  }

  async count(filter) {
    return Product.countDocuments(filter);
  }

  async findById(id) {
    return Product.findById(id);
  }

  async softDelete(id) {
    return Product.findByIdAndUpdate(
      id,
      { deletedAt: new Date() },
      { new: true }
    );
  }
}

module.exports = new ProductRepository();