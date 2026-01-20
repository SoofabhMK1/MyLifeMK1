// src/stores/navigation.ts

import { defineStore } from 'pinia'

// 🔥 TS特有：定义state的类型（就像给数据加标签）
interface NavigationState {
  currentRoute: string
  currentTitle: string
}

export const useNavigationStore = defineStore('navigation', {
  // 这里() => ({}) 是箭头函数返回对象
  state: (): NavigationState => ({
    currentRoute: '',
    currentTitle: '页面加载中...'
  }),
  
  actions: {
    // 🔥 TS特有：参数加类型注解 (routeName: string)
    updateRoute(routeName: string, routeTitle: string) {
      this.currentRoute = routeName
      this.currentTitle = routeTitle || '未命名页面'
    }
  },
  
  getters: {
    // 这两个getters会自动推断返回类型为boolean
    shouldShowHome: (state) => state.currentRoute !== 'Home',
    shouldShowSettings: (state) => state.currentRoute !== 'Settings',
    pageTitle: (state) => state.currentTitle
  }
})
