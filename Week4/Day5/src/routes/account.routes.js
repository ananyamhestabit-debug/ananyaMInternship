const express = require("express");
const router = express.Router();

const accountController = require("../controllers/account.controller");
const { validateAccount, validateLogin } = require("../middlewares/validate");

router.post("/", validateAccount, accountController.createAccount);
router.post("/login", validateLogin, accountController.login);
router.get("/", accountController.getAccounts);


module.exports = router;