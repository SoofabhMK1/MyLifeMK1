<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import Navbar from '../components/Navbar.vue' 
import { 
  User, Trophy, Wallet, Lightning, 
  Aim, Reading, Connection, SwitchButton 
} from '@element-plus/icons-vue'

const userStore = useUserStore()

// 2. 挂载时请求后端数据
onMounted(() => {
  userStore.getUserInfo()
})
</script>

<template>
  <div class="app-layout">
    
    <!-- 3. 使用 Navbar 组件 -->
    <Navbar />

    <div class="dashboard-content">

    <!-- 主要内容区域 -->
    <el-row :gutter="20">
      
      <!-- 左侧：角色形象与基础状态 -->
      <el-col :xs="24" :md="8" :lg="6">
        <el-card class="character-card hover-effect">
          <div class="avatar-section">
            <el-avatar :size="120" :src="userStore.userInfo.avatarUrl" shape="square" class="hero-avatar" />
            <h2 class="hero-name">{{ userStore.userInfo.username }}</h2>
            <el-tag effect="dark" round class="hero-title">{{ userStore.userInfo.title }}</el-tag>
          </div>
          
          <el-divider><el-icon><User /></el-icon> 基础状态</el-divider>
          
          <div class="status-bars">
            <div class="bar-item">
              <span>LV.{{ userStore.userInfo.level }}</span>
              <el-progress :percentage="userStore.userInfo.exp" :format="() => 'EXP'" striped striped-flow />
            </div>
            <div class="bar-item">
              <span>HP</span>
              <el-progress :percentage="100" status="success" :show-text="false" />
            </div>
            <div class="bar-item">
              <span>MP</span>
              <el-progress :percentage="80" color="#409eff" :show-text="false" />
            </div>
          </div>
        </el-card>

        <!-- 资产卡片 -->
        <el-card class="wallet-card hover-effect" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span><el-icon><Wallet /></el-icon> 资产账户</span>
            </div>
          </template>
          <el-statistic 
            :value="userStore.userInfo.cash" 
            prefix="¥" 
            :precision="2" 
            group-separator=","
            class="cash-display"
          />
        </el-card>
      </el-col>

      <!-- 右侧：详细属性面板 -->
      <el-col :xs="24" :md="16" :lg="18">
        <!-- 四维属性 -->
        <el-row :gutter="20" class="attribute-row">
          <el-col :span="12" :md="6" v-for="attr in userStore.userInfo.attributes" :key="attr.label">
            <el-card shadow="hover" class="stat-card">
              <div class="stat-content">
                <span class="stat-label">{{ attr.label }}</span>
                <el-progress type="dashboard" :percentage="attr.value" :color="attr.color" :width="80">
                  <template #default="{ percentage }">
                    <span class="stat-value">{{ percentage }}</span>
                  </template>
                </el-progress>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 技能树 -->
        <el-card class="skill-section hover-effect">
          <template #header>
            <div class="card-header">
              <span><el-icon><Lightning /></el-icon> 已习得技能 (Skills)</span>
              <el-button type="primary" size="small" plain round>技能树 +</el-button>
            </div>
          </template>
          
          <div class="skill-grid">
            <div v-for="skill in userStore.userInfo.skills" :key="skill.name" class="skill-item">
              <div class="skill-icon-placeholder">
                <el-icon :size="24"><Trophy /></el-icon>
              </div>
              <div class="skill-info">
                <h4>{{ skill.name }}</h4>
                <el-tag size="small" :type="skill.type as any">{{ skill.level }}</el-tag>
              </div>
            </div>
            <!-- 增加一个空的添加槽位 -->
            <div class="skill-item add-skill">
              <el-icon><Connection /></el-icon>
              <span>学习新技能</span>
            </div>
          </div>
        </el-card>

        <!-- 任务日志 (占位) -->
        <el-card class="quest-log hover-effect" style="margin-top: 20px;">
          <template #header>
            <span><el-icon><Aim /></el-icon> 当前任务 (Current Quest)</span>
          </template>
          <el-steps direction="vertical" :active="1">
            <el-step title="部署到 VPS" description="将 Vue 和 FastAPI 项目成功运行在服务器上" />
            <el-step title="完善个人中心" description="设计并实现一个酷炫的 Dashboard" />
            <el-step title="连接数据库" description="待开始..." />
          </el-steps>
        </el-card>

      </el-col>
    </el-row>
    </div>
  </div>
</template>

<style lang="scss" scoped>
/* 4. 修改样式结构 */
.app-layout {
  @include app-layout;
}

.dashboard-content {
  @include container;
}

.system-status {
  color: #67c23a;
  font-size: 12px;
  margin-right: 15px;
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
}

/* 卡片通用效果 */
.hover-effect {
  transition: all 0.3s;
  border-radius: 12px;
  border: none;
}
.hover-effect:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

/* 左侧：角色卡片 */
.character-card {
  text-align: center;
  background: linear-gradient(145deg, #ffffff, #f9fafc);
}
.hero-avatar {
  border: 4px solid #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  margin-bottom: 15px;
}
.hero-name {
  margin: 10px 0 5px;
  font-size: 24px;
  color: #303133;
}
.status-bars .bar-item {
  margin-bottom: 12px;
  text-align: left;
}
.status-bars span {
  font-size: 12px;
  color: #909399;
  font-weight: bold;
  display: block;
  margin-bottom: 4px;
}

/* 左侧：钱包 */
.cash-display {
  text-align: center;
  color: #e6a23c;
}
:deep(.el-statistic__content) {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: bold;
  color: #e6a23c;
}

/* 右侧：四维属性 */
.attribute-row {
  margin-bottom: 20px;
}
.stat-card {
  text-align: center;
  margin-bottom: 10px; /* 移动端适配 */
}
.stat-label {
  display: block;
  margin-bottom: 10px;
  font-size: 14px;
  color: #606266;
  font-weight: 600;
}
.stat-value {
  font-size: 18px;
  font-weight: bold;
}

/* 右侧：技能网格 */
.skill-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 15px;
}
.skill-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #ebeef5;
  transition: 0.3s;
}
.skill-item:hover {
  background-color: #ecf5ff;
  border-color: #c6e2ff;
}
.skill-icon-placeholder {
  width: 40px;
  height: 40px;
  background: #fff;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.skill-info h4 {
  margin: 0 0 5px;
  font-size: 14px;
}
.add-skill {
  justify-content: center;
  color: #909399;
  cursor: pointer;
  border-style: dashed;
}
</style>