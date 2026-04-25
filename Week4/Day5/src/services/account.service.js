const Account = require("../models/Account");
const bcrypt = require("bcrypt");
const { generateToken } = require("../utils/jwt");
const AppError = require("../utils/AppError");

class AccountService {
  async register(data) {
    return Account.create(data);
  }

  async login(email, password) {
    if (!email || !password) {
      throw new AppError("Email and password required", 400);
    }

    const account = await Account.findOne({
      email: email.toLowerCase(),
    });

    if (!account) {
      throw new AppError("Invalid email or password", 401);
    }

    const isMatch = await bcrypt.compare(password, account.password);

    if (!isMatch) {
      throw new AppError("Invalid email or password", 401);
    }

    const token = generateToken({
      id: account._id,
      email: account.email,
    });

    return { token };
  }

  async getAccounts(page, limit) {
    const skip = (page - 1) * limit;

    return Account.find()
      .skip(skip)
      .limit(limit);
  }
}

module.exports = new AccountService();