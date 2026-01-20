<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import { 
  Cpu, 
  Operation, 
  Connection, 
  Check, 
  Close, 
  Plus, 
  Delete 
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// --- 类型定义 ---
interface ApiConfig {
  id: string
  name: string
  baseUrl: string
  apiKey: string
  model: string
  temperature: number
  maxTokens: number
  topP: number
}

// 定义自动补全建议项的接口
interface SuggestionItem {
  value: string
}

// --- 1. API 设定逻辑 ---

const defaultConfig: ApiConfig = {
  id: '', 
  name: 'New Configuration',
  baseUrl: 'https://api.openai.com/v1',
  apiKey: '',
  model: 'gpt-3.5-turbo',
  temperature: 0.7,
  maxTokens: 2000,
  topP: 1.0
}

// 模拟已保存的多个配置
const configList = ref<ApiConfig[]>([
  {
    id: '1',
    name: 'OpenAI Official',
    baseUrl: 'https://api.openai.com/v1',
    apiKey: 'sk-xxxxxx',
    model: 'gpt-4',
    temperature: 0.7,
    maxTokens: 4096,
    topP: 1.0
  },
  {
    id: '2',
    name: 'DeepSeek (Local/Proxy)',
    baseUrl: 'https://api.deepseek.com',
    apiKey: 'sk-yyyyyy',
    model: 'deepseek-coder',
    temperature: 0.1,
    maxTokens: 8000,
    topP: 0.9
  }
])

const currentConfigId = ref<string>('1')
const apiForm = reactive<ApiConfig>({ ...defaultConfig })

// --- 修复点：将 fetch-suggestions 提取为具体函数 ---
const querySearch = (queryString: string, cb: (results: SuggestionItem[]) => void) => {
  // 这里定义推荐的模型列表
  const suggestions: SuggestionItem[] = [
    { value: 'gpt-3.5-turbo' },
    { value: 'gpt-4' },
    { value: 'gpt-4o' },
    { value: 'claude-3-5-sonnet' },
    { value: 'deepseek-chat' }
  ]
  // 直接调用回调函数返回数据
  cb(suggestions)
}

// 切换配置
const handleConfigChange = (val: string) => {
  const target = configList.value.find(c => c.id === val)
  if (target) {
    Object.assign(apiForm, target)
    ElMessage.info(`已切换至: ${target.name}`)
  }
}

// 新增配置
const handleAddConfig = () => {
  const newId = Date.now().toString()
  const newConfig: ApiConfig = { 
    ...defaultConfig, 
    id: newId, 
    name: `配置 #${configList.value.length + 1}` 
  }
  configList.value.push(newConfig)
  currentConfigId.value = newId
  Object.assign(apiForm, newConfig)
  ElMessage.success('已创建新配置')
}

// 删除配置
const handleDeleteConfig = () => {
  if (configList.value.length <= 1) {
    return ElMessage.warning('至少保留一个配置')
  }
  
  ElMessageBox.confirm(
    `确定要删除配置 "${apiForm.name}" 吗？`,
    '警告',
    { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' }
  ).then(() => {
    const index = configList.value.findIndex(c => c.id === currentConfigId.value)
    
    if (index !== -1) {
      configList.value.splice(index, 1)
      
      const nextConfig = configList.value[0]

      if (nextConfig) {
        currentConfigId.value = nextConfig.id
        Object.assign(apiForm, nextConfig)
      } else {
        handleAddConfig()
      }
      
      ElMessage.success('配置已删除')
    }
  })
}

// 保存当前配置
const loading = ref(false)
const handleSaveApi = () => {
  loading.value = true
  setTimeout(() => {
    // 更新列表中的数据
    const index = configList.value.findIndex(c => c.id === apiForm.id)
    if (index !== -1) {
      configList.value[index] = { ...apiForm }
    }
    loading.value = false
    ElMessage.success(`配置 "${apiForm.name}" 已保存并同步`)
  }, 800)
}

// 初始化
onMounted(() => {
  handleConfigChange(currentConfigId.value)
})

// --- 2. 系统设定数据 ---
const systemForm = reactive({
  theme: 'light',
  notifications: true,
  sound: false,
  language: 'zh-CN'
})
const handleSaveSystem = () => ElMessage.success('系统偏好已更新')
</script>

<template>
  <div class="app-layout">
    <Navbar />

    <div class="dashboard-content">
      <el-row :gutter="20">
        
        <!-- 左侧：API 设定 -->
        <el-col :xs="24" :md="12" :lg="12">
          <el-card class="setting-card hover-effect">
            <template #header>
              <div class="card-header">
                <div class="header-left">
                  <span class="header-icon-box api-color">
                    <el-icon><Cpu /></el-icon>
                  </span>
                  <span class="card-title">API 神经连接</span>
                </div>
                
                <div class="header-right">
                  <el-select 
                    v-model="currentConfigId" 
                    placeholder="选择配置" 
                    size="small" 
                    style="width: 140px; margin-right: 8px;"
                    @change="handleConfigChange"
                  >
                    <el-option 
                      v-for="item in configList" 
                      :key="item.id" 
                      :label="item.name" 
                      :value="item.id" 
                    />
                  </el-select>
                  
                  <el-tooltip content="新建配置" placement="top">
                    <el-button circle size="small" :icon="Plus" @click="handleAddConfig" />
                  </el-tooltip>
                  <el-tooltip content="删除当前配置" placement="top">
                    <el-button circle size="small" type="danger" plain :icon="Delete" @click="handleDeleteConfig" />
                  </el-tooltip>
                </div>
              </div>
            </template>

            <el-form :model="apiForm" label-position="top">
              
              <el-row :gutter="12">
                <el-col :span="10">
                   <el-form-item label="配置别名 (Alias)">
                    <el-input v-model="apiForm.name" placeholder="给配置起个名" />
                  </el-form-item>
                </el-col>
                <el-col :span="14">
                  <el-form-item label="接口地址 (Base URL)">
                    <el-input v-model="apiForm.baseUrl" placeholder="https://api.openai.com/v1">
                      <template #prefix><el-icon><Connection /></el-icon></template>
                    </el-input>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="访问密钥 (API Key)">
                <el-input 
                  v-model="apiForm.apiKey" 
                  type="password" 
                  show-password 
                  placeholder="sk-........................"
                />
              </el-form-item>

              <el-form-item label="目标模型 (Model)">
                <!-- 修复点：绑定 :fetch-suggestions="querySearch" -->
                <el-autocomplete
                  v-model="apiForm.model"
                  :fetch-suggestions="querySearch"
                  placeholder="选择或输入模型名称"
                  style="width: 100%"
                >
                  <template #suffix><el-icon><Cpu /></el-icon></template>
                </el-autocomplete>
              </el-form-item>

              <el-divider content-position="center" style="margin: 18px 0;">
                <span style="color: #909399; font-size: 12px;">生成参数 (Generation Params)</span>
              </el-divider>

              <el-row :gutter="12">
                <el-col :span="12">
                   <el-form-item label="随机性 (Temperature)">
                    <el-slider v-model="apiForm.temperature" :min="0" :max="2" :step="0.1" show-input :show-input-controls="false" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="最大长度 (Max Tokens)">
                    <el-input-number v-model="apiForm.maxTokens" :step="100" :min="100" style="width: 100%" />
                  </el-form-item>
                </el-col>
              </el-row>
              
               <el-row :gutter="12">
                 <el-col :span="12">
                    <el-form-item label="核采样 (Top P)">
                      <el-input-number v-model="apiForm.topP" :precision="1" :step="0.1" :max="1" :min="0" style="width: 100%" />
                    </el-form-item>
                 </el-col>
               </el-row>

              <div class="card-footer">
                <el-button 
                  type="primary" 
                  class="save-btn" 
                  :loading="loading"
                  @click="handleSaveApi"
                  round
                  :icon="Check"
                >
                  保存配置并测试连接
                </el-button>
              </div>
            </el-form>
          </el-card>
        </el-col>

        <!-- 右侧：其它设定 -->
        <el-col :xs="24" :md="12" :lg="12">
          <el-card class="setting-card hover-effect">
            <template #header>
              <div class="card-header">
                <span class="header-icon-box system-color">
                  <el-icon><Operation /></el-icon>
                </span>
                <span class="card-title">系统偏好</span>
              </div>
            </template>

            <el-form :model="systemForm" label-position="left" label-width="120px">
              <div class="setting-group">
                <div class="group-title">界面显示</div>
                <el-form-item label="深色模式">
                  <el-switch v-model="systemForm.theme" active-value="dark" inactive-value="light" inline-prompt active-icon="Check" inactive-icon="Close" />
                </el-form-item>
                <el-form-item label="系统语言">
                  <el-radio-group v-model="systemForm.language" size="small">
                    <el-radio-button label="zh-CN">中文</el-radio-button>
                    <el-radio-button label="en-US">ENG</el-radio-button>
                  </el-radio-group>
                </el-form-item>
              </div>

              <el-divider border-style="dashed" />

              <div class="setting-group">
                <div class="group-title">反馈交互</div>
                <el-form-item label="操作音效">
                  <el-switch v-model="systemForm.sound" />
                </el-form-item>
                <el-form-item label="实时通知">
                  <el-switch v-model="systemForm.notifications" />
                </el-form-item>
              </div>

              <div class="card-footer" style="margin-top: 30px;">
                <el-button plain @click="handleSaveSystem" style="width: 100%">应用配置</el-button>
              </div>
            </el-form>
          </el-card>
        </el-col>

      </el-row>
    </div>
  </div>
</template>

<style scoped>

.app-layout {
  min-height: 100vh;
  background-color: #f0f2f5;
  background-image: radial-gradient(#e1e4e8 1px, transparent 1px);
  background-size: 20px 20px;
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* 卡片样式 */
.setting-card {
  border-radius: 12px;
  border: none;
  background: rgba(255, 255, 255, 0.95);
  margin-bottom: 20px;
  min-height: 520px; 
}

.hover-effect {
  transition: all 0.3s;
}
.hover-effect:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left, .header-right {
  display: flex;
  align-items: center;
}

.card-title {
  font-weight: bold;
  font-size: 16px;
  margin-left: 10px;
}

.header-icon-box {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
}
.api-color {
  background: linear-gradient(135deg, #626aef, #a0cfff);
  box-shadow: 0 4px 10px rgba(98, 106, 239, 0.3);
}
.system-color {
  background: linear-gradient(135deg, #909399, #c8c9cc);
}

.group-title {
  font-size: 12px;
  color: #909399;
  margin-bottom: 15px;
  font-weight: bold;
}

.card-footer {
  text-align: right;
  margin-top: 20px;
}

.save-btn {
  width: 100%;
  font-weight: bold;
  letter-spacing: 1px;
  background: linear-gradient(90deg, #409eff, #337ecc);
  border: none;
}
.save-btn:hover {
  background: linear-gradient(90deg, #66b1ff, #409eff);
}
</style>