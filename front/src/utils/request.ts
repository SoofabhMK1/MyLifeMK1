import axios from 'axios'
import { ElMessage } from 'element-plus'
// import router from '../router'

// 1. 创建 axios 实例
const service = axios.create({
  // 这里的 '/api' 配合 vite.config.ts 的 proxy 转发
  baseURL: '/api', 
  timeout: 10000 // 请求超时时间：10秒
})

// 2. 请求拦截器 (Request Interceptor)
// 发送请求前自动执行：如果有 token，自动加到 header 里
service.interceptors.request.use(
  (config) => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('token')
    if (token) {
      // 如果有 token，加到请求头 Authorization 中
      config.headers.Authorization = token
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 3. 响应拦截器 (Response Interceptor)
// 收到响应后自动执行：统一处理错误（如 401 过期）
service.interceptors.response.use(
  (response) => {
    // 2xx 范围内的状态码都会触发该函数
    return response
  },
  (error) => {
    // 超出 2xx 范围的状态码都会触发该函数
    const { response } = error
    
    if (response) {
      switch (response.status) {
        case 401:
          ElMessage.error('登录状态已过期，请重新登录')
          localStorage.removeItem('token')
          
          // ✅ 修改这里：使用原生 BOM 对象跳转
          // 这不仅解决了循环依赖，还能强制刷新页面，清除所有内存状态，更安全
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('拒绝访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(response.data.detail || '网络连接异常')
      }
    } else {
      // 没收到响应（比如断网了）
      ElMessage.error('网络连接失败，请检查网络')
    }
    
    return Promise.reject(error)
  }
)

export default service