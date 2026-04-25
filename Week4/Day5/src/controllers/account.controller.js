const AccountService = require("../services/account.service");

exports.createAccount = async (req, res, next) => {
  try {
    const account = await AccountService.register(req.body);

    const accountObj = account.toObject();
    delete accountObj.password;

    res.status(201).json({
      success: true,
      data: accountObj,
    });
  } catch (error) {
    next(error);
  }
};

exports.login = async (req, res, next) => {
  try {
    const { email, password } = req.body;

    const result = await AccountService.login(email, password);

    res.json({
      success: true,
      token: result.token,
    });
  } catch (error) {
    next(error);
  }
};

exports.getAccounts = async (req, res, next) => {
  try {
    const { page = 1, limit = 10 } = req.query;

    const accounts = await AccountService.getAccounts(page, limit);

    res.json({
      success: true,
      data: accounts,
    });
  } catch (error) {
    next(error);
  }
};