const OrderRepository = require("../repositories/order.repository");
const AppError = require("../utils/AppError");

class OrderService {
  async createOrder(data) {
    return OrderRepository.create(data);
  }

  async getOrder(id) {
    const order = await OrderRepository.findById(id);

    if (!order) {
      throw new AppError("Order not found", 404);
    }

    return order;
  }

  async updateOrder(id, data) {
    return OrderRepository.update(id, data);
  }

  async deleteOrder(id) {
    return OrderRepository.delete(id);
  }
}

module.exports = new OrderService();