import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../components/LoginView.vue'
import Settings from '../views/Settings.vue'
import { useNavigationStore } from '@/stores/navigation'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: { 
        requiresAuth: true,
        title: '意识投影主页'
      }
    },
    { 
    path: '/settings', 
    name: 'Settings', 
    component: Settings,
    meta: { 
      requiresAuth: true,
      title: '系统控制台'
    }
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  const navigationStore = useNavigationStore()
  if (typeof to.name === 'string') {
    const pageTitle = (to.meta?.title as string) || to.name
    navigationStore.updateRoute(to.name, pageTitle)
  }
  
  if (to.meta.requiresAuth && !token) {
    // 如果去主页但没token，跳转到登录
    next('/login')
  } else {
    next()
  }
})

export default router
