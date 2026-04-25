const ProductRepository = require("../repositories/product.repository");
const AppError = require("../utils/AppError");

class ProductService {

  async createProduct(data) {
    return ProductRepository.create(data);
  }

  async listProducts(query) {
    const {
      search,
      minPrice,
      maxPrice,
      tags,
      sort,
      page = 1,
      limit = 10,
      includeDeleted,
    } = query;

    const filter = {};
    const shouldIncludeDeleted = includeDeleted === "true";

    if (!shouldIncludeDeleted) {
      filter.deletedAt = null;
    }

    if (search) {
      filter.$or = [
        { name: { $regex: search, $options: "i" } },
        { tags: { $regex: search, $options: "i" } },
      ];
    }

    if (minPrice || maxPrice) {
      filter.price = {};
      if (minPrice) filter.price.$gte = Number(minPrice);
      if (maxPrice) filter.price.$lte = Number(maxPrice);
    }

    if (tags) {
      filter.tags = { $in: tags.split(",") };
    }

    let sortOption = { createdAt: -1 };
    if (sort) {
      const [field, order] = sort.split(":");
      sortOption = { [field]: order === "desc" ? -1 : 1 };
    }

    const pageNumber = Number(page);
    const limitNumber = Number(limit);
    const skip = (pageNumber - 1) * limitNumber;

    const products = await ProductRepository.find(filter, {
      sort: sortOption,
      skip,
      limit: limitNumber,
    });

    const total = await ProductRepository.count(filter);

    return {
      total,
      page: pageNumber,
      products,
    };
  }

  async deleteProduct(id) {
    const product = await ProductRepository.findById(id);

    if (!product) {
      throw new AppError("Product not found", 404, "PRODUCT_NOT_FOUND");
    }

    return ProductRepository.softDelete(id);
  }
}

module.exports = new ProductService();