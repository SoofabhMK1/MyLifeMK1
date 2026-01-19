<script setup lang="ts">
import { ref, reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()

const loginForm = reactive({
  username: '',
  password: ''
})

const isLoading = ref(false)

const handleLogin = async () => {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  isLoading.value = true
  
  const formData = new FormData()
  formData.append('username', loginForm.username)
  formData.append('password', loginForm.password)

  try {
    // const response = await axios.post('http://localhost:8000/token', formData)
    const response = await axios.post('/api/token', formData)
    const token = response.data.access_token
    const tokenType = response.data.token_type
    localStorage.setItem('token', `${tokenType} ${token}`)
    
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error: any) {
    ElMessage.error('登录失败，请检查账号密码')
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <div class="header">
        <h2 class="title">Admin System</h2>
        <p class="subtitle">后台管理系统登录</p>
      </div>

      <el-form :model="loginForm" size="large">
        <el-form-item>
          <el-input 
            v-model="loginForm.username" 
            placeholder="请输入用户名"
            :prefix-icon="User"
          />
        </el-form-item>

        <el-form-item>
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-button 
          type="primary" 
          class="login-btn" 
          :loading="isLoading"
          @click="handleLogin"
          round
        >
          立即登录
        </el-button>
      </el-form>
      
      <div class="footer">
        <span>&copy; 2024 Your Company</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 1. 确保外层容器铺满整个屏幕 */
.login-container {
  position: fixed; /* 强制固定定位，防止被其他父元素影响 */
  top: 0;
  left: 0;
  width: 100vw;  /* 视口宽度 100% */
  height: 100vh; /* 视口高度 100% */
  
  /* Flexbox 居中三件套 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  
  /* 背景色：淡蓝紫色渐变 */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
}

/* 2. 限制卡片宽度，确保在桌面上是小卡片，而不是拉伸满屏 */
.login-card {
  width: 420px; /* 固定宽度 */
  padding: 50px 40px;
  background: #ffffff;
  border-radius: 16px; /* 圆角更大一点 */
  
  /* 添加一个明显的阴影，增加立体感 */
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15); 
  text-align: center;
}

.title {
  font-size: 32px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.subtitle {
  color: #999;
  font-size: 14px;
  margin-bottom: 40px;
}

.login-btn {
  width: 100%;
  margin-top: 20px;
  font-size: 16px;
  padding: 22px 0; /* 让按钮更高一点，更现代 */
}

.footer {
  margin-top: 30px;
  font-size: 12px;
  color: #ccc;
}
</style>