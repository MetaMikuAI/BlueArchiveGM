import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
// import Give from '../views/Give.vue'
import GiveAll from '../views/GiveAll.vue'
import Player from '../views/Player.vue'
import GameMail from '../views/GameMail.vue'
// import GetEmailCode from '../views/GetEmailCode.vue'
import IdList from '../views/IdList.vue'
import Character from '../views/Character.vue'
import About from '../views/About.vue'
import GameSetting from '../views/GameSetting.vue'
// import Command from '../views/Command.vue'
import ConfigMaker from '../views/ConfigMaker.vue'
import Mail from '../views/Mail.vue'
// import MailCode from '@/views/MailCode.vue'
import Account from '@/views/Account.vue'
import Command from '@/views/Command.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  // { path: '/give', name: 'Give', component: Give },
  { path: '/GiveAll', name: 'GiveAll', component: GiveAll },
  { path: '/Player', name: 'Player', component: Player },
  { path: '/GameMail', name: 'GameMail', component: GameMail },
  // { path: '/get-email-code', name: 'GetEmailCode', component: GetEmailCode },
  { path: '/IdList', name: 'IdList', component: IdList },
  { path: '/Character', name: 'Character', component: Character },
  { path: '/About', name: 'About', component: About },
  { path: '/Setting', name: 'GameSetting', component: GameSetting },
  // { path: '/command', name: 'Command', component: Command },
  { path: '/ConfigMaker', name: 'ConfigMaker', component: ConfigMaker },
  { path: '/Mail', name: 'Mail', component: Mail },
  // { path: '/MailCode', name: 'MailCode', component: MailCode },
  { path: '/Account', name: 'Account', component: Account },
  { path: '/Command', name: 'Command', component: Command },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
