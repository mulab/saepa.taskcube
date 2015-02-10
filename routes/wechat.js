/**
 * Created by hqythu on 2/4/2015.
 */
function wechat (req, res, next) {
  var message = req.weixin;
  res.reply('hello');
}

module.export = wechat;
