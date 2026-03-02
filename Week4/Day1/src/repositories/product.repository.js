const Product = require("../models/Product");

class ProductRepository {

  async create(data) {
    return await Product.create(data);
  }

  async find(filter, options) {
    return await Product.find(filter)
      .sort(options.sort)
      .skip(options.skip)
      .limit(options.limit);
  }

  async count(filter) {
    return await Product.countDocuments(filter);
  }

  async findById(id) {
    return await Product.findById(id);
  }

  async softDelete(id) {
    return await Product.findByIdAndUpdate(
      id,
      { deletedAt: new Date() },
      { new: true }
    );
  }
}

module.exports = new ProductRepository();