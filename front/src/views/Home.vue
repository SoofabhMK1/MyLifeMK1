<!-- frontend/src/views/Home.vue -->
<template>
  <div style="padding: 50px; text-align: center;">
    <h1>🎉 登录成功！这里是主页</h1>
    <el-button type="danger" @click="logout">退出登录</el-button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('token')
  ElMessage.success('已退出')
  router.push('/login')
}
</script>