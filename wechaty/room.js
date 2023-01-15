import {
  WechatyBuilder,
  log
}             from 'wechaty'
import qrTerm from 'qrcode-terminal'


// set alarm clock, 10 am at default
function getLeftTimeInMillis(hour=10, minute=0) {
  var now = new Date();
  var millisTill10 = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hour, minute, 0, 0) - now;
  if (millisTill10 < 0) {
       millisTill10 += 86400000; // it's after 10am, try 10am tomorrow.
  }
  // above time is for GMT, convert to los angeles
  millisTill10 += 8*60*60*1000
  millisTill10 = millisTill10 % 86400000
  // setTimeout(function(){alert("It's 10am!")}, millisTill10);
  return millisTill10
}

function speak(ID, bot, hour=7, minute=30, roomname='路迦信息群', content='醒了') {
  // '-39剑社-'
  let leftTime = getLeftTimeInMillis(hour, minute);
  setTimeout(async function(){
    if (roomname in ID) {
      const room = await bot.Room.find({id: ID[roomname]})
      console.log(room)

      // 1. Send text inside Room
      await room.say(content);
      console.log(`successfully speak ${content} to ${roomname}`);
    } else {
      console.log(`cannot find ${roomname} in ${ID}`);
    }
  }, leftTime)
  console.log(`The message [${content}] will be send to [${roomname}] after [${leftTime/1000/60/60} hours]`);
}


const bot = WechatyBuilder.build({
  name: 'auto-speak-bot'
});

bot
.on('scan', (qrcode, status) => {
  qrTerm.generate(qrcode, { small: true })
  const qrcodeImageUrl = [
    'https://wechaty.js.org/qrcode/',
    encodeURIComponent(qrcode),
  ].join('')

  console.log(`${status}: ${qrcode} - Scan QR Code of the url to login: ${qrcodeImageUrl}`)
})
.on('logout'  , user => log.info('Bot', `${user.name()} logouted`))
.on('error'   , e => log.info('Bot', 'error: %s', e))

.on('login', async function(user) {
  const logintime = new Date().toLocaleString("en-US", { timeZone: "America/Los_Angeles" });
  const msg = `${user.name()} logined at ${logintime}`

  log.info('Bot', msg)

  let ID = {};

  let timer = setInterval(async function(){
    const roomList = await bot.Room.findAll();
    let groups = roomList.map(({ payload }) => [payload['topic'], payload['id']])
    // console.log(groups);

    // ID of both rooms or friends will always change after each login
    for(let val of groups) {
        ID[val[0]] = val[1];
    }

    if ('路迦信息群' in ID) {
      console.log("Found 路迦信息群, stop finding rooms")
      clearInterval(timer);
    }
  }, 10000);

  speak(ID, bot, 7, 30, '路迦信息群', '醒了')
})
await bot.start()


// after logged in...

// const msg = await room.say('Hello world!') // only supported by puppet-padplus

// // 2. Send media file inside Room
// import { FileBox }  from 'wechaty'
// const fileBox1 = FileBox.fromUrl('https://wechaty.github.io/wechaty/images/bot-qr-code.png')
// const fileBox2 = FileBox.fromLocal('/tmp/text.txt')
// await room.say(fileBox1)
// const msg1 = await room.say(fileBox1) // only supported by puppet-padplus
// await room.say(fileBox2)
// const msg2 = await room.say(fileBox2) // only supported by puppet-padplus

// // 3. Send Contact Card in a room
// const contactCard = await bot.Contact.find({name: 'lijiarui'}) // change 'lijiarui' to any of the room member
// await room.say(contactCard)
// const msg = await room.say(contactCard) // only supported by puppet-padplus

// // 4. Send text inside room and mention @mention contact
// const contact = await bot.Contact.find({name: 'lijiarui'}) // change 'lijiarui' to any of the room member
// await room.say('Hello world!', contact)
// const msg = await room.say('Hello world!', contact) // only supported by puppet-padplus

// // 5. Send text inside room and mention someone with Tagged Template
// const contact2 = await bot.Contact.find({name: 'zixia'}) // change 'zixia' to any of the room member
// await room.say`Hello ${contact}, here is the world ${contact2}`
// const msg = await room.say`Hello ${contact}, here is the world ${contact2}` // only supported by puppet-padplus

// // 6. send url link in a room

// const urlLink = new UrlLink ({
//   description : 'WeChat Bot SDK for Individual Account, Powered by TypeScript, Docker, and Love',
//   thumbnailUrl: 'https://avatars0.githubusercontent.com/u/25162437?s=200&v=4',
//   title       : 'Welcome to Wechaty',
//   url         : 'https://github.com/wechaty/wechaty',
// })
// await room.say(urlLink)
// const msg = await room.say(urlLink) // only supported by puppet-padplus

// // 7. send mini program in a room

// const miniProgram = new MiniProgram ({
//   username           : 'gh_xxxxxxx',     //get from mp.weixin.qq.com
//   appid              : '',               //optional, get from mp.weixin.qq.com
//   title              : '',               //optional
//   pagepath           : '',               //optional
//   description        : '',               //optional
//   thumbnailurl       : '',               //optional
// })
// await room.say(miniProgram)
// const msg = await room.say(miniProgram) // only supported by puppet-padplus