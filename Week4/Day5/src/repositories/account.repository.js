const Account = require("../models/Account");

class AccountRepository {
  async create(data) {
    return Account.create(data);
  }

  async findById(id) {
    return Account.findById(id);
  }

  async findByEmail(email) {
    return Account.findOne({ email });
  }

  async findPaginated(page = 1, limit = 10) {
    const skip = (page - 1) * limit;

    return Account.find()
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit);
  }

  async update(id, data) {
    return Account.findByIdAndUpdate(id, data, { new: true });
  }

  async delete(id) {
    return Account.findByIdAndDelete(id);
  }
}

module.exports = new AccountRepository();