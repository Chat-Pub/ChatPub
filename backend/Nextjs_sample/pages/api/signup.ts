import Cookies from "cookies";
import * as EmailValidator from 'email-validator';
import { clientPromise, queryPromise } from "../../lib/mysql";
const { createHash } = require("node:crypto");

export default async function handler(req, res) {
  if (req.method == "POST") {
    const username = req.body["username"];
    const password = req.body["password"];
    const passwordagain = req.body["passwordagain"];
    const emailVerification = req.body["emailVerification"];

    // email 검증하기 
    if (!EmailValidator.validate(username)){
      res.redirect("/signup?msg=The Email don't match the form");
      return;
    }; 

    // email 보내서 test하기
    // if (emailVerification != "true")




    if (password != passwordagain) {
      res.redirect("/signup?msg=The two passwords don't match");
      return;
    }

    await clientPromise.connect();

    try {
      let sql = `select * from users where username = "${username}"`;
      const results = await queryPromise(sql);
      if (results.length > 0) {
        res.redirect("/signup?msg=A user already has this username");
        return;
      }

      const password_hash = createHash("sha256").update(password).digest("hex");
      sql = `insert into users (username, password) values ("${username}", "${password_hash}")`;
      await queryPromise(sql);
    } catch (err) {
      console.error(err);
    }

    const cookies = new Cookies(req, res);
    cookies.set("username", username);
    res.redirect("/");
  } else {
    res.redirect("/");
  }
}
