
// import { WechatyBuilder } from 'wechaty'

// const wechaty = WechatyBuilder.build() // get a Wechaty instance
// wechaty
//   .on('scan', (qrcode, status) => console.log(`Scan QR Code to login: ${status}\nhttps://wechaty.js.org/qrcode/${encodeURIComponent(qrcode)}`))
//   .on('login',            user => console.log(`User ${user} logged in`))
//   .on('message',       message => console.log(`Message: ${message}`))
// wechaty.start()




//  import 'dotenv/config.js'

//  import {
//   WechatyBuilder,
//   ScanStatus,
//   log,
// }                     from 'wechaty'
// import qrcodeTerminal from 'qrcode-terminal'

// function onScan (qrcode, status) {
//   if (status === ScanStatus.Waiting || status === ScanStatus.Timeout) {
//     qrcodeTerminal.generate(qrcode, { small: true })  // show qrcode on console

//     const qrcodeImageUrl = [
//       'https://wechaty.js.org/qrcode/',
//       encodeURIComponent(qrcode),
//     ].join('')

//     log.info('StarterBot', 'onScan: %s(%s) - %s', ScanStatus[status], status, qrcodeImageUrl)

//   } else {
//     log.info('StarterBot', 'onScan: %s(%s)', ScanStatus[status], status)
//   }
// }

// function onLogin (user) {
//   log.info('StarterBot', '%s login', user)
// }

// function onLogout (user) {
//   log.info('StarterBot', '%s logout', user)
// }

// async function onMessage (msg) {
//   log.info('StarterBot', msg.toString())

//   if (msg.text() === 'ding') {
//     await msg.say('dong')
//   }
// }

// const bot = WechatyBuilder.build({
//   name: 'ding-dong-bot',
//   /**
//    * How to set Wechaty Puppet Provider:
//    *
//    *  1. Specify a `puppet` option when instantiating Wechaty. (like `{ puppet: 'wechaty-puppet-padlocal' }`, see below)
//    *  1. Set the `WECHATY_PUPPET` environment variable to the puppet NPM module name. (like `wechaty-puppet-padlocal`)
//    *
//    * You can use the following providers:
//    *  - wechaty-puppet-wechat (no token required)
//    *  - wechaty-puppet-padlocal (token required)
//    *  - wechaty-puppet-service (token required, see: <https://wechaty.js.org/docs/puppet-services>)
//    *  - etc. see: <https://github.com/wechaty/wechaty-puppet/wiki/Directory>
//    */
//   // puppet: 'wechaty-puppet-wechat',
// })

// bot.on('scan',    onScan)
// bot.on('login',   onLogin)
// bot.on('logout',  onLogout)
// bot.on('message', onMessage)

// bot.start()
//   .then(() => log.info('StarterBot', 'Starter Bot Started.'))
//   .catch(e => log.error('StarterBot', e))




import qrTerm from 'qrcode-terminal'

import {
  IoClient,
  WechatyBuilder,
  config,
  log,
}             from 'wechaty'

console.log(`
=============== Powered by Wechaty ===============
-------- https://github.com/Chatie/wechaty --------
I'm the BUSY BOT, I can do auto response message for you when you are BUSY.
Send command to FileHelper to:
1. '#busy' - set busy mode ON
2. '#busy I'm busy' - set busy mode ON and set a Auto Reply Message
3. '#free' - set busy mode OFF
4. '#status' - check the current Busy Mode and Auto Reply Message.
Loading... please wait for QrCode Image Url and then scan to login.
`)

let bot

const token = config.token

if (token) {
  log.info('Wechaty', 'TOKEN: %s', token)

  bot = WechatyBuilder.build({ profile: token })
  const ioClient = new IoClient({
    token,
    wechaty: bot,
  })

  ioClient.start().catch(e => {
    log.error('Wechaty', 'IoClient.init() exception: %s', e)
    bot.emit('error', e)
  })
} else {
  log.verbose('Wechaty', 'TOKEN: N/A')
  bot = WechatyBuilder.build()
}

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
  const msg = `${user.name()} logined`

  log.info('Bot', msg)
  await this.say(msg)

})

/**
 * Global Event: message
 */

let busyIndicator    = false
let busyAnnouncement = `Automatic Reply: I cannot read your message because I'm busy now, will talk to you when I get back.`

bot.on('message', async function(msg) {
  log.info('Bot', '(message) %s', msg)

  const filehelper = bot.Contact.load('filehelper')

  const sender   = msg.talker()
  const receiver = msg.to()
  const text     = msg.text()
  const room     = msg.room()

  // if (msg.age() > 60) {
  //   log.info('Bot', 'on(message) skip age(%d) > 60 seconds: %s', msg.age(), msg)
  //   return
  // }

  if (!sender || !receiver) {
    return
  }

  if (receiver.id === 'filehelper') {
    console.log("enter filehelper")
    if (text === '#status') {
      await filehelper.say('in busy mode: ' + busyIndicator)
      await filehelper.say('auto reply: ' + busyAnnouncement)

    } else if (text === '#free') {
      busyIndicator = false
      await filehelper.say('auto reply stopped.')

    } else if (/^#busy/i.test(text)) {

      busyIndicator = true
      await filehelper.say('in busy mode: ' + 'ON')

      const matches = text.match(/^#busy (.+)$/i)
      if (!matches || !matches[1]) {
        await filehelper.say('auto reply message: "' + busyAnnouncement + '"')

      } else {
        busyAnnouncement = matches[1]
        await filehelper.say('set auto reply to: "' + busyAnnouncement + '"')

      }
    }

    return
  }

  if (sender.type() !== bot.Contact.Type.Personal) {
    console.log("enter not Personal")
    return
  }

  if (!busyIndicator) {
    console.log("enter free")
    return  // free
  }

  if (msg.self()) {
    console.log("enter self")
    return
  }

  /**
   * 1. Send busy anoncement to contact
   */
  if (!room) {
    console.log("enter not room")
    await msg.say(busyAnnouncement)
    return
  }

  /**
   * 2. If there's someone mentioned me in a room,
   *  then send busy annoncement to room and mention the contact who mentioned me.
   */
  const contactList = await msg.mention()
  const contactIdList = contactList.map(c => c.id)
  if (contactIdList.includes(this.userSelf().id)) {
    await msg.say(busyAnnouncement, sender)
  }
  console.log("enter nothing")

})

bot.start()
.catch(e => console.error(e))