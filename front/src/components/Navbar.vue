<!-- frontend/src/components/Navbar.vue -->
<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { useNavigationStore } from '@/stores/navigation'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  SwitchButton, 
  Setting, 
  Monitor, 
  Bell,
  HomeFilled
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const navigationStore = useNavigationStore()

const goHome = () => {
  router.push('/')
}
// 处理设置点击
const handleSettings = () => {
  router.push('/settings')
}

// 处理退出登录
const handleLogout = () => {
  // 增加一个确认弹窗，更有“系统操作”的感觉
  ElMessageBox.confirm(
    '确定要断开与系统的连接吗？',
    '系统警告',
    {
      confirmButtonText: '确认断开',
      cancelButtonText: '保持连接',
      type: 'warning',
    }
  ).then(() => {
    userStore.logout()
    router.push('/login')
  }).catch(() => {
    // 取消操作，不做处理
  })
}
</script>

<template>
  <div class="navbar-container">
    <!-- 左侧：Logo 和系统名称 -->
    <div class="nav-left" @click="goHome">
      <div class="logo-box">
        <el-icon :size="22" class="logo-icon"><Monitor /></el-icon>
      </div>
      <div class="titles">
        <span class="main-title">ADMIN SYSTEM</span>
        <span class="sub-title">Ver 1.0.0</span>
      </div>
    </div>
    <!-- 中间：页面名称 -->
    <div class="nav-center">
      <span class="page-name">{{ navigationStore.currentTitle }}</span>
    </div>
    <!-- 右侧：功能按钮区 -->
    <div class="nav-right">

      <el-tooltip v-if="navigationStore.shouldShowHome" content="系统主页" placement="bottom">
        <div class="icon-btn" @click="goHome">
          <el-icon :size="20"><HomeFilled /></el-icon>
        </div>
      </el-tooltip>
      
      <!-- 设置按钮 -->
      <el-tooltip v-if="navigationStore.shouldShowSettings" content="系统设置" placement="bottom">
        <div class="icon-btn" @click="handleSettings">
          <el-icon :size="20"><Setting /></el-icon>
        </div>
      </el-tooltip>

      <!-- 消息通知 -->
      <el-tooltip content="系统通知" placement="bottom">
        <div class="icon-btn">
          <el-badge is-dot class="item">
            <el-icon :size="20"><Bell /></el-icon>
          </el-badge>
        </div>
      </el-tooltip>

      <el-divider direction="vertical" class="divider" />

      <!-- 退出按钮 -->
      <div class="logout-btn" @click="handleLogout">
        <el-icon style="margin-right: 5px"><SwitchButton /></el-icon>
        <span>注销</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.navbar-container {
  height: 60px;
  background: #ffffff;
  /* 底部增加阴影，更有层次感 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  /* 固定在顶部 */
  position: sticky;
  top: 0;
  z-index: 1000; 
  /* 稍微一点磨砂透明效果 */
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

/* 左侧 Logo 区域 */
.nav-left {
  display: flex;
  align-items: center;
  cursor: pointer; 
  transition: opacity 0.3s;
  min-width: 200px; /* 确保左侧固定宽度 */
}

.nav-left:hover {
  opacity: 0.8;
}

.logo-box {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #409eff, #337ecc);
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  margin-right: 12px;
  box-shadow: 0 4px 6px rgba(64, 158, 255, 0.3);
}

.titles {
  display: flex;
  flex-direction: column;
}

.main-title {
  font-weight: 800;
  font-size: 16px;
  color: #303133;
  letter-spacing: 1px;
  line-height: 1.2;
}

.sub-title {
  font-size: 10px;
  color: #909399;
  font-family: 'Courier New', Courier, monospace;
}

/* 中间页面标题 */
.nav-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  pointer-events: none; /* 防止阻挡点击事件 */
}

.page-name {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  letter-spacing: 0.5px;
  /* 添加微妙的发光效果 */
  text-shadow: 0 0 1px rgba(64, 158, 255, 0.3);
}

/* 右侧按钮区域 */
.nav-right {
  display: flex;
  align-items: center;
  gap: 15px;
  min-width: 200px; /* 确保右侧固定宽度 */
  justify-content: flex-end; /* 右对齐 */
}

.icon-btn {
  width: 36px;
  height: 36px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  cursor: pointer;
  color: #606266;
  transition: all 0.3s;
}

.icon-btn:hover {
  background-color: #f2f6fc;
  color: #409eff;
  transform: rotate(15deg); /* 鼠标放上去稍微转一下，增加趣味 */
}

.divider {
  height: 20px;
  border-color: #dcdfe6;
}

.logout-btn {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 6px 16px;
  border-radius: 20px;
  background-color: #fef0f0;
  color: #f56c6c;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.logout-btn:hover {
  background-color: #f56c6c;
  color: white;
  box-shadow: 0 4px 12px rgba(245, 108, 108, 0.3);
}
</style>