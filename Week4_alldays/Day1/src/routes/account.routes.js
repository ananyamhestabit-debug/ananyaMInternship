const express = require("express");
const router = express.Router();

const accountController = require("../controllers/account.controller");
const { validateAccount } = require("../middlewares/validate");

router.post("/", validateAccount, accountController.createAccount);
router.post("/login", accountController.login);
router.get("/", accountController.getAccounts);


module.exports = router;