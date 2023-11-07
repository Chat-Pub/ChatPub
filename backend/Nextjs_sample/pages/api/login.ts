import Cookies from "cookies";
import { clientPromise, queryPromise } from "../../lib/mysql";
const { createHash } = require("node:crypto");

export default async function handler(req, res) {
  if (req.method == "POST") {
    const username = req.body["username"];
    const guess = req.body["password"];

    await clientPromise.connect();

    let sql = `select * from users where username = "${username}"`;
    try {
      const result = await queryPromise(sql);
      if (result.length == 0) {
        res.redirect("/login?msg=Incorrect username or password");
        return;
      }

      let user = result[0];

      const guess_hash = createHash("sha256").update(guess).digest("hex");

      if (guess_hash == user.password) {
        const cookies = new Cookies(req, res);
        cookies.set("username", username);
        res.redirect("/");
      } else {
        res.redirect("/login?msg=Incorrect username or password");
      }
    } catch (err) {
      console.error(err);
    }
  } else {
    res.redirect("/");
  }
}
