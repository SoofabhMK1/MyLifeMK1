import { defineStore } from 'pinia'
import request from '../utils/request'
import { ElMessage } from 'element-plus'

// 1. 定义接口 (把 Home.vue 里的接口搬到这里，方便全局复用)
export interface Attribute {
  label: string;
  value: number;
  color: string;
}
export interface Skill {
  name: string;
  level: string;
  type: string;
}
export interface UserInfo {
  username: string;
  level: number;
  title: string;
  exp: number;
  avatarUrl: string;
  cash: number;
  attributes: Attribute[];
  skills: Skill[];
}

export const useUserStore = defineStore('user', {
  // 2. State: 相当于组件的 data
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: {
      username: 'Loading...',
      level: 0,
      title: '',
      exp: 0,
      avatarUrl: '',
      cash: 0,
      attributes: [],
      skills: []
    } as UserInfo
  }),

  // 3. Actions: 相当于组件的 methods
  actions: {
    // 登录动作
    async login(formData: FormData) {
      try {
        const response = await request.post('/token', formData)
        const tokenStr = `${response.data.token_type} ${response.data.access_token}`
        
        // 保存到状态和本地存储
        this.token = tokenStr
        localStorage.setItem('token', tokenStr)
        return true
      } catch (error) {
        return false
      }
    },

    // 获取用户信息动作
    async getUserInfo() {
      // 优化：如果 username 不是初始值，说明已经加载过了，直接返回，不再请求
      // (当然，如果你希望每次进主页都刷新数据，可以去掉这个判断)
      if (this.userInfo.username !== 'Loading...' && this.userInfo.level !== 0) {
        return
      }

      try {
        const res = await request.get('/users/me')
        this.userInfo = res.data
      } catch (error) {
        console.error('获取用户信息失败', error)
      }
    },

    // 登出动作
    logout() {
      this.token = ''
      this.userInfo = { // 重置为初始状态
        username: 'Loading...',
        level: 0,
        title: '',
        exp: 0,
        avatarUrl: '',
        cash: 0,
        attributes: [],
        skills: []
      }
      localStorage.removeItem('token')
      ElMessage.success('已安全退出')
    }
  }
})